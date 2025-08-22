#!/bin/bash

### egrep -e "\\\\section" -e "\\\\input" */*.txt | sed "s?[^/]*/??" | sed "s/.txt//" >titles.txt

input="titles.txt"   # your input list with the pairs
while read -r line1 && read -r line2; do
    # folder and title
    folder=$(echo "$line1" | cut -d: -f1)
    title=$(echo "$line1" | sed -n 's/.*\\section{\(.*\)}/\1/p')

    # folder and file (without extension)
    file=$(echo "$line2" | sed -n 's/.*\\input{\(.*\)}/\1/p')

    texfile="$folder/$file.tex"

    echo "Updating $texfile → title: $title"

    # replace \xmtitle{TITLE} with \xmtitle{<title>}
    sed -i "s|\\\\xmtitle{TITLE}|\\\\xmtitle{$title}|" "$texfile"

done < "$input"
