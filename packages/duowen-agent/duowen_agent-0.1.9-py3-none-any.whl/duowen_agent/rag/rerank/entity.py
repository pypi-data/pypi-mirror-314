from typing import Optional

from pydantic import BaseModel


class VectorDocument(BaseModel):
    id: str
    content: str
    metadata: dict = {}
    kb: Optional[list] = None
    label: Optional[list] = None
    content_split: str = None
    vector_384: list = None
    vector_512: list = None
    vector_768: list = None
    vector_1024: list = None
    vector_1536: list = None


class VectorSetting(BaseModel):
    vector_weight: float


class KeywordSetting(BaseModel):
    keyword_weight: float


class Weights(BaseModel):
    """Model for weighted rerank."""
    vector_weight: float
    keyword_weight: float
