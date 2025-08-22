import argparse, json, pathlib
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text
from app.config import DATABASE_URL, CHUNK_SIZE, CHUNK_OVERLAP
from app.models import Document
from app.rag import embed_texts
from app.utils_text import simple_chunk

def main():
    parser = argparse.ArgumentParser(description="Ingest .txt/.md files into Postgres+pgvector")
    parser.add_argument("--path", required=True, help="Folder or file")
    parser.add_argument("--title", help="Optional title when ingesting a single file")
    args = parser.parse_args()

    engine = create_engine(DATABASE_URL, pool_pre_ping=True, future=True)
    with engine.begin() as conn:
        p = pathlib.Path(args.path)
        files = [p] if p.is_file() else list(p.glob("**/*"))
        files = [f for f in files if f.suffix.lower() in {".txt", ".md"}]
        for f in files:
            text_content = f.read_text(encoding="utf-8", errors="ignore")
            title = args.title or f.name
            doc = conn.execute(text("INSERT INTO documents (title, meta) VALUES (:t, :m) RETURNING id"),
                               {"t": title, "m": json.dumps({"path": str(f)})}).scalar_one()

            chunks = simple_chunk(text_content, CHUNK_SIZE, CHUNK_OVERLAP)
            vecs = embed_texts(chunks)
            ins = text("INSERT INTO chunks (document_id, chunk_index, content, embedding) VALUES (:d, :i, :c, :e)")
            for i, (c, v) in enumerate(zip(chunks, vecs)):
                conn.execute(ins, {"d": str(doc), "i": i, "c": c, "e": v.tolist()})
        print(f"Ingested {len(files)} files.")

if __name__ == "__main__":
    main()