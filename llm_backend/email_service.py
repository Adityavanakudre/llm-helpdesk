import smtplib
from email.message import EmailMessage

# Replace with your sending email and password (for Gmail use App Password)
EMAIL_ADDRESS = "adityavanakudre15@gmail.com"
EMAIL_PASSWORD = "efwc pzit uuxp jyek"  # Don't use real password if 2FA is enabled

def send_ticket_confirmation(user_email, ticket_id, category, message):
    msg = EmailMessage()
    msg["Subject"] = f"IT Ticket Confirmation: {ticket_id}"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = user_email

    msg.set_content(f"""
Hello,

Your support ticket has been received and is being processed.

Ticket ID: {ticket_id}
Category: {category}
Your Message: {message}

We will notify you once it's resolved.

Thank you,
IT Helpdesk
""")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print("❌ Email failed:", e)
        return False


def send_ticket_resolution_email(to_email, ticket_id, final_response):
    from email.message import EmailMessage
    import smtplib

    EMAIL_ADDRESS = "adityavanakudre15@gmail.com"
    EMAIL_PASSWORD = "efwc pzit uuxp jyek"

    msg = EmailMessage()
    msg["Subject"] = f"Your Ticket #{ticket_id} Has Been Resolved"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email

    msg.set_content(f"""
Hello,

Your ticket has been resolved by our IT team.

Ticket ID: {ticket_id}
Response:
{final_response}

If the issue persists, feel free to submit a new ticket.

Regards,  
IT Helpdesk
""")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("✅ Resolution email sent.")
    except Exception as e:
        print("❌ Email sending failed:", e)
