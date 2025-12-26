# Pulse Coding Assignment – SaaS Review Scraper

## Overview
Python script to scrape SaaS product reviews from G2 and Capterra and export them as JSON.

## Setup
pip install -r requirements.txt

## Usage
python review_scraper.py --company slack --source g2 --start_date 2023-01-01 --end_date 2023-12-31

## Notes
Scraping is best-effort due to anti-bot protections on review platforms.

