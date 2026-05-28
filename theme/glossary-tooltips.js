<script type="module">
  // Tooltip data is emitted by scripts/build_nav.py to _includes/generated/.
  // Quarto copies site resources to the root; fetch relative to site root.
  const url = "/intmacro/glossary-tooltips.json";  // GH Pages base path
  let dict = {};
  try { dict = await (await fetch(url)).json(); } catch (e) { /* dev: no base path */ }
  if (Object.keys(dict).length === 0) {
    try { dict = await (await fetch("glossary-tooltips.json")).json(); } catch (e) {}
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
