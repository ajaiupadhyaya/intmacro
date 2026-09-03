<script type="module">
  // Tooltip data is emitted by scripts/build_nav.py to _includes/generated/.
  // Quarto copies site resources to the root; fetch relative to site root.
  // Try GH Pages base path, then site root relative to this page's depth.
  const candidates = [
    "/intmacro/glossary-tooltips.json",
    "glossary-tooltips.json",
    "../glossary-tooltips.json",
  ];
  let dict = {};
  for (const url of candidates) {
    try {
      const res = await fetch(url);
      if (res.ok) { dict = await res.json(); break; }
    } catch (e) { /* try next */ }
  }

  let tip, tipFor;
  function hide() {
    if (tip) { tip.remove(); tip = null; }
    if (tipFor) { tipFor.removeAttribute("aria-describedby"); tipFor = null; }
  }
  function show(el) {
    const key = el.dataset.term || el.textContent.trim().toLowerCase();
    const entry = dict[key];
    if (!entry) return;
    hide();
    tip = document.createElement("div");
    tip.className = "im-glossary-tooltip";
    tip.id = "im-glossary-tip";
    tip.setAttribute("role", "tooltip");
    tip.textContent = entry.short;
    document.body.appendChild(tip);
    el.setAttribute("aria-describedby", tip.id);
    tipFor = el;

    // Position below the term, clamped to the viewport so terms near the right
    // edge (or low on the page) stay fully readable.
    const r = el.getBoundingClientRect();
    const w = tip.offsetWidth, h = tip.offsetHeight;
    const pad = 8;
    let left = window.scrollX + r.left;
    left = Math.min(left, window.scrollX + document.documentElement.clientWidth - w - pad);
    left = Math.max(left, window.scrollX + pad);
    let top = window.scrollY + r.bottom + 6;
    if (r.bottom + 6 + h > window.innerHeight && r.top - h - 6 > 0) {
      top = window.scrollY + r.top - h - 6;   // flip above when there's no room below
    }
    tip.style.left = left + "px";
    tip.style.top = top + "px";
  }

  document.querySelectorAll(".im-glossary-term").forEach(el => {
    // Make the term reachable without a mouse: keyboard users get it via Tab,
    // screen readers get an explicit role/description, touch users get a tap.
    if (!el.hasAttribute("tabindex")) el.setAttribute("tabindex", "0");
    if (!el.hasAttribute("role")) el.setAttribute("role", "button");

    el.addEventListener("mouseenter", () => show(el));
    el.addEventListener("mouseleave", hide);
    el.addEventListener("focus", () => show(el));
    el.addEventListener("blur", hide);
    el.addEventListener("click", (e) => {         // tap on touch devices
      e.preventDefault();
      if (tipFor === el) hide(); else show(el);
    });
    el.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); tipFor === el ? hide() : show(el); }
    });
  });

  document.addEventListener("keydown", (e) => { if (e.key === "Escape") hide(); });
  document.addEventListener("click", (e) => {   // tap elsewhere dismisses
    if (tipFor && !e.target.closest(".im-glossary-term")) hide();
  });
  window.addEventListener("scroll", hide, { passive: true });
</script>
