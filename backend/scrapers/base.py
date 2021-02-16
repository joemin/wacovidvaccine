import attr
import datetime

from typing import List

@attr.s
class Availability():
    date: datetime.date = attr.ib(kw_only=True)
    slots_available: List[datetime.time] = attr.ib(kw_only=True)

@attr.s
class VaccineLocation():
    location_type: str = attr.ib(kw_only=True)
    name: str = attr.ib(kw_only=True)
    street_address: str = attr.ib(kw_only=True)
    city: str = attr.ib(kw_only=True)
    state: str = attr.ib(kw_only=True)
    zip_code: str = attr.ib(kw_only=True)
    county: str = attr.ib(kw_only=True)
    signup_url: str = attr.ib(kw_only=True)

    def scrape_availability(self):
        pass

    def __str__(self):
        return f'{self.name}: {self.signup_url}'
