import math
from collections import Counter
from typing import Optional

import numpy as np

from duowen_agent.rag.datasource.keyword.jieba_keyword_table_handler import JiebaKeywordTableHandler
from duowen_agent.rag.datasource.vdb.vector_base import BaseVector
from duowen_agent.rag.models import Document
from duowen_agent.rag.rerank.entity import Weights


class WeightRerankRunner:
    def __init__(self, weights: Weights, vector: BaseVector) -> None:
        self.weights = weights
        self.vector = vector

    def run(self, query: str, documents: list[Document], score_threshold: Optional[float] = None,
            top_n: Optional[int] = None, ) -> list[Document]:
        """
        Run rerank model
        :param query: search query
        :param documents: documents for reranking
        :param score_threshold: score threshold
        :param top_n: top n
        :param user: unique user id if needed

        :return:
        """
        docs = []
        doc_id = []
        unique_documents = []
        for document in documents:
            if document.metadata["doc_id"] not in doc_id:
                doc_id.append(document.metadata["doc_id"])
                docs.append(document.page_content)
                unique_documents.append(document)

        documents = unique_documents

        rerank_documents = []
        query_scores = self._calculate_keyword_score(query, documents)

        query_vector_scores = self._calculate_cosine(query, documents)
        for document, query_score, query_vector_score in zip(documents, query_scores, query_vector_scores):
            # format document
            score = (self.weights.vector_weight * query_vector_score + self.weights.keyword_weight * query_score)
            if score_threshold and score < score_threshold:
                continue
            document.metadata["score"] = score
            rerank_documents.append(document)
        rerank_documents = sorted(rerank_documents, key=lambda x: x.metadata["score"], reverse=True)
        return rerank_documents[:top_n] if top_n else rerank_documents

    def _calculate_keyword_score(self, query: str, documents: list[Document]) -> list[float]:
        """
        Calculate BM25 scores
        :param query: search query
        :param documents: documents for reranking

        :return:
        """
        keyword_table_handler = JiebaKeywordTableHandler()
        query_keywords = keyword_table_handler.extract_keywords(query, None)
        documents_keywords = []
        for document in documents:
            # get the document keywords
            document_keywords = keyword_table_handler.extract_keywords(document.page_content, None)
            document.metadata["keywords"] = document_keywords
            documents_keywords.append(document_keywords)

        # Counter query keywords(TF)
        query_keyword_counts = Counter(query_keywords)

        # total documents
        total_documents = len(documents)

        # calculate all documents' keywords IDF
        all_keywords = set()
        for document_keywords in documents_keywords:
            all_keywords.update(document_keywords)

        keyword_idf = {}
        for keyword in all_keywords:
            # calculate include query keywords' documents
            doc_count_containing_keyword = sum(1 for doc_keywords in documents_keywords if keyword in doc_keywords)
            # IDF
            keyword_idf[keyword] = math.log((1 + total_documents) / (1 + doc_count_containing_keyword)) + 1

        query_tfidf = {}

        for keyword, count in query_keyword_counts.items():
            tf = count
            idf = keyword_idf.get(keyword, 0)
            query_tfidf[keyword] = tf * idf

        # calculate all documents' TF-IDF
        documents_tfidf = []
        for document_keywords in documents_keywords:
            document_keyword_counts = Counter(document_keywords)
            document_tfidf = {}
            for keyword, count in document_keyword_counts.items():
                tf = count
                idf = keyword_idf.get(keyword, 0)
                document_tfidf[keyword] = tf * idf
            documents_tfidf.append(document_tfidf)

        def cosine_similarity(vec1, vec2):
            intersection = set(vec1.keys()) & set(vec2.keys())
            numerator = sum(vec1[x] * vec2[x] for x in intersection)

            sum1 = sum(vec1[x] ** 2 for x in vec1)
            sum2 = sum(vec2[x] ** 2 for x in vec2)
            denominator = math.sqrt(sum1) * math.sqrt(sum2)

            if not denominator:
                return 0.0
            else:
                return float(numerator) / denominator

        similarities = []
        for document_tfidf in documents_tfidf:
            similarity = cosine_similarity(query_tfidf, document_tfidf)
            similarities.append(similarity)

        # for idx, similarity in enumerate(similarities):
        #     print(f"Document {idx + 1} similarity: {similarity}")

        return similarities

    def _calculate_cosine(self, query: str, documents: list[Document], ) -> list[float]:
        """
        Calculate Cosine scores
        :param query: search query
        :param documents: documents for reranking

        :return:
        """
        query_vector_scores = []
        query_vector = self.vector.query_to_embeding(query)
        for document in documents:
            # calculate cosine similarity
            # if "score" in document.metadata:
            #     query_vector_scores.append(document.metadata["score"])
            # else:
            # transform to NumPy
            vec1 = np.array(query_vector)
            vec2 = np.array(document.vector)

            # calculate dot product
            dot_product = np.dot(vec1, vec2)

            # calculate norm
            norm_vec1 = np.linalg.norm(vec1)
            norm_vec2 = np.linalg.norm(vec2)

            # calculate cosine similarity
            cosine_sim = dot_product / (norm_vec1 * norm_vec2)
            query_vector_scores.append(cosine_sim)

        return query_vector_scores


if __name__ == "__main__":
    weights = Weights(**{"vector_weight": 0.70, "keyword_weight": 0.3})
    wr = WeightRerankRunner(weights)

    query = "通信消费信息有哪些?"

    documents = [Document(**{
        "page_content": "该模型记录了广东省全品牌用户在指定月份内的通信消费信息，包括语音业务费、数业费用、固话费、G3上网本套餐费、G3上网本超出套餐流量费用等，以及通信计费时长和通信次数等业务统计信息。",
        "metadata": {"doc_id": 'aaaaa'}, })]

    wr.run(query, documents, 0.9, 10)
