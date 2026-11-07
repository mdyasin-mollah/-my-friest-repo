import os
import smtplib
from email.message import EmailMessage

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_wtf.csrf import CSRFProtect


def create_app():
    application = Flask(__name__)
    application.config.update(
        SECRET_KEY=os.environ.get("SECRET_KEY", "development-key-change-before-deploy"),
        MAX_CONTENT_LENGTH=16 * 1024,
        WTF_CSRF_TIME_LIMIT=3600,
    )
    CSRFProtect(application)

    @application.get("/")
    def home():
        return render_template("index.html")

    @application.post("/contact")
    def contact():
        if request.form.get("company_website", "").strip():
            flash("Thanks. Your message has been received.", "success")
            return redirect(url_for("home") + "#contact")

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        service = request.form.get("service", "").strip()
        message = request.form.get("message", "").strip()

        if not name or len(name) > 100:
            flash("Please enter your name (up to 100 characters).", "error")
        elif not email or len(email) > 254 or "@" not in email:
            flash("Please enter a valid email address.", "error")
        elif len(message) < 10 or len(message) > 5000 or len(service) > 100:
            flash("Please choose a service and write a message between 10 and 5,000 characters.", "error")
        else:
            smtp_host = os.environ.get("SMTP_HOST")
            destination = os.environ.get("CONTACT_EMAIL")
            sender = os.environ.get("MAIL_FROM")
            username = os.environ.get("SMTP_USERNAME")
            password = os.environ.get("SMTP_PASSWORD")

            if not all((smtp_host, destination, sender, username, password)):
                flash(
                    "The contact form inbox is not configured yet. Please contact the site owner.",
                    "error",
                )
            else:
                mail = EmailMessage()
                mail["Subject"] = f"Website enquiry — {service or 'General'}"
                mail["From"] = sender
                mail["To"] = destination
                mail["Reply-To"] = email
                mail.set_content(
                    f"New enquiry from NEXT IT BD website\n\n"
                    f"Name: {name}\nEmail: {email}\nService: {service or 'Not specified'}\n\n"
                    f"Message:\n{message}"
                )
                try:
                    port = int(os.environ.get("SMTP_PORT", "587"))
                    if os.environ.get("SMTP_USE_SSL", "false").lower() == "true":
                        with smtplib.SMTP_SSL(smtp_host, port, timeout=15) as smtp:
                            smtp.login(username, password)
                            smtp.send_message(mail)
                    else:
                        with smtplib.SMTP(smtp_host, port, timeout=15) as smtp:
                            smtp.ehlo()
                            smtp.starttls()
                            smtp.ehlo()
                            smtp.login(username, password)
                            smtp.send_message(mail)
                    flash("Thanks! Your enquiry has been sent successfully.", "success")
                except (OSError, smtplib.SMTPException, ValueError):
                    application.logger.exception("Contact form email delivery failed")
                    flash("We couldn't send your message right now. Please try again later.", "error")

        return redirect(url_for("home") + "#contact")

    return application


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")), debug=False)
