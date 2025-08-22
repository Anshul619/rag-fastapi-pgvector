from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import db, models, schemas, llm
from app.embeddings import embedder
from sqlalchemy import text
from app.rag import sentence_chunk

# Create FastAPI app
app = FastAPI(title="RAG FastAPI + pgvector")

# Dependency to get DB session
def get_db():
    session = db.SessionLocal()
    try:
        yield session
    finally:
        session.close()


@app.get("/")
def root():
    return {"message": "RAG FastAPI is running!"}


@app.post("/ingest")
def ingest_document(doc: schemas.DocumentCreate, session: Session = Depends(get_db)):
    document = models.Document(title=doc.title, content=doc.text)
    session.add(document)
    session.flush()  # get document.id

    for chunk in sentence_chunk(doc.text, chunk_size=5, overlap=2):
        embedding = embedder.encode(chunk).tolist()
        session.add(models.Chunk(document_id=document.id, content=chunk, embedding=embedding))

    session.commit()
    return {"status": "ok", "document_id": document.id}

@app.post("/query")
def query_documents(req: schemas.QueryRequest, session: Session = Depends(get_db)):
    # get embedding for the query
    q_embedding = embedder.encode(req.question).tolist()

    # pgvector similarity search
    docs = session.execute(
        text("""
        SELECT id, content, document_id, embedding <-> (:q_embedding)::vector AS distance
        FROM chunks
        ORDER BY embedding <-> (:q_embedding)::vector
        LIMIT :top_k
        """),
        {"q_embedding": q_embedding, "top_k": req.top_k or 5}
    ).mappings().all()

    context = "\n\n".join([d["content"] for d in docs])

    answer = llm.ask_model(context, req.question)

    return {
        "answer": answer,
        "sources": docs
    }