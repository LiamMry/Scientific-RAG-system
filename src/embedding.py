import json
from pathlib import Path
from sentence_transformers import SentenceTransformer

ROOT_DIR = Path(__file__).resolve().parent.parent
CHK_DIR = ROOT_DIR / "data/chunks"
EMB_DIR = ROOT_DIR / "data/embeddings"

MODEL_NAME = "all-MiniLM-L6-v2"


def embed_all(chk_dir: Path = CHK_DIR, emb_dir: Path = EMB_DIR, model_name: str = MODEL_NAME):
    emb_dir.mkdir(parents=True, exist_ok=True)

    model = SentenceTransformer(model_name)

    for json_path in chk_dir.glob("*.json"):
        chunks = json.loads(json_path.read_text())

        texts = [chunk["text"] for chunk in chunks]
        embeddings = model.encode(texts, show_progress_bar=False)

        for chunk, embedding in zip(chunks, embeddings):
            chunk["embedding"] = embedding.tolist()

        emb_path = emb_dir / json_path.name
        emb_path.write_text(json.dumps(chunks))


if __name__ == "__main__":
    embed_all()
