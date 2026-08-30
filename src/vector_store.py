import json
from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

ROOT_DIR = Path(__file__).resolve().parent.parent
EMB_DIR = ROOT_DIR / "data/embeddings"
DB_DIR = ROOT_DIR / "data/chroma"

COLLECTION_NAME = "papers"
MODEL_NAME = "all-MiniLM-L6-v2"


def build_index(emb_dir: Path = EMB_DIR, db_dir: Path = DB_DIR, collection_name: str = COLLECTION_NAME):
    client = chromadb.PersistentClient(path=str(db_dir))
    collection = client.get_or_create_collection(collection_name)

    for json_path in emb_dir.glob("*.json"):
        paper_id = json_path.stem
        chunks = json.loads(json_path.read_text())

        ids = [f"{paper_id}_{i}" for i in range(len(chunks))]
        embeddings = [chunk["embedding"] for chunk in chunks]
        documents = [chunk["text"] for chunk in chunks]
        metadatas = [
            {
                "paper_id": paper_id,
                "title": chunk["title"],
                "section": chunk["section"],
                "chunk_index": chunk["chunk_index"],
            }
            for chunk in chunks
        ]

        collection.upsert(ids=ids, embeddings=embeddings, documents=documents, metadatas=metadatas)

    return collection


def query(text: str, n_results: int = 5, db_dir: Path = DB_DIR, collection_name: str = COLLECTION_NAME, model_name: str = MODEL_NAME):
    model = SentenceTransformer(model_name)
    embedding = model.encode([text])[0].tolist()

    client = chromadb.PersistentClient(path=str(db_dir))
    collection = client.get_collection(collection_name)

    return collection.query(query_embeddings=[embedding], n_results=n_results)


if __name__ == "__main__":
    build_index()
