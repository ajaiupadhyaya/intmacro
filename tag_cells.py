import nbformat
from pathlib import Path

# Set the directory where your notebooks are located
NOTEBOOK_DIR = Path("macrobook/content")

# Loop through each .ipynb file
for notebook_path in NOTEBOOK_DIR.rglob("*.ipynb"):
    print(f"Processing {notebook_path}...")
    with open(notebook_path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    modified = False

    for cell in nb.cells:
        if cell.cell_type == "code":
            tags = cell.get("metadata", {}).get("tags", [])

            # Only add tags if not already present
            if "thebe-init" not in tags:
                tags.append("thebe-init")
                modified = True
            if "hide-input" not in tags:
                tags.append("hide-input")
                modified = True

            cell.setdefault("metadata", {})["tags"] = tags

    # Save the notebook if it was changed
    if modified:
        with open(notebook_path, "w", encoding="utf-8") as f:
            nbformat.write(nb, f)
        print(f"✅ Tags added to {notebook_path}")
    else:
        print(f"ℹ️ No changes needed for {notebook_path}")