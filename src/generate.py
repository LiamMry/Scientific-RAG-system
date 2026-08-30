import ollama
from vector_store import query

MODEL_NAME = "llama3.1:8b"

SYSTEM_PROMPT = """You are a research assistant answering questions about scientific papers.
Answer only using the provided excerpts. If the excerpts don't contain the answer, say so.
Cite the paper title and section for every claim you make."""


def build_context(results: dict) -> str:
    excerpts = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        excerpts.append(f"[{meta['title']} - {meta['section']}]\n{doc}")
    return "\n\n---\n\n".join(excerpts)


def answer(question: str, n_results: int = 5) -> str:
    results = query(question, n_results=n_results)
    context = build_context(results)

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Excerpts:\n\n{context}\n\nQuestion: {question}"},
        ],
    )

    return response["message"]["content"]


if __name__ == "__main__":
    question = "How does temporal consistency work in video diffusion models?"
    print(answer(question))
