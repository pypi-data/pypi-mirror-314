import logging
from typing import Any, Union, List
from urllib.parse import urlparse
import jieba, re
import requests
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from pydantic import BaseModel, model_validator

from duowen_agent.error import EmbeddingError
from duowen_agent.rag.datasource.vdb.elasticsearch.mapping import metadata_mapping
from duowen_agent.llm.embedding_model import OpenAIEmbedding, EmbeddingCache

from duowen_agent.rag.datasource.keyword.stopwords import STOPWORDS
from duowen_agent.rag.datasource.vdb.field import Field
from duowen_agent.rag.models import Document
from duowen_agent.rag.rerank.entity import VectorDocument
from duowen_agent.rag.datasource.vdb.vector_base import BaseVector
from os import getenv
from dotenv import load_dotenv

load_dotenv(verbose=True)


logger = logging.getLogger(__name__)


class ElasticSearchConfig(BaseModel):
    host: str
    port: int
    username: str = None
    password: str = None

    @model_validator(mode="before")
    @classmethod
    def validate_config(cls, values: dict) -> dict:
        if not values["host"]:
            raise ValueError("config HOST is required")
        if not values["port"]:
            raise ValueError("config PORT is required")
        # if not values["username"]:
        #     raise ValueError("config USERNAME is required")
        # if not values["password"]:
        #     raise ValueError("config PASSWORD is required")
        return values


class ElasticSearchVector(BaseVector):
    def __init__(self, config: ElasticSearchConfig,
                 embedding: Union[OpenAIEmbedding, EmbeddingCache],
                 index_name: str):
        super().__init__(index_name.lower())
        self._collection_name = index_name
        self._client = self._init_client(config)
        self._version = self._get_version()
        self._embeddings = embedding
        self.meta_mapping = metadata_mapping

    def _init_client(self, config: ElasticSearchConfig) -> Elasticsearch:
        try:
            parsed_url = urlparse(config.host)
            if parsed_url.scheme in {"http", "https"}:
                hosts = f"{config.host}:{config.port}"
            else:
                hosts = f"http://{config.host}:{config.port}"
            client = Elasticsearch(
                hosts=hosts,
                request_timeout=100000,
                retry_on_timeout=True,
                max_retries=10000,
            )
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Vector database connection error")

        return client

    def _get_version(self) -> str:
        info = self._client.info()
        return info["version"]["number"]

    def _check_version(self):
        if self._version < "8.0.0":
            raise ValueError("Elasticsearch vector database version must be greater than 8.0.0")

    def text_exists(self, id: str) -> bool:
        return bool(self._client.exists(index=self._collection_name, id=id))

    def delete_by_ids(self, ids: list[str]) -> None:
        for id in ids:
            self._client.delete(index=self._collection_name, id=id)

    def delete_by_metadata_field(self, key: str, value: str) -> None:
        query_str = {"query": {"match": {f"metadata.{key}": f"{value}"}}}
        results = self._client.search(index=self._collection_name, body=query_str)
        ids = [hit["_id"] for hit in results["hits"]["hits"]]
        if ids:
            self.delete_by_ids(ids)

    def delete(self) -> None:
        self._client.indices.delete(index=self._collection_name)

    def search_by_vector(self, query: str, **kwargs: Any) -> list[Document]:
        top_k = kwargs.get("top_k", 10)

        query_vector = self.query_to_embeding(query)

        field = f"{Field.VECTOR.value}_{self._embeddings.dimension}"
        _query = {
            "query": {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": f"cosineSimilarity(params.query_vector, '{field}') + 1.0",
                        "params": {
                            "query_vector": query_vector
                        }
                    }
                }
            }
        }
        query = {
            "query": {
                "bool": {
                    "must": [_query["query"]],
                    "filter": []
                }
            },
            "size": top_k
        }
        # 外部filter，完整的filter结构
        filter = kwargs.get('filter')
        # 自定义filter
        _filter = kwargs.get("_filter")
        if filter:
            query["query"]["bool"]["filter"] = filter
        elif _filter:
            for field, value in _filter.items():
                # 根据值的类型添加不同的过滤器
                if isinstance(value, list):
                    # 多个值，使用terms查询
                    query["query"]["bool"]["filter"].append({"terms": {field: value}})
                elif isinstance(value, dict):
                    # 字典类型，假设为范围查询
                    query["query"]["bool"]["filter"].append({"range": {field: value}})
                else:
                    # 单个值，使用term查询
                    query["query"]["bool"]["filter"].append({"term": {field: value}})

        results = self._client.search(index=self._collection_name, body=query)
        print("语义召回条数", len(results["hits"]["hits"]))
        docs_and_scores = []
        for hit in results["hits"]["hits"]:
            docs_and_scores.append(
                (
                    Document(
                        page_content=hit["_source"][Field.CONTENT.value],
                        vector=hit["_source"][field],
                        metadata=hit["_source"][Field.METADATA.value],
                        kb=hit["_source"].get('kb'),
                        label=hit["_source"].get('label'),
                        id=hit["_source"].get('id')
                    ),
                    hit["_score"],
                )
            )

        docs = []
        for doc, score in docs_and_scores:
            score_threshold = float(kwargs.get("score_threshold") or 0.0)

            if score > score_threshold:
                doc.metadata["score"] = score
            docs.append(doc)
        return docs

    @staticmethod
    def jieba_split(text):
        return " ".join(
            [i for i in jieba.cut_for_search(text) if re.match(r'[a-zA-Z0-9\u4e00-\u9fa5]', i) and i not in STOPWORDS])

    @staticmethod
    def query_jieba_split(text):
        ch_res = [i for i in jieba.lcut(text) if re.match(r'[a-zA-Z0-9\u4e00-\u9fa5]', i) and i not in STOPWORDS]

        # eng_res = [i for i in translate.trans(text) if i not in STOPWORDS]
        eng_res = []
        return " ".join(ch_res + eng_res)

    def search_by_full_text(self, query: str, **kwargs: Any) -> list[Document]:
        if query:
            query = self.rm_www(query)
            query_str = {"match": {Field.CONTENT_SPLIT.value: self.query_jieba_split(query)}}

            query = {
                "query": {
                    "bool": {
                        "must": [query_str],
                        "filter": []
                    }
                },
                "size": kwargs.get("top_k", 10)
            }

            _filter = kwargs.get('_filter')
            filter = kwargs.get("filter")
            if filter:
                query["query"]["bool"]["filter"] = filter
            elif _filter:
                for field, value in _filter.items():
                    # 根据值的类型添加不同的过滤器
                    if isinstance(value, list):
                        # 多个值，使用terms查询
                        query["query"]["bool"]["filter"].append({"terms": {field: value}})
                    elif isinstance(value, dict):
                        # 字典类型，假设为范围查询
                        query["query"]["bool"]["filter"].append({"range": {field: value}})
                    else:
                        # 单个值，使用term查询
                        query["query"]["bool"]["filter"].append({"term": {field: value}})
        else:
            query = {"query": {}}
            if kwargs.get("filter"):
                query["query"]["bool"] = {"filter": kwargs.get("filter")}
            else:
                query["query"]["match_all"] = {}


        results = self._client.search(index=self._collection_name, body=query)
        print("全文召回条数", len(results["hits"]["hits"]))

        docs = []
        vector_filed = f"{Field.VECTOR.value}_{self._embeddings.dimension}"
        for hit in results["hits"]["hits"]:
            docs.append(
                Document(
                    page_content=hit["_source"][Field.CONTENT.value],
                    vector=hit["_source"][vector_filed],
                    metadata=hit["_source"][Field.METADATA.value],
                    kb=hit["_source"].get('kb'),
                    label=hit["_source"].get('label'),
                    id=hit["_source"].get('id')
                )
            )

        return docs

    def create_collection(self):
        if not self._client.indices.exists(index=self._collection_name):
            self._client.indices.create(index=self._collection_name, body=self.meta_mapping)

    def add_vector_data(self, vector_data: dict) -> str:

        _vector = self._embeddings.get_embedding(vector_data["content"])[0]
        content_split = self.jieba_split(vector_data["content"])
        if not vector_data.get(Field.METADATA.value):
            vector_data[Field.METADATA.value] = {}
        vector_data[Field.METADATA.value]['doc_id'] = vector_data['id']

        _data = {}
        # 将其他数据添加塞到metadata中
        f_list = list(VectorDocument.__fields__.keys())
        for k, v in vector_data.items():
            if k not in f_list:
                vector_data["metadata"][k] = v
            else:
                _data[k] = v
        _data['metadata'] = vector_data['metadata']
        _data['content_split'] = content_split
        _data[f"{Field.VECTOR.value}_{self._embeddings.dimension}"] = _vector

        if self.text_exists(_data["id"]):
            self._client.update(index=self._collection_name,
                                id=_data["id"],
                                body={"doc": _data})
        else:
            self._client.index(index=self._collection_name, id=_data["id"], body=_data)

        return vector_data["id"]

    def batch_add_vector_data(self, vds: list[dict], batch_num=100):
        _batch_embedding = self.generate_batch_embedding([_i["content"].strip() for _i in vds])

        actions = []
        for index, vd in enumerate(vds):
            _vector = _batch_embedding[index]
            content_split = self.jieba_split(vd["content"])
            if not vd.get(Field.METADATA.value):
                vd[Field.METADATA.value] = {}
            vd[Field.METADATA.value]['doc_id'] = vd['id']
            _data = {}
            # 将其他数据添加塞到metadata中
            f_list = list(VectorDocument.__fields__.keys())
            for k, v in vd.items():
                if k not in f_list:
                    vd["metadata"][k] = v
                else:
                    _data[k] = v
            _data['metadata'] = vd['metadata']
            _data['content_split'] = content_split
            _data[f"{Field.VECTOR.value}_{self._embeddings.dimension}"] = _vector
            action = {
                "_index": self._collection_name,
                "_id": _data["id"],
                "_source": _data
            }
            actions.append(action)

            if len(actions) >= batch_num:
                bulk(self._client, action)
                actions = []

        if actions:
            bulk(self._client, actions)
        self.refresh()
        return [doc['id'] for doc in vds]

    def refresh(self):
        """手动刷新索引"""
        self._client.indices.refresh(index=self._collection_name)

    def get_datas_by_ids(self, ids: list[str], size=1000):
        query = {
            "query": {
                "bool": {
                    "filter": [
                        {"terms": {"id": ids}}
                    ]
                }
            }
        }

        return self._client.search(index=self._collection_name, body=query, size=size)

    def rm_www(self, txt):
        patts = [
            (r"是*(什么样的|哪家|一下|那家|请问|啥样|咋样了|什么时候|何时|何地|何人|是否|是不是|多少|哪里|怎么|哪儿|怎么样|如何|哪些|是啥|啥是|啊|吗|呢|吧|咋|什么|有没有|呀)是*",""),
            (r"(^| )(what|who|how|which|where|why)('re|'s)? ", " "),
            (r"(^| )('s|'re|is|are|were|was|do|does|did|don't|doesn't|didn't|has|have|be|there|you|me|your|my|mine|just|please|may|i|should|would|wouldn't|will|won't|done|go|for|with|so|the|a|an|by|i'm|it's|he's|she's|they|they're|you're|as|by|on|in|at|up|out|down|of) "," ")
        ]
        for r, p in patts:
            txt = re.sub(r, p, txt, flags=re.IGNORECASE)
        return txt

    def update_by_query(self, update_query: dict):
        return self._client.update_by_query(index=self._collection_name, body=update_query)

    def delete_by_query(self, query: dict):

        return self._client.delete_by_query(index=self._collection_name, body=query)

    def query_to_embeding(self, query: str) -> list[float]:
        return self._embeddings.get_embedding(query)[0]

    def generate_batch_embedding(self, data: List[str], **kwargs) -> List[List[float]]:
        try:
            return self._embeddings.get_embedding(data)
        except Exception as e:
            raise EmbeddingError(msg=str(e), base_url=self._embeddings.base_url, model_name=self._embeddings.model_name)


class ESVector:

    def __init__(self, embedding: Union[OpenAIEmbedding, EmbeddingCache],
                 index_name: str):
        self.index_name = index_name
        self.embedding = embedding

    def init_vector(self) -> ElasticSearchVector:

        return ElasticSearchVector(
            config=ElasticSearchConfig(
                host=getenv("ES_HOST"),
                port=getenv("ES_PORT"),
                username=getenv("ES_USERNAME"),
                password=getenv("ES_PASSWORD")
            ),
            embedding=self.embedding,
            index_name=self.index_name
        )


