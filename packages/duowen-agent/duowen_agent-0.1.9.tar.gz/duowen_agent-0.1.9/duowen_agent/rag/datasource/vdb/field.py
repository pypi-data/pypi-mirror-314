from enum import Enum


class Field(Enum):
    # CONTENT_KEY = "page_content"
    CONTENT_SPLIT = "content_split"
    METADATA = "metadata"
    VECTOR = "vector"
    CONTENT = "content"
    PRIMARY_KEY = "id"    # doc_id
    LABEL = 'label'
    KB = 'kb'
    DOC_ID = "metadata.doc_id"
    FILE_ID = "metadata.file_id"

