import json
from hashlib import sha1
from typing import List

from duowen_agent.error import EmbeddingError
from duowen_agent.utils.cache import Cache
from openai import OpenAI


class OpenAIEmbedding:
    def __init__(self, base_url: str = 'https://api.openai.com/v1', model: str = 'text-embedding-ada-002',
                 api_key: str = 'xxx', timeout: float = 120, dimension: int = 1024, **kwargs):
        self.base_url = base_url
        self.model = model
        self.timeout = timeout
        self.api_key = api_key
        self.dimension = dimension
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url, timeout=self.timeout)

    def get_embedding(self, input_text: str | List[str]) -> List[List[float]]:
        if isinstance(input_text, list):
            _input_text = input_text
        elif isinstance(input_text, str):
            _input_text = [input_text]
        else:
            _input_text = [str(input_text)]

        try:
            _embeddings = self.client.embeddings.create(model=self.model, input=_input_text, timeout=self.timeout)
        except Exception as e:
            raise EmbeddingError(str(e), self.base_url, self.model)

        return [i.embedding for i in _embeddings.data]


class EmbeddingCache:
    def __init__(self, emb_cache: Cache, model_instance: OpenAIEmbedding, cache_ttl: int = 3600):
        self.emb_cache = emb_cache
        self.model_instance = model_instance
        self.cache_ttl = cache_ttl
        self.base_url = self.model_instance.base_url
        self.model = self.model_instance.model
        self.timeout = self.model_instance.timeout
        self.api_key = self.model_instance.api_key
        self.dimension = self.model_instance.dimension

    def _generate_key(self, question: str):
        return f"embed::{self.model_instance.model}::{sha1(question.encode()).hexdigest()}"

    def get_embedding(self, input_text: str | List[str], cache_ttl: int = None) -> List[List[float]]:
        """
        获取嵌入向量，首先检查缓存，如果缓存中不存在则调用模型生成并存入缓存

        :param input_text: 输入的文本或文本列表
        :param cache_ttl: 缓存时间，单位为秒，默认为3600秒（1小时）
        :return: 嵌入向量列表
        """
        if isinstance(input_text, str):
            questions = [input_text]
        else:
            questions = input_text

        if cache_ttl:
            _cache_ttl = cache_ttl
        elif self.cache_ttl:
            _cache_ttl = self.cache_ttl
        else:
            _cache_ttl = 3600

        embeddings = []
        uncached_questions = []
        cache_keys = [self._generate_key(question) for question in questions]
        cached_embeddings = self.emb_cache.mget(cache_keys)

        # 使用字典存储缓存和未缓存的嵌入向量
        embedding_dict = {}

        for question, cache_key, cached_embedding in zip(questions, cache_keys, cached_embeddings):
            if cached_embedding:
                # 如果缓存中存在，直接返回缓存的嵌入向量
                embedding_dict[question] = json.loads(cached_embedding)
            else:
                # 如果缓存中不存在，记录下来稍后生成嵌入向量
                uncached_questions.append(question)

        if uncached_questions:
            # 生成未缓存的嵌入向量
            new_embeddings = self.model_instance.get_embedding(uncached_questions)
            for question, embedding in zip(uncached_questions, new_embeddings):
                cache_key = self._generate_key(question)
                self.emb_cache.set(cache_key, json.dumps(embedding), _cache_ttl)
                embedding_dict[question] = embedding

        # 按照输入问题的顺序重新组合嵌入向量
        for question in questions:
            embeddings.append(embedding_dict[question])

        return embeddings
