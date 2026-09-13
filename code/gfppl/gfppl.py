from dataclasses import dataclass

import sympy as sp
from parsy import forward_declaration, regex, seq, string

type Stmt = VarDecl | ObserveNonzero | ObserveZero | Return | FnDecl
type Expr = VarRef | FnCall | NumLit | Tuple | IfThen | Sum

@dataclass
class Block: # { stmts... result } (result is the block's value, if any)
    stmts: list[Stmt]
    result: Expr | None = None

@dataclass
class VarDecl: # (bindings...) <- expr
    bindings: list[str]
    expr: Expr

@dataclass
class FnCall: # name(args...)
    name: str
    args: list[Expr]

@dataclass
class ObserveNonzero: # observe var != 0
    var: str
@dataclass
class ObserveZero: # observe var = 0
    var: str

@dataclass
class Return: # return var
    var: str

@dataclass
class VarRef:
    name: str

@dataclass
class NumLit:
    val: sp.Number

@dataclass
class Tuple: # (elems...)
    elems: list[Expr]

@dataclass
class FnDecl: # fn name(param_names...) { ... }
    name: str
    param_names: list[str]
    body: Block

@dataclass
class IfThen: # if cond then then_ else else_
    cond: Expr
    then_: Block
    else_: Block

@dataclass
class Sum: # sum n { body }
    n: str
    body: Block

ws = regex(r"(\s|#[^\n]*)*")  # whitespace and `# ...` comments
sym = lambda s: string(s) << ws
kw = lambda w: regex(rf"{w}\b") << ws
KEYWORD = r"(?!(?:fn|observe|if|then|else|sum|return)\b)"
ident = regex(KEYWORD + r"[a-zA-Z]\w*") << ws
call_head = regex(KEYWORD + r"[a-zA-Z]\w*(?=\()") << sym("(")  # `f(` with no space
num = regex(r"\d+(?:\.\d+)?").map(sp.Rational) << ws
names = ident.sep_by(sym(","))

expr, stmt = forward_declaration(), forward_declaration()
block = sym("{") >> seq(stmt.many(), expr.optional()).combine(Block) << sym("}")
branch = block | expr.map(lambda e: Block([], e))
args = expr.sep_by(sym(",")) << sym(")")
paren = sym("(") >> args
expr.become(
    seq(kw("if") >> expr, kw("then") >> branch, kw("else") >> branch).combine(IfThen)
    | seq(kw("sum") >> ident, block).combine(Sum)
    | num.map(NumLit)
    | seq(call_head, args).combine(FnCall)
    | ident.map(VarRef)
    | paren.map(lambda es: es[0] if len(es) == 1 else Tuple(es))
)
stmt.become(
    seq(kw("fn") >> call_head, names << sym(")"), block).combine(FnDecl)
    | (kw("observe") >> ident << sym("!=") << sym("0")).map(ObserveNonzero)
    | (kw("observe") >> ident << sym("=") << sym("0")).map(ObserveZero)
    | (kw("return") >> ident).map(Return)
    | seq(ident.map(lambda x: [x]) | sym("(") >> names << sym(")"), sym("<-") >> expr).combine(VarDecl)
)
parse = (ws >> stmt.many().map(Block)).parse

def bernoulli(y, theta):
    return lambda e: e * (1 - theta + theta * y)

def poisson(y, lambda_):
    return lambda e: e * sp.exp(lambda_ * (y - 1))

def const(y, c):
    return lambda e: e * y**c

def copy(y, x):
    return lambda e: e.subs(x, x * y)

def total_mass(e):
    return e.subs({v: 1 for v in e.free_symbols})

def marginalize(e, xs):
    return e.subs({x: 1 for x in xs})

def observe(x):
    def transform(e):
        survivors = e - e.subs(x, 0)
        return survivors / total_mass(survivors)
    return transform

def observe_zero(x):
    def transform(e):
        survivors = e.subs(x, 0)
        return survivors / total_mass(survivors)
    return transform

def if_(y, then, else_):
    def transform(e):
        p_zero = total_mass(e.subs(y, 0))   # P[Y = 0]
        g_then = then(observe(y)(e))        # pgf of ..., X | Y != 0
        g_else = else_(observe_zero(y)(e))  # pgf of ..., X | Y == 0
        return (1 - p_zero) * g_then + p_zero * g_else
    return transform

def sum_(n, body):
    def transform(e):
        body_gf = body(sp.Integer(1))
        return e.subs(n, n * body_gf)
    return transform

BUILTINS = {"bernoulli": bernoulli, "poisson": poisson}

type GF = sp.Expr
type Env = dict[str, sp.Expr]  # name -> sympy symbol or constant

def compile(prog: Block) -> tuple[GF, sp.Symbol | None]:
    """Return (pgf of the returned variable, its symbol)."""
    fns: dict[str, FnDecl] = {}
    ret: sp.Symbol | None = None

    def lookup(x: NumLit | VarRef, env: Env) -> sp.Expr:
        return x.val if isinstance(x, NumLit) else env[x.name]

    def run(stmts: list[Stmt], env: Env, e: GF) -> GF:
        nonlocal ret
        for s in stmts:
            match s:
                case FnDecl(name): fns[name] = s
                case ObserveNonzero(var): e = observe(env[var])(e)
                case ObserveZero(var): e = observe_zero(env[var])(e)
                case Return(var): ret = env[var]
                case VarDecl(bindings, expr):
                    ys = [sp.Dummy(b) for b in bindings]
                    e = bind(ys, expr, env, e)
                    env.update(zip(bindings, ys))
        return e

    def block(b: Block, env: Env, ys: list[sp.Symbol], e: GF) -> GF:  # ys <- { b }
        local = env.copy()
        return bind(ys, b.result, local, run(b.stmts, local, e))

    def bind(ys: list[sp.Symbol], x: Expr, env: Env, e: GF) -> GF:  # ys <- x
        match x:
            case NumLit(c):
                return const(ys[0], c)(e)
            case VarRef(name):
                v = env[name]
                if v.is_Symbol:
                    return copy(ys[0], v)(e)
                return const(ys[0], v)(e)
            case Tuple(elems):
                for y, el in zip(ys, elems):
                    e = bind([y], el, env, e)
                return e
            case IfThen(cond, then_, else_):
                g_then = lambda e: block(then_, env, ys, e)
                g_else = lambda e: block(else_, env, ys, e)
                return if_(env[cond.name], g_then, g_else)(e)
            case Sum(n, body):
                body_t = lambda e: block(body, env, ys, e)
                return sum_(env[n], body_t)(e)
            case FnCall(name, args) if name in fns:
                fn = fns[name]
                params = {p: lookup(a, env) for p, a in zip(fn.param_names, args)}
                return block(fn.body, params, ys, e) # body only has access to params
            case FnCall(name, args):
                return BUILTINS[name](ys[0], *(lookup(a, env) for a in args))(e)

    e = run(prog.stmts, {}, sp.Integer(1))
    return marginalize(e, e.free_symbols - {ret}), ret
