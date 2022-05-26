from django.conf import settings
from django.core.mail import send_mail


def send_approval_email_to_user(name, email):
    subject = 'Sahibmoney Payment Approved'
    message = f'Hi {name}, your payment on Sahibmoney has been approved.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    send_mail( subject, message, email_from, recipient_list )


def send_refusal_email_to_user(name, email):
    subject = 'Sahibmoney Payment Declined'
    message = f'Hi {name}, your payment on Sahibmoney has been declined.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    send_mail( subject, message, email_from, recipient_list )


def send_payment_request_email_to_admin(url):
    subject = 'Payment Request Initiated'
    message = f'Hi Admin, a payment <a href="{url}" target ="_blank">request</a> on Sahibmoney has been initiated.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [settings.APP_ADMIN_EMAIL, ]
    send_mail( subject, message, email_from, recipient_list )
