.PHONY: all check_clean clean
EMACS_CONF_PATH = $(realpath ./emacs.site.conf/init.el)

jsons := $(subst public/org-files,public/json,$(patsubst %.org,%.json, $(wildcard public/org-files/*.org)))
htmls := $(subst public/org-files,public/html,$(patsubst %.org,%.html, $(wildcard public/org-files/*.org)))

all: $(htmls) $(jsons) public/json-index.json public/intro.json

public/json/%.json : public/org-files/%.org
	emacs $< --batch -l $(EMACS_CONF_PATH) --eval "(org-export-to-file 'json \"$(join $(realpath public/json),/$(notdir $@))\")"
	python -mjson.tool $@ $@.pretty 
	mv $@.pretty $@


public/html/%.html : public/org-files/%.org
	pandoc $< -o $@

public/json-index.json : $(jsons) scripts/make-json-index.py
	python scripts/make-json-index.py
	python -mjson.tool ./public/json-index.json json-index.pretty
	mv json-index.pretty ./public/json-index.json
	#cp -r public/org-files/images/* public/images

public/intro.json : public/json-index.json scripts/make-intro.py
	python scripts/make-intro.py public/json-index.json > tmp.org
	emacs tmp.org --batch -l $(EMACS_CONF_PATH) --eval "(org-export-to-file 'json \"$(join $(realpath public),/$(notdir $@))\")" &> /dev/null
	rm tmp.org

check_clean:
	@echo -n "This will erase every file in \`public/json\` and \`public/json-index.json\`. Are you sure? [y/N] " && read ans && [ $${ans:-N} = y ]

clean: check_clean
	rm public/json/*
	rm public/html/*
	rm public/json-index.json

