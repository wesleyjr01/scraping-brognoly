from bs4 import BeautifulSoup
import requests
import csv
from datetime import datetime

# Brognoly Scraper
all_houses_urls = []
pages_counter = 1
is_url_empty = False
while not is_url_empty:
    print(f"Scraping URL number {pages_counter}...")
    start_url = (
        f"https://www.brognoli.com.br/imoveis/page/{pages_counter}"
        "/?filtering=off&sort=newest&ini=1&search_type=16&search_category"
        "=445&gsearch_city=FLORIAN%C3%93POLIS&search_city"
        "=FLORIAN%C3%93POLIS&search_neighborhood%5B0%5D"
    )
    html_text = requests.get(start_url).text
    soup = BeautifulSoup(html_text, "lxml")

    current_houses_urls = [
        house.a["href"] for house in soup.find_all("div", class_="item active")
    ]
    all_houses_urls = all_houses_urls + current_houses_urls
    if len(current_houses_urls) == 0:
        is_url_empty = True

    pages_counter += 1

# Write list of URLS to csv file
now = datetime.now().strftime("%Y%m%d")
with open(f"houses_urls_brognoly_{now}.csv", "w") as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(all_houses_urls)