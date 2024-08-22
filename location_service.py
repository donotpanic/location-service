import argparse
import os
import re
import requests

api_key = os.environ.get('LOCATION_API_KEY')

class ApiKeyInvalid(Exception):
    pass

class ApiKeyMissing(Exception):
    pass

def get_by_city(city, country_code='US'):
    url = "http://api.openweathermap.org/geo/1.0/direct"

    params = {
        "q": f"{city},{country_code}",
        "limit": 1,
        "appid": api_key
    }

    if api_key is None: raise ApiKeyMissing("API key is missing")

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]
        else:
            print("No data returned for the specified city.")
            return None
    elif response.status_code == 401:
        raise ApiKeyInvalid
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)
        return None


def get_by_zipcode(zipcode, country_code='US'):
    url = "http://api.openweathermap.org/geo/1.0/zip"

    params = {
        "zip": f"{zipcode},{country_code}",
        "appid": api_key
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)
        return None


def get_lat_lon(*locations, country_code='US'):
    results = []
    keys = ["name", "lat", "lon"]

    # TODO: Wrap in Try/Except for improved error handling
    # TODO: User friendly message for api_key invalid (common)
    for loc in locations:
        if re.fullmatch(r'\d{5}', loc):
            data = get_by_zipcode(loc, country_code)
        elif re.fullmatch(r"^[A-Za-z]+(?:[\s-][A-Za-z]+)*, [A-Z]{2}$", loc):
            data = get_by_city(loc, country_code)
        else:
            data = None

        if data:
            result = {key: data.get(key) for key in keys if key in data}
            results.append(result)
        else:
            results.append(None)

    return results


def main():
    parser = argparse.ArgumentParser(description="Retrieve latitude, longitude, and city name for given locations.")
    parser.add_argument(
        'locations',
        nargs='+',
        help="List of city names or ZIP codes to retrieve information for."
    )
    parser.add_argument(
        '--country-code',
        default='US',
        help="Country code for ZIP code lookups (default is 'US')."
    )

    args = parser.parse_args()
    locations = args.locations
    country_code = args.country_code

    location_infos = get_lat_lon(*locations, country_code=country_code)

    for loc, info in zip(locations, location_infos):
        if info:
            print(f"Location: {loc}")
            print(f"  City: {info.get('name')}")
            print(f"  Latitude: {info.get('lat')}")
            print(f"  Longitude: {info.get('lon')}")
        else:
            print(f"Location: {loc} - Data could not be retrieved.")


if __name__ == "__main__":
    main()
