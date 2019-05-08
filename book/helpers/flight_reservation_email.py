from django.core.mail import EmailMessage
from bookings.settings import EMAIL_HOST_USER


async def send_flight_reservation_email(user, flight_number, departure):
    message = EmailMessage(
        "Booking Info",
        "Thanks {} for booking this flight. Flight number is {} and departure is {}".format(
            user.username, flight_number, departure
        ),
        EMAIL_HOST_USER,
        to=[user.email],
    )
    message.send()
