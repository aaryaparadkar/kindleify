import trafilatura
from trafilatura.metadata import extract_metadata

from kindleify.converter.epub_builder import EpubBuilder
from kindleify.utils import text_to_html, sanitize_filename


def url_to_epub(url: str, output_path: str | None = None) -> str:
    """
    Convert a URL into an EPUB file.
    Returns the output file path.
    """

    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        raise ValueError("Failed to fetch URL content")

    text = trafilatura.extract(downloaded)
    if not text:
        raise ValueError("Failed to extract readable content")

    metadata = extract_metadata(downloaded)
    title = metadata.title if metadata and metadata.title else "Untitled"

    html_content = f"<html><body>{text_to_html(text)}</body></html>"

    if not output_path:
        filename = sanitize_filename(title) or "book"
        output_path = f"{filename}.epub"

    builder = EpubBuilder(title)
    builder.add_chapter("Content", html_content)
    builder.build(output_path)

    return output_path
