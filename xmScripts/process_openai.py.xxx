#!/usr/bin/env python3
import sys
import os
import shutil
from openai import OpenAI
import re

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} file1 [file2 ...]")
        sys.exit(1)

    # load prompt from prompt.txt
    with open("prompt.txt", "r", encoding="utf-8") as f:
        base_prompt = f.read().strip()

    client = OpenAI()

    files_to_process = []
    concatenated_content = ""

    # read all files and concatenate
    for filename in sys.argv[1:]:
        if not os.path.isfile(filename):
            print(f"Skipping {filename}: not a file")
            continue

        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()

        files_to_process.append((filename, content))
        concatenated_content += f"--- File: {filename} ---\n{content}\n\n"

    if not files_to_process:
        print("No valid files to process.")
        sys.exit(0)

    # build full user request
    user_request = (
        f"{base_prompt}\n\n"
        f"You are given multiple LaTeX files separated by markers '--- File: filename ---'.\n"
        f"Please edit/improve each file **individually**, keeping all LaTeX formatting intact.\n"
        f"Ensure each output is **valid LaTeX code** and return each file wrapped in the same marker format.\n\n"
        f"{concatenated_content}\n"
        f"Output each file as:\n"
        f"--- File: filename ---\n<content>\n--- End of file ---\n"
    )

    # send to API
    response = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {"role": "system", "content": "You are a LaTeX expert assistant."},
            {"role": "user", "content": user_request},
        ],
    )

    result = response.choices[0].message.content

    # extract content per file
    file_pattern = re.compile(r"--- File:\s*(.+?)\s*---\n(.*?)\n--- End of file ---", re.DOTALL)
    matches = file_pattern.findall(result)

    if not matches:
        print("No valid output detected from the model.")
        print("Raw output:\n", result)
        sys.exit(1)

    for filename, content in matches:
        filename = filename.strip()
        content = content.strip()

        # backup original
        backup = filename + ".orig"
        if not os.path.exists(backup):
            shutil.copy2(filename, backup)
            print(f"Backup created: {backup}")
        else:
            print(f"Backup already exists: {backup} (not overwritten)")

        # overwrite file
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"Processed {filename} (original in {backup})")

if __name__ == "__main__":
    main()
