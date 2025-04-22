# tag_cells.py
import os
import nbformat

folder_path = "./macrobook/content"

for filename in os.listdir(folder_path):
    if filename.endswith(".ipynb"):
        full_path = os.path.join(folder_path, filename)
        with open(full_path, "r", encoding="utf-8") as f:
            nb = nbformat.read(f, as_version=4)

        tagged = False
        for cell in nb.cells:
            if cell.cell_type == "code" and not tagged:
                cell.metadata["tags"] = ["thebe-init"]
                tagged = True
                break

        with open(full_path, "w", encoding="utf-8") as f:
            nbformat.write(nb, f)

print("✅ All first code cells tagged with 'thebe-init'")