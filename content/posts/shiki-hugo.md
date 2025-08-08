---
title: Highlighting codeblocks with Shiki in Hugo
date: '2024-07-27'
summary: 'A guide on using Shiki for syntax highlighting in Hugo websites'
description: 'A guide on using Shiki for syntax highlighting in Hugo websites'
tags: [programming, hugo]
---

Over the past months, I have been helping to build a [new documentation
website](https://docs-beta.yagpdb.xyz/) for the [YAGPDB project](https://yagpdb.xyz) using Hugo. To
provide more accurate syntax highlighting for our code snippets, which use a custom scripting
language, we needed to switch away from Hugo's built-in
[Chroma](https://github.com/alecthomas/chroma)-powered highlighting.[^1]

After evaluating various alternative syntax highlighting solutions, we ultimately settled on
[Shiki](https://shiki.style/). Shiki is powered by TextMate grammars, which are also used by VSCode.
In practice, this means that Shiki can take advantage of the massive existing ecosystem of VSCode
themes and language extensions to provide accurate, highly customizable highlighting with little
effort.

Since there is a lack of existing resources on using different syntax highlighters with Hugo, I
wrote up a brief guide in this blog post.

## Some important caveats

Shiki is highly extensible and looks nice, but using it in a Hugo website has significant drawbacks.
Notably, Shiki is only available as a JavaScript library; this not only ties you to the dreaded npm
ecosystem but also means that Shiki cannot be integrated smoothly into Hugo's build process.
**Instead, Shiki must run in a separate build step that post-processes the HTML files output by
Hugo.[^2]**

Concretely, instead of building with

```shell
$ hugo
```

one must instead run

```shell
$ hugo && node scripts/highlight.mjs
```

or similar, where `scripts/highlight.mjs` overwrites the output HTML files in `public/`. This
additional build step is also rather sluggish relative to Hugo; in our experience, Shiki takes ~1
second to highlight 60 files.

Moreover, Hugo's built-in development server,

```shell
$ hugo server
```

cannot be made to work with Shiki with this approach: codeblocks will render differently in
development and production. In some sense, this is actually beneficial, as avoiding invoking Shiki
in development preserves quick iteration cycles. (It is still, of course, possible to preview the
production appearance by building via `hugo && node scripts/highlight.mjs` and then serving the
`public/` directory.)

---

If these caveats are acceptable to you, read on. For us, our
theme---[Doks](https://getdoks.org/)---already tied us to the npm ecosystem, and having accurate
highlighting for our custom scripting language was well worth the drawbacks.

## A step-by-step guide

**Disable Chroma.** First, disable Hugo's built-in syntax highlighting in your website configuration
(`config.toml` or similar):

```toml {hl_lines=3}
[markup]
    [markup.highlight]
        codeFences = false
```

---

**Set up npm project.** Next, install Node.js on your machine, create a new npm project in your
website root, and install the packages required by the build script with

```shell
$ npm init # prompts for project name among other details; any will do

$ npm install glob # for locating built HTML files to highlight
$ npm install htmlparser2 domutils dom-serializer # for editing HTML files
$ npm install shiki
```

---

**Add build script.** Now, copy the build script---responsible for highlighting the HTML files
output by Hugo---to `scripts/highlight.mjs`. A [longer explanation](#appendix-build-script-explanation)
of how the build script works is available for the curious.

You must change the glob pattern on line 30 to match your file structure: in our case, we had
documentation under `content/docs`, so the correct pattern for the output HTML files was
`public/docs/**/index.html`.

```js {linenos=true, hl_lines=30}
import { createHighlighter, bundledLanguages } from 'shiki';

import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { readFile, writeFile } from 'node:fs/promises';

import { glob } from 'glob';

import { parseDocument } from 'htmlparser2';
import { findAll, findOne, textContent, replaceElement } from 'domutils';
import render from 'dom-serializer';

const __dirname = dirname(fileURLToPath(import.meta.url));

main();

async function main() {
	// You need some custom CSS to integrate light and dark themes with your website.
	// See https://shiki.style/guide/dual-themes.
	const LIGHT_THEME = 'github-light';
	const DARK_THEME = 'github-dark';

	const start = Date.now();

	const highlighter = await createHighlighter({
		themes: [LIGHT_THEME, DARK_THEME],
		langs: Object.keys(bundledLanguages),
	});

	const files = await glob(join(__dirname, '../public/docs/**/index.html'));
	await Promise.all(
		files.map((filepath) => highlightFile(highlighter, filepath, { lightTheme: LIGHT_THEME, darkTheme: DARK_THEME }))
	);

	console.log(`Highlighted ${files.length} files in ${Math.round(Date.now() - start)} ms`);
}

async function highlightFile(highlighter, filepath, { lightTheme, darkTheme }) {
	const contents = await readFile(filepath, { encoding: 'utf-8' });
	await writeFile(filepath, highlightHtmlContent(highlighter, contents, { lightTheme, darkTheme }));
}

function highlightHtmlContent(highlighter, htmlContent, { lightTheme, darkTheme }) {
	const doc = parseDocument(htmlContent);
	for (const preNode of findAll((e) => e.name === 'pre', doc.children)) {
		const codeNode = findOne((e) => e.name === 'code', preNode.children);
		if (!codeNode) continue;

		const lang = codeNode.attribs['class']?.replace(/^language-/, '') ?? 'text';
		const code = textContent(codeNode);
		const highlighted = highlighter.codeToHtml(code, {
			lang,
			themes: { light: lightTheme, dark: darkTheme },
		});

		const highlightedPreNode = parseDocument(highlighted).children[0];
		replaceElement(preNode, highlightedPreNode);
	}

	return render(doc);
}
```

For convenience, you may wish to add a npm script that runs both Hugo and the build script in
`package.json`.

```json {hl_lines=[4,5]}
{
    ...
    "scripts": {
		"build": "hugo && npm run highlight",
		"highlight": "node scripts/highlight.mjs"
    }
}
```

You may now build your website with `npm run build` and view the result by serving the `public`
directory with your webserver of choice.

---

With that, we are done! The finishing touch is to modify your deployment process to invoke
the build script in addition to Hugo; see
[the GitHub workflow](https://github.com/botlabs-gg/yagpdb-docs-v2/blob/master/.github/workflows/hugo.yml)
we use in the YAGPDB documentation repository for inspiration.

Enjoy your new Shiki-powered codeblocks :)

## Appendix: build script explanation

When Hugo processes markdown files, it transforms codeblocks to HTML structured as follows:

```html
<pre>
    <code class="language-xxx">
        ...
    </code>
</pre>
```

so, for each output HTML file, we should

- target all `pre` nodes,
- read the language from the `class` attribute of the inner `code` node,
- and use Shiki to transform the content of the `code` node, then replace the `pre` node with the
  highlighted `pre` node.

The function `highlightHtmlContent`, which is the bulk of the build script, accomplishes this.

```js
function highlightHtmlContent(highlighter, htmlContent, { lightTheme, darkTheme }) {
	const doc = parseDocument(htmlContent);
	for (const preNode of findAll((e) => e.name === 'pre', doc.children)) {
		const codeNode = findOne((e) => e.name === 'code', preNode.children);
		if (!codeNode) continue;

		const lang = codeNode.attribs['class']?.replace(/^language-/, '') ?? 'text';
		const code = textContent(codeNode);
		const highlighted = highlighter.codeToHtml(code, {
			lang,
			themes: { light: lightTheme, dark: darkTheme },
		});

		const highlightedPreNode = parseDocument(highlighted).children[0];
		replaceElement(preNode, highlightedPreNode);
	}

	return render(doc);
}
```

The rest of the build script is driver code that invokes `highlightHtmlContent` on each output file
and overwrites the contents.

[^1]:
    Though Chroma is extensible with custom lexers, Hugo [does not surface this extension
    point](https://github.com/gohugoio/hugo/issues/11496) at the moment.

[^2]:
    In the future, Hugo may support [running WASM scripts as part of the
    build](https://github.com/gohugoio/hugo/pull/12679), potentially ameliorating this issue as
    Shiki can then, in theory, be compiled to WASM and invoked. However, the separate build script
    is the best we can do for now.
