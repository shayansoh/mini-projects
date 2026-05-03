from sqlalchemy.orm import Session
from app.models import ShortURL

class URLRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_short_code(self, short_code: str) -> ShortURL | None:
        return (
            self.db.query(ShortURL)
            .filter(ShortURL.short_code == short_code)
            .first()
        )

    def get_by_original_url(self, original_url: str) -> ShortURL | None:
        return (
            self.db.query(ShortURL)
            .filter(ShortURL.original_url == original_url)
            .first()
        )

    def create(self, original_url: str, short_code: str) -> ShortURL:
        record = ShortURL(original_url=original_url, short_code=short_code)
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def update(self, record: ShortURL, new_url: str) -> ShortURL:
        record.original_url = new_url
        self.db.commit()
        self.db.refresh(record)
        return record

    def delete(self, record: ShortURL) -> None:
        self.db.delete(record)
        self.db.commit()

    def increment_access_count(self, record: ShortURL) -> None:
        record.access_count += 1
        self.db.commit()