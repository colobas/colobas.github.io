This is my website, built with Jekyll and Svelte.

It has some logic to use Svelte components in Jekyll, which I took from 
[this blogpost](https://web.archive.org/web/20210618184658/https://davidtang.io/2020-01-25-adding-svelte-3-to-a-jekyll-site/),
although at the moment I'm only using it for the "$ Hello friend" message on the home page.

The general layout is based on [klise](https://github.com/piharpi/jekyll-klise) and
the style for the posts is based on [my fork of tufte-pandoc-jekyll](https://github.com/colobas/tufte-pandoc-jekyll)


# General flow

- I write posts in org-mode
- I have local emacs configs to export org files as latex. My default style is tufte-handout, so it's consistent with the post style here
- My Makefile looks for org files in a specific location and uses org-latex-export to export them to .tex (so that I can make use of some latex specific configs)
- I use pandoc together with some scripts to do the latex -> markdown conversion (using script org2jekyll.sh)
