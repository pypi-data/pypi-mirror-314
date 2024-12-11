########################################################################################################################
# IMPORTS

import logging

import requests

from ..params.nominatim import POSTCODES

########################################################################################################################
# CLASSES

logger = logging.getLogger(__name__)


class GeoNames:
    def __init__(self, endpoint):
        self.endpoint = endpoint

    @staticmethod
    def validate_postcode(postcode):
        if isinstance(postcode, int):
            postcode = str(postcode)

        if postcode and len(postcode) == 5 and postcode[:2] in POSTCODES:
            return postcode
        
        if postcode and len(postcode) == 4:
            postcode = f"0{postcode}"
            if postcode[:2] in POSTCODES:
                return postcode

    @staticmethod
    def get_province_from_postcode(postcode):
        if postcode:
            return POSTCODES[postcode[:2]]

    def reverse(self, lat, lon):
        return requests.get(f"{self.endpoint}/reverse?lat={lat}&lon={lon}").json()


class Nominatim:
    def __init__(self, nominatim_endpoint, geonames_endpoint):
        self.endpoint = nominatim_endpoint
        self.geonames = GeoNames(geonames_endpoint)

    @staticmethod
    def get_attribute(raw_json, keys):
        for key in keys:
            if key in raw_json:
                return raw_json[key]

    def geocode(self, address):
        return requests.get(f"{self.endpoint}/?q={address}&format=json").json()

    def geocode_parsed(self, address):
        results = self.geocode(address)

        if results:
            return self.reverse_parsed(results[0]["lat"], results[0]["lon"])

    def reverse(self, lat, lon):
        return requests.get(f"{self.endpoint}/reverse?lat={lat}&lon={lon}&format=json").json()

    def reverse_parsed(self, lat, lon):
        raw_json = self.reverse(lat, lon).get("address", {})
        geoname = self.geonames.reverse(lat, lon)

        postcode = self.geonames.validate_postcode(
            str(geoname.get("postal_code", ""))
        ) or self.geonames.validate_postcode(str(raw_json.get("postcode")))

        city = self.get_attribute(raw_json, ["city", "town", "village"]) or geoname.get("place_name")

        district, quarter = self.get_district_quarter(raw_json)
        return {
            "country": raw_json.get("country"),
            "country_code": raw_json.get("country_code") or geoname.get("country_code"),
            "state": raw_json.get("state") or geoname.get("community"),
            "province": self.geonames.get_province_from_postcode(postcode),
            "city": city,
            "postcode": postcode,
            "district": district,
            "quarter": quarter,
            "street": raw_json.get("road"),
            "number": raw_json.get("house_number"),
        }

    def get_district_quarter(self, raw_json):
        district = self.get_attribute(raw_json, ["city_district", "suburb", "borough"])
        quarter = self.get_attribute(raw_json, ["quarter", "neighbourhood"])

        if not district and quarter:
            district = quarter
            quarter = None

        return district, quarter


class NominatimInterface(Nominatim):
    def __init__(self, config):
        if "osm" in config:
            self.config = config["osm"]

            self.nominatim_endpoint = self.config["nominatim_endpoint"]
            self.geonames_endpoint = self.config["geonames_endpoint"]

            super().__init__(self.nominatim_endpoint, self.geonames_endpoint)
        else:
            logger.warning("no osm section in config")
