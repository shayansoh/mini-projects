import random
import string
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repository import URLRepository
from app.models import ShortURL

class URLService:
    SHORT_CODE_LENGTH = 6
    SHORT_CODE_CHARS = string.ascii_letters + string.digits

    def __init__(self, db: Session):
        self.repo = URLRepository(db)

    def _generate_short_code(self) -> str:
        while True:
            code = "".join(
                random.choices(self.SHORT_CODE_CHARS, k=self.SHORT_CODE_LENGTH)
            )
            if not self.repo.get_by_short_code(code):
                return code

    def _get_or_raise(self, short_code: str) -> ShortURL:
        record = self.repo.get_by_short_code(short_code)
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Short code '{short_code}' not found"
            )
        return record

    def create_short_url(self, original_url: str) -> ShortURL:
        existing = self.repo.get_by_original_url(original_url)
        if existing:
            return existing
        short_code = self._generate_short_code()
        return self.repo.create(original_url, short_code)

    def get_short_url(self, short_code: str) -> ShortURL:
        record = self._get_or_raise(short_code)
        self.repo.increment_access_count(record)
        return record

    def update_short_url(self, short_code: str, new_url: str) -> ShortURL:
        record = self._get_or_raise(short_code)
        return self.repo.update(record, new_url)

    def delete_short_url(self, short_code: str) -> None:
        record = self._get_or_raise(short_code)
        self.repo.delete(record)

    def get_stats(self, short_code: str) -> ShortURL:
        return self._get_or_raise(short_code)