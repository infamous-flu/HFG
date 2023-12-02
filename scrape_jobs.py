import re
import json
from pprint import pprint
from requests_html import HTMLSession
from bs4 import BeautifulSoup

baseurl = "https://www.joshswaterjobs.com/jobs/?_jobs_region=africa&_per_page=100"


def clean_text(text):
    text = text.replace('\n', ' ').replace('\r', '')
    text = ''.join(char for char in text if ord(char) < 128)
    text = re.sub(
        r'[\x00-\x1F\x7F-\x9F\u200B-\u200D\u2028-\u2029\u3000]', '', text)
    return text.strip()


def get_urls(url):
    response = HTMLSession().get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    urls = [p.find("a")["href"]
            for p in soup.find_all("p", class_="job-title pb-2 m-0")]
    return urls


def get_data(url):
    response = HTMLSession().get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find("h1").string
    company = soup.find("p", class_="org m-0 pb-2").string
    locations = [p.string for p in soup.find_all(
        "p", class_="location m-0")]
    body = soup.find("div", class_="col-lg-12 job-body-content")
    description = " ".join([p.get_text(strip=True)
                           for p in body.find_all("p")])
    return {
        "title": clean_text(title),
        "company": clean_text(company),
        "locations": [clean_text(location) for location in locations],
        "description": clean_text(description),
    } if description else {}


if __name__ == "__main__":
    urls = get_urls(baseurl)
    jobs = []
    for url in urls:
        try:
            data = get_data(url)
            if data:
                jobs.append(data)
            print(f"scraped {url}")
        except:
            print(f"failed to scrape {url}")
    with open("jobs.json", "w") as file:
        json.dump(jobs, file, indent=2)
