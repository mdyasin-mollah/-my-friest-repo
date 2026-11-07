# NEXT IT BD — Company Website

A professional, responsive company website for NEXT IT BD, built with Python Flask.

## Features

- Premium responsive landing page with mobile navigation
- Services, about, process, FAQ and contact sections
- Accessible navigation and reduced-motion support
- Contact form with server-side validation, CSRF protection and bot honeypot
- Optional SMTP email delivery configured through environment variables
- Render deployment configuration

## Technology

- Python 3.11+
- Flask and Flask-WTF
- HTML, CSS and vanilla JavaScript
- Gunicorn for production

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000.

## Contact form setup

The form only sends email after SMTP settings are configured. Add these environment variables in your hosting provider:

- `SECRET_KEY`: a long random secret
- `SMTP_HOST`: SMTP server hostname
- `SMTP_PORT`: usually 587 (STARTTLS) or 465 (SSL)
- `SMTP_USERNAME`
- `SMTP_PASSWORD`
- `CONTACT_EMAIL`: destination inbox
- `MAIL_FROM`: verified sender address
- `SMTP_USE_SSL`: `true` when using port 465

Never commit passwords or secret keys to GitHub. Until SMTP is configured, the contact form will show a clear notice rather than claiming an email was sent.

## Deploy on Render

1. Create a new Web Service in Render and connect this repository.
2. Render can use the included `render.yaml` build and start commands.
3. Set a strong `SECRET_KEY` in the service environment.
4. Add SMTP environment variables to enable contact email delivery.

## Project structure

```
.
├── app.py
├── requirements.txt
├── render.yaml
├── Procfile
├── templates/
│   └── index.html
└── static/
    ├── css/style.css
    └── js/main.js
```

## Brand details

The site uses the NEXT IT BD name, Dhaka, Bangladesh location and the existing website link https://nextit-bd.web.app/. Service descriptions and illustrative design elements are starter content; confirm all company claims and replace sample details with verified information before launch.
