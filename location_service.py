import os
import re
import requests

api_key = os.environ.get('location_api_key')


def get_by_city(city, country_code='US'):
    url = "http://api.openweathermap.org/geo/1.0/direct"

    params = {
        "q": f"{city},{country_code}",
        "limit": 1,
        "appid": api_key
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]
        else:
            print("No data returned for the specified city.")
            return None
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

    for loc in locations:
        if re.fullmatch(r'\d{5}', loc):
            data = get_by_zipcode(loc, country_code)
        else:
            data = get_by_city(loc, country_code)

        if data:
            result = {key: data.get(key) for key in keys if key in data}
            results.append(result)
        else:
            results.append(None)

    return results


import argparse


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
