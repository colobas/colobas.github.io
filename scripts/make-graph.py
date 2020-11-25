#!/usr/bin/env python3

import sys
import os
import sqlite3
import re
import json

DB_PATH = sys.argv[1]
BASE_PATH = sys.argv[2]

def get_file_title(fpath):
    with open(fpath) as f:
        s = re.findall(r"#\+title:\s(.*)", f.read(), flags=re.IGNORECASE)

    if len(s) > 0:
        return s[0]
    return ""

def is_note_file(fpath):
    return (
        os.path.dirname(fpath) == BASE_PATH and
        os.path.splitext(fpath)[1] == ".org"
    )

def make_slug(fpath):
    return os.path.splitext(os.path.basename(fpath))[0]

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

    if not (is_note_file(source) and is_note_file(dest)):
        continue

    src_slug = make_node(source, nodes)
    dest_slug = make_node(dest, nodes)

    edges.append({"source": src_slug, "target": dest_slug})
    edge_dict[src_slug]["children"].append(dest_slug)

graph = {"nodes": [dict(_) for _ in nodes], "edges": edges, "edge_dict": edge_dict}

print(json.dumps(graph))
