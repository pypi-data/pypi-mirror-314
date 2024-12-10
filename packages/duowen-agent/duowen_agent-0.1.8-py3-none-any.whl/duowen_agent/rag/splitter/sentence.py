from bisect import bisect_left
from itertools import accumulate
from typing import List, Union

from duowen_agent.llm.tokenizer import tokenizer
from duowen_agent.rag.models import Document


class SentenceChunker:
    """
    SentenceChunker splits the sentences in a text based on token limits and sentence boundaries.

    Args:
        chunk_size: Maximum number of tokens per chunk
        chunk_overlap: Number of tokens to overlap between chunks
        min_sentences_per_chunk: Minimum number of sentences per chunk (defaults to 1)

    Raises:
        ValueError: If parameters are invalid
    """

    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 128, min_sentences_per_chunk: int = 1,
                 min_chunk_size: int = 2, use_approximate: bool = True,
                 delim: Union[str, List[str]] = [".", "。", "!", "！", "?", "？", "\n"]):
        """Initialize the SentenceChunker with configuration parameters.

        SentenceChunker splits the sentences in a text based on token limits and sentence boundaries.

        Args:
            tokenizer: The tokenizer instance to use for encoding/decoding
            chunk_size: Maximum number of tokens per chunk
            chunk_overlap: Number of tokens to overlap between chunks
            min_sentences_per_chunk: Minimum number of sentences per chunk (defaults to 1)
            min_chunk_size: Minimum number of tokens per sentence (defaults to 2)
            use_approximate: Whether to use approximate token counting (defaults to True)

        Raises:
            ValueError: If parameters are invalid

        """

        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive")
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be less than chunk_size")
        if min_sentences_per_chunk < 1:
            raise ValueError("min_sentences_per_chunk must be at least 1")
        if min_chunk_size < 1:
            raise ValueError("min_chunk_size must be at least 1")

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.min_sentences_per_chunk = min_sentences_per_chunk
        self.min_chunk_size = min_chunk_size
        self.use_approximate = use_approximate
        self.delim = delim
        self.sep = "🦛"

    def _split_sentences(self, text: str) -> List[str]:
        """Fast sentence splitting while maintaining accuracy.

        This method is faster than using regex for sentence splitting and is more accurate than using the spaCy sentence tokenizer.

        Args:
            text: Input text to be split into sentences

        Returns:
            List of sentences

        """
        t = text
        for c in self.delim:
            t = t.replace(c, c + self.sep)

        # Initial split
        splits = [s for s in t.split(self.sep) if s != ""]
        # print(splits)

        # Combine short splits with previous sentence
        sentences = []
        current = ""

        for s in splits:
            if len(s.strip()) < (self.min_chunk_size * 6):
                current += s
            else:
                if current:
                    sentences.append(current)
                current = s

        if current:
            sentences.append(current)

        return sentences

    def _get_token_counts(self, sentences: List[str]) -> List[int]:
        """Get token counts for a list of sentences in batch.

        Args:
            sentences: List of sentences

        Returns:
            List of token counts for each sentence

        """
        # Batch encode all sentences at once
        encoded_sentences = self._encode_batch(sentences)
        return [len(encoded) for encoded in encoded_sentences]

    def _estimate_token_counts(self, text: str) -> int:
        """Estimate token count using character length."""
        CHARS_PER_TOKEN = 6.0  # Avg. char per token for llama3 is b/w 6-7
        if type(text) is str:
            return max(1, int(len(text) / CHARS_PER_TOKEN))
        elif type(text) is list and type(text[0]) is str:
            return [max(1, int(len(t) / CHARS_PER_TOKEN)) for t in text]
        else:
            raise ValueError(f"Unknown type passed to _estimate_token_count: {type(text)}")

    def _get_feedback(self, estimate: int, actual: int) -> float:
        """Validate against the actual token counts and correct the estimates."""
        feedback = 1 - ((estimate - actual) / estimate)
        return feedback

    def _prepare_sentences(self, text: str) -> List[Document]:
        """Prepare sentences with either estimated or accurate token counts."""
        # Split text into sentences
        sentence_texts = self._split_sentences(text)
        if not sentence_texts:
            return []

        # Calculate positions once
        positions = []
        current_pos = 0
        for sent in sentence_texts:
            positions.append(current_pos)
            current_pos += len(sent) + 1  # +1 for space/separator

        if not self.use_approximate:
            # Get accurate token counts in batch
            token_counts = self._get_token_counts(sentence_texts)
        else:
            # Estimate token counts using character length
            token_counts = self._estimate_token_counts(sentence_texts)

        # Create sentence objects
        return [
            Document(page_content=sent, metadata=dict(start_index=pos, end_index=pos + len(sent), token_count=count))
            for sent, pos, count in zip(sentence_texts, positions, token_counts)]

    def _create_chunk(self, sentences: List[Document], token_count: int) -> Document:
        """Create a chunk from a list of sentences.

        Args:
            sentences: List of sentences to create chunk from
            token_count: Total token count for the chunk

        Returns:
            Chunk object

        """
        chunk_text = "".join([sentence.page_content for sentence in sentences])
        return Document(page_content=chunk_text,
                        metadata=dict(start_index=sentences[0].metadata["start_index"], end_index=sentences[-1].metadata["end_index"],
                                      token_count=token_count, sentences=sentences))

    def chunk(self, text: str) -> List[Document]:
        """Split text into overlapping chunks based on sentences while respecting token limits.

        Args:
            text: Input text to be chunked

        Returns:
            List of Chunk objects containing the chunked text and metadata

        """
        if not text.strip():
            return []

        # Get prepared sentences with token counts
        sentences = self._prepare_sentences(text)  # 28mus
        if not sentences:
            return []

        # Pre-calculate cumulative token counts for bisect
        # Add 1 token for spaces between sentences
        token_sums = list(accumulate([s.metadata["token_count"] for s in sentences], lambda a, b: a + b, initial=0))

        chunks = []
        feedback = 1.0
        pos = 0

        while pos < len(sentences):
            # use updated feedback on the token sums
            token_sums = [int(s * feedback) for s in token_sums]

            # Use bisect_left to find initial split point
            target_tokens = token_sums[pos] + self.chunk_size
            split_idx = bisect_left(token_sums, target_tokens) - 1
            split_idx = min(split_idx, len(sentences))

            # Ensure we include at least one sentence beyond pos
            split_idx = max(split_idx, pos + 1)

            # Handle minimum sentences requirement
            if split_idx - pos < self.min_sentences_per_chunk:
                split_idx = pos + self.min_sentences_per_chunk

            # Get the estimated token count
            estimate = token_sums[split_idx] - token_sums[pos]

            # Get candidate sentences and verify actual token count
            chunk_sentences = sentences[pos:split_idx]
            chunk_text = " ".join(s.page_content for s in chunk_sentences)
            actual = len(self._encode(chunk_text))

            # Given the actual token_count and the estimate, get a feedback value for the next loop
            feedback = self._get_feedback(estimate, actual)
            # print(f"Estimate: {estimate} Actual: {actual} feedback: {feedback}")

            # Back off one sentence at a time if we exceeded chunk size
            while (actual > self.chunk_size and len(chunk_sentences) > self.min_sentences_per_chunk):
                split_idx -= 1
                chunk_sentences = sentences[pos:split_idx]
                chunk_text = " ".join(s.page_content for s in chunk_sentences)
                actual = len(self._encode(chunk_text))

            chunks.append(self._create_chunk(chunk_sentences, actual))

            # Calculate next position with overlap
            if self.chunk_overlap > 0 and split_idx < len(sentences):
                # Calculate how many sentences we need for overlap
                overlap_tokens = 0
                overlap_idx = split_idx - 1

                while overlap_idx > pos and overlap_tokens < self.chunk_overlap:
                    sent = sentences[overlap_idx]
                    next_tokens = overlap_tokens + sent.metadata["token_count"] + 1  # +1 for space
                    if next_tokens > self.chunk_overlap:
                        break
                    overlap_tokens = next_tokens
                    overlap_idx -= 1

                # Move position to after the overlap
                pos = overlap_idx + 1
            else:
                pos = split_idx

        return chunks

    def _encode_batch(self, texts: List[str]) -> List[List[int]]:
        """Encode a batch of texts using the backend tokenizer."""
        return tokenizer.emb_encoder.encode_batch(texts)

    def _encode(self, text: str) -> List[int]:
        """Encode text using the backend tokenizer."""

        return tokenizer.emb_encoder.encode(text)

    def __repr__(self) -> str:
        """Return a string representation of the SentenceChunker."""
        return (f"SentenceChunker(chunk_size={self.chunk_size}, "
                f"chunk_overlap={self.chunk_overlap}, "
                f"min_sentences_per_chunk={self.min_sentences_per_chunk})")
