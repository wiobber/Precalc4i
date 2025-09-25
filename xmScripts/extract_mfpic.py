#!/usr/bin/env python3
"""
Extract all \\begin{mfpic} … \\end{mfpic} environments from .tex files,
write each to a separate file, and replace the original block with
\\input{<basename>_pic<N>.tex}.

Usage:
    ./extract_mfpic.py file1.tex file2.tex ...
"""

import re
import sys
from pathlib import Path

def should_skip(tex_path: Path) -> bool:
    """Skip files matching *_pic<number>.tex"""
    return re.search(r"_pic\d+\.tex$", tex_path.name) is not None

def process_file(tex_path: Path):
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
        print(f"No mfpic environments found in {tex_path}")
        return

    # Base name without suffix
    base = tex_path.stem

    # Build the new content piece by piece
    new_parts = []
    last_end = 0

    for idx, m in enumerate(matches, start=1):
        # Write the extracted block to its own file
        out_name = tex_path.parent / f"{base}_pic{idx}.tex"
        out_name.write_text(m.group(0), encoding="utf-8")
        print(f"Wrote {out_name}")

        # Append the text before this block unchanged
        new_parts.append(content[last_end:m.start()])

        # Insert the \input line
        new_parts.append(f"\\input{{{out_name.name}}}\n")

        last_end = m.end()

    # Append trailing text
    new_parts.append(content[last_end:])

    # Overwrite the original file
    tex_path.write_text("".join(new_parts), encoding="utf-8")
    print(f"Updated {tex_path} with \\input statements.")

def main():
    if len(sys.argv) < 2:
        sys.stderr.write(f"Usage: {sys.argv[0]} <tex-file> [<tex-file> ...]\n")
        sys.exit(1)

    for arg in sys.argv[1:]:
        tex_path = Path(arg)
        if not tex_path.is_file():
            print(f"Skipping {arg}: not a file")
            continue
        if should_skip(tex_path):
            print(f"Skipping {tex_path}: matches *_pic<number>.tex")
            continue

        process_file(tex_path)

if __name__ == "__main__":
    main()
