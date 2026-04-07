import smtplib
from email.message import EmailMessage


def send_to_kindle(
    file_path: str,
    to_email: str,
    from_email: str,
    app_password: str
):
    """
    Send EPUB file to Kindle via email.
    """

    msg = EmailMessage()
    msg["Subject"] = "Kindleify Book"
    msg["From"] = from_email
    msg["To"] = to_email

    msg.set_content("Sent via Kindleify")

    with open(file_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="epub+zip",
            filename="book.epub"
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(from_email, app_password)
        smtp.send_message(msg)
