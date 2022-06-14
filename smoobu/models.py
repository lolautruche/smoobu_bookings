from datetime import timedelta, date


def parse_date_string(date_as_string: str) -> date:
    """
    Parses YYY-MM-DD string to convert it as date object.
    I know, I could have used dateutil, but I wanted to only use stdlib
    """
    year, month, day = date_as_string.split('-')

    return date(int(year), int(month), int(day))


class SmoobuBooking:
    """
    Class representing a reservation in Smoobu
    """

    overdue_delta = timedelta(days=30)
    # 940882: Direct reservation (manually defined)
    # 940885: From the website (aka "Homepage")
    direct_booking_ids = (940882, 940885)

    def __init__(self, booking: dict):
        self._inner_booking = booking
        self.id = booking['id']
        self.arrival = parse_date_string(booking['arrival'])
        self.departure = parse_date_string(booking['departure'])
        self.apartment = booking['apartment']['name']
        self.apartment_id = booking['apartment']['id']
        self.channel = booking['channel']['name']
        self.channel_id = booking['channel']['id']
        self.guest = SmoobuGuest(booking['firstname'], booking['lastname'], booking['email'], booking['phone'])
        self.price = booking['price']
        self.fully_paid = booking['price-paid'] == 'Yes'
        self.prepayment = booking['prepayment']
        self.prepayment_paid = booking['prepayment-paid'] == 'Yes'
        self.guest_app = booking['guest-app-url']

    def __str__(self):
        return f'Booking #{self.id} ({self.guest}) from {self.arrival} to {self.departure}'

    def __repr__(self):
        return str(self.__str__())

    def is_overdue(self) -> bool:
        return not self.fully_paid and (self.arrival - date.today()) <= self.overdue_delta

    def is_direct_booking(self) -> bool:
        return self.channel_id in self.direct_booking_ids


class SmoobuGuest:
    """
    Class representing a guest in Smoobu
    """

    def __init__(self, firstname: str, lastname: str, email: str, phone: str):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.phone = phone

    def __str__(self):
        return f'{self.firstname} {self.lastname}'
