#! /usr/bin/env python
import configparser

from smoobu import SmoobuBookingsFetcher

config = configparser.ConfigParser()
config.read('config.ini')
API_KEY = config['Default']['SMOOBU_API_KEY']


if __name__ == '__main__':
    in_debt_bookings = SmoobuBookingsFetcher(API_KEY).get_overdue_direct_bookings()
    print(in_debt_bookings)
