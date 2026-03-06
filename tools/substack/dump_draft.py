#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "python-dotenv>=1.0.0",
#   "requests>=2.31.0",
# ]
# ///
"""Dump a Substack draft JSON payload.

Given a draft id, fetches it via the Substack API and prints the response.

This is useful for reverse-engineering how Substack represents tables, math,
footnotes, etc. when created in the web editor.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Make the vendored submodule importable without installing it.
_REPO_ROOT = Path(__file__).resolve().parents[2]
_SUBSTACK_SRC = _REPO_ROOT / "external" / "python-substack"
sys.path.insert(0, str(_SUBSTACK_SRC))


def load_substack_env() -> None:
    candidates: list[str] = []
    if os.getenv("SUBSTACK_DOTENV_PATH"):
        candidates.append(os.getenv("SUBSTACK_DOTENV_PATH"))

    candidates.append(str(Path(__file__).with_name(".env")))
    candidates.append(str(Path.cwd() / ".env"))

    for p in candidates:
        if p and os.path.exists(p):
            load_dotenv(p, override=False)
            return

    load_dotenv(override=False)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("draft_id", help="Draft id (number)")
    ap.add_argument(
        "--body-only",
        action="store_true",
        help="Print only draft_body (parsed JSON) instead of the full API response",
    )
    args = ap.parse_args()

    load_substack_env()

    from substack import Api

    api = Api(
        email=os.getenv("EMAIL"),
        password=os.getenv("PASSWORD"),
        cookies_path=os.getenv("COOKIES_PATH"),
        cookies_string=os.getenv("COOKIES_STRING"),
        publication_url=os.getenv("PUBLICATION_URL"),
    )

    draft = api.get_draft(args.draft_id)

    if args.body_only:
        body = draft.get("draft_body")
        if isinstance(body, str):
            try:
                body = json.loads(body)
            except Exception:
                pass
        print(json.dumps(body, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(draft, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
