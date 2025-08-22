import nltk
from typing import List

# # Ensure punkt is downloaded (do this once)
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)

from nltk.tokenize import sent_tokenize

def sentence_chunk(text: str, chunk_size: int = 200, overlap: int = 50) -> List[str]:
    """
    Split text into sentence-based chunks.
    Each chunk is a group of sentences not exceeding `chunk_size` words.
    Overlap ensures continuity between chunks.
    """
    sentences = sent_tokenize(text)
    if len(sentences) == 1:  # fallback if only one "sentence"
        words = text.split()
        chunks = []
        step = chunk_size - overlap
        for i in range(0, len(words), step):
            chunks.append(" ".join(words[i:i+chunk_size]))
        return chunks

    chunks = []
    current_chunk = []
    current_length = 0

    for sent in sentences:
        words = sent.split()
        if current_length + len(words) <= chunk_size:
            current_chunk.append(sent)
            current_length += len(words)
        else:
            # save current chunk
            chunks.append(" ".join(current_chunk))
            # overlap: carry last few words to next chunk
            if overlap > 0 and current_chunk:
                overlap_words = " ".join(current_chunk).split()[-overlap:]
                current_chunk = overlap_words[:]
            else:
                current_chunk = []

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks