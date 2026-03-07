# gpir.es

Personal website built with **Jekyll** plus a small **Svelte** bundle.

The base layout is derived from [jekyll-klise](https://github.com/piharpi/jekyll-klise). Post typography is Tufte-inspired (tufte-css + pandoc-oriented tweaks in `assets/css/tufte-jekyll-bundle.scss`).

## Writing / publishing posts (current workflow)

Source-of-truth drafts live as **Org-mode** files in `~/org/` (commonly under `~/org/articles/`).

### 1) Write an Org file

Use these document keywords:

```org
#+TITLE: My Post Title
#+DATE: 2026-03-06          ; optional, defaults to today
#+FILETAGS: :tag1:tag2:     ; optional
#+OPTIONS: tags:nil toc:nil ; optional
```

Write normally (headings, lists, code blocks, tables, footnotes). Math is written using `$...$` / `$$...$$`.

### 2) Export Org → Jekyll `_posts/*.md`

In Doom Emacs, run:

- `M-x colobas/publish-post-to-blog`

This command is implemented in:

- `~/.doom.d/modules/org/blog.el`

It:

- calls **pandoc** directly (`org` → `markdown`)
- prepends **YAML front matter** (`layout: post`, `title`, `date`, `tags`, `math: true`)
- writes the result into:
  - `~/dev/colobas.github.io/_posts/YYYY-MM-DD-<slug>.md`

Notes about the export:

- It uses a pandoc markdown target roughly equivalent to “GFM + $-math + pipe tables”.
- It strips pandoc-emitted raw org blocks (e.g. for unrecognized org keywords).
- It disables raw HTML emission from Org export (so you generally shouldn’t rely on inline HTML coming from Org).

### 3) Commit + push

This repo is deployed via GitHub Actions on pushes to `main`.

## Site rendering pipeline (Jekyll + Pandoc)

This repo uses `jekyll-pandoc` (`_config.yml` sets `markdown: Pandoc`). At build time, Jekyll invokes **pandoc** to convert Markdown → HTML with options like:

- `mathjax`
- `section-divs`
- `shift-heading-level-by: 1`
- `lua-filter: pandoc-sidenote.lua`

The `pandoc-sidenote.lua` filter is currently installed in the user pandoc data dir:

- `~/.local/share/pandoc/filters/pandoc-sidenote.lua`

## Local development

Jekyll:

```bash
bundle install
bundle exec jekyll serve
```

Svelte bundle (only needed if you change `svelte-components/`):

```bash
make svelte
```

## Cross-posting to Substack

Cross-post tooling lives under:

- `tools/substack/`

It uses an (unofficial) Substack API client vendored as a git submodule:

- `external/python-substack`

Notes:

- Substack supports LaTeX as *blocks*; the crossposter emits `latex_block` nodes for `$$...$$`.
- Substack doesn’t support native tables; pipe tables can be converted to a KaTeX-friendly `array` block.
- Substack footnotes are supported and emitted as native `footnote` nodes.

See:

- `tools/substack/README.md`
