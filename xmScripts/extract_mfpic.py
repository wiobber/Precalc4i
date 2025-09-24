#!/usr/bin/env python3
"""
Extract all \\begin{mfpic} … \\end{mfpic} environments from a .tex file,
write each to a separate file, and replace the original block with
\\input{<basename>_pic<N>.tex}.

Usage:
    ./extract_mfpic.py myfile.tex
"""

import re
import sys
from pathlib import Path

def main(tex_path: Path):
    # Read the whole source file
    content = tex_path.read_text(encoding="utf-8")

    # Regex that matches a complete mfpic environment, non‑greedy across lines
    pattern = re.compile(
        r"\\begin\{mfpic\}.*?\\end\{mfpic\}",
        re.DOTALL | re.MULTILINE,
    )

    # Find all matches
    matches = list(pattern.finditer(content))
    if not matches:
        print("No mfpic environments found.")
        return

    # Base name without suffix (e.g. 'myfile' from 'myfile.tex')
    base = tex_path.stem

    # We'll build a new version of the file piece by piece
    new_parts = []
    last_end = 0

    for idx, m in enumerate(matches, start=1):
        # Write the extracted block to its own file
        out_name = f"{base}_pic{idx}.tex"
        Path(out_name).write_text(m.group(0), encoding="utf-8")
        print(f"Wrote {out_name}")

        # Append the text before this block unchanged
        new_parts.append(content[last_end:m.start()])

        # Insert the \input line that points to the new file
        new_parts.append(f"\\input{{{out_name}}}\n")

        # Update the cursor
        last_end = m.end()

    # Append any trailing text after the last block
    new_parts.append(content[last_end:])

    # Write the modified source back (you could also write to a new file)
    tex_path.write_text("".join(new_parts), encoding="utf-8")
    print(f"Updated {tex_path.name} with \\input statements.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: %s <tex‑file>\n" % sys.argv[0])
        sys.exit(1)

    tex_file = Path(sys.argv[1])
    if not tex_file.is_file():
        sys.stderr.write(f"Error: file '{tex_file}' not found.\n")
        sys.exit(1)

    main(tex_file)