"""PDF Merger - Merges two PDF files into one."""

from pathlib import Path
from pypdf import PdfReader, PdfWriter


def merge_pdfs(pdf1_path: str | Path, pdf2_path: str | Path, output_path: str | Path) -> Path:
    """
    Merge two PDF files into a single PDF.

    Args:
        pdf1_path: Path to the first PDF (will appear first in output)
        pdf2_path: Path to the second PDF (will appear after first)
        output_path: Path where the merged PDF will be saved

    Returns:
        Path to the merged PDF file

    Raises:
        FileNotFoundError: If either input PDF doesn't exist
        ValueError: If input files are not valid PDFs
    """
    pdf1_path = Path(pdf1_path)
    pdf2_path = Path(pdf2_path)
    output_path = Path(output_path)

    # Validate input files exist
    if not pdf1_path.exists():
        raise FileNotFoundError(f"First PDF not found: {pdf1_path}")
    if not pdf2_path.exists():
        raise FileNotFoundError(f"Second PDF not found: {pdf2_path}")

    # Create output directory if needed
    output_path.parent.mkdir(parents=True, exist_ok=True)

    writer = PdfWriter()

    # Read and append first PDF
    try:
        reader1 = PdfReader(pdf1_path)
        for page in reader1.pages:
            writer.add_page(page)
    except Exception as e:
        raise ValueError(f"Failed to read first PDF '{pdf1_path}': {e}")

    # Read and append second PDF
    try:
        reader2 = PdfReader(pdf2_path)
        for page in reader2.pages:
            writer.add_page(page)
    except Exception as e:
        raise ValueError(f"Failed to read second PDF '{pdf2_path}': {e}")

    # Write merged PDF
    with open(output_path, "wb") as output_file:
        writer.write(output_file)

    return output_path


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Merge two PDF files into one")
    parser.add_argument("pdf1", help="Path to first PDF file")
    parser.add_argument("pdf2", help="Path to second PDF file")
    parser.add_argument("-o", "--output", default="merged.pdf", help="Output file path (default: merged.pdf)")

    args = parser.parse_args()

    try:
        result = merge_pdfs(args.pdf1, args.pdf2, args.output)
        print(f"Successfully merged PDFs into: {result}")
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
