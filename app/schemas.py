from pydantic import BaseModel
from typing import Optional

class DocumentCreate(BaseModel):
    title: str
    text: str   # matches your ingest body {"title": "...", "text": "..."}

class QueryRequest(BaseModel):
    question: str
    top_k: Optional[int] = 5