import requests
import time
import json

res = requests.get(
    "https://community.openstreetmap.org/search.json",
    params={"q": "tags:import after:2023-01-01"},
    headers={"Accept": "application/json"},
)


all_topics = res.json()

time.sleep(1)

replies = []

for post in all_topics["topics"]:
    topic_id = post["id"]

    res = requests.get(
        f"https://community.openstreetmap.org/t/{topic_id}.json",
        headers={"Accept": "application/json"},
    )

    post_data = res.json()

    for reply in post_data["post_stream"]["posts"]:
        replies.append(
            {
                "username": reply["username"],
                "date": reply["updated_at"],
                "subject": reply["topic_slug"],
                "topic_id": topic_id,
                "url": f"https://community.openstreetmap.org/t/{topic_id}"
                # "country": subject_country_map[subject]
            }
        )

    time.sleep(1)

with open("discourse.json", "w") as f:
    json.dump(replies, f)
