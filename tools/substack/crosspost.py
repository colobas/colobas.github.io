#!/usr/bin/env python3
"""Cross-post a Jekyll Markdown post to Substack.

This reads a Jekyll post (YAML front matter + Markdown body) and creates a
Substack draft (or publishes it) using the python-substack library.

Assumptions / current limitations:
- We optionally strip the "Tufte Layout Exerciser" section (it contains raw HTML
  intended for tufte-css, which Substack will not render as intended).
- We do a minimal footnote rewrite (single-line footnotes only).
- We shift headings down by one level ("#" -> "##", etc.) so Substack's default
  typography is closer to the blog.
"""

from __future__ import annotations

import argparse
import os
import re
from dataclasses import dataclass
from typing import Dict

import yaml
from dotenv import load_dotenv

# python-substack is pulled in via the git submodule in external/python-substack
# and typically installed in editable mode:
#   pip install -e external/python-substack


@dataclass
class JekyllPost:
    front_matter: Dict
    body: str


_FRONT_MATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n(.*)\Z", re.S)


def read_jekyll_post(path: str) -> JekyllPost:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    m = _FRONT_MATTER_RE.match(text)
    if not m:
        return JekyllPost(front_matter={}, body=text)

    fm_raw, body = m.group(1), m.group(2)
    front = yaml.safe_load(fm_raw) or {}
    return JekyllPost(front_matter=front, body=body)


def strip_section_by_h1(body: str, heading: str) -> str:
    """Remove a top-level markdown section like:

    # Heading
    ...
    # Next

    The removed block includes the "# Heading" line.
    """
    # Match from "# heading" to next "# " or end-of-file.
    # Use re.MULTILINE anchors.
    pat = re.compile(
        rf"^#\s+{re.escape(heading)}\s*\n.*?(?=^#\s+|\Z)",
        re.M | re.S,
    )
    return re.sub(pat, "", body)


def shift_headings(body: str, delta: int = 1) -> str:
    """Shift markdown headings by `delta` levels, ignoring fenced code blocks."""
    out_lines = []
    in_code = False
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            out_lines.append(line)
            continue

        if not in_code:
            m = re.match(r"^(#{1,6})(\s+.*)$", line)
            if m:
                hashes, rest = m.group(1), m.group(2)
                new_level = min(len(hashes) + delta, 6)
                out_lines.append("#" * new_level + rest)
                continue

        out_lines.append(line)

    return "\n".join(out_lines) + ("\n" if body.endswith("\n") else "")


def rewrite_simple_footnotes(body: str) -> str:
    """Handle simple single-line footnotes.

    Rewrites:
      ... foo.[^1]
      ...
      [^1]: footnote text

    into:
      ... foo. (footnote: footnote text)

    Limitations:
    - only handles single-line definitions
    - only handles numeric footnote keys cleanly
    """
    footnotes: Dict[str, str] = {}
    kept_lines = []

    # Collect definitions
    for line in body.splitlines():
        m = re.match(r"^\[\^([^\]]+)\]:\s*(.*)\s*$", line)
        if m:
            footnotes[m.group(1)] = m.group(2)
        else:
            kept_lines.append(line)

    body2 = "\n".join(kept_lines) + ("\n" if body.endswith("\n") else "")

    # Replace references
    def repl(m: re.Match) -> str:
        key = m.group(1)
        txt = footnotes.get(key)
        if not txt:
            return ""  # drop unknown footnote refs
        return f" (footnote: {txt})"

    body2 = re.sub(r"\[\^([^\]]+)\]", repl, body2)
    return body2


def build_api():
    from substack import Api

    load_dotenv()
    return Api(
        email=os.getenv("EMAIL"),
        password=os.getenv("PASSWORD"),
        cookies_path=os.getenv("COOKIES_PATH"),
        cookies_string=os.getenv("COOKIES_STRING"),
        publication_url=os.getenv("PUBLICATION_URL"),
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("path", help="Path to a Jekyll markdown post (e.g. _posts/....md)")
    ap.add_argument("--publish", action="store_true", help="Publish after creating the draft")
    ap.add_argument(
        "--keep-tufte-section",
        action="store_true",
        help="Do not strip the '# Tufte Layout Exerciser' section",
    )
    ap.add_argument(
        "--dump-markdown",
        action="store_true",
        help="Print the transformed markdown (the version sent to Substack) and exit",
    )
    ap.add_argument(
        "--markdown-out",
        help="Write the transformed markdown (the version sent to Substack) to a file and exit",
    )
    args = ap.parse_args()

    post = read_jekyll_post(args.path)

    title = post.front_matter.get("title") or "(untitled)"
    subtitle = post.front_matter.get("subtitle") or ""

    body = post.body
    if not args.keep_tufte_section:
        body = strip_section_by_h1(body, "Tufte Layout Exerciser")

    body = rewrite_simple_footnotes(body)
    body = shift_headings(body, delta=1)

    if args.dump_markdown or args.markdown_out:
        if args.markdown_out:
            with open(args.markdown_out, "w", encoding="utf-8") as f:
                f.write(body)
        else:
            print(body)
        return

    api = build_api()
    user_id = api.get_user_id()

    from substack.post import Post

    sb_post = Post(title=title, subtitle=subtitle, user_id=user_id)
    sb_post.from_markdown(body, api=api)

    draft = api.post_draft(sb_post.get_draft())

    draft_id = draft.get("id")
    print(f"Draft created: id={draft_id}")

    if args.publish:
        api.prepublish_draft(draft_id)
        api.publish_draft(draft_id)
        print("Published.")


if __name__ == "__main__":
    main()
