#!/usr/bin/env python3
import os
import json
import time
import argparse
import requests

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Please set OPENAI_API_KEY environment variable")

BATCH_URL = "https://api.openai.com/v1/batches"

def create_jsonl(latex_files, prompt_file, output_file="batch_requests.jsonl"):
    """Create a JSONL batch file for all LaTeX files"""
    if not os.path.isfile(prompt_file):
        raise FileNotFoundError(f"Prompt file '{prompt_file}' not found.")

    with open(prompt_file, "r", encoding="utf-8") as f:
        prompt = f.read().strip()

    tasks = []
    for filename in latex_files:
        if not os.path.isfile(filename):
            print(f"Skipping {filename}: not a file")
            continue

        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()

        task = {
            "custom_id": filename,
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": "gpt-5",
                "messages": [
                    {"role": "system", "content": "You are a LaTeX expert assistant."},
                    {
                        "role": "user",
                        "content": f"{prompt}\n\nYou are given a LaTeX file: {filename}\n"
                                   f"Please edit/improve it while preserving all LaTeX formatting.\n"
                                   f"Ensure the output is valid LaTeX code.\nReturn only LaTeX.\n\n{content}"
                    },
                ]
            }
        }
        tasks.append(task)

    with open(output_file, "w", encoding="utf-8") as f:
        for task in tasks:
            f.write(json.dumps(task) + "\n")

    print(f"Created batch JSONL file '{output_file}' with {len(tasks)} tasks")
    return output_file

def upload_file(jsonl_file):
    """Upload JSONL file for batch processing"""
    with open(jsonl_file, "rb") as f:
        resp = requests.post(
            "https://api.openai.com/v1/files",
            headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
            files={"file": (jsonl_file, f)},
            data={"purpose": "batch"}
        )
    resp.raise_for_status()
    file_id = resp.json()["id"]
    print(f"Uploaded file. File ID: {file_id}")
    return file_id

def create_batch_job(file_id):
    """Create a batch job using the uploaded file"""
    payload = {
        "input_file_id": file_id,
        "endpoint": "/v1/chat/completions",
        "completion_window": "24h",
        "metadata": {"description": "Batch processing LaTeX files"}
    }
    resp = requests.post(BATCH_URL, headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
                         json=payload)
    resp.raise_for_status()
    batch_id = resp.json()["id"]
    print(f"Created batch job. Batch ID: {batch_id}")
    return batch_id

def monitor_batch(batch_id):
    """Monitor batch job until completion"""
    url = f"{BATCH_URL}/{batch_id}"
    while True:
        resp = requests.get(url, headers={"Authorization": f"Bearer {OPENAI_API_KEY}"})
        resp.raise_for_status()
        status = resp.json()["status"]
        print(f"Batch status: {status}")
        if status == "succeeded":
            print("Batch completed successfully.")
            break
        elif status == "completed":
            print("Batch completed successfully.")
            break
        elif status == "failed":
            raise RuntimeError("Batch failed")
        time.sleep(60)

def retrieve_results(batch_id):
    """Retrieve batch results and overwrite LaTeX files with backups"""
    url = f"{BATCH_URL}/{batch_id}/results"
    resp = requests.get(url, headers={"Authorization": f"Bearer {OPENAI_API_KEY}"})
    resp.raise_for_status()
    results = resp.json()["data"]

    for item in results:
        filename = item["custom_id"]
        content = item["body"]["choices"][0]["message"]["content"].strip()

        # backup original
        backup = filename + ".orig"
        if not os.path.exists(backup):
            os.rename(filename, backup)
            print(f"Backup created: {backup}")

        # write result
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Processed {filename}")

def main():
    parser = argparse.ArgumentParser(description="Process multiple LaTeX files using OpenAI Batch API.")
    parser.add_argument("-p", "--prompt", default="prompt.txt", help="Prompt file")
    parser.add_argument("files", nargs="+", help="LaTeX files to process")
    args = parser.parse_args()

    jsonl_file = create_jsonl(args.files, args.prompt)
    file_id = upload_file(jsonl_file)
    batch_id = create_batch_job(file_id)
    monitor_batch(batch_id)
    retrieve_results(batch_id)

if __name__ == "__main__":
    main()
