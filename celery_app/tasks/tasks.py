import asyncio

from app.event.services import EventService
from celery_app import celery_app
from core.utils.email_sender import EmailSender


@celery_app.task(name="send_notifications")
def send_notifications():
    events = asyncio.run(EventService().get_upcoming_events())
    for event in events:
        EmailSender().send_email(..., ..., [subscriber.email for subscriber in event.subscribers])
