# Web-Scraper
DeepSolv Assignment
# Shopify Insights Fetcher API

A FastAPI-based backend service that scrapes and fetches detailed insights from publicly accessible Shopify stores. It collects product catalogs, hero products, store policies, FAQs, social handles, and contact details, storing all data in a MySQL database using SQLAlchemy ORM.

---

## Features

- Extracts product information including price, description, and images.
- Captures hero products featured by the store.
- Gathers store policies like privacy, refund, and return policies.
- Collects FAQs, social media handles, contact details, and important links.
- Saves all scraped data in a MySQL database with duplicate handling.
- Provides a REST API endpoint to query store insights by Shopify store URL.
- Supports configuration via environment variables for database credentials.

---

## Tech Stack

- Python 3.10+
- FastAPI
- SQLAlchemy ORM
- MySQL (with PyMySQL driver)
- Pydantic for data validation
- Uvicorn ASGI server

---

## Installation
1. Clone the repo:

git clone https://github.com/yourusername/shopify-insights-fetcher.git
cd shopify-insights-fetcher

2. Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate

3. Install dependencies:
pip install -r requirements.txt


4. Setup MySQL database and user:
CREATE DATABASE shopify_insights;

---

## Running the App

Start the FastAPI server with:

uvicorn main:app --reload

Access the API at:
http://127.0.0.1:8000

---

## Usage

### Get Shopify Store Insights

Send a GET request to:

/shopify_insights?website_url={shopify_store_url}

**Example:**

http://127.0.0.1:8000/shopify_insights?website_url=https://memy.co.in

Returns detailed JSON data about the store.

## Project Structure

- `main.py` - FastAPI app with API endpoints
- `db.py` - SQLAlchemy models and DB setup
- `utils.py` - Functions for saving scraped data to DB
- `models.py` - Pydantic models for validation
- `scraper.py` - Shopify store scraping logic
- `.env` - Environment variables (not committed)
- `requirements.txt` - Python dependencies

---
