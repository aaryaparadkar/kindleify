import click

from kindleify.converter.url import url_to_epub
from kindleify.converter.pdf import pdf_to_epub
from kindleify.delivery.kindle import send_to_kindle


@click.group()
def cli():
    """Kindleify CLI"""
    pass


@cli.command()
@click.argument("url")
@click.option("-o", "--output", default=None, help="Output EPUB file")
def url(url, output):
    """Convert URL to EPUB"""
    path = url_to_epub(url, output)
    click.echo(f"Saved EPUB: {path}")


@cli.command()
@click.argument("pdf_path")
@click.option("-o", "--output", default="output.epub", help="Output EPUB file")
def pdf(pdf_path, output):
    """Convert PDF to EPUB"""
    pdf_to_epub(pdf_path, output)
    click.echo(f"Saved EPUB: {output}")


@cli.command()
@click.argument("file")
@click.option("--to", required=True, help="Kindle email address")
@click.option("--from-email", required=True, help="Sender email")
@click.option("--password", required=True, help="App password")
def send(file, to, from_email, password):
    """Send EPUB to Kindle"""
    send_to_kindle(file, to, from_email, password)
    click.echo(f"Sent {file} to {to}")
