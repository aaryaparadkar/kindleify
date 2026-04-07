# Kindleify

Convert URLs and PDFs to EPUB format for Kindle.

## Installation

```bash
pip install kindleify
```

## Usage

### Convert URL to EPUB

```bash
kindleify url "https://example.com/article" -o article.epub
```

### Convert PDF to EPUB

```bash
kindleify pdf document.pdf -o book.epub
```

### Send to Kindle

First, configure your Kindle email:

```bash
kindleify config set
```

Then send EPUB to your Kindle:

```bash
kindleify send book.epub
```

### Commands

- `kindleify url` - Convert URL to EPUB
- `kindleify pdf` - Convert PDF to EPUB
- `kindleify send` - Send EPUB to Kindle
- `kindleify config set` - Configure Kindle credentials
- `kindleify config show` - Show current configuration
- `kindleify config clear` - Clear stored credentials

## License

MIT
