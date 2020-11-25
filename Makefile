ROAM_DB = /home/colobas/.emacs.d/.local/etc/org-roam.db
NOTES_PATH = /home/colobas/org/knowledge-base/notes
orig_orgs =  $(wildcard $(NOTES_PATH)/*.org)
orig_mds =  $(wildcard $(NOTES_PATH)/*.md)
target_md_dir = _posts

.PHONY: all svelte check_clean clean images

# sadly, this has to be run before the `all` rule, so that the dependency list is available then
define make_target_list =
$(eval date := $(shell stat -c "%w" $(1) | awk '{print $$1}'))
$(eval orig_md := $(patsubst %.org,%.md,$(1)))
$(eval target := $(target_md_dir)/$(date)-$(notdir $(orig_md)))
$(eval target_mds += $(target))
endef

# make the rule for each file
define make_target_rule =
$(eval date := $(shell stat -c "%w" $(1) | awk '{print $$1}'))
$(eval orig_md := $(patsubst %.org,%.md,$(1)))
$(eval target := $(target_md_dir)/$(date)-$(notdir $(orig_md)))
$(target) : $(orig_md) scripts/postprocess_md.py graph.json
	python scripts/postprocess_md.py $(orig_md) $(target) graph.json

endef

# compute the dependency list for the `all` target
$(foreach org,$(orig_orgs),$(eval $(call make_target_list,$(org))))

all: $(target_mds) svelte images

images:
	cp $(NOTES_PATH)/img/* images

svelte:
	cd svelte-components && npm run build

# expand the rules for each file
$(foreach org,$(orig_orgs),$(eval $(call make_target_rule,$(org))))

graph.json : scripts/make-graph.py $(orig_mds)
	python scripts/make-graph.py $(ROAM_DB) $(NOTES_PATH) > graph.json.tmp
	python -mjson.tool graph.json.tmp > graph.json
	rm graph.json.tmp

check_clean:
	@echo -n "This will erase every file in \`_posts\`. Are you sure? [y/N] " && read ans && [ $${ans:-N} = y ]

clean: check_clean
	rm _posts/*

