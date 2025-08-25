import nbformat
import os
import json

def clean_notebook(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            notebook = nbformat.read(f, as_version=4)
        
        # Clean the notebook and ensure it's valid JSON
        with open(file_path, 'w', encoding='utf-8') as f:
            nbformat.write(notebook, f)
        print(f"Cleaned {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.ipynb') and not file.startswith('.'):
                file_path = os.path.join(root, file)
                clean_notebook(file_path)
