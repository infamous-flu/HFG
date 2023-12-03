import re

with open('data/mock_jobs.txt', 'r') as file:
    jobs_text = file.read()

# Split jobs based on the pattern
jobs_list = re.split(r'\d+\.', jobs_text)[1:]

# Save each job in a separate text file
for i, job_text in enumerate(jobs_list, start=1):
    job_filename = f'job_{i}.txt'
    with open(f'data/{job_filename}', 'w') as job_file:
        job_file.write(job_text.strip())
    print(f'Job {i} saved as {job_filename}')
