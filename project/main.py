import sqlite3
from datetime import datetime
import datetime
import requests
import json
import pandas as pd

import settings

DATABASE_LOCATION = settings.DATABASE_LOCATION
USER_ID = settings.USER_ID
TOKEN = settings.TOKEN
URL = settings.URL


if __name__ == '__main__':
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer {token}".format(token=TOKEN)
    }

    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    params = {
        "limit": 50,
        "after": yesterday_unix_timestamp
    }

    response = requests.get(URL, headers=headers, params=params)
    data = response.json()

    print(data)

    # track_titles = []
    # artist_names = []
    # played_at = []
    # timestamps = []

    # for track in data["items"]:
    #     track_titles.append(track["track"]["name"])
    #     artist_names.append(track["track"]["album"]["artists"][0]["name"])
    #     played_at.append(track["played_at"])
    #     timestamps.append(track["played_at"][0:10])

    # track_dict = {
    #     "track_title": track_titles,
    #     "artist_name": artist_names,
    #     "played_at": played_at,
    #     "timestamp": timestamps,
    # }

    # track_df = pd.Dataframe(
    #     track_dict,
    #     columns=["track_title", "artist_name", "played_at", "timestamp"]
    # )

    # print(track_df)
