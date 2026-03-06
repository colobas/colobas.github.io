# Substack cross-post tooling

This folder contains a small script to turn a Jekyll post (`_posts/*.md`) into a Substack draft using the `python-substack` library vendored as a git submodule.

## Setup

1. Create a venv.
2. Install dependencies:

```bash
pip install -r tools/substack/requirements.txt
pip install -e external/python-substack
```

3. Create a `.env` file (you can copy from `tools/substack/.env.example`) and set Substack credentials.

## Create a draft

```bash
python tools/substack/crosspost.py _posts/2026-02-25-a-demo-post-slides-handouts-and-the-hybrid-workflow.md
```

Defaults:

- strips the `# Tufte Layout Exerciser` section
- converts some tufte-specific HTML into plain Markdown approximations

If you want to keep the exerciser section (to see what survives on Substack):

```bash
python tools/substack/crosspost.py --keep-tufte-section _posts/2026-02-25-a-demo-post-slides-handouts-and-the-hybrid-workflow.md
```

If you want to disable the HTML→Markdown cleanup:

```bash
python tools/substack/crosspost.py --keep-tufte-section --no-tufte-html-conversion _posts/2026-02-25-a-demo-post-slides-handouts-and-the-hybrid-workflow.md
```

## Publish

```bash
python tools/substack/crosspost.py --publish _posts/2026-02-25-a-demo-post-slides-handouts-and-the-hybrid-workflow.md
```
