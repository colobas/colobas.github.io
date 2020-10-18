import json
import glob

index = dict()

for json_fpath in glob.glob("public/json/*.json"):
    with open(json_fpath) as f:
        post = json.load(f)["properties"]
        fname = json_fpath.split("/")[-1]

        title = (post["title"][0] if len(post["title"]) > 0 
                 else fname.split(".")[0])

        index[fname.split(".")[0]] = {
            "title": title,
            "url": f"/json/{fname}",
            "tags": post["filetags"],
            "date": post["date"][0] if len(post["date"]) > 0 else None
        }

with open("public/json-index.json", "w") as f:
    json.dump(index, f)

all_tags = list(set(sum([post["tags"] for post in index.values()], [])))

with open("public/all-tags.json", "w") as f:
    json.dump(all_tags, f)
