from django.conf import settings
from django.core.mail import send_mail
from core.models import PhoneNumber, SecondaryEmail, User, Quotes
from celery import shared_task
from dotenv import load_dotenv
from twilio.rest import Client

import random
import requests
import os

load_dotenv()
TWILIO_API_KEY = os.getenv("TWILIO_API_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")

QUOTES_API_KEY = os.getenv("QUOTES_API_KEY")

QUOTES_API = "https://api.api-ninjas.com/v1/quotes?category="

QUOTES_CATEGORIES = ["happiness", "inspirational", "courage", "knowledge"]

@shared_task()
def send_welcome_email_task(username, email):
    send_mail(
        subject=f"Welcome to Quote a Day, {username}!",
        message="""Thank you for signing up for quote a day!
You will recieve your first quote at 1pm EST""",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
    )

@shared_task()
def get_quote_task():
    response = requests.get(
        f"{QUOTES_API}{random.choice(QUOTES_CATEGORIES)}",
        headers={"X-Api-Key": QUOTES_API_KEY},
    )
    print(response.json())
    quote_data = response.json()[0]
    quote_entry = Quotes(quote=quote_data["quote"], author=quote_data["author"])
    quote_entry.save()

@shared_task()
def queue_email_task():
    quote = Quotes.objects.latest("date")
    emails = User.objects.all()
    second_emails = SecondaryEmail.objects.all()
    for email in emails:
        send_quote_email_task.delay(quote.quote, quote.author, email.email)
    for email in second_emails:
        send_quote_email_task.dekay(quote.quote, quote.author,  email.email)

@shared_task()
def send_quote_email_task(quote, quote_author, email):
    send_mail(
        subject=f"Your daily quote!",
        message=f"{quote} \n -{quote_author}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )

@shared_task()
def queue_sms_task():
    quote = Quotes.objects.latest("date")
    nums = PhoneNumber.objects.all()
    for num in nums:
        send_quote_sms_task.delay(quote.quote, quote.author, num.phone_number)

@shared_task()
def send_quote_sms_task(quote, quote_author, phone_num):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_API_KEY)
    message = client.messages.create(
        body=f"Your daily quote!\n{quote} \n -{quote_author}",
        from_="+18555402978",
        to=f"+1{phone_num}",
    )
