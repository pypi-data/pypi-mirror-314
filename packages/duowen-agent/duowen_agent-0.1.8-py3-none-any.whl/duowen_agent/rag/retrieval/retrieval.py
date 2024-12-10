import threading
from typing import Optional, Any

from duowen_agent.llm.rerank_model import GeneralRerank
from duowen_agent.rag.datasource.vdb.vector_base import BaseVector
from duowen_agent.rag.models import Document
from duowen_agent.rag.rerank.entity import Weights
from duowen_agent.rag.retrieval.retrieval_service import RetrievalService


class Retrieval:
    def __init__(self, vector: BaseVector, rerank: GeneralRerank = None):
        self.vector = vector
        self.rerank_model = rerank

    def full_text_search(self, query: str, top_k: int = 10, score_threshold: Optional[float] = 0.0, filter: list = None,
                         _filter: dict = None):
        """全文检索"""
        results = RetrievalService.retrieve(query=query, top_k=top_k, vector=self.vector,
            retrieval_type="full_text_search", score_threshold=score_threshold, filter=filter, _filter=_filter)

        return results

    def semantic_search(self, query: str, top_k: int = 10, score_threshold: Optional[float] = 0.0, filter: list = None,
                        _filter: dict = None):
        """语义检索"""
        results = RetrievalService.retrieve(query=query, top_k=top_k, vector=self.vector,
            retrieval_type="semantic_search", score_threshold=score_threshold, filter=filter, _filter=_filter)

        return results

    def hybrid_search(self, query: str, top_k: int = 10, score_threshold: Optional[float] = 0.0,
                      vector_weight: float = 0.7, keyword_weight: float = 0.3, filter: list = None,
                      _filter: dict = None):
        """混合检索"""
        threads = []
        all_documents = []
        retrieval_thread = threading.Thread(target=RetrievalService._retriever,
            kwargs={"query": query, "top_k": top_k, "all_documents": all_documents, "vector": self.vector,
                "retrieval_type": "hybrid_search", "score_threshold": score_threshold, "filter": filter,
                "_filter": filter}, )
        threads.append(retrieval_thread)
        retrieval_thread.start()
        for thread in threads:
            thread.join()

        # 计算权重
        weights = Weights(**{"vector_weight": vector_weight, "keyword_weight": keyword_weight})
        docs = RetrievalService.retrieval_weights(query, all_documents, weights, self.vector, top_k, score_threshold)

        return docs

    def rerank(self, query: str, documents: list[Document], max_chunks_per_doc: int = 1000, overlap_tokens: int = 80,
               top_n: Any | None = None, threshold_score: Any | None = None, timeout: int = 10, max_retries: int = 3):
        if not self.rerank_model:
            raise ValueError("rerank模型不能为空")

        """rerank模型重排"""
        return RetrievalService.retrieval_rerank(self.rerank_model, query, documents,
                                                 max_chunks_per_doc=max_chunks_per_doc, overlap_tokens=overlap_tokens,
                                                 top_n=top_n, threshold_score=threshold_score, timeout=timeout,
                                                 max_retries=max_retries)

    def re_order(self, documents: list[Document]) -> list[Document]:
        """打乱顺序"""
        return RetrievalService.re_order(documents)

    def calculate_document_token(self, documents: list[Document], max_token):
        """计算docs token长度"""
        return RetrievalService.calculate_document_token(documents, max_token)
