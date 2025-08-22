CREATE EXTENSION IF NOT EXISTS vector;

-- Documents table holds metadata
CREATE TABLE IF NOT EXISTS documents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  meta JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Chunks table stores text + embedding
-- Ensure EMBEDDING_DIM matches your model (default 384 for MiniLM)
CREATE TABLE IF NOT EXISTS chunks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
  content TEXT NOT NULL,
  embedding vector(384), -- update if you change model
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Useful composite index: IVFFlat for cosine similarity
-- Requires ANALYZE and a non-empty table to build effectively.
CREATE INDEX IF NOT EXISTS idx_chunks_embedding_ivfflat
  ON chunks USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 100);

CREATE INDEX IF NOT EXISTS idx_chunks_docid ON chunks(document_id);