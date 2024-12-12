metadata_mapping = {
    "settings": {
        "index": {
            "number_of_shards": 2,
            "number_of_replicas": 0,
            "refresh_interval": "1000ms",
        }
    },
    "mappings": {
        "properties": {
            "id": {"type": "keyword", "store": "true"},
            "content": {"type": "text", "index": "false", "store": "true"},  # 文档内容
            "metadata": {
                "type": "object",
                "properties": {},
                "dynamic": "true",
                "enabled": "true",
            },
            "content_split": {  # 文档内容分词(jieba)  eg: 中 国
                "type": "text",
                "analyzer": "whitespace",
                "store": "true",
            },
            "kb": {  # 知识库 ['xxxx'， 'xxxxxx']
                "type": "keyword",
                "store": "true",
                "index": "true",
            },
            "label": {  # 标签  ['xxx', 'xxx']
                "type": "keyword",
                "store": "true",
                "index": "true",
            },
            "vector_384": {
                "type": "dense_vector",
                "dims": 384,
                "index": "true",
                "similarity": "cosine",
            },
            "vector_512": {
                "type": "dense_vector",
                "dims": 512,
                "index": "true",
                "similarity": "cosine",
            },
            "vector_768": {
                "type": "dense_vector",
                "dims": 768,
                "index": "true",
                "similarity": "cosine",
            },
            "vector_1024": {
                "type": "dense_vector",
                "dims": 1024,
                "index": "true",
                "similarity": "cosine",
            },
            "vector_1536": {
                "type": "dense_vector",
                "dims": 1536,
                "index": "true",
                "similarity": "cosine",
            },
        },
        "date_detection": "true",
        "dynamic_templates": [
            {
                "metadata_int": {
                    "path_match": "metadata.*_int",
                    "match_mapping_type": "long",
                    "mapping": {"type": "integer", "store": "true"},
                }
            },
            {
                "metadata_ulong": {
                    "path_match": "metadata.*_ulong",
                    "match_mapping_type": "long",
                    "mapping": {"type": "unsigned_long", "store": "true"},
                }
            },
            {
                "metadata_long": {
                    "path_match": "metadata.*_long",
                    "match_mapping_type": "long",
                    "mapping": {"type": "long", "store": "true"},
                }
            },
            {
                "metadata_short": {
                    "path_match": "metadata.*_short",
                    "match_mapping_type": "long",
                    "mapping": {"type": "short", "store": "true"},
                }
            },
            {
                "metadata_numeric": {
                    "path_match": "metadata._flt",
                    "match_mapping_type": "double",
                    "mapping": {"type": "float", "store": "true"},
                }
            },
            {
                "metadata_kwd": {
                    "match_pattern": "regex",
                    "path_match": "^metadata\\..*(_kwd|id|uid)$",
                    "match_mapping_type": "string",
                    "mapping": {
                        "type": "keyword",
                        "similarity": "boolean",
                        "store": "true",
                    },
                }
            },
            {
                "metadata_dt": {
                    "match_pattern": "regex",
                    "path_match": "^metadata\\..*_(at|dt|time|date)$",
                    "match_mapping_type": "string",
                    "mapping": {
                        "type": "date",
                        "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||yyyy-MM-dd_HH:mm:ss",
                        "store": "true",
                    },
                }
            },
            {
                "metadata_nested": {
                    "path_match": "metadata.*_nst",
                    "match_mapping_type": "object",
                    "mapping": {"type": "nested"},
                }
            },
            {
                "metadata_object": {
                    "path_match": "metadata.*_obj",
                    "match_mapping_type": "object",
                    "mapping": {"type": "object", "dynamic": "true"},
                }
            },
            {
                "metadata_string": {
                    "path_match": "metadata.*_str",
                    "match_mapping_type": "string",
                    "mapping": {"type": "text", "index": "false", "store": "true"},
                }
            },
        ],
    },
}
