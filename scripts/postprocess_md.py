import re
import sys
import os
import json
from pathlib import Path
from fire import Fire

def extract_and_remove_tags(markdown):
    if not "# Tags" in markdown:
        return markdown, []

    pattern = r"\# Tags\n*(.*?)(?:\n\n|\Z)"
    tag_text = re.search(pattern, markdown, flags=re.DOTALL).groups()[0]

    pattern = r"\# Tags\n*(?:.*?)(?:\n\n|\Z)"
    markdown_no_tags = "".join(re.split(pattern, markdown, flags=re.DOTALL, maxsplit=1))

    tags = re.findall(r"\[([^\]]*)\]", tag_text)

    return markdown_no_tags, tags


def add_tag_line(markdown, tags):
    if len(tags) == 0:
        return markdown

    lines = markdown.split("\n")
    tag_line = "tags: " + " ".join(tag.replace("#","") for tag in tags)
    lines.insert(2, tag_line)
    return "\n".join(lines)


def get_backlinks(graph, slug):
    nodes = {_["id"]:_ for _ in graph["nodes"]}
    backlinks = []
    for edge in graph["edges"]:
        if edge["target"] == slug:
            backlinks.append(nodes[edge["source"]])
    return backlinks


def add_backlinks(markdown, backlinks):
    if len(backlinks) > 0:
        markdown += "\n\n# Links to this file\n\n"
        for link in backlinks:
            markdown += f"- [{link['title']}]({link['url']})\n"
    return markdown


def _main(original, graph, slug):
    original_no_tags, tags = extract_and_remove_tags(original)
    added_tags = add_tag_line(original_no_tags, tags)

    backlinks = get_backlinks(graph, slug)
    added_backlinks = add_backlinks(added_tags, backlinks)

    return added_backlinks

def main(original_path, target_path, graph_path):
    original_path = Path(original_path)
    target_path = Path(target_path)
    graph_path = Path(graph_path)

    slug = original_path.stem

    with open(original_path, "r") as f:
        original = f.read()

    with open(graph_path) as f:
        graph = json.load(f)

    result = _main(original, graph, slug)

    with open(target_path, "w") as f:
        f.write(result)


if __name__ == "__main__":
    Fire(main)
