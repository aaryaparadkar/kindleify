# Copyright (c) 2026 Kindleify
# MIT License - see LICENSE file

from pypdf import PdfReader
from ebooklib import epub

from kindleify.converter.epub_builder import EpubBuilder
from kindleify.converter.language import detect_language


def pdf_to_epub(input_path: str, output_path: str, language: str = "auto") -> str:
    """
    Convert PDF to EPUB using pypdf.
    If language is 'auto', detect from extracted text.
    """
    reader = PdfReader(input_path)

    title = reader.metadata.get("/Title", "") if reader.metadata else ""
    if not title:
        title = "Untitled"

    if language == "auto":
        sample_text = ""
        pages_to_sample = min(10, len(reader.pages))
        for i in range(pages_to_sample):
            text = reader.pages[i].extract_text()
            if text and text.strip():
                sample_text += text + "\n"
        language = detect_language(sample_text)

    book = epub.EpubBook()
    book.set_identifier("kindleify")
    book.set_title(title)
    book.set_language(language)

    chapters = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if not text.strip():
            continue

        chapter = epub.EpubHtml(
            title=f"Page {i + 1}", file_name=f"page_{i + 1}.xhtml", lang=language
        )

        html_content = f"""<html>
<head><title>Page {i + 1}</title></head>
<body>
<pre style="font-family: Georgia, serif; font-size: 1em; line-height: 1.6;">{text}</pre>
</body>
</html>"""
        chapter.set_content(html_content)

        book.add_item(chapter)
        chapters.append(chapter)

    nav = epub.EpubNav(file_name="nav.xhtml")
    book.add_item(nav)

    book.toc = tuple(chapters)
    book.spine = [nav] + chapters
    book.add_item(epub.EpubNcx())

    epub.write_epub(output_path, book)
    return output_path
