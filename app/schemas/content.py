from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.models.content import SentimentEnum


class ContentCreate(BaseModel):
    text_body: str = Field(..., min_length=10, description="Content text to analyze")


class ContentResponse(BaseModel):
    id: int
    user_id: str
    text_body: str
    summary: Optional[str]
    sentiment: Optional[SentimentEnum]
    created_at: datetime
    
    class Config:
        from_attributes = True


class ContentListResponse(BaseModel):
    total: int
    contents: list[ContentResponse]
