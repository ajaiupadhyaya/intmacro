<script>
// Graceful fallback for legacy ipywidgets models.
//
// The static site has no Python kernel, so notebook cells whose output is an
// `ipywidgets` view (application/vnd.jupyter.widget-view+json) render as an
// empty box — the code shows but the model never appears. Until each chapter is
// rebuilt as an in-browser Observable JS simulator, this script hides those
// dead cells and leaves a single, restrained notice in their place so the page
// reads as a clean explanation rather than a broken widget.
(function () {
  function run() {
    var views = document.querySelectorAll(
      'script[type="application/vnd.jupyter.widget-view+json"]'
    );
    if (!views.length) return;

    var deadCells = [];
    var seen = new Set();
    views.forEach(function (view) {
      var cell = view.closest("div.cell");
      if (!cell || seen.has(cell)) return;
      seen.add(cell);
      deadCells.push(cell);
    });
    if (!deadCells.length) return;

    var notice = document.createElement("div");
    notice.className = "im-model-pending";
    var label = document.createElement("span");
    label.className = "im-model-pending-label";
    label.textContent = "Interactive simulator in preparation";
    notice.appendChild(label);
    notice.appendChild(
      document.createTextNode(
        "The model and its intuition are explained in full below. An " +
          "in-browser interactive version of this chapter is being added."
      )
    );

    var first = deadCells[0];
    first.parentNode.insertBefore(notice, first);
    deadCells.forEach(function (cell) {
      cell.style.display = "none";
    });

    // This is a legacy notebook page (dead widgets present). Besides the
    // executed cells (already hidden via echo:false), these chapters also carry
    // Python snippets embedded in their markdown — implementation detail, not
    // economics. Hide those too so the page reads as a clean explanation.
    document.querySelectorAll("div.sourceCode").forEach(function (block) {
      block.style.display = "none";
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else {
    run();
  }
})();
</script>
