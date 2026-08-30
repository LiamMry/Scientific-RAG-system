import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
CLN_DIR = ROOT_DIR / "data/processed"
CHK_DIR = ROOT_DIR / "data/chunks"

MAX_WORDS = 300
OVERLAP_WORDS = 50


def split_text(text: str, max_words: int = MAX_WORDS, overlap_words: int = OVERLAP_WORDS) -> list[str]:
    words = text.split()

    if len(words) <= max_words:
        return [text]

    step = max_words - overlap_words
    chunks = []
    for start in range(0, len(words), step):
        chunk_words = words[start:start + max_words]
        chunks.append(" ".join(chunk_words))
        if start + max_words >= len(words):
            break

    return chunks


def chunk_paper(data: dict) -> list[dict]:
    chunks = []

    sections = {"Abstract": data["abstract"], **data["section"]}

    for section_name, text in sections.items():
        for i, chunk_text in enumerate(split_text(text)):
            chunks.append({
                "title": data["title"],
                "section": section_name,
                "chunk_index": i,
                "text": chunk_text,
            })

    return chunks


def chunk_all(cln_dir: Path = CLN_DIR, chk_dir: Path = CHK_DIR):
    chk_dir.mkdir(parents=True, exist_ok=True)

    for json_path in cln_dir.glob("*.json"):
        data = json.loads(json_path.read_text())
        chunks = chunk_paper(data)

        chk_path = chk_dir / json_path.name
        chk_path.write_text(json.dumps(chunks, indent=2))


if __name__ == "__main__":
    chunk_all()
