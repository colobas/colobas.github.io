import sys
import json
import datetime

from collections import defaultdict

def extract_year_mo(datestr):
    try:
        date = datetime.datetime.strptime(datestr, '%Y-%m-%d')
        return f"{date.year}-{date.month:02}"
    except:
        return "no-date"


intro = """
#+TITLE: gpir.es

* This is my personal website
** Some posts on it will be written as a tree of cards
** Some other posts will be normal text
* Use the keyboard to navigate
"""

with open(sys.argv[1]) as f:
    index = json.load(f)

tags = set(sum([entry["tags"] for entry in index.values()], []))

intro += "\n* Entries per tag"

for tag in tags:
    intro += f"\n** #{tag}"
    for _id, entry in index.items():
        if tag in entry["tags"]:
            #intro += f'\n*** <a href="/post/tree/{_id}">{entry["title"]}</a>'
            intro += f'\n*** [[/post/tree/{_id}][{entry["title"]}]]'
            intro += '\n Tags: ' + " ".join([f'#{_tag}' for _tag in entry["tags"]])
            intro += f'\n Date: {entry["date"]}'


intro += "\n* Entries per date"

per_year_mo = defaultdict(dict)
for key in index:
    per_year_mo[extract_year_mo(index[key]["date"])][key] = index[key]

year_mos = sorted(per_year_mo.keys())

for year_mo in year_mos:
    intro += f"\n** {year_mo}"
    for _id, entry in per_year_mo[year_mo].items():
        intro += f'\n*** [[/post/tree/{_id}][{entry["title"]}]]'
        intro += '\n Tags: ' + " ".join([f'#{_tag}' for _tag in entry["tags"]])
        intro += f'\n Date: {entry["date"]}'

print(intro)
