from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://hotspot:hotspot123@db:5432/hotspotdb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
