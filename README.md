![example workflow](https://github.com/donotpanic/location-service/actions/workflows/python-package-conda.yml/badge.svg)

# Location Service

## Installation
Install python and required packages:

```
pip install -r requirements.txt
```

If unfamiliar with python I would recommend [Anaconda](https://docs.anaconda.com/anaconda/install/) and installing any additional packages should not be necessary.

## Setup environmental variable
Setup the following environmental variable:
LOCATION_API_KEY={API KEY}

You can generate a free api key [open weather map](https://openweathermap.org/api/geocoding-api)

MacOS
```
export LOCATION_API_KEY="{API KEY}"
```

## Running from command line
```
python location_service.py "Madison, WI" "77578" "00000"
```

Response
```
Location: Madison, WI
  City: Madison
  Latitude: 43.074761
  Longitude: -89.3837613
Location: 77578
  City: Manvel
  Latitude: 29.4694
  Longitude: -95.3503
Location: 00000 - Data could not be retrieved.
```

## Random
- The code is available to view and execute in [Google colab/jupyter notebook](https://colab.research.google.com/drive/1WyWRyjQcoAdN7c6tHKvsQlwltg1ZzsOm) as well. Welcome to play around with it there. Including prototype of it using OOP. Be sure to set the secret "api_key".
- [Github actions workflow](https://github.com/donotpanic/location-service/actions) is setup. Tests are executed for every commit to the main branch.

