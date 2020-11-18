import re
import sys
import os

BASENAME = os.path.splitext(sys.argv[1])[0]
DEST = sys.argv[2]

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

