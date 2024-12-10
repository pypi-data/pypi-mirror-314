from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from duowen_agent.rag.models import Document


class BaseVector(ABC):
    def __init__(self, collection_name: str):
        self._collection_name = collection_name

    @abstractmethod
    def text_exists(self, id: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def delete_by_ids(self, ids: list[str]) -> None:
        raise NotImplementedError

    def get_ids_by_metadata_field(self, key: str, value: str):
        raise NotImplementedError

    @abstractmethod
    def delete_by_metadata_field(self, key: str, value: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def search_by_vector(self, query: str, **kwargs: Any) -> list[Document]:
        raise NotImplementedError

    @abstractmethod
    def search_by_full_text(self, query: str, **kwargs: Any) -> list[Document]:
        raise NotImplementedError

    @abstractmethod
    def add_vector_data(self, vector_data: dict):
        raise NotImplementedError

    @abstractmethod
    def batch_add_vector_data(self, vds: list[dict], batch_num: int=100):
        raise NotImplementedError

    @abstractmethod
    def get_datas_by_ids(self, ids: list[str], size=1000):
        raise NotImplementedError

    @abstractmethod
    def delete(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def create_collection(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def query_to_embeding(self, query: str) -> list[float]:
        raise NotImplementedError

    @abstractmethod
    def update_by_query(self, update_query: dict):
        raise NotImplementedError

    @abstractmethod
    def delete_by_query(self, query: dict):
        raise NotImplementedError

    def _filter_duplicate_texts(self, texts: list[Document]) -> list[Document]:
        for text in texts.copy():
            doc_id = text.metadata["doc_id"]
            exists_duplicate_node = self.text_exists(doc_id)
            if exists_duplicate_node:
                texts.remove(text)

        return texts

    @property
    def collection_name(self):
        return self._collection_name
