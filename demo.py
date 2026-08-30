"""End-to-end demo: download a couple of papers, run the full pipeline, ask a question.

Requires GROBID (src/launch_grobid_server.sh) and Ollama (src/launch_ollama_server.sh)
running in separate terminals, and the model pulled with `ollama pull llama3.1:8b`.

Usage:
    python demo.py
"""
import sys
import urllib.request
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR / "src"))

DEMO_QUERY = "retrieval augmented generation"
DEMO_MAX_RESULTS = 3
DEMO_QUESTION = "What are the main advantages of retrieval-augmented generation over standard language models?"


def check_server(url: str, name: str, help_cmd: str):
    try:
        urllib.request.urlopen(url, timeout=3)
    except Exception:
        sys.exit(f"[demo] {name} isn't reachable at {url}.\nStart it with: {help_cmd}")


def main():
    check_server("http://localhost:8070/api/isalive", "GROBID", "bash src/launch_grobid_server.sh")
    check_server("http://localhost:11434/api/tags", "Ollama", "bash src/launch_ollama_server.sh")

    import arxiv_download
    import grobid_parse
    import clean
    import chunking
    import embedding
    import vector_store
    import generate

    print(f"[demo] Downloading {DEMO_MAX_RESULTS} papers on '{DEMO_QUERY}'...")
    arxiv_download.search_and_process(query=DEMO_QUERY, max_results=DEMO_MAX_RESULTS)

    print("[demo] Parsing PDFs with GROBID...")
    grobid_parse.parse()

    print("[demo] Cleaning parsed output...")
    clean.clean_all()

    print("[demo] Chunking sections...")
    chunking.chunk_all()

    print("[demo] Embedding chunks...")
    embedding.embed_all()

    print("[demo] Indexing in ChromaDB...")
    vector_store.build_index()

    print(f"[demo] Question: {DEMO_QUESTION}\n")
    print(generate.answer(DEMO_QUESTION))


if __name__ == "__main__":
    main()
