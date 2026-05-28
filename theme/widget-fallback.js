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
    label.textContent = "Interactive model being rebuilt";
    notice.appendChild(label);
    notice.appendChild(
      document.createTextNode(
        "This chapter's simulator is being upgraded to run live in your " +
          "browser. The walkthrough below still covers the economics in full."
      )
    );

    var first = deadCells[0];
    first.parentNode.insertBefore(notice, first);
    deadCells.forEach(function (cell) {
      cell.style.display = "none";
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else {
    run();
  }
})();
</script>
