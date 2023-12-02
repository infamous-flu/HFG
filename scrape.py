import json
from pprint import pprint
from scraper import Scraper

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

for country in countries:
    try:
        scraper = Scraper(country)
        scraper.run_scraper()
    except Exception:
        print(Exception)
