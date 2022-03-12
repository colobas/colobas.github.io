import sys
import os
import sqlite3
import re
import json
from pathlib import Path

DB_PATH = sys.argv[1]
BASE_PATH = sys.argv[2]

def get_file_title(fpath):
    if not fpath.endswith(".md"):
        fpath += ".md"

    with open(fpath) as f:
        lines = f.readlines()

    title = "".join(lines[1].split("title:")).strip()

    if title[0] == '"':
        title = title[1:-1]

    return title

def is_published(fpath):
    if not fpath.endswith(".md"):
        fpath += ".md"
    with open(fpath) as f:
        for line in f.readlines():
            if "published: " in line:
                if "false" in line:
                    return False
                else:
                    return True
    return True

def make_slug(fpath):
    slug = os.path.splitext(os.path.basename(fpath))[0]
    #slug = re.split(r"^[0-9]*-")[0]
    return slug

def make_url(fpath):
    return f"/{make_slug(fpath)}"

def make_node(fpath, nodes):
    slug = make_slug(fpath)
    url = make_url(fpath)
    title = get_file_title(fpath)
    nodes.add(tuple({"id": slug, "title":title, "url":url}.items()))

    return slug

class my_default_dict(dict):
    def __missing__(self, key):
        res = self[key] = {"name": key, "children": list()}
        return res

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

edges = list()
nodes = set()
edge_dict = my_default_dict()

for (source, dest) in c.execute("SELECT source, dest FROM links WHERE type == '\"file\"'"):
    source = os.path.expanduser(source.replace('"', ""))
    dest = os.path.expanduser(dest.replace('"', ""))

    if not (Path(source).is_file() and Path(dest).is_file()):
        continue

    if not (is_published(source) and is_published(dest)):
        continue

    src_slug = make_node(source, nodes)
    dest_slug = make_node(dest, nodes)

    edges.append({"source": src_slug, "target": dest_slug})
    edge_dict[src_slug]["children"].append(dest_slug)

graph = {"nodes": [dict(_) for _ in nodes], "edges": edges, "edge_dict": edge_dict}

print(json.dumps(graph))
