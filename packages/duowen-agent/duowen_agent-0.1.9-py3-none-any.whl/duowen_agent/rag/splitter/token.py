from typing import List, Union

from duowen_agent.llm.tokenizer import tokenizer
from duowen_agent.rag.models import Document


class TokenChunker:

    def __init__(self, chunk_size: int = 512, chunk_overlap: Union[int, float] = 128):
        self.chunk_size = chunk_size
        self.chunk_overlap = (chunk_overlap if isinstance(chunk_overlap, int) else int(chunk_overlap * chunk_size))

    def chunk(self, text: str) -> List[Document]:

        if not text.strip():
            return []

        # Encode full text
        text_tokens = tokenizer.emb_encode(text)
        chunks = []

        # Calculate chunk positions
        start_indices = range(0, len(text_tokens), self.chunk_size - self.chunk_overlap)

        for start_idx in start_indices:
            # Get token indices for this chunk
            end_idx = min(start_idx + self.chunk_size, len(text_tokens))

            # Extract and decode tokens for this chunk
            chunk_tokens = text_tokens[start_idx:end_idx]
            chunk_text = tokenizer.emb_decode(chunk_tokens)

            chunks.append(Document(page_content=chunk_text, metadata=dict(start_index=start_idx, end_index=end_idx,
                                                                          token_count=len(chunk_tokens))))
            # Break if we've reached the end of the text
            if end_idx == len(text_tokens):
                break

        return chunks

    def __repr__(self) -> str:
        return (f"TokenChunker(chunk_size={self.chunk_size}, "
                f"chunk_overlap={self.chunk_overlap})")
