import re
import sys
import os
import json

BASENAME = os.path.splitext(sys.argv[1])[0]
SLUG = os.path.basename(BASENAME)
DEST = sys.argv[2]
GRAPH = sys.argv[3]

with open(GRAPH) as f:
    graph = json.load(f)

nodes = {_["id"]:_ for _ in graph["nodes"]}
backlinks = []
for edge in graph["edges"]:
    if edge["target"] == SLUG:
        backlinks.append(nodes[edge["source"]])

def search_or_empty(search, text):
    find_ = re.search(search, text, flags=re.IGNORECASE)
    return (find_.groups()[0] if find_ is not None else "")

def convert_url(url):
    dest = url.split("file:")[1]
    dest = os.path.splitext(dest)[0]
    return f"/#/post/{dest}"

with open(BASENAME+".org", "r") as f:
    orgfile = f.read()
    title = search_or_empty(r"#\+title:\s(.*)", orgfile)
    post_type = search_or_empty(r"#\+type:\s(.*)", orgfile)
    if post_type == "":
        post_type = "normal"
    tags_line = search_or_empty(r"- tags ::\s(.*)", orgfile)
    tags = re.findall(r"\[\[([^\]]*)\]\[([^\]]*)\]\]", tags_line)

with open(BASENAME+".md", "r") as f:
    markdown_lines = f.readlines()

with open(DEST, "w") as f:
    content = (
        f"---\n"
        f"title: {title}\n"
        f"type: {post_type}\n"
        f"---\n\n"
    )

    if len(tags) > 0:
        content += "tags : "
        for tag in tags:
            content += f"[{tag[1]}]({convert_url(tag[0])}) , "
        content = content[:-2]
        content += "\n\n"

    f.write(content)
    for line in markdown_lines:
        if line == "tags\n":
            continue
        if line.startswith(":"):
            continue
        f.write(line.strip()+"\n")

    if len(backlinks) > 0:
        f.write("\n\n# Links to this file\n\n")
        for link in backlinks:
            f.write(f"- [{link['title']}]({link['url']})\n")

