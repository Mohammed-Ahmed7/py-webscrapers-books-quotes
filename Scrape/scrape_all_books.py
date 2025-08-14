import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from urllib.parse import urljoin

URL = "http://books.toscrape.com/"

def fetch_all_books(start_url):
    url = start_url
    all_books = []
    
    while True:
        resp = requests.get(url)
        resp.raise_for_status()
        resp.encoding = "utf-8"
        soup = BeautifulSoup(resp.content, "lxml")
        
        
        word2num = {"One":1, "Two":2, "Three":3, "Four":4, "Five":5}
        
        for item in soup.select("li.col-xs-6.col-sm-4.col-md-3.col-lg-3"):
            article = item.select_one("article.product_pod")
            if not article:
                continue

            title = article.select_one("h3 > a")["title"]
            price = article.select_one("p.price_color").get_text(strip=True)
            availability = article.select_one(
                "p.instock.availability").get_text(strip=True)
            
            # Hier holen wir die Bewertung:
            rating_text = article.select_one("p.star-rating")["class"][1]
            # rating_tag["class"] liefert z.B. ["star-rating", "Three"]
            rating_num = word2num[rating_text]

            all_books.append({
                "title": title,
                "price": price,
                "availability": availability,
                "rating": rating_num
        })
        next_li = soup.select_one("li.next > a")
        if not next_li:
            break
        
        next_href = next_li["href"]
        url = urljoin(url, next_href)
        print(f"Wechsel zu {url}")
    return all_books

def save_to_csv(items, filename="bookss.csv"):
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "price", "availability","rating"])
        writer.writeheader()
        writer.writerows(items)
        
def save_to_excel(items, filename="bookss.xlsx"):
    # Aus Liste von Dicts einen DataFrame bauen
    df = pd.DataFrame(items)
    # Als .xlsx speichern (OpenPyXL im Hintergrund)
    df.to_excel(filename, index=False)

if __name__ == "__main__":
    data = fetch_all_books(URL)
    print(f"{len(data)} Bücher gefunden.")
    save_to_csv(data)
    save_to_excel(data)
    print("Daten in books.csv gespeichert.")