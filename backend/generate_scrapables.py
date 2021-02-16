import attr
import json
import logging
import os
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from scrapers.base import VaccineLocation


def parse_location(location_type, county_name, county_location) -> VaccineLocation:
    signup_url = county_location.find_element_by_tag_name('a').get_attribute('href')
    name = county_location.find_element_by_tag_name('a').get_attribute('innerHTML')
    location_info = county_location.find_element_by_class_name('col-sm-6').find_elements_by_tag_name('p')
    street_address = location_info[1].get_attribute('innerHTML')
    other_address_info = location_info[2].get_attribute('innerHTML').split(', ')
    city = other_address_info[0].strip()
    state_and_zip = other_address_info[1].split(' ')
    state = state_and_zip[0]
    zip_code = state_and_zip[1]
    vaccine_location = VaccineLocation(
        location_type=location_type,
        name=name,
        street_address=street_address,
        city=city,
        state=state,
        zip_code=zip_code,
        county=county_name,
        signup_url=signup_url
    )
    return vaccine_location


def generate_scrapables():
    # Selenium driver options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)

    wa_doh_url = 'https://www.doh.wa.gov/YouandYourFamily/Immunization/VaccineLocations'
    driver.get(wa_doh_url)
    driver.implicitly_wait(15)

    supported_location_types = ['Costco']
    locations = []

    # Expand locations list for each county
    # TODO: use custom `until` wait conditions for WebDriver
    counties = driver.find_elements_by_class_name('panel-default')
    while len(counties) < 39:
        logging.warning('Waiting for counties to load.')
        WebDriverWait(driver, 5)
        counties = driver.find_elements_by_class_name('panel-default')
    for county in counties:
        county_name = county.find_element_by_class_name('panel-title').text
        print(f'Scraping {county_name}')
        county_locations = county.find_elements_by_class_name('row')
        for county_location in county_locations:
            location_name = county_location.get_attribute('data-search-content')
            for supported_location_type in supported_location_types:
                if supported_location_type not in location_name:
                    continue
                locations.append(
                    attr.asdict(parse_location(
                        supported_location_type, county_name, county_location
                    ))
                )

    project_root = os.environ.get('PROJECT_ROOT', '/wacv')
    results_dir = f'{project_root}/results'
    locations_file = f'{results_dir}/locations.json'
    with open(locations_file, 'w') as f:
        json.dump(locations, f, indent=4)
