from app.database import engine, Base
from app.models import ShortURL

def create_tables():
    Base.metadata.create_all(bind=engine)