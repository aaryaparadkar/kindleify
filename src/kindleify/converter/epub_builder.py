from ebooklib import epub

class EpubBuilder:
    def __init__(self, title: str):
        self.book = epub.EpubBook()
        self.book.set_identifier("kindleify")
        self.book.set_title(title)
        self.book.set_language("en")
        self.chapters = []

    def add_chapter(self, title: str, content: str):
        chapter = epub.EpubHtml(
            title=title,
            file_name=f"{title}.xhtml",
            lang="en"
        )
        chapter.content = content

        self.book.add_item(chapter)
        self.chapters.append(chapter)

    def build(self, output_path: str):
        self.book.toc = tuple(self.chapters)

        self.book.add_item(epub.EpubNcx())
        self.book.add_item(epub.EpubNav())

        epub.write_epub(output_path, self.book)
