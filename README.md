# Scientific RAG System

A local, fully self-hosted Retrieval-Augmented Generation (RAG) pipeline for querying arXiv papers. No paid API required — parsing, embeddings, vector search, and generation all run on your machine.

## Pipeline

```
arxiv_download.py   ->  download papers + metadata from arXiv (data/raw/pdf, data/raw/metadata)
grobid_parse.py      ->  parse PDFs to structured TEI/JSON via GROBID (data/raw/tei)
clean.py              ->  flatten GROBID output into {title, authors, abstract, section} (data/processed)
chunking.py           ->  split sections into word-bounded chunks with overlap (data/chunks)
embedding.py          ->  embed chunks with Sentence Transformers (data/embeddings)
vector_store.py       ->  index embeddings in ChromaDB, expose query() (data/chroma)
generate.py           ->  retrieve relevant chunks + answer questions with a local LLM (Ollama)
```

Each stage reads/writes to `data/`, keyed by arXiv short ID, so the pipeline can be re-run incrementally.

## Prerequisites

- Python 3.9+
- [Docker](https://www.docker.com/) (to run the GROBID server)
- [Ollama](https://ollama.com/) (to run the local LLM)

## Setup

```bash
# 1. Create and activate the virtual environment
python3 -m venv srag
source srag/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Pull the local LLM used for generation
ollama pull llama3.1:8b
```

## Running the servers

GROBID and Ollama each need to be running before their respective pipeline steps. Run each in its own terminal tab:

```bash
bash src/launch_grobid_server.sh   # GROBID on localhost:8070
bash src/launch_ollama_server.sh   # Ollama on localhost:11434
```

## Demo

With both servers running, `srag` activated, and the model pulled, run the whole pipeline end to end on a couple of papers and ask a sample question:

```bash
python demo.py
```

## Usage

With both servers running and `srag` activated, run the pipeline stages in order:

```bash
python src/arxiv_download.py
python src/grobid_parse.py
python src/clean.py
python src/chunking.py
python src/embedding.py
python src/vector_store.py
```

Then ask questions:

```bash
python src/generate.py
```

or from Python:

```python
from src.generate import answer
print(answer("How does temporal consistency work in video diffusion models?"))
```

## Project structure

```
src/           pipeline scripts
data/          generated artifacts (gitignored — reproducible by re-running the pipeline)
srag/          Python virtual environment (gitignored)
```
