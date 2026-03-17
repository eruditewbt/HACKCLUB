# import requests
# import sqlite3
# import time

# conn = sqlite3.connect("dictionary.db")
# cursor = conn.cursor()

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS words(
# id INTEGER PRIMARY KEY AUTOINCREMENT,
# word TEXT UNIQUE,
# data TEXT
# )
# """)

# with open("words_alpha.txt") as f:
#     words = f.read().splitlines()

# for word in words:

#     url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

#     try:
#         r = requests.get(url)

#         if r.status_code == 200:
#             data = r.text

#             cursor.execute(
#                 "INSERT OR IGNORE INTO words(word,data) VALUES (?,?)",
#                 (word, data)
#             )

#             conn.commit()

#             print("saved:", word)

#         time.sleep(0.3)

#     except Exception as e:
#         print("error:", word, e)




























# import requests
# import sqlite3
# import time
# from datetime import datetime

# DB = "dictionary.db"
# WORD_FILE = "words_alpha.txt"

# conn = sqlite3.connect(DB)
# cursor = conn.cursor()

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS words(
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     word TEXT UNIQUE,
#     data TEXT,
#     status TEXT DEFAULT 'pending',
#     attempts INTEGER DEFAULT 0,
#     last_attempt TEXT,
#     error_message TEXT
# )
# """)

# conn.commit()


# def load_words():
#     """Insert words into DB if they don't exist"""
#     with open(WORD_FILE) as f:
#         words = f.read().splitlines()

#     cursor.executemany(
#         "INSERT OR IGNORE INTO words(word) VALUES (?)",
#         [(w,) for w in words]
#     )

#     conn.commit()


# def get_pending(limit=100):
#     """Fetch words that still need processing"""
#     cursor.execute("""
#         SELECT word, attempts
#         FROM words
#         WHERE status IN ('pending','retry')
#         ORDER BY id
#         LIMIT ?
#     """, (limit,))
#     return cursor.fetchall()


# def update_success(word, data):
#     cursor.execute("""
#         UPDATE words
#         SET data=?, status='done', last_attempt=?
#         WHERE word=?
#     """, (data, datetime.utcnow(), word))
#     conn.commit()


# def update_not_found(word):
#     cursor.execute("""
#         UPDATE words
#         SET status='not_found', last_attempt=?
#         WHERE word=?
#     """, (datetime.utcnow(), word))
#     conn.commit()


# def update_error(word, error, attempts):
#     status = "retry" if attempts < 5 else "error"

#     cursor.execute("""
#         UPDATE words
#         SET status=?, attempts=?, last_attempt=?, error_message=?
#         WHERE word=?
#     """, (status, attempts, datetime.utcnow(), str(error), word))

#     conn.commit()


# def fetch_word(word, attempts):

#     url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

#     try:
#         r = requests.get(url, timeout=10)

#         if r.status_code == 200:
#             update_success(word, r.text)
#             print("saved:", word)

#         elif r.status_code == 404:
#             update_not_found(word)
#             print("not found:", word)

#         else:
#             update_error(word, f"HTTP {r.status_code}", attempts+1)

#     except Exception as e:
#         update_error(word, e, attempts+1)
#         print("error:", word, e)


# def main():

#     load_words()

#     while True:

#         batch = get_pending(50)

#         if not batch:
#             print("All words processed")
#             break

#         for word, attempts in batch:
#             fetch_word(word, attempts)
#             time.sleep(0.3)


# if __name__ == "__main__":
#     main()


























import requests
import sqlite3
import json
import time
from datetime import datetime

DB = "dictionary.db"

conn = sqlite3.connect(DB)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS words(
    word TEXT PRIMARY KEY,
    data TEXT,
    source TEXT,
    status TEXT,
    attempts INTEGER DEFAULT 0,
    last_attempt TEXT
)
""")

conn.commit()


def dictionary_api(word):

    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

    r = requests.get(url)

    if r.status_code == 200:
        return r.json()

    return None


def wiki_api(word):

    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{word}"

    r = requests.get(url)

    if r.status_code != 200:
        return None

    data = r.json()

    if "extract" not in data:
        return None

    return convert_wiki(word, data)


def detect_pos(description):

    if not description:
        return "noun"

    d = description.lower()

    if "verb" in d:
        return "verb"

    if "adjective" in d:
        return "adjective"

    if "adverb" in d:
        return "adverb"

    return "noun"


def convert_wiki(word, wiki):

    pos = detect_pos(wiki.get("description", ""))

    definition = wiki.get("extract", "")

    result = [
        {
            "word": word,
            "phonetic": "",
            "phonetics": [],
            "origin": "",
            "meanings": [
                {
                    "partOfSpeech": pos,
                    "definitions": [
                        {
                            "definition": definition,
                            "example": "",
                            "synonyms": [],
                            "antonyms": []
                        }
                    ]
                }
            ]
        }
    ]

    return result


def save(word, data, source):

    cursor.execute("""
    INSERT OR REPLACE INTO words
    (word,data,source,status,last_attempt)
    VALUES (?,?,?,?,?)
    """, (
        word,
        json.dumps(data),
        source,
        "done",
        datetime.utcnow()
    ))

    conn.commit()


def mark_not_found(word):

    cursor.execute("""
    INSERT OR REPLACE INTO words
    (word,status,last_attempt)
    VALUES (?,?,?)
    """, (word, "not_found", datetime.utcnow()))

    conn.commit()


def process(word):

    print("checking:", word)

    data = dictionary_api(word)

    if data:
        save(word, data, "dictionaryapi")
        print("saved via dictionaryapi")
        return

    print("fallback → wikipedia")

    data = wiki_api(word)

    if data:
        save(word, data, "wikipedia")
        print("saved via wikipedia")
        return

    mark_not_found(word)
    print("not found")


def main():

    with open("words_alpha.txt") as f:
        words = f.read().splitlines()

    for word in words:

        process(word)

        time.sleep(0.3)


if __name__ == "__main__":
    main()











