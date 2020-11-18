.PHONY: all check_clean clean

mds := $(subst public/org-files,public/markdown,$(patsubst %.org,%.md, $(wildcard public/org-files/*.org)))
ROAM_DB=/home/colobas/.emacs.d/.local/etc/org-roam.db
NOTES_PATH=/home/colobas/org/knowledge-base/notes

all: $(mds) public/graph.json

public/markdown/%.md : public/org-files/%.md scripts/postprocess_md.py
	python scripts/postprocess_md.py $< $@

public/graph.json : scripts/make-graph.py $(mds)
	python scripts/make-graph.py $(ROAM_DB) $(NOTES_PATH) > public/graph.json.tmp
	python -mjson.tool public/graph.json.tmp > public/graph.json
	rm public/graph.json.tmp

check_clean:
	@echo -n "This will erase every file in \`public/markdow\`. Are you sure? [y/N] " && read ans && [ $${ans:-N} = y ]

clean: check_clean
	rm public/markdown/*

