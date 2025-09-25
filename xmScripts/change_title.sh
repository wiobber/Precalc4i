#!/usr/bin/env bash
# Usage: ./fix_titles.sh file1.tex file2.tex ...

for f in "$@"; do
  [ -f "$f" ] || continue   # skip non-files

  base=$(basename "$f" .tex)

  # Step 1: ensure "Exercisesfor" → "Exercises for"
  mod=$(echo "$base" | sed 's/Exercisesfor/Exercises for/')

  # Step 2: split CamelCase -> add spaces before capitals
  words=$(echo "$mod" | sed -E 's/([a-z])([A-Z])/\1 \2/g')

  # Step 3: build replacement line
  replacement="\\\\xmtitle{$words}{}\n"

  # Step 4: replace only the first \xmtitle{Exercises}, keep rest unchanged
  awk -v repl="$replacement" '
    !done && /\\xmtitle{Exercises}/ {
      sub(/\\xmtitle{Exercises}/, repl)
      done=1
    }
    { print }
  ' "$f" > "$f.tmp" && mv "$f.tmp" "$f"
done
