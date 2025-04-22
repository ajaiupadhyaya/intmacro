#!/bin/bash

# Ensure script is run from the root of your repo
mkdir -p macrobook/content

# Move all notebooks into content folder (customize if your notebooks are deeper)
mv *.ipynb macrobook/content/ 2>/dev/null
mv solow_sim/*.ipynb macrobook/content/ 2>/dev/null

# Create an intro page
cat > macrobook/content/intro.md <<EOF
# Welcome to Intermediate Macroeconomics 🚀

This site presents interactive, professional-grade visualizations, models, and walkthroughs for key topics in **Intermediate Macroeconomics**, inspired by *Charles I. Jones*, *UVA Econ 3020*, and *GrowthEcon.com*.

Explore topics like:
- Solow Growth
- Romer Ideas
- Two-Period Consumption
- AD-AS
- Investment Theory
- Balanced Growth
- Convergence and Beyond!

Use the sidebar to dive into the models!
EOF

# Generate a minimal _config.yml
cat > macrobook/_config.yml <<EOF
title: Intermediate Macroeconomics Interactive Guide
author: Ajai Upadhyaya
logo: ""
only_build_toc_files: true
repository:
  url: https://github.com/ajaiupadhyaya/intmacro
  branch: gh-pages
  path_to_book: macrobook
  provider: github
launch_buttons:
  binderhub_url: ""
  thebe: true
execute:
  execute_notebooks: "off"
EOF

# Auto-generate _toc.yml with all notebooks
echo "format: jb-book" > macrobook/_toc.yml
echo "root: content/intro" >> macrobook/_toc.yml
echo "chapters:" >> macrobook/_toc.yml
for nb in macrobook/content/*.ipynb; do
  name=$(basename "$nb" .ipynb)
  echo "  - file: content/$name" >> macrobook/_toc.yml
done

echo "✅ Jupyter Book structure created!"