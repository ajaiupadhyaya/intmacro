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

  let tip;
  function show(el) {
    const key = el.dataset.term || el.textContent.trim().toLowerCase();
    const entry = dict[key];
    if (!entry) return;
    tip = document.createElement("div");
    tip.className = "im-glossary-tooltip";
    tip.textContent = entry.short;
    document.body.appendChild(tip);
    const r = el.getBoundingClientRect();
    tip.style.left = (window.scrollX + r.left) + "px";
    tip.style.top  = (window.scrollY + r.bottom + 6) + "px";
  }
  function hide() { if (tip) { tip.remove(); tip = null; } }

  document.querySelectorAll(".im-glossary-term").forEach(el => {
    el.addEventListener("mouseenter", () => show(el));
    el.addEventListener("mouseleave", hide);
    el.addEventListener("focus", () => show(el));
    el.addEventListener("blur", hide);
  });
</script>
