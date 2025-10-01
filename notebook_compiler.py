import os
import nbmerge
import nbformat

def notebook_compiler(assignment_num):
    folder = f"Assignment {assignment_num}"
    file_names = os.listdir(folder)

    # Collect only .ipynb files
    ipynb_files = [os.path.join(folder, f) for f in file_names if f.endswith(".ipynb")]

    # Sort to keep them in alphanumeric order 
    ipynb_files.sort()

    if not ipynb_files:
        print("No notebooks found!")
        return

    # Merge notebooks
    merged = nbmerge.merge_notebooks(file_paths=ipynb_files, base_dir = "Assignment {assignment_number}")

    # Formatting Title
    md_cell = nbformat.v4.new_markdown_cell(
        f"# Assignment {assignment_num}\n"
        f"Prepared by Ali Younis & Manuel Martinez Garcia"
    )
    merged.cells.insert(0, md_cell)

    # Save merged notebook
    out_name = f"Assignment {assignment_num}/hw{assignment_num}-solutions.ipynb"
    with open(out_name, "w", encoding="utf-8") as f:
        nbformat.write(merged, f)

    print(f"Succesfully compiled {len(ipynb_files)} notebooks into {out_name}")

if __name__ == "__main__":
    assignment_num = input("Enter Assignment # to compile: ")
    notebook_compiler(assignment_num)