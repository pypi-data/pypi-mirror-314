import os
import sys

from ncd_anon.anonimizer import Anonimizer
from ncd_anon.convert import convert_pdf_to_str


def usage() -> str:
    return """
    NCD Anonymizer Tool
    ==================

    A command-line tool to anonymize PDF and TXT files by removing or masking sensitive information.

    Usage
    -----
        python ncd-anon.py <file_or_folder_path>

    Arguments
    ---------
        file_or_folder_path : str
            Path to either a single file (.pdf or .txt) or a directory containing multiple files.

    Output
    ------
        For each processed file, creates a new file with '.anon.txt' extension in the same directory.
        Example: 'document.pdf' -> 'document.anon.txt'

    Examples
    --------
        # Anonymize a single PDF file
        python ncd-anon.py /path/to/document.pdf

        # Anonymize a single text file
        python ncd-anon.py /path/to/document.txt

        # Anonymize all PDF and TXT files in a directory
        python ncd-anon.py /path/to/directory

    Notes
    -----
        - Only .pdf and .txt files are processed
        - Files already ending in '.anon.txt' are skipped
        - The tool will create anonymized text versions of all processed files
    """


def anonymize_file(anonimizer: Anonimizer, path_file_source: str, path_file_target: str) -> None:
    print(f"Anonymizing {path_file_source} to {path_file_target}", flush=True)
    if path_file_source.endswith(".pdf"):
        text = convert_pdf_to_str(path_file_source)
    elif path_file_source.endswith(".txt"):
        with open(path_file_source, "r") as f:
            text = f.read()
    else:
        raise ValueError(f"Unsupported file type: {path_file_source} only pdf and txt are supported")
    text = anonimizer.anonymize(text)
    with open(path_file_target, "w") as f:
        f.write(text)


def main():
    # Get the first argument
    if len(sys.argv) < 2:
        print(usage())
        sys.exit(1)

    path_source = os.path.abspath(sys.argv[1])
    if not os.path.exists(path_source):
        print(f"Error: {path_source} is nether a file nor a directory")
        sys.exit(1)

    anonimizer = Anonimizer()
    if os.path.isfile(path_source):
        path_file_source = path_source
        # Handle single file
        path_file_target = path_file_source.replace(".pdf", ".anon.txt")
        path_file_target = path_file_source.replace(".txt", ".anon.txt")
        anonymize_file(anonimizer, path_file_source, path_file_target)
    elif os.path.isdir(path_source):
        path_dir_source = path_source
        # Handle directory
        list_name_file = os.listdir(path_dir_source)

        for name_file in list_name_file:
            if name_file.endswith(".anon.txt"):
                print(f"Skipping {name_file} because it is already anonymized")
                continue
            path_file_source = os.path.join(path_dir_source, name_file)
            if not name_file.endswith(".pdf") and not name_file.endswith(".txt"):
                print(f"Skipping {name_file} because it is not a txt or pdf file")
                continue
            if name_file.endswith(".pdf"):
                path_file_target = path_file_source.replace(".pdf", ".anon.txt")
            elif name_file.endswith(".txt"):
                path_file_target = path_file_source.replace(".txt", ".anon.txt")
            else:
                raise ValueError(f"Unsupported file type: {name_file} only pdf and txt are supported")
            anonymize_file(anonimizer, path_file_source, path_file_target)


if __name__ == "__main__":
    main()
