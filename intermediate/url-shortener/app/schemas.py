from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime

class ShortenURLRequest(BaseModel):
    url: HttpUrl

class URLResponse(BaseModel):
    id: int
    url: str = Field(alias="original_url")
    short_code: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True, "populate_by_name": True}

class URLStatsResponse(URLResponse):
    access_count: int