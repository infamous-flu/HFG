import os
import json
from dotenv import load_dotenv
from serpapi import GoogleSearch

load_dotenv()

class Scraper:
    countries = {
        "Angola": "ao",
        "Benin": "bj",
        "Botswana": "bw",
        "Burkina Faso": "bf",
        "Burundi": "bi",
        "Cameroon": "cm",
        "Cape Verde": "cv",
        "Central African Republic": "cf",
        "Chad": "td",
        "Comoros": "km",
        "Congo": "cg",
        "Congo, the Democratic Republic of the": "cd",
        "Cote D'ivoire": "ci",
        "Djibouti": "dj",
        "Equatorial Guinea": "gq",
        "Eritrea": "er",
        "Ethiopia": "et",
        "Gabon": "ga",
        "Ghana": "gh",
        "Guinea": "gn",
        "Guinea-Bissau": "gw",
        "Kenya": "ke",
        "Lesotho": "ls",
        "Liberia": "lr",
        "Madagascar": "mg",
        "Malawi": "mw",
        "Mali": "ml",
        "Mauritania": "mr",
        "Mauritius": "mu",
        "Mozambique": "mz",
        "Namibia": "na",
        "Niger": "ne",
        "Nigeria": "ng",
        "Rwanda": "rw",
        "Sao Tome and Principe": "st",
        "Senegal": "sn",
        "Seychelles": "sc",
        "Sierra Leone": "sl",
        "Somalia": "so",
        "South Africa": "za",
        "Sudan": "sd",
        "Swaziland": "sz",
        "Togo": "tg",
        "Uganda": "ug",
        "Western Sahara": "eh",
        "Zambia": "zm",
        "Zimbabwe": "zw"
    }

    def __init__(self, country):
        self.country = country
        self.params = {
            'api_key': os.getenv('SERPAPI_KEY'),        # https://serpapi.com/manage-api-key
            'uule': 'w+CAIQICINVW5pdGVkIFN0YXRlcw',		# encoded location (USA)
            'q': f'Water jobs in {self.country}',       # search query
            'hl': 'en',                         		# language of the search
            'gl': self.countries[self.country],         # country of the search
            'engine': 'google_jobs',					# SerpApi search engine
            'start': 0									# pagination
        }
        self.job_listings = []

    def search_jobs(self):
        while True:
            search = GoogleSearch(self.params)
            result_dict = search.get_dict()
            if 'error' in result_dict:
                break
            for result in result_dict["jobs_results"]:
                self.job_listings.append(result)
            self.params['start'] += 10

    def output_to_json(self):
        with open(f'data/raw_data/{self.countries[self.country]}.json', 'w') as o:
            json.dump(self.job_listings, o, indent=2, ensure_ascii=False)

    def run_scraper(self):
        self.search_jobs()
        self.output_to_json()
