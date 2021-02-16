import json
import os
import time
from selenium.common.exceptions import WebDriverException

from scrapers.costco import Costco
from generate_scrapables import generate_scrapables

def main():
    project_root = os.environ.get('PROJECT_ROOT', '/wacv')
    results_dir = f'{project_root}/results'
    locations_file = f'{results_dir}/locations.json'

    if not os.path.isfile(locations_file):
        print('Generating Scrapables, part of a balanced breakfast!')
        generate_scrapables()

    with open(locations_file, 'r') as f:
        locations = json.load(f)

    parsed_locations = []
    for location in locations:
        max_tries = 3
        if location['location_type'] == 'Costco':
            costco_location = (Costco(**location))
            for try_num in range(max_tries):
                try:
                    availability_for_location = costco_location.scrape_availability()
                    break
                except WebDriverException as wde:
                    if try_num == max_tries-1:
                        raise wde
                    # Maybe this will help?
                    time.sleep(5)
            # parsed_locations.append(costco_location)

if __name__ == "__main__":
    main()
