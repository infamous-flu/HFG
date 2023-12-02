import os
import re
import json
from pprint import pprint


def clean_text(text):
    text = text.replace('\n', ' ').replace('\r', '')
    text = ''.join(char for char in text if ord(char) < 128)
    text = re.sub(
        r'[\x00-\x1F\x7F-\x9F\u200B-\u200D\u2028-\u2029\u3000]', '', text)
    return text.strip()


def clean_data():
    for filename in os.listdir('data/raw_data'):
        if filename.endswith('.json'):
            input_file = os.path.join('data/raw_data', filename)
            outpt_file = os.path.join('data/processed_data', filename)
        with open(input_file, 'r') as file:
            data = json.load(file)
        processed_jobs = []
        for unprocessed_job in data:
            processed_job = {
                'title': clean_text(unprocessed_job.get('title', '')),
                'company': clean_text(unprocessed_job.get('company_name', '')),
                'location': clean_text(unprocessed_job.get('location', '')),
                'description': clean_text(unprocessed_job.get('description', ''))
            }
            processed_jobs.append(processed_job)
            with open(outpt_file, 'w') as file:
                json.dump(processed_jobs, file, indent=2)


if __name__ == "__main__":
    clean_data()
