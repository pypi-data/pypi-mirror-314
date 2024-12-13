import threading
import traceback
from typing import Optional, Any

from duowen_agent.llm.rerank_model import GeneralRerank
from duowen_agent.llm.tokenizer import tokenizer
from duowen_agent.rag.datasource.vdb.vector_base import BaseVector
from duowen_agent.rag.models import Document
from duowen_agent.rag.rerank.entity import Weights
from duowen_agent.rag.rerank.weight_rerank import WeightRerankRunner


class RetrievalService:
    @classmethod
    def retrieve(
        cls,
        query: str,
        top_k: int,
        vector: BaseVector,
        retrieval_type: str = "full_text_search",
        score_threshold: Optional[float] = 0.0,
        filter: list = None,
        _filter: dict = None,
    ):
        all_documents = []
        threads = []
        exceptions = []

        if retrieval_type in ["semantic_search", "hybrid_search"]:
            embedding_thread = threading.Thread(
                target=RetrievalService.embedding_search,
                kwargs={
                    "query": query,
                    "top_k": top_k,
                    "vector": vector,
                    "score_threshold": score_threshold,
                    "all_documents": all_documents,
                    "exceptions": exceptions,
                    "filter": filter,
                    "_filter": _filter,
                },
            )
            threads.append(embedding_thread)
            embedding_thread.start()

        if retrieval_type in ["full_text_search", "hybrid_search"]:
            full_text_index_thread = threading.Thread(
                target=RetrievalService.full_text_index_search,
                kwargs={
                    "query": query,
                    "top_k": top_k,
                    "vector": vector,
                    "score_threshold": score_threshold,
                    "all_documents": all_documents,
                    "exceptions": exceptions,
                    "filter": filter,
                    "_filter": _filter,
                },
            )
            threads.append(full_text_index_thread)
            full_text_index_thread.start()

        for thread in threads:
            thread.join()

        if exceptions:
            exception_message = ";\n".join(exceptions)
            raise Exception(exception_message)

        return all_documents

    @classmethod
    def _retriever(
        cls,
        query: str,
        top_k: int,
        all_documents: list,
        vector: BaseVector,
        retrieval_type: str = "hybrid_search",
        score_threshold: Optional[float] = 0.0,
        filter: list = None,
        _filter: dict = None,
    ):
        if top_k > 0:
            documents = cls.retrieve(
                query=query,
                top_k=top_k,
                vector=vector,
                retrieval_type=retrieval_type,
                score_threshold=score_threshold,
                filter=filter,
                _filter=_filter,
            )

            all_documents.extend(documents)

    @classmethod
    def embedding_search(
        cls,
        query: str,
        top_k: int,
        score_threshold: Optional[float],
        all_documents: list,
        exceptions: list,
        vector: BaseVector,
        filter: list = None,
        _filter: dict = None,
    ):
        try:
            documents = vector.search_by_vector(
                cls.escape_query_for_search(query),
                search_type="similarity_score_threshold",
                top_k=top_k,
                score_threshold=score_threshold,
                filter=filter,
                _filter=_filter,
            )

            if documents:
                all_documents.extend(documents)
        except Exception as e:
            print(traceback.format_exc())
            exceptions.append(str(e))

    @classmethod
    def full_text_index_search(
        cls,
        query: str,
        top_k: int,
        vector: BaseVector,
        all_documents: list,
        exceptions: list,
        score_threshold: float = 0.0,
        filter: list = None,
        _filter: dict = None,
    ):
        try:
            documents = vector.search_by_full_text(
                cls.escape_query_for_search(query),
                top_k=top_k,
                filter=filter,
                _filter=_filter,
            )

            if documents:
                all_documents.extend(documents)
        except Exception as e:
            print(traceback.format_exc())
            exceptions.append(str(e))

    @staticmethod
    def escape_query_for_search(query: str) -> str:
        return query.replace('"', '\\"')

    @staticmethod
    def text_rerank(
        rerank: GeneralRerank,
        query: str,
        docs: list,
        max_chunks_per_doc: int = 1000,
        overlap_tokens: int = 80,
        top_n: Any = None,
        threshold_score: Any = None,
        timeout: int = 10,
        max_retries: int = 3,
    ):
        # 切片重排
        return rerank.rerank(
            query=query,
            documents=docs,
            max_chunks_per_doc=max_chunks_per_doc,
            overlap_tokens=overlap_tokens,
            top_n=top_n,
            threshold_score=threshold_score,
            timeout=timeout,
            max_retries=max_retries,
        )

    @staticmethod
    def retrieval_weights(
        query: str,
        documents: list[Document],
        weights: Weights,
        vector: BaseVector,
        top_n: int,
        score_threshold: float = 0.0,
    ):
        # 计算权重
        weight_ranner = WeightRerankRunner(weights, vector)
        docs = weight_ranner.run(query, documents, score_threshold, top_n)

        return docs

    @staticmethod
    def retrieval_rerank(
        rerank: GeneralRerank,
        query: str,
        documents: list[Document],
        max_chunks_per_doc: int = 1000,
        overlap_tokens: int = 80,
        top_n: Any | None = None,
        threshold_score: Any | None = None,
        timeout: int = 10,
        max_retries: int = 3,
    ) -> list[Document]:

        # rerank 模型重排
        contents = []
        for document in documents:
            contents.append(document.page_content)

        rerank_result = RetrievalService.text_rerank(
            rerank,
            query,
            contents,
            max_chunks_per_doc=max_chunks_per_doc,
            overlap_tokens=overlap_tokens,
            top_n=top_n,
            threshold_score=threshold_score,
            timeout=timeout,
            max_retries=max_retries,
        )

        rerank_documents = []
        for rst in rerank_result:
            rerank_document = Document(
                id=documents[rst["index"]].id,
                page_content=contents[rst["index"]],
                metadata=documents[rst["index"]].metadata,
                kb=documents[rst["index"]].kb,
                label=documents[rst["index"]].label,
            )
            rerank_document.metadata["score"] = rst["relevance_score"]
            rerank_documents.append(rerank_document)

        return rerank_documents

    @staticmethod
    def re_order(documents: list[Document]) -> list[Document]:
        # Retrieve elements from odd indices (0, 2, 4, etc.) of the documents list
        odd_elements = documents[::2]

        # Retrieve elements from even indices (1, 3, 5, etc.) of the documents list
        even_elements = documents[1::2]

        # Reverse the list of elements from even indices
        even_elements_reversed = even_elements[::-1]

        new_documents = odd_elements + even_elements_reversed

        return new_documents

    @staticmethod
    def calculate_document_token(documents: list[Document], max_token):
        current_s = ""
        index = 0
        if len(documents) > 0:
            if tokenizer.chat_len(documents[0].page_content) > max_token:
                raise ValueError(f"第一条召回数据token长度超过{max_token}")

        for i in documents:
            if tokenizer.chat_len(current_s + i.page_content) > max_token:
                break
            else:
                current_s = current_s + i.page_content
            index = index + 1

        return documents[:index]
