# tag_cells.py
import os
import nbformat

folder = "./macrobook/content"

for file in os.listdir(folder):
    if file.endswith(".ipynb"):
        path = os.path.join(folder, file)
        with open(path, "r", encoding="utf-8") as f:
            nb = nbformat.read(f, as_version=4)

        for cell in nb.cells:
            if cell.cell_type == "code":
                cell.metadata.setdefault("tags", []).extend(["thebe-init", "hide-input"])
                break

        with open(path, "w", encoding="utf-8") as f:
            nbformat.write(nb, f)

print("✅ Applied 'thebe-init' and 'hide-input' to all notebooks")