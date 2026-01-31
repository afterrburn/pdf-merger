# PDF Merger

A simple command-line tool to merge two PDF files into one.

## Requirements

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

## Installation

```bash
git clone https://github.com/afterrburn/pdf-merger.git
cd pdf-merger
uv sync
```

## Usage

```bash
uv run python pdf_merger.py <first.pdf> <second.pdf> -o <output.pdf>
```

### Example

```bash
uv run python pdf_merger.py document1.pdf document2.pdf -o combined.pdf
```

The first PDF's pages will appear first, followed by the second PDF's pages.

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `-o`, `--output` | Output file path | `merged.pdf` |

## Running Tests

```bash
uv sync --extra dev
uv run pytest -v
```
