from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class FAQ(BaseModel):
    question: str
    answer: str

class Product(BaseModel):
    id: str
    title: str
    url: Optional[str]
    price: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None

class BrandContext(BaseModel):
    brand_name: Optional[str]
    website_url: HttpUrl
    product_catalog: List[Product]
    hero_products: List[Product]
    privacy_policy: Optional[str]
    return_policy: Optional[str]
    refund_policy: Optional[str]
    faq: List[FAQ]
    social_handles: List[str]
    contact_details: List[str]
    about_brand: Optional[str]
    important_links: List[str]
    success: bool = True
