# PDF Merger

Merge two PDF files into one.

## Setup (One Time)

Open Terminal and run:

```bash
# Install uv (Python package manager)
brew install uv

# Download this tool
git clone https://github.com/afterrburn/pdf-merger.git
cd pdf-merger

# Install dependencies
uv sync
```

## How to Merge PDFs

```bash
cd pdf-merger
uv run python pdf_merger.py first.pdf second.pdf -o combined.pdf
```

Replace `first.pdf` and `second.pdf` with your actual file paths.

### Example

```bash
uv run python pdf_merger.py ~/Downloads/doc1.pdf ~/Downloads/doc2.pdf -o ~/Desktop/merged.pdf
```

This creates `merged.pdf` on your Desktop with all pages from `doc1.pdf` followed by all pages from `doc2.pdf`.
