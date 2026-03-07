# Substack cross-post tooling

This folder contains a small script to turn a Jekyll post (`_posts/*.md`) into a Substack draft using the `python-substack` library vendored as a git submodule.

## Setup (uv + PEP 723)

These scripts use **PEP 723 inline dependency metadata**, so you do not need to create/manage a venv manually.

1. Create a `.env` file at `tools/substack/.env` (copy from `tools/substack/.env.example`) and set Substack credentials.

2. Run scripts via `uv run` (uv will resolve/install the inline dependencies automatically):

```bash
uv run python tools/substack/check_auth.py
uv run python tools/substack/crosspost.py --help
```

To inspect a draft’s raw JSON (useful for implementing tables/math/footnotes properly):

```bash
uv run python tools/substack/dump_draft.py <draft_id> --body-only
```

Notes:

- `python-substack` is vendored as a git submodule under `external/python-substack`.
- The scripts add that directory to `sys.path` at runtime, so there is no separate install step for it.

## Create a draft

```bash
uv run python tools/substack/crosspost.py _posts/YYYY-MM-DD-your-post-slug.md
```

Defaults:

- strips the `# Tufte Layout Exerciser` section
- converts some tufte-specific HTML into plain Markdown approximations
- converts Markdown footnotes into Substack-native footnote nodes
- converts pipe tables into LaTeX array blocks (Substack doesn’t support native tables)
- leaves inline math ($...$) alone by default (Substack doesn’t support inline LaTeX; converting it into blocks is lossy)

If you want to keep the exerciser section (to see what survives on Substack):

```bash
uv run python tools/substack/crosspost.py --keep-tufte-section _posts/YYYY-MM-DD-your-post-slug.md
```

If you want to disable the HTML→Markdown cleanup:

```bash
uv run python tools/substack/crosspost.py --keep-tufte-section --no-tufte-html-conversion _posts/YYYY-MM-DD-your-post-slug.md
```

To disable table conversion:

```bash
uv run python tools/substack/crosspost.py \
  --keep-tufte-section \
  --no-latex-tables \
  _posts/YYYY-MM-DD-your-post-slug.md
```

To also convert inline math ($...$) into LaTeX blocks (lossy):

```bash
uv run python tools/substack/crosspost.py \
  --keep-tufte-section \
  --inline-math-to-blocks \
  _posts/YYYY-MM-DD-your-post-slug.md
```

## Publish

```bash
uv run python tools/substack/crosspost.py --publish _posts/YYYY-MM-DD-your-post-slug.md
```
