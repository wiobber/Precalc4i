#!/usr/bin/env python3
import sys
import os
import shutil
from openai import OpenAI

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} file1 [file2 ...]")
        sys.exit(1)

    # load prompt from prompt.txt
    with open("prompt.txt", "r", encoding="utf-8") as f:
        prompt = f.read().strip()

    client = OpenAI()

    for filename in sys.argv[1:]:
        if not os.path.isfile(filename):
            print(f"Skipping {filename}: not a file")
            continue

        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()

        # build the full user request
        user_request = f"{prompt}\n\n---\n\n{content}"

        # send to API
        response = client.chat.completions.create(
            model="gpt-5",  # or gpt-4o / gpt-4.1 if you prefer
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_request},
            ],
        )

        result = response.choices[0].message.content

        # backup original
        backup = filename + ".orig"
        if not os.path.exists(backup):
            shutil.copy2(filename, backup)
            print(f"Backup created: {backup}")
        else:
            print(f"Backup already exists: {backup} (not overwritten)")

        # overwrite file with new content
        with open(filename, "w", encoding="utf-8") as f:
            f.write(result)

        print(f"Processed {filename} (original in {backup})")

if __name__ == "__main__":
    main()
