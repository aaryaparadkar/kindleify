from pdf2epub import convert_pdf


def pdf_to_epub(input_path: str, output_path: str):
    """
    Convert PDF to EPUB using pdf2epub.
    """
    convert_pdf(input_path, output_path)
    return output_path
