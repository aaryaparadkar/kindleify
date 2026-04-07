import trafilatura
from trafilatura.metadata import extract_metadata

from kindleify.converter.epub_builder import EpubBuilder
from kindleify.utils import sanitize_filename


def url_to_epub(url: str, output_path: str | None = None) -> str:
    """
    Convert a URL into an EPUB file.
    Returns the output file path.
    """

    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        raise ValueError("Failed to fetch URL content")

    text = trafilatura.extract(downloaded, output_format="html", include_comments=False)
    if not text:
        raise ValueError("Failed to extract readable content")

    body_content = (
        text.replace("<html>", "")
        .replace("</html>", "")
        .replace("<body>", "")
        .replace("</body>", "")
        .strip()
    )

    metadata = extract_metadata(downloaded)
    title = metadata.title if metadata and metadata.title else "Untitled"

    html_content = f"""<html>
<head>
    <title>{title}</title>
    <style>
        body {{ font-family: Georgia, serif; font-size: 1em; line-height: 1.6; padding: 1em; }}
        p {{ margin-bottom: 1em; }}
        li {{ margin-bottom: 0.5em; }}
    </style>
</head>
<body>
{body_content}
</body>
</html>"""

    if not output_path:
        filename = sanitize_filename(title) or "book"
        output_path = f"{filename}.epub"

    builder = EpubBuilder(title)
    builder.add_chapter("Content", html_content)
    builder.build(output_path)

    return output_path
