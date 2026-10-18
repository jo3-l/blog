// Highlights the sidebar TOC entry for the section currently being read.
const sidebar = document.querySelector(".toc-sidebar");
if (sidebar) {
	const inner = sidebar.querySelector(".toc-sidebar-inner");

	const links = new Map();
	for (const a of sidebar.querySelectorAll("a[href^='#']")) {
		const heading = document.getElementById(decodeURIComponent(a.hash.slice(1)));
		if (heading) links.set(heading, a);
	}
	const headings = [...links.keys()];

	// The active section is the last heading above this fraction of the viewport.
	const THRESHOLD = 0.2;
	let active = null;
	const update = () => {
		const line = window.innerHeight * THRESHOLD;
		let current = null;
		for (const h of headings) {
			if (h.getBoundingClientRect().top > line) break;
			current = h;
		}
		const link = current && links.get(current);
		if (link === active) return;
		active?.classList.remove("active");
		active?.removeAttribute("aria-current");
		link?.classList.add("active");
		link?.setAttribute("aria-current", "location");
		active = link;

		// Keep the active entry visible if the sidebar itself overflows, without
		// scrolling the page (which scrollIntoView would do).
		if (link && inner.scrollHeight > inner.clientHeight) {
			const top = link.offsetTop - inner.offsetTop;
			if (top < inner.scrollTop || top > inner.scrollTop + inner.clientHeight - link.offsetHeight) {
				inner.scrollTop = top - inner.clientHeight / 2;
			}
		}
	};

	// Only recompute when a heading crosses the threshold line, rather than on
	// every scroll event. scrollend catches headings skipped over by fast scrolls.
	const observer = new IntersectionObserver(update, {
		rootMargin: `0px 0px -${100 - THRESHOLD * 100}% 0px`,
	});
	for (const h of headings) observer.observe(h);
	window.addEventListener("scrollend", update, { passive: true });
	update();
}
