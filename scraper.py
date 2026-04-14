#!/usr/bin/env python3
"""
Task 2: Web Data Scraper
Scrapes article titles/product data using requests + BeautifulSoup.
Saves results to a CSV file.

Install dependencies:
    pip install requests beautifulsoup4
"""

import csv
import sys
from datetime import datetime

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Missing dependencies. Run: pip install requests beautifulsoup4")
    sys.exit(1)

OUTPUT_CSV = "scraped_data.csv"


# ──────────────────────────────────────────────
# Scraper 1: Hacker News — article titles
# ──────────────────────────────────────────────
def scrape_hacker_news(pages=1):
    """Scrape top story titles and links from Hacker News."""
    results = []
    for page in range(1, pages + 1):
        url = f"https://news.ycombinator.com/?p={page}"
        print(f"  Fetching {url} ...")
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"  ❌ Request failed: {e}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        for item in soup.select(".titleline > a"):
            results.append({
                "source": "Hacker News",
                "title": item.get_text(strip=True),
                "url": item.get("href", ""),
                "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            })

    print(f"   Scraped {len(results)} articles from Hacker News.")
    return results


# ──────────────────────────────────────────────
# Scraper 2: Books to Scrape — product details
# ──────────────────────────────────────────────
def scrape_books(pages=1):
    """Scrape book titles, prices, and ratings from books.toscrape.com."""
    BASE = "https://books.toscrape.com/catalogue"
    RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    results = []

    for page in range(1, pages + 1):
        url = f"{BASE}/page-{page}.html"
        print(f"  Fetching {url} ...")
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"  ❌ Request failed: {e}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        for article in soup.select("article.product_pod"):
            title = article.h3.a["title"]
            price = article.select_one(".price_color").get_text(strip=True)
            rating_class = article.p["class"][1]  # e.g., "Three"
            rating = RATING_MAP.get(rating_class, 0)
            availability = article.select_one(".availability").get_text(strip=True)
            results.append({
                "source": "Books to Scrape",
                "title": title,
                "price": price,
                "rating": rating,
                "availability": availability,
                "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            })

    print(f"   Scraped {len(results)} books from books.toscrape.com.")
    return results


# ──────────────────────────────────────────────
# Save to CSV
# ──────────────────────────────────────────────
def save_to_csv(data, filepath=OUTPUT_CSV):
    if not data:
        print("No data to save.")
        return
    fieldnames = list(data[0].keys())
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(data)
    print(f"\n💾 Saved {len(data)} rows → {filepath}")


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────
def main():
    print("=== Web Data Scraper ===\n")
    print("Choose a scraper:")
    print("  1. Hacker News article titles")
    print("  2. Books to Scrape product details")
    print("  3. Both\n")

    choice = input("Enter choice (1/2/3): ").strip()
    pages = input("How many pages to scrape? [1]: ").strip()
    pages = int(pages) if pages.isdigit() and int(pages) > 0 else 1

    all_data = []

    if choice in ("1", "3"):
        print("\n[Hacker News]")
        all_data.extend(scrape_hacker_news(pages))

    if choice in ("2", "3"):
        print("\n[Books to Scrape]")
        all_data.extend(scrape_books(pages))

    if not all_data:
        print("No data scraped. Exiting.")
        return

    save_to_csv(all_data)
    print("\nFirst 3 results preview:")
    for item in all_data[:3]:
        print(" ", item)


if __name__ == "__main__":
    main()