# Copyright (c) 2026 Kindleify
# MIT License - see LICENSE file

import os
from pathlib import Path

from kindleify.converter.pdf import pdf_to_epub
from kindleify.converter.url import url_to_epub
from kindleify.utils import sanitize_filename


def batch_pdfs(input_dir: str, output_dir: str, language: str = "auto") -> list[str]:
    """
    Recursively find all PDFs in input_dir and convert to EPUB.
    Preserves directory structure in output_dir.
    Returns list of output file paths.
    """
    input_path = Path(input_dir).resolve()
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    output_files = []

    for root, _, files in os.walk(input_path):
        for file in files:
            if not file.lower().endswith(".pdf"):
                continue

            pdf_path = Path(root) / file
            rel_path = pdf_path.relative_to(input_path)

            epub_filename = sanitize_filename(rel_path.stem) + ".epub"

            if rel_path.parent != Path(""):
                output_subdir = output_path / rel_path.parent
                output_subdir.mkdir(parents=True, exist_ok=True)
                output_file = output_subdir / epub_filename
            else:
                output_file = output_path / epub_filename

            try:
                pdf_to_epub(str(pdf_path), str(output_file), language)
                output_files.append(str(output_file))
            except Exception as e:
                print(f"Error converting {pdf_path}: {e}")

    return output_files


def batch_urls(urls_file: str, output_dir: str, language: str = "auto") -> list[str]:
    """
    Read URLs from file (one per line) and convert to EPUB.
    Saves to output_dir with one file per URL.
    Returns list of output file paths.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    output_files = []

    with open(urls_file, "r") as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    for i, url in enumerate(urls):
        try:
            output_file = output_path / f"url_{i + 1}.epub"
            url_to_epub(url, str(output_file), language)
            output_files.append(str(output_file))
        except Exception as e:
            print(f"Error converting {url}: {e}")

    return output_files