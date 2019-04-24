from datetime import date, datetime, timedelta
from django.core.mail import EmailMessage

from book.models import Book
from bookings.settings import EMAIL_HOST_USER


def send_flight_reminder_mail():
    date_format = '%Y-%m-%d %H:%M:%S'
    next_day = datetime.now().day + 1
    month = datetime.now().month
    year = datetime.now().year
    bookings =  Book.objects.select_related('user', 'flight').filter(
        flight__departure__day=next_day,
        flight__departure__month=month,
        flight__departure__year=year
    )

    email_list = []
    departure_datetime = set([])
    if bookings:
        for booking in bookings:
            email_list.append(booking.user.email)
            departure_datetime.add(booking.flight.departure.strftime(date_format))

        (element,) = departure_datetime
        message = EmailMessage(
            "Flight reminder",
            'Hello, this is a reminder that your flight is scheduled for {}'.format(element),
            EMAIL_HOST_USER,
            to=email_list
        ) 
        message.send()