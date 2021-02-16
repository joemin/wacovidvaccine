import attr
import datetime
import logging
import time
from .base import VaccineLocation

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


@attr.s
class Costco(VaccineLocation):
    location_type: str = attr.ib(kw_only=True)
    name: str = attr.ib(kw_only=True)
    street_address: str = attr.ib(kw_only=True)
    city: str = attr.ib(kw_only=True)
    state: str = attr.ib(kw_only=True)
    zip_code: str = attr.ib(kw_only=True)
    county: str = attr.ib(kw_only=True)
    signup_url: str = attr.ib(kw_only=True)

    def scrape_availability(self):
        print(f'Scraping Costco location: {self.name} ({self.city})')
        # Selenium driver options
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(f'{self.signup_url}#/')

        max_tries = 3

        # Wait for book appointment button, then navigate to the availability page
        # The Costco pharmacy page sometimes just loads a blank screen so... retry
        for try_num in range(max_tries):
            try:
                book_appointment_button = WebDriverWait(driver, 10).until(
                    expected_conditions.element_to_be_clickable(
                        (By.CSS_SELECTOR, 'a[aria-label="Book Appointment"]')
                    )
                )
                break
            except TimeoutException as te:
                logging.info(f'Could not find book appointment button on try number {try_num}.')
                if try_num == max_tries-1:
                    logging.error('Failed to get book appointment button.')
                    raise te
                logging.info('Refreshing.')
                driver.refresh()
        book_appointment_button.click()

        # Wait for table to show
        for try_num in range(max_tries):
            try:
                availability_container = WebDriverWait(driver, 10).until(
                    expected_conditions.presence_of_element_located(
                        (By.CLASS_NAME, 'date-time-container')
                    )
                )
                break
            except TimeoutException as te:
                logging.info(f'Could not find date-time-container on try number {try_num}.')
                if try_num == max_tries-1:
                    logging.error('Failed to get date-time-container.')
                    raise te
                logging.info('Refreshing.')
                driver.refresh()
        available_dates = availability_container.find_elements_by_class_name('hours-col')

        if not available_dates:
            print(f'No availability at {self.name} ({self.city}).')
            return []

        print(f'Number of available dates: {len(available_dates)}')
        for available_date in available_dates:
            date = available_date.find_element_by_tag_name('h5').get_attribute('innerHTML')
            print(date)

    def __str__(self):
        return f'{self.name}: {self.signup_url}'
