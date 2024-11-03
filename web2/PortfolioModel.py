# models.py
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database setup
DATABASE_URL = "sqlite:///./portfolio.db"  # SQLite database file named portfolio.db

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the Portfolio model for SQLAlchemy
class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)  # User ID
    name = Column(String, index=True)
    description = Column(String)
    file_path = Column(String, index=True)  # Path to the uploaded file

# Create the database tables
Base.metadata.create_all(bind=engine)
