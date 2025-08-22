from sentence_transformers import SentenceTransformer

# load once at startup
embedder = SentenceTransformer("all-MiniLM-L6-v2")