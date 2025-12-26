# review_scraper.py
# Pulse Coding Assignment – SaaS Review Scraper

import argparse
import json
from datetime import datetime
import requests
from bs4 import BeautifulSoup


def parse_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d")


def is_within_range(review_date, start, end):
    return start <= review_date <= end


def scrape_g2(company, start_date, end_date, max_pages=3):
    reviews = []
    base_url = f"https://www.g2.com/products/{company.lower().replace(' ', '-')}/reviews"
    headers = {"User-Agent": "Mozilla/5.0"}

    for page in range(1, max_pages + 1):
        url = f"{base_url}?page={page}"
        try:
            resp = requests.get(url, headers=headers, timeout=10)
        except Exception:
            break

        if resp.status_code != 200:
            break

        soup = BeautifulSoup(resp.text, "html.parser")
        blocks = soup.select("div.paper")

        for block in blocks:
            try:
                title = block.select_one("h3").get_text(strip=True)
                body = block.select_one("p").get_text(strip=True)
                date_text = block.select_one("time").get("datetime")[:10]
                review_date = parse_date(date_text)

                if not is_within_range(review_date, start_date, end_date):
                    continue

                reviews.append({
                    "title": title,
                    "review": body,
                    "date": date_text,
                    "rating": None,
                    "reviewer": "Anonymous"
                })
            except Exception:
                continue

    return reviews


def scrape_capterra(company, start_date, end_date, max_pages=3):
    reviews = []
    base_url = f"https://www.capterra.com/p/{company.lower().replace(' ', '-')}/reviews/"
    headers = {"User-Agent": "Mozilla/5.0"}

    for page in range(1, max_pages + 1):
        url = f"{base_url}?page={page}"
        try:
            resp = requests.get(url, headers=headers, timeout=10)
        except Exception:
            break

        if resp.status_code != 200:
            break

        soup = BeautifulSoup(resp.text, "html.parser")
        blocks = soup.select("div.review")

        for block in blocks:
            try:
                title = block.select_one("h3").get_text(strip=True)
                body = block.select_one("p").get_text(strip=True)
                date_text = block.select_one("time").get("datetime")[:10]
                review_date = parse_date(date_text)

                if not is_within_range(review_date, start_date, end_date):
                    continue

                reviews.append({
                    "title": title,
                    "review": body,
                    "date": date_text,
                    "rating": None,
                    "reviewer": "Anonymous"
                })
            except Exception:
                continue

    return reviews


def parse_args():
    parser = argparse.ArgumentParser(description="SaaS Review Scraper")
    parser.add_argument("--company", help="Company name (slug preferred)")
    parser.add_argument("--source", choices=["g2", "capterra"], help="Review source")
    parser.add_argument("--start_date", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end_date", help="End date (YYYY-MM-DD)")
    return parser


def main(args):
    start = parse_date(args.start_date)
    end = parse_date(args.end_date)

    if args.source == "g2":
        reviews = scrape_g2(args.company, start, end)
    else:
        reviews = scrape_capterra(args.company, start, end)

    output_file = f"{args.company}_{args.source}_reviews.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(reviews, f, indent=2, ensure_ascii=False)

    print(f"Scraped {len(reviews)} reviews. Saved to {output_file}")


if __name__ == "__main__":
    parser = parse_args()
    args = parser.parse_args()

    if not all([args.company, args.source, args.start_date, args.end_date]):
        print("No CLI arguments provided. Showing help and exiting gracefully.\n")
        parser.print_help()
    else:
        main(args)
