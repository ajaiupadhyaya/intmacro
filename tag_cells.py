# tag_cells.py
import nbformat
import os

path = "macrobook/content"

for root, _, files in os.walk(path):
    for file in files:
        if file.endswith(".ipynb"):
            full_path = os.path.join(root, file)
            with open(full_path, "r", encoding="utf-8") as f:
                nb = nbformat.read(f, as_version=4)

            for cell in nb.cells:
                if cell.cell_type == "code":
                    tags = cell.metadata.get("tags", [])
                    if "thebe-init" not in tags:
                        tags.append("thebe-init")
                    else:
                        tags = list(set(tags))  # remove duplicates
                    cell.metadata["tags"] = tags

            with open(full_path, "w", encoding="utf-8") as f:
                nbformat.write(nb, f)

print("✅ Cleaned and updated all thebe-init tags without duplication.")