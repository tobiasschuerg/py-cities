import csv
import json
import os
from collections import defaultdict

import pycountry
from unidecode import unidecode

from region_mapping import region_mapping
from update import download_and_unzip

INPUT_DATA_FILE_NAME = "data/allCountries.txt"


def name_equals(sub_name, other):
    sub_name_decoded = unidecode(sub_name.replace("-", ""))
    other_decoded = unidecode(other.replace("-", ""))
    return sub_name_decoded.casefold() == other_decoded.casefold()


def find_subdivision(county_code, region_only_code, region_name):
    if region_only_code:
        region_code = county_code + "-" + region_only_code
        mapped_region_code = region_mapping.get(region_code, region_code)
        subdivision = pycountry.subdivisions.get(code=mapped_region_code)
        if subdivision is not None:
            return subdivision
    # try to get subdivision by region name:
    if region_name is not None:
        subs = pycountry.subdivisions.get(country_code=county_code)

        subs = list(filter(lambda sub: name_equals(sub.name, region_name), subs))
        if len(subs) > 0:
            return subs[0]
        # else:
        # else google?

    if county_code == 'AS': return pycountry.subdivisions.get(code='US-AS')
    if county_code == 'AX': return pycountry.subdivisions.get(code='FI-01')

    print(f'... unable to determine a region for {county_code} "{region_name}"')
    return None


def create_cities():
    all_cities_by_country = defaultdict(list)
    all_countries_skipped = 0
    all_countries_total = 0
    with open(INPUT_DATA_FILE_NAME, encoding='utf-8') as file:
        tsv_file = csv.reader(file, delimiter="\t")
        for line in tsv_file:
            all_countries_total += 1
            country_code = line[0]

            if country_code not in {"AT", "CH", "FR", "DE", "PL"}:
                all_countries_skipped += 1
                continue

            city_name = line[2]
            region_name = line[3]
            region_only_code = line[4]

            subdivision = find_subdivision(country_code, region_only_code, region_name)
            if subdivision is None:
                print(f'{city_name} has no region')
                all_countries_skipped += 1
                continue

            city = {
                "name": city_name,
                "country_code": country_code,
                "region_code": subdivision.code,
                "postal_code": line[1],
                "region_name": region_name
            }
            all_cities_by_country[country_code].append(city)
            # print(x)
    file.close()
    print('\n===\n')
    print(f'Done - skipped {all_countries_skipped} of {all_countries_total} cities.')

    for key, value in all_cities_by_country.items():
        with open(f'output/cities_{key}.json', 'w', encoding='utf-8') as f:
            json.dump(value, f, ensure_ascii=False, indent=2)


def check_same_city(city_to_match, city_name):
    return city_to_match.get('nameLowerCase') == city_name.lower()


if __name__ == '__main__':
    if not os.path.isfile(INPUT_DATA_FILE_NAME):
        download_and_unzip()

    create_cities()
