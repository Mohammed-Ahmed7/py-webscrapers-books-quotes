import requests
from bs4 import BeautifulSoup
import csv

URL = "https://quotes.toscrape.com"

def fetch_quotes(url):
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")
    
    quotes_data = []
    for quote in soup.select("div.quote"):
        text   = quote.select_one("span.text").get_text(strip=True)
        author = quote.select_one("small.author").get_text(strip=True)
        quotes_data.append({"text": text, "author": author})

    return quotes_data

def save_to_csv(quotes, filename="quotes.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "author"])
        writer.writeheader()
        writer.writerows(quotes)
        
if __name__ == "__main__":
    data = fetch_quotes(URL)
    print(f"{len(data)} Zitate gefunden.")
    save_to_csv(data)
    print("In quotes.csv gespeichert.")