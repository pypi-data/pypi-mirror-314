from io import BytesIO

import pdfplumber
from pdfplumber.pdf import PDF


# Function to format the extracted table into a more readable string
def format_table(table: list[list[str]]) -> str:
    if not table:
        return ""

    # Calculate the maximum width for each column
    col_widths = [max(len(str(cell)) for cell in column) for column in zip(*table)]

    # Build the formatted table string
    formatted_table = []
    for row in table:
        formatted_row = "  ".join(str(cell).ljust(width) for cell, width in zip(row, col_widths))
        formatted_table.append(formatted_row)

    # Add a separator after the header
    if table[0]:
        header_line = "  ".join("-" * width for width in col_widths)
        formatted_table.insert(1, header_line)

    # Append an end-of-table marker
    end_of_table_line = "-" * sum(col_widths)
    formatted_table.append(end_of_table_line)

    return "\n".join(formatted_table)


def process_pdf_bytes(bytes_io: BytesIO) -> str:
    with pdfplumber.open(bytes_io) as pdf:
        text = parse(pdf)
        return text


def parse(pdf: PDF) -> str:
    all_text = []
    for page in pdf.pages:
        # Extract text from the page
        text = page.extract_text(x_tolerance=3, y_tolerance=3, layout=False, x_density=7.25, y_density=13)
        if text:
            all_text.append(text)

        # Extract and format the table from the page
        table = page.extract_table()
        if table:
            formatted_table = format_table(table)  # type: ignore
            all_text.append(formatted_table)

    return "\n\n".join(all_text)


def convert_pdf_to_str(path_file_source: str) -> str:
    with pdfplumber.open(path_file_source) as pdf:
        text = parse(pdf)
    return text
