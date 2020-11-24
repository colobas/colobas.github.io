orig_orgs =  $(wildcard public/org-files/*.org)
orig_mds =  $(wildcard public/org-files/*.md)
ROAM_DB = /home/colobas/.emacs.d/.local/etc/org-roam.db
NOTES_PATH = /home/colobas/org/knowledge-base/notes

.PHONY: all

# sadly, this has to be run before the `all` rule, so that the dependency list is available then
define make_target_list =
$(eval date := $(shell stat -c "%w" $(1) | awk '{print $$1}'))
$(eval orig_md := $(patsubst %.org,%.md,$(1)))
$(eval target := public/markdown/$(date)-$(notdir $(orig_md)))
$(eval target_mds += $(target))
endef

# make the rule for each file
define make_target_rule =
$(eval date := $(shell stat -c "%w" $(1) | awk '{print $$1}'))
$(eval orig_md := $(patsubst %.org,%.md,$(1)))
$(eval target := public/markdown/$(date)-$(notdir $(orig_md)))
$(target) : scripts/postprocess_md.py public/graph.json
	python scripts/postprocess_md.py $(orig_md) $(target) public/graph.json

endef

# compute the dependency list for the `all` target
$(foreach org,$(orig_orgs),$(eval $(call make_target_list,$(org))))

all: $(target_mds)

# expand the rules for each file
$(foreach org,$(orig_orgs),$(eval $(call make_target_rule,$(org))))

public/graph.json : scripts/make-graph.py $(orig_mds)
	python scripts/make-graph.py $(ROAM_DB) $(NOTES_PATH) > public/graph.json.tmp
	python -mjson.tool public/graph.json.tmp > public/graph.json
	rm public/graph.json.tmp

check_clean:
	@echo -n "This will erase every file in \`public/markdown\`. Are you sure? [y/N] " && read ans && [ $${ans:-N} = y ]

clean: check_clean
	rm public/markdown/*

