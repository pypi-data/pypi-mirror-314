# 多闻(duowen)语言模型工具包

LLM核心开发包

## 模型

### 语言模型

```python
from duowen_agent.llm import OpenAIChat
from os import getenv

llm_cfg = {"model": "THUDM/glm-4-9b-chat", "base_url": "https://api.siliconflow.cn/v1",
           "api_key": getenv("SILICONFLOW_API_KEY")}

_llm = OpenAIChat(**llm_cfg)

print(_llm.chat('''If you are here, please only reply "1".'''))

for i in _llm.chat_for_stream('''If you are here, please only reply "1".'''):
    print(i)

```

### 嵌入模型

#### 调用

```python
from duowen_agent.llm import OpenAIEmbedding
from os import getenv

emb_cfg = {"model": "BAAI/bge-large-zh-v1.5", "base_url": "https://api.siliconflow.cn/v1",
           "api_key": getenv("SILICONFLOW_API_KEY")}

_emb = OpenAIEmbedding(**emb_cfg)
print(_emb.get_embedding('123'))
print(_emb.get_embedding(['123', '456']))
```

#### 缓存

```python
from duowen_agent.llm import OpenAIEmbedding, EmbeddingCache
from os import getenv
from duowen_agent.utils.cache import Cache
from redis import StrictRedis
from typing import List, Optional, Any

emb_cfg = {"model": "BAAI/bge-large-zh-v1.5", "base_url": "https://api.siliconflow.cn/v1",
           "api_key": getenv("SILICONFLOW_API_KEY")}

_emb = OpenAIEmbedding(**emb_cfg)

redis = StrictRedis(host='127.0.0.1', port=6379)


class RedisCache(Cache):
    # 基于Cache 接口类实现  redis缓存
    def __init__(self, redis_cli: StrictRedis):
        self.redis_cli = redis_cli
        super().__init__()

    def set(self, key, value, expire=60):
        return self.redis_cli.set(key, value, ex=expire)

    def mget(self, keys: List[str]) -> List[Optional[Any]]:
        return self.redis_cli.mget(keys)

    def get(self, key: str) -> Optional[Any]:
        return self.redis_cli.get(key)

    def delete(self, key: str):
        return self.redis_cli.delete(key)

    def exists(self, key: str) -> bool:
        return self.redis_cli.exists(key)

    def clear(self):
        raise InterruptedError("不支持")


embedding_cache = EmbeddingCache(RedisCache(redis), _emb)
print(embedding_cache.get_embedding('hello world'))
for i in embedding_cache.get_embedding(['sadfasf', 'hello world']):
    print(i)
```

## 重排
```python
from duowen_agent.llm import GeneralRerank
from os import getenv
import tiktoken

rerank_cfg = {
    "model": "BAAI/bge-reranker-v2-m3", 
    "base_url": "https://api.siliconflow.cn/v1/rerank",
    "api_key": getenv("SILICONFLOW_API_KEY")}

rerank = GeneralRerank(
    model=rerank_cfg["model"], 
    api_key=rerank_cfg["api_key"],
    base_url=rerank_cfg["base_url"], 
    encoding=tiktoken.get_encoding("o200k_base")
)

data = rerank.rerank(query='Apple', documents=["苹果", "香蕉", "水果", "蔬菜"], top_n=3)
for i in data:
    print(i)
```
