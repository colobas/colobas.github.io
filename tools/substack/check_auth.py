#!/usr/bin/env python3
"""Sanity-check Substack auth and publication selection.

Loads env vars the same way as crosspost.py and prints:
- whether auth worked
- user id
- available publications (subdomain + url)

Useful when cookie auth fails or PUBLICATION_URL doesn't match any publication.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv


def load_substack_env() -> None:
    # Match tools/substack/crosspost.py behavior.
    candidates = []
    if os.getenv("SUBSTACK_DOTENV_PATH"):
        candidates.append(os.getenv("SUBSTACK_DOTENV_PATH"))

    candidates.append(os.path.join(os.path.dirname(__file__), ".env"))
    candidates.append(os.path.join(os.getcwd(), ".env"))

    for p in candidates:
        if p and os.path.exists(p):
            load_dotenv(p, override=False)
            return

    load_dotenv(override=False)


def main() -> None:
    load_substack_env()

    from substack import Api

    api = Api(
        email=os.getenv("EMAIL"),
        password=os.getenv("PASSWORD"),
        cookies_path=os.getenv("COOKIES_PATH"),
        cookies_string=os.getenv("COOKIES_STRING"),
        publication_url=os.getenv("PUBLICATION_URL"),
    )

    print("user_id:", api.get_user_id())

    pubs = api.get_user_publications()
    for p in pubs:
        print(f"- {p.get('subdomain')}: {p.get('publication_url')}")


if __name__ == "__main__":
    main()
