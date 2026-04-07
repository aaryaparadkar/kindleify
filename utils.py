import re

def text_to_html(text: str) -> str:
    """
    Convert plain text into basic HTML paragraphs.
    """
    paragraphs = text.split("\n\n")
    html = "".join(f"<p>{p.strip()}</p>" for p in paragraphs if p.strip())
    return html

def sanitize_filename(name: str) -> str:
    """
    Remove invalid filename characters.
    """
    return re.sub(r'[<>:"/\\|?*]+', "", name).strip().replace(" ", "_")
