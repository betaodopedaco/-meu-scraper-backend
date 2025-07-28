import os
import requests
from collections import namedtuple
from urllib.parse import urlencode, urlunparse
from dotenv import load_dotenv
load_dotenv()


BASE_URL = "api.openweathermap.org/geo/1.0/direct"


Components = namedtuple(
    typename='Components',
    field_names=['scheme', 'netloc', 'url', 'path', 'query', 'fragment']
)


def getcoords(CITY):
    print(f"CITY - {CITY}")
    query_params = {
        "q": CITY,
        "limit": 1,
        "appid": os.getenv("OPENWEATHER_KEY")
    }

    url = urlunparse(
        Components(scheme="http",
                   netloc=BASE_URL,
                   query=urlencode(query_params),
                   path="",
                   url="",
                   fragment="")
    )

    response = requests.get(url)

    data = response.json()[0]

    return data["lat"], data["lon"]
