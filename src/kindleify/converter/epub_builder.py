# Copyright (c) 2026 Kindleify
# MIT License - see LICENSE file

from ebooklib import epub


class EpubBuilder:
    def __init__(self, title: str):
        self.book = epub.EpubBook()
        self.book.set_identifier("kindleify")
        self.book.set_title(title)
        self.book.set_language("en")
        self.chapters = []

    def add_chapter(self, title: str, content: str):
        chapter = epub.EpubHtml(title=title, file_name=f"{title}.xhtml", lang="en")
        chapter.set_content(content)

        self.book.add_item(chapter)
        self.chapters.append(chapter)

    def build(self, output_path: str):
        # Create nav first
        nav = epub.EpubNav(file_name="nav.xhtml")
        self.book.add_item(nav)

        # Set TOC
        self.book.toc = tuple(self.chapters)

        # Set spine - reading order (nav first, then chapters)
        self.book.spine = [nav] + self.chapters

        # Add NCX for backward compatibility
        self.book.add_item(epub.EpubNcx())

        epub.write_epub(output_path, self.book)
