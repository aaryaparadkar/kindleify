# Copyright (c) 2026 Kindleify
# MIT License - see LICENSE file

import smtplib
from email.message import EmailMessage

from kindleify import config as cfg


def send_to_kindle(
    file_path: str,
    to_email: str | None = None,
    from_email: str | None = None,
    app_password: str | None = None,
):
    """
    Send EPUB file to Kindle via email.
    Uses stored credentials if not provided as arguments.
    """
    stored = cfg.get_kindle_config()

    to_email = to_email or stored.get("to_email")
    from_email = from_email or stored.get("from_email")
    app_password = app_password or stored.get("password")

    if not to_email:
        raise ValueError("Kindle email not configured. Run: kindleify config")
    if not from_email or not app_password:
        raise ValueError("Sender credentials not configured. Run: kindleify config")

    msg = EmailMessage()
    msg["Subject"] = "Kindleify Book"
    msg["From"] = from_email
    msg["To"] = to_email

    msg.set_content("Sent via Kindleify")

    with open(file_path, "rb") as f:
        msg.add_attachment(
            f.read(), maintype="application", subtype="epub+zip", filename="book.epub"
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(from_email, app_password)
        smtp.send_message(msg)


def send_batch_to_kindle(
    file_paths: list[str],
    to_email: str | None = None,
    from_email: str | None = None,
    app_password: str | None = None,
):
    """
    Send multiple EPUB files to Kindle via email.
    Uses stored credentials if not provided as arguments.
    """
    stored = cfg.get_kindle_config()

    to_email = to_email or stored.get("to_email")
    from_email = from_email or stored.get("from_email")
    app_password = app_password or stored.get("password")

    if not to_email:
        raise ValueError("Kindle email not configured. Run: kindleify config")
    if not from_email or not app_password:
        raise ValueError("Sender credentials not configured. Run: kindleify config")

    msg = EmailMessage()
    msg["Subject"] = f"Kindleify Books ({len(file_paths)} files)"
    msg["From"] = from_email
    msg["To"] = to_email

    msg.set_content(f"Sent via Kindleify - {len(file_paths)} books")

    for file_path in file_paths:
        with open(file_path, "rb") as f:
            filename = file_path.split("/")[-1]
            msg.add_attachment(
                f.read(), maintype="application", subtype="epub+zip", filename=filename
            )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(from_email, app_password)
        smtp.send_message(msg)
