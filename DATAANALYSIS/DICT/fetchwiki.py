import requests
import time
import json

URL = "https://en.wikipedia.org/api/rest_v1/page/summary/{}"

# Words grouped by known POS
words = {
    "noun": [
        "dog", "tree", "computer", "city", "teacher", "river"
    ],
    "verb": [
        "run", "eat", "sleep", "write", "build", "drive"
    ],
    "adjective": [
        "beautiful", "happy", "fast", "blue", "ancient"
    ],
    "adverb": [
        "quickly", "slowly", "silently", "happily"
    ],
    "exclamation": [
        "hello", "wow", "oops", "hey"
    ]
}


# def fetch_summary(word):

#     url = URL.format(word)

#     try:
#         r = requests.get(url, timeout=10)

#         if r.status_code != 200:
#             return None

#         data = r.json()

#         return {
#             "title": data.get("title"),
#             "description": data.get("description"),
#             "extract": data.get("extract")
#         }

#     except Exception as e:
#         print("error:", word, e)
#         return None

def fetch_summary(word):

    url = URL.format(word)

    headers = {
        "User-Agent": "dictionary-agent/1.0 (research)"
    }

    try:
        r = requests.get(url, headers=headers, timeout=10)

        print(word, "status:", r.status_code)

        if r.status_code != 200:
            return None

        data = r.json()

        return {
            "title": data.get("title"),
            "description": data.get("description"),
            "extract": data.get("extract")
        }

    except Exception as e:
        print("error:", word, e)
        return None


results = {}

for pos, word_list in words.items():

    results[pos] = []

    for word in word_list:

        print("fetching:", word)

        data = fetch_summary(word)

        if data and data["extract"]:
            results[pos].append({
                "word": word,
                "description": data["description"],
                "extract": data["extract"]
            })
            
        else:
            print("missing data:", word)
            
        time.sleep(0.5)


# Save results for analysis
with open("wiki_pos_patterns.json", "w") as f:
    json.dump(results, f, indent=2)


# Pretty print for inspection
for pos, entries in results.items():

    print("\n======================")
    print("POS:", pos)
    print("======================")

    for e in entries:
        print("\nWORD:", e["word"])
        print("DESC:", e["description"])
        print("DEF:", e["extract"])