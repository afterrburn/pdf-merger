"""Tests for PDF Merger."""

import tempfile
from pathlib import Path

import pytest
from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from pdf_merger import merge_pdfs


def create_test_pdf(path: Path, pages: list[str]) -> Path:
    """Create a test PDF with specified text on each page."""
    c = canvas.Canvas(str(path), pagesize=letter)
    for i, text in enumerate(pages):
        c.drawString(100, 700, text)
        c.drawString(100, 680, f"Page {i + 1} of {len(pages)}")
        if i < len(pages) - 1:
            c.showPage()
    c.save()
    return path


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


class TestMergePdfs:
    def test_merge_single_page_pdfs(self, temp_dir):
        """Merge two single-page PDFs."""
        pdf1 = create_test_pdf(temp_dir / "doc1.pdf", ["Document 1 - Page 1"])
        pdf2 = create_test_pdf(temp_dir / "doc2.pdf", ["Document 2 - Page 1"])
        output = temp_dir / "merged.pdf"

        result = merge_pdfs(pdf1, pdf2, output)

        assert result.exists()
        reader = PdfReader(result)
        assert len(reader.pages) == 2

    def test_merge_multi_page_pdfs(self, temp_dir):
        """Merge PDFs with multiple pages each."""
        pdf1 = create_test_pdf(temp_dir / "doc1.pdf", ["Doc1 Page1", "Doc1 Page2", "Doc1 Page3"])
        pdf2 = create_test_pdf(temp_dir / "doc2.pdf", ["Doc2 Page1", "Doc2 Page2"])
        output = temp_dir / "merged.pdf"

        result = merge_pdfs(pdf1, pdf2, output)

        reader = PdfReader(result)
        assert len(reader.pages) == 5  # 3 + 2

    def test_page_order_preserved(self, temp_dir):
        """Verify pages appear in correct order (pdf1 first, then pdf2)."""
        pdf1 = create_test_pdf(temp_dir / "first.pdf", ["FIRST_DOC_MARKER"])
        pdf2 = create_test_pdf(temp_dir / "second.pdf", ["SECOND_DOC_MARKER"])
        output = temp_dir / "merged.pdf"

        merge_pdfs(pdf1, pdf2, output)

        reader = PdfReader(output)
        page1_text = reader.pages[0].extract_text()
        page2_text = reader.pages[1].extract_text()

        assert "FIRST_DOC_MARKER" in page1_text
        assert "SECOND_DOC_MARKER" in page2_text

    def test_missing_first_pdf_raises_error(self, temp_dir):
        """Error when first PDF doesn't exist."""
        pdf2 = create_test_pdf(temp_dir / "doc2.pdf", ["Page 1"])
        output = temp_dir / "merged.pdf"

        with pytest.raises(FileNotFoundError, match="First PDF not found"):
            merge_pdfs(temp_dir / "nonexistent.pdf", pdf2, output)

    def test_missing_second_pdf_raises_error(self, temp_dir):
        """Error when second PDF doesn't exist."""
        pdf1 = create_test_pdf(temp_dir / "doc1.pdf", ["Page 1"])
        output = temp_dir / "merged.pdf"

        with pytest.raises(FileNotFoundError, match="Second PDF not found"):
            merge_pdfs(pdf1, temp_dir / "nonexistent.pdf", output)

    def test_invalid_pdf_raises_error(self, temp_dir):
        """Error when input is not a valid PDF."""
        pdf1 = temp_dir / "not_a_pdf.pdf"
        pdf1.write_text("This is not a PDF file")
        pdf2 = create_test_pdf(temp_dir / "doc2.pdf", ["Page 1"])
        output = temp_dir / "merged.pdf"

        with pytest.raises(ValueError, match="Failed to read first PDF"):
            merge_pdfs(pdf1, pdf2, output)

    def test_creates_output_directory(self, temp_dir):
        """Output directory is created if it doesn't exist."""
        pdf1 = create_test_pdf(temp_dir / "doc1.pdf", ["Page 1"])
        pdf2 = create_test_pdf(temp_dir / "doc2.pdf", ["Page 1"])
        output = temp_dir / "subdir" / "nested" / "merged.pdf"

        result = merge_pdfs(pdf1, pdf2, output)

        assert result.exists()
        assert result.parent.exists()

    def test_returns_output_path(self, temp_dir):
        """Return value is the output path."""
        pdf1 = create_test_pdf(temp_dir / "doc1.pdf", ["Page 1"])
        pdf2 = create_test_pdf(temp_dir / "doc2.pdf", ["Page 1"])
        output = temp_dir / "merged.pdf"

        result = merge_pdfs(pdf1, pdf2, output)

        assert result == output

    def test_accepts_string_paths(self, temp_dir):
        """Works with string paths, not just Path objects."""
        pdf1 = create_test_pdf(temp_dir / "doc1.pdf", ["Page 1"])
        pdf2 = create_test_pdf(temp_dir / "doc2.pdf", ["Page 1"])
        output = temp_dir / "merged.pdf"

        result = merge_pdfs(str(pdf1), str(pdf2), str(output))

        assert result.exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
