from fastapi import FastAPI, HTTPException, Query
from models import BrandContext
from scraper import scrape_shopify_store
from utils import save_brand_context
from db import init_db

app = FastAPI(title="Shopify Insights Fetcher")

@app.on_event("startup")
def startup_event():
    # Initialize database tables
    init_db()

@app.get("/")
def root():
    return {
        "message": "Welcome to Shopify Insights Fetcher API. Use /shopify_insights?website_url=https://colourpop.com/products/black-lengthening-mascara to get store data."
    }

@app.get("/shopify_insights", response_model=BrandContext)
def get_shopify_insights(website_url: str = Query(..., description="Shopify store URL")):
    result, status = scrape_shopify_store(website_url)
    if status == 401:
        raise HTTPException(status_code=401, detail="Website not found or inaccessible")
    elif status == 500:
        raise HTTPException(status_code=500, detail="Internal error occurred during scraping")
    # Save data to DB after successful scrape
    save_brand_context(result)
    return result
