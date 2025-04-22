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
                cell.metadata.setdefault("tags", [])
                if "thebe-init" not in cell.metadata["tags"]:
                    cell.metadata["tags"].append("thebe-init")
                if "hide-input" not in cell.metadata["tags"]:
                    cell.metadata["tags"].append("hide-input")
                break  # only tag the first code cell

        with open(path, "w", encoding="utf-8") as f:
            nbformat.write(nb, f)

print("✅ Applied 'thebe-init' and 'hide-input' to first code cell of each notebook.")