POSTS_PATH = /home/colobas/org/articles
orig_orgs =  $(wildcard $(POSTS_PATH)/*.org)

target_md_dir = _posts

.PHONY: all svelte check_clean clean images

# create the list of target markdowns. the filenames have to be prepended
# with the appropriate date.
# this has to be run before the `all` rule so that the dependency list
# is available then
define make_target_list =
$(eval date := $(shell stat -c '%w' $(1) | awk '{print $$1}'))
$(eval target := $(target_md_dir)/$(date)-$(subst .org,.md,$(notdir $(1))))
$(eval target_mds += $(target))
endef

# make the rule for each file
define make_target_rule =
$(eval date := $(shell stat -c '%w' $(1) | awk '{print $$1}'))
$(eval target := $(target_md_dir)/$(date)-$(subst .org,.md,$(notdir $(1))))
$(target) : $(1)
	./scripts/org2jekyll.sh $(1) $(target)
endef

# compute the dependency list for the `all` target
$(foreach org,$(orig_orgs),$(eval $(call make_target_list,$(org))))

all: $(target_mds) svelte images

images:
	cp -r $(POSTS_PATH)/images/. images

svelte:
	cd svelte-components && npm install && npm run build

# expand the rules for each file
$(foreach org,$(orig_orgs),$(info making rule for $(org))$(eval $(call make_target_rule,$(org))))


check_clean:
	@echo -n "This will erase every file in \`_posts\`. Are you sure? [y/N] " && read ans && [ $${ans:-N} = y ]

clean: check_clean
	rm -rf _posts/*

