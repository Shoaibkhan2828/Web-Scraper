from db import (
    Brand, Product, HeroProduct, FAQ, SocialHandle, ContactDetail, ImportantLink, SessionLocal
)
from models import BrandContext
from sqlalchemy.exc import IntegrityError

def save_brand_context(context: BrandContext) -> int:
    session = SessionLocal()
    try:
        # Remove existing brand entry to avoid duplicates
        existing_brand = session.query(Brand).filter_by(website_url=str(context.website_url)).first()
        if existing_brand:
            session.delete(existing_brand)
            session.commit()

        # Create new brand record
        brand = Brand(
            brand_name=context.brand_name,
            website_url=str(context.website_url),
            privacy_policy=context.privacy_policy,
            return_policy=context.return_policy,
            refund_policy=context.refund_policy,
            about_brand=context.about_brand
        )
        session.add(brand)
        session.commit()  # Commit to get brand.id for FK references

        # Save products
        unique_products = {prod.id: prod for prod in context.product_catalog}.values()
        for prod in unique_products:
            existing_product = session.get(Product, prod.id)
            if existing_product:
                # Update fields if needed
                existing_product.title = prod.title
                existing_product.url = prod.url
                existing_product.price = prod.price
                existing_product.image = prod.image
                existing_product.description = prod.description
                existing_product.brand_id = brand.id
            else:
                p = Product(
                    id=prod.id,
                    title=prod.title,
                    url=prod.url,
                    price=prod.price,
                    image=prod.image,
                    description=prod.description,
                    brand_id=brand.id
                )
                session.add(p)

        # Save hero products with deduplication and check
        unique_hero_products = {hero.id: hero for hero in context.hero_products}.values()
        for hero in unique_hero_products:
            existing_hero = session.get(HeroProduct, hero.id)
            if existing_hero:
                existing_hero.title = hero.title
                existing_hero.url = hero.url
                existing_hero.price = hero.price
                existing_hero.image = hero.image
                existing_hero.description = hero.description
                existing_hero.brand_id = brand.id
            else:
                h = HeroProduct(
                    id=hero.id,
                    title=hero.title,
                    url=hero.url,
                    price=hero.price,
                    image=hero.image,
                    description=hero.description,
                    brand_id=brand.id
                )
                session.add(h)

        # FAQs
        for faq in context.faq:
            existing_faq = session.query(FAQ).filter_by(
                question=faq.question, answer=faq.answer, brand_id=brand.id
            ).first()
            if not existing_faq:
                f = FAQ(
                    question=faq.question,
                    answer=faq.answer,
                    brand_id=brand.id
                )
                session.add(f)

        # Social handles (deduplicate)
        unique_socials = set(context.social_handles)
        for s in unique_socials:
            existing_s = session.query(SocialHandle).filter_by(handle=s, brand_id=brand.id).first()
            if not existing_s:
                sh = SocialHandle(handle=s, brand_id=brand.id)
                session.add(sh)

        # Contact details (deduplicate)
        unique_contacts = set(context.contact_details)
        for c in unique_contacts:
            existing_c = session.query(ContactDetail).filter_by(detail=c, brand_id=brand.id).first()
            if not existing_c:
                cd = ContactDetail(detail=c, brand_id=brand.id)
                session.add(cd)

        # Important links (deduplicate)
        unique_links = set(context.important_links)
        for l in unique_links:
            existing_l = session.query(ImportantLink).filter_by(link=l, brand_id=brand.id).first()
            if not existing_l:
                il = ImportantLink(link=l, brand_id=brand.id)
                session.add(il)

        session.commit()
        return brand.id

    except IntegrityError as e:
        session.rollback()
        raise e
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
