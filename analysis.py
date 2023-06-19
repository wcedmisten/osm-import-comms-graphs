import matplotlib.pyplot as plt
import pandas as pd
import json

with open('mailing_archive.csv', 'r') as f:
    # use email address as username
    mailing_df = pd.read_csv(f, delimiter='|').rename(columns={"email": "username"})

topic_country_map = {
    9005: "DE",
    9018: "TW",
    8214: "DE",
    7876: "US",
    96843: None,
    8798: "SE",
    99509: "DK",
    8779: "ES",
    95130: "SE",
    97957: None,
    98617: "RU",
    8707: "SE",
    6884: "BE",
    7945: "SE",
    99309: None,
    91712: "RS",
    99372: "BE",
    97410: "SE",
    98461: "US",
    8357: "BR",
    98356: "DE",
    9005: "DE",
    98023: "MX",
    9020: None,
    97455: None,
    9376: "EE",
    9285: "IT"
}

with open("discourse.json", "r") as f:
    data = json.load(f)

from datetime import datetime

for comment in data:
    comment["country"] = topic_country_map[comment["topic_id"]]

discourse_df = pd.DataFrame(data)

def parse_rfc3339(datetime_str: str) -> datetime:
    try:
        return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%f%z")
    except ValueError:
        # Perhaps the datetime has a whole number of seconds with no decimal
        # point. In that case, this will work:
        return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S%z")

mailing_df['date'] = mailing_df.apply(lambda x: parse_rfc3339(x["date"]), axis=1)
discourse_df['date'] = discourse_df.apply(lambda x: parse_rfc3339(x["date"]), axis=1)

with open("country_names.json", "r") as f:
    country_names = json.load(f)

# the query finds replies to posts that are older than the filter date, so we need to filter those out ourselves
discourse_df = discourse_df[discourse_df['date'] > parse_rfc3339("2023-01-01T00:00:00Z")]

MAILING_COLOR = '#440154'
DISCOURSE_COLOR = '#edbd4c'

plt.hist([discourse_df['date'], mailing_df['date']], bins=50, color=[MAILING_COLOR, DISCOURSE_COLOR], label=["Discourse import tag", "Imports Mailing List"])
plt.legend()
plt.title("Number of comments since 2023-01-01")
plt.ylabel("Number of comments")
plt.show()

plt.title("Number of unique users making comments since 2023-01-01")
plt.bar("Imports Mailing List", mailing_df['username'].nunique(), color=MAILING_COLOR)
plt.bar("Discourse import tag", discourse_df['username'].nunique(), color=DISCOURSE_COLOR)
plt.ylabel("Number of unique users")
plt.show()

plt.title("Number of unique comments since 2023-01-01")
plt.bar("Imports Mailing List", mailing_df['username'].size, color=MAILING_COLOR)
plt.bar("Discourse import tag", discourse_df['username'].size, color=DISCOURSE_COLOR)
plt.ylabel("Number of comments")
plt.show()

# rename ISO codes to full country names
mailing_df['country'] = mailing_df.apply(lambda x: country_names[x['country']], axis=1)
discourse_df['country'] = discourse_df.apply(lambda x: country_names.get(x['country'], "N/A"), axis=1)

mailing_msg_per_country = mailing_df.groupby('country')['username'].count()
discourse_msg_per_country = discourse_df.groupby('country')['username'].count()

width = 0.35

plt.bar(mailing_msg_per_country.keys(), mailing_msg_per_country.values, -width, color=MAILING_COLOR, align='edge', label="Imports Mailing List")
plt.bar(discourse_msg_per_country.keys(), discourse_msg_per_country.values, width, color=DISCOURSE_COLOR, align='edge', label="Discourse import tag")
plt.legend()

plt.title("Number of comments per country since 2023-01-01")
plt.ylabel('Number of comments')
plt.xticks(rotation=45)
plt.xlabel('Country')
plt.show()

mailing_users_per_country = mailing_df.groupby('country')['username'].nunique()
discourse_users_per_country = discourse_df.groupby('country')['username'].nunique()

plt.bar(mailing_users_per_country.keys(), mailing_users_per_country.values, -width, color=MAILING_COLOR, align='edge', label="Imports Mailing List")
plt.bar(discourse_users_per_country.keys(), discourse_users_per_country.values, width, color=DISCOURSE_COLOR, align='edge', label="Discourse import tag")
plt.legend()

plt.title("Number of unique users per country since 2023-01-01")
plt.ylabel('Number of unique users')
plt.xticks(rotation=45)
plt.xlabel('Country')
plt.show()
