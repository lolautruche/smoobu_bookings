import json
from urllib import request

from smoobu.models import SmoobuBooking


class SmoobuBookingsFetcher:
    """
    Fetches all upcoming reservations from Smoobu.
    """

    API_URL = 'https://login.smoobu.com/api/reservations?pageSize=100'

    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch(self) -> list[SmoobuBooking]:
        """Returns all the upcoming reservations as a list of SmoobuBooking objects"""
        headers = {
            'Api-Key': self.api_key,
            'Cache-Control': 'no-cache'
        }
        req = request.Request(self.API_URL, headers=headers)
        json_value = request.urlopen(req).read()

        bookings = []
        json_bookings = json.loads(json_value)
        for booking_dict in json_bookings['bookings']:
            bookings.append(SmoobuBooking(booking_dict))

        return bookings

    def get_overdue_direct_bookings(self) -> list:
        return [booking for booking in self.fetch() if booking.is_overdue() and booking.is_direct_booking()]
