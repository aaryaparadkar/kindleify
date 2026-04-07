# Copyright (c) 2026 Kindleify
# MIT License - see LICENSE file

import click

from kindleify import config as cfg
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
@click.option("--to", default=None, help="Kindle email address")
@click.option("--from-email", default=None, help="Sender email")
@click.option("--password", default=None, help="App password")
def send(file, to, from_email, password):
    """Send EPUB to Kindle"""
    try:
        send_to_kindle(file, to, from_email, password)
        click.echo(f"Sent {file}")
    except ValueError as e:
        raise click.ClickException(str(e))


@cli.group()
def config():
    """Manage Kindleify configuration"""
    pass


@config.command("set")
def config_set():
    """Set Kindle email credentials"""
    click.echo("Configure your Kindle email settings:")

    to_email = click.prompt("Kindle email address", type=str)
    from_email = click.prompt("Sender email (Gmail)", type=str)
    password = click.prompt("Gmail app password", type=str, hide_input=True)

    cfg.set_kindle_config(to_email, from_email, password)
    click.echo("Configuration saved!")


@config.command("show")
def config_show():
    """Show current configuration"""
    kindle_cfg = cfg.get_kindle_config()

    if not kindle_cfg:
        click.echo("No configuration found. Run: kindleify config set")
        return

    to_email = kindle_cfg.get("to_email", "")
    from_email = kindle_cfg.get("from_email", "")
    password = kindle_cfg.get("password", "")
    masked = "•" * 8 if password else ""

    click.echo(f"Kindle email: {to_email}")
    click.echo(f"Sender email: {from_email}")
    click.echo(f"Password: {masked}")


@config.command("clear")
def config_clear():
    """Clear stored configuration"""
    if not cfg.has_kindle_config():
        click.echo("No configuration to clear.")
        return

    if click.confirm("Clear all stored credentials?"):
        cfg.clear_kindle_config()
        click.echo("Configuration cleared.")
    else:
        click.echo("Cancelled.")
