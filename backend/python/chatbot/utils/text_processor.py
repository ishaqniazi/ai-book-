from typing import List
import re


class TextProcessor:
    def __init__(self):
        pass

    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
        """
        Split text into chunks of approximately chunk_size tokens with overlap.
        This implementation uses a simple word-based approach.
        """
        # Split text into sentences to avoid breaking them across chunks
        sentences = re.split(r'(?<=[.!?])\s+', text)

        chunks = []
        current_chunk = ""

        for sentence in sentences:
            # If adding the next sentence would exceed chunk size
            if len(current_chunk) + len(sentence) > chunk_size:
                if current_chunk:
                    # Add the current chunk to the list
                    chunks.append(current_chunk.strip())

                    # Handle overlap by taking the last part of the current chunk
                    if overlap > 0:
                        words = current_chunk.split()
                        overlap_text = ' '.join(words[-min(len(words), overlap):])
                        current_chunk = overlap_text + ' ' + sentence
                    else:
                        current_chunk = sentence
                else:
                    # If current chunk is empty, add the sentence anyway
                    # (this sentence is longer than chunk_size)
                    chunks.append(sentence.strip())
                    current_chunk = ""
            else:
                # Add the sentence to the current chunk
                current_chunk += " " + sentence if current_chunk else sentence

        # Add the last chunk if it's not empty
        if current_chunk:
            chunks.append(current_chunk.strip())

        # Handle very long chunks by splitting them by words if needed
        final_chunks = []
        for chunk in chunks:
            if len(chunk) > chunk_size:
                # Split by words if the chunk is still too large
                final_chunks.extend(self._split_large_chunk(chunk, chunk_size, overlap))
            else:
                final_chunks.append(chunk)

        return final_chunks

    def _split_large_chunk(self, chunk: str, chunk_size: int, overlap: int) -> List[str]:
        """
        Split a large chunk into smaller pieces by words.
        """
        words = chunk.split()
        chunks = []
        current_sub_chunk = []
        current_size = 0

        for word in words:
            if current_size + len(word) > chunk_size and current_sub_chunk:
                # Add current sub-chunk to chunks
                chunks.append(' '.join(current_sub_chunk))

                # Handle overlap
                if overlap > 0:
                    # Take the last 'overlap' words from the current chunk
                    overlap_words = current_sub_chunk[-overlap:] if len(current_sub_chunk) >= overlap else current_sub_chunk
                    current_sub_chunk = overlap_words + [word]
                    current_size = sum(len(w) for w in current_sub_chunk) + len(current_sub_chunk) - 1
                else:
                    current_sub_chunk = [word]
                    current_size = len(word)
            else:
                current_sub_chunk.append(word)
                current_size += len(word) + 1  # +1 for space

        # Add the last sub-chunk
        if current_sub_chunk:
            chunks.append(' '.join(current_sub_chunk))

        return chunks

    def clean_text(self, text: str) -> str:
        """
        Clean text by removing extra whitespace and normalizing.
        """
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove extra newlines but preserve paragraph structure
        text = re.sub(r'\n\s*\n', '\n\n', text)
        return text.strip()

    def extract_headings(self, text: str) -> List[dict]:
        """
        Extract headings from markdown text.
        Returns a list of dictionaries with heading level, text, and position.
        """
        headings = []
        lines = text.split('\n')

        for i, line in enumerate(lines):
            # Match markdown headings (# ## ### etc.)
            match = re.match(r'^(#{1,6})\s+(.+)', line)
            if match:
                level = len(match.group(1))
                heading_text = match.group(2).strip()
                headings.append({
                    'level': level,
                    'text': heading_text,
                    'position': i
                })

        return headings