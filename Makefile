NOTES_PATH = /home/colobas/org/articles
orig_mds =  $(wildcard $(NOTES_PATH)/*.md)
target_md_dir = _posts

.PHONY: all svelte check_clean clean images

# create the list of target markdowns. the filenames have to be prepended
# with the appropriate date.
# this has to be run before the `all` rule so that the dependency list
# is available then
define make_target_list =
$(eval date := $(shell stat -c "%w" $(1) | awk '{print $$1}'))
$(eval target := $(target_md_dir)/$(date)-$(notdir $(1)))
$(eval target_mds += $(target))
endef

# make the rule for each file
define make_target_rule =
$(eval date := $(shell stat -c "%w" $(1) | awk '{print $$1}'))
$(eval target := $(target_md_dir)/$(date)-$(notdir $(1)))
$(target) : $(1) scripts/postprocess_md.py graph.json
	python scripts/postprocess_md.py $(1) $(target) graph.json

endef

# compute the dependency list for the `all` target
$(foreach md,$(orig_mds),$(eval $(call make_target_list,$(md))))

all: $(target_mds) svelte images

images:
	cp $(NOTES_PATH)/img/* images

svelte:
	cd svelte-components && npm run build

# expand the rules for each file
$(foreach md,$(orig_mds),$(eval $(call make_target_rule,$(md))))

#graph.json : scripts/make-graph.py $(orig_mds)
#	python scripts/make-graph.py $(ROAM_DB) $(NOTES_PATH) > graph.json.tmp
#	python -mjson.tool graph.json.tmp > graph.json
#	rm graph.json.tmp

check_clean:
	@echo -n "This will erase every file in \`_posts\`. Are you sure? [y/N] " && read ans && [ $${ans:-N} = y ]

clean: check_clean
	rm -rf _posts/*

