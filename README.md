# py-cities

Small python script which uses [pycountry](https://pypi.org/project/pycountry/)
and [geonames.org](https://download.geonames.org/export/zip/) in order to create JSONs for "all" (?) cities in the
world.

Sadly the region codes used by geonames are sometimes outdated or
use [FIPS region codes](https://en.wikipedia.org/wiki/List_of_FIPS_region_codes). That's the reason why some kind of
manual mapping is still needed.

## usage

Just run `py ./main.py` which will download and unzip data from geonames.org and with the help of pycountry add the correct country (
ISO 3166) and region (3166-2) codes.

## output

Resulting output will be in `/output/cities_{country_code}.json` with each entry looking like:

```json
{
  "name": "Lüneburg",
  "country_code": "DE",
  "region_code": "DE-NI",
  "postal_code": "21337",
  "region_name": "Niedersachsen"
}
```

See [output/cities_DE.json](output/cities_DE.json) for example.


