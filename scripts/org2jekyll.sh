#!/bin/bash

org_file="$1"
target_file="$2"
tex_file="${org_file%.org}.tex"

echo $org_file
echo $tex_file
echo $target_file

# export org file as latex file (to make it easy to stay compatible with pdf exports from org)
doom-export-posts "$org_file"

# convert latex file into markdown
pandoc -s -f latex -t markdown+raw_tex "$tex_file" |
    sed 's/{{/{ {/g' |
    sed 's/}}/} }/g' |
    sed -E 's/^(#[^{}]*)\{[^}]*\}/\1/' |    # remove header anchor if it exists
    awk '{
        if ($0 ~ /^---$/ && !found_front_matter) {
            found_front_matter = 1
            print $0
            print "math: true"
        } else {
            print $0
        }
    }' > "$target_file"

# remove temporary latex file
rm "$tex_file"
