import os
import requests
from dotenv import load_dotenv

load_dotenv()

DOMAIN = os.getenv("MAILGUN_DOMAIN")


def send_simple_message(to, subject, body):
    return requests.post(
        f"https://api.mailgun.net/v3/{DOMAIN}/messages",
        auth=("api", os.getenv("MAILGUN_API_KEY")),
        data={
            "from": f"MCQ <mailgun@{DOMAIN}>",
            "to": [to],
            "subject": [subject],
            "text": [body],
        },
    )


def send_employee_added_email(admin_email, first_name, last_name):
    return send_simple_message(
        admin_email,
        "An employee was successfully added to the HR REST API.",
        f"Employee added: {first_name} {last_name}",
    )
