from sqlalchemy import (
    create_engine, Column, String, Text, ForeignKey, Integer
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

DB_USER = 'root'
DB_PASSWORD = 'khan'
DB_HOST = 'localhost'
DB_PORT = 3306
DB_NAME ='shopify_insights'

print("Successfully connected!")


Base = declarative_base()

class Brand(Base):
    __tablename__ = 'brands'
    id = Column(Integer, primary_key=True, autoincrement=True)
    brand_name = Column(String(255))
    website_url = Column(String(255), unique=True)
    privacy_policy = Column(Text, nullable=True)
    return_policy = Column(Text, nullable=True)
    refund_policy = Column(Text, nullable=True)
    about_brand = Column(Text, nullable=True)

    products = relationship('Product', back_populates='brand', cascade="all, delete-orphan")
    hero_products = relationship('HeroProduct', back_populates='brand', cascade="all, delete-orphan")
    faqs = relationship('FAQ', back_populates='brand', cascade="all, delete-orphan")
    social_handles = relationship('SocialHandle', back_populates='brand', cascade="all, delete-orphan")
    contact_details = relationship('ContactDetail', back_populates='brand', cascade="all, delete-orphan")
    important_links = relationship('ImportantLink', back_populates='brand', cascade="all, delete-orphan")

class Product(Base):
    __tablename__ = 'products'
    id = Column(String(64), primary_key=True)
    title = Column(String(255))
    url = Column(String(255), nullable=True)
    price = Column(String(64), nullable=True)
    image = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    brand_id = Column(Integer, ForeignKey('brands.id'))
    brand = relationship("Brand", back_populates="products")

class HeroProduct(Base):
    __tablename__ = 'hero_products'
    id = Column(String(64), primary_key=True)
    title = Column(String(255))
    url = Column(String(255), nullable=True)
    price = Column(String(64), nullable=True)
    image = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    brand_id = Column(Integer, ForeignKey('brands.id'))
    brand = relationship("Brand", back_populates="hero_products")

class FAQ(Base):
    __tablename__ = 'faqs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(Text)
    answer = Column(Text)
    brand_id = Column(Integer, ForeignKey('brands.id'))
    brand = relationship("Brand", back_populates="faqs")

class SocialHandle(Base):
    __tablename__ = 'social_handles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    handle = Column(String(255))
    brand_id = Column(Integer, ForeignKey('brands.id'))
    brand = relationship("Brand", back_populates="social_handles")

class ContactDetail(Base):
    __tablename__ = 'contact_details'
    id = Column(Integer, primary_key=True, autoincrement=True)
    detail = Column(String(255))
    brand_id = Column(Integer, ForeignKey('brands.id'))
    brand = relationship("Brand", back_populates="contact_details")

class ImportantLink(Base):
    __tablename__ = 'important_links'
    id = Column(Integer, primary_key=True, autoincrement=True)
    link = Column(String(255))
    brand_id = Column(Integer, ForeignKey('brands.id'))
    brand = relationship("Brand", back_populates="important_links")

def get_engine():
    # Update this connection string with your MySQL credentials
    # Use the PyMySQL driver which is better supported on Windows (install with: pip install pymysql)
    return create_engine(
        'mysql+pymysql://root:khan@localhost:3306/shopify_insights',
        echo=True,
        future=True
    )

SessionLocal = sessionmaker(bind=get_engine(), autoflush=False, autocommit=False)

def init_db():
    engine = get_engine()
    Base.metadata.create_all(engine)
