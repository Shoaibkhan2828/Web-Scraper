import requests
from bs4 import BeautifulSoup
from models import BrandContext, Product, FAQ

def fetch_products(shop_url):
    """Fetches all products from /products.json endpoint."""
    products = []
    try:
        resp = requests.get(f"{shop_url.rstrip('/')}/products.json", timeout=10)
        resp.raise_for_status()
        data = resp.json().get("products", [])
        for p in data:
            products.append(Product(
                id=str(p.get("id")),
                title=p.get("title"),
                url=f"{shop_url}/products/{p.get('handle')}",
                price=str(p.get("variants", [])[0].get("price")) if p.get("variants") else None,
                image=p.get("images")["src"] if p.get("images") else None,
                description=p.get("body_html"),
            ))
    except Exception as ex:
        print("Error fetching products:", ex)
    return products


def fetch_policy(shop_url, policy_type):
    """Scrape privacy/return/refund policy using route conventions or keywords."""
    possible_paths = [f"/pages/{policy_type}", f"/policies/{policy_type}-policy", f"/{policy_type}-policy"]
    for path in possible_paths:
        try:
            resp = requests.get(f"{shop_url.rstrip('/')}{path}", timeout=10)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                # Try to extract main content
                text = soup.get_text(separator='\n')
                if text:
                    return text[:2000]  # Trim long content
        except Exception:
            continue
    return None

def extract_links_and_context(soup, shop_url):
    """Extract all important links, contact info, FAQs, socials, brand context from homepage."""
    links, faqs, socials, contacts, about_brand = [], [], [], [], None

    # Links
    for a in soup.find_all('a', href=True):
        href = a['href']
        text = a.get_text(strip=True).lower()
        if "track" in text or "contact" in text or "blog" in text or "faq" in text:
            links.append(shop_url.rstrip('/') + href if href.startswith('/') else href)
        # Socials
        for s in ["instagram", "facebook", "tiktok", "twitter", "linkedin"]:
            if s in href or s in text:
                socials.append(href)
        # Contact
        if "mailto" in href or "tel:" in href:
            contacts.append(href)
    # About
    about_section = soup.find(string=lambda t: "about" in t.lower())
    if about_section:
        about_brand = about_section

    # FAQs
    faq_section = soup.find(string=lambda t: "faq" in t.lower())
    if faq_section:
        faqs.append(FAQ(question=faq_section, answer="See website for details"))

    return links, faqs, socials, contacts, about_brand

def extract_hero_products(soup, shop_url):
    """Try to extract hero products from homepage cards/carousels."""
    heroes = []
    # This logic should be tailored based on shopify themes but generally they live in home page product cards
    for prod_section in soup.find_all("a", href=True):
        href = prod_section['href']
        if "/products/" in href:
            title = prod_section.get_text(strip=True)
            heroes.append(Product(
                id=href.split("/")[-1],
                title=title,
                url=shop_url.rstrip("/") + href if href.startswith("/") else href,
            ))
            if len(heroes) > 8:
                break
    return heroes

def scrape_shopify_store(shop_url):
    """Main orchestrator for scraping the store."""
    context = BrandContext(
        brand_name=None,
        website_url=shop_url,
        product_catalog=[],
        hero_products=[],
        privacy_policy=None,
        return_policy=None,
        refund_policy=None,
        faq=[],
        social_handles=[],
        contact_details=[],
        about_brand=None,
        important_links=[]
    )
    try:
        # Home page
        resp = requests.get(shop_url, timeout=10)
        if resp.status_code != 200:
            return None, 401
        soup = BeautifulSoup(resp.text, "html.parser")

        # Brand name
        if soup.title:
            context.brand_name = soup.title.string.split('|')[0].strip() if "|" in soup.title.string else soup.title.string.strip()

        # All products
        context.product_catalog = fetch_products(shop_url)

        # Hero products (from homepage)
        context.hero_products = extract_hero_products(soup, shop_url)

        # Policies
        for p in ['privacy', 'return', 'refund']:
            setattr(context, f"{p}_policy", fetch_policy(shop_url, p))

        # Links/socials/contacts/brand text/faqs
        links, faqs, socials, contacts, about_brand = extract_links_and_context(soup, shop_url)
        context.important_links = links
        context.faq = faqs
        context.social_handles = socials
        context.contact_details = contacts
        context.about_brand = about_brand

        return context, 200
    except Exception as e:
        print("Error in scraping:", e)
        return None, 500
