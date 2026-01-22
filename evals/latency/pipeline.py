# pipeline.py
import time
import random
from typing import Dict, List
from latency.timers import latency_timer


# ----------------------------
# Utility: realistic latency
# ----------------------------

def jitter(base_ms: float, variance: float = 0.15) -> float:
    """
    Adds realistic jitter to latency.
    variance = 15% by default.
    """
    noise = random.uniform(-variance, variance)
    return max(0.0, base_ms * (1 + noise))


# ----------------------------
# Pipeline stages
# ----------------------------

def preprocess(query: str) -> str:
    """
    Realistic preprocessing:
    latency scales with input size.
    """
    base_ms = 2 + 0.03 * len(query)
    time.sleep(jitter(base_ms) / 1000)
    return query.strip().lower()


def retrieve_documents(query: str) -> List[str]:
    """
    Simulates RAG retrieval:
    - vector DB search
    - metadata filtering
    - variable number of chunks
    """
    num_chunks = random.choice([3, 4, 5, 6])

    # vector search + filtering cost
    base_ms = 40 + (num_chunks * 25)
    time.sleep(jitter(base_ms) / 1000)

    return [
        f"Document chunk {i} relevant to '{query}'"
        for i in range(num_chunks)
    ]


def build_prompt(query: str, docs: List[str]) -> str:
    """
    Prompt construction cost grows with context size.
    """
    token_estimate = sum(len(d) for d in docs) / 4
    base_ms = 5 + 0.02 * token_estimate
    time.sleep(jitter(base_ms) / 1000)

    context = "\n".join(docs)
    return f"""
Answer the question using the context below.

Context:
{context}

Question:
{query}
"""


def call_llm(prompt: str) -> str:
    """
    LLM inference latency depends on:
    - input tokens
    - output tokens
    - queue / GPU variance
    """
    input_tokens = len(prompt) / 4
    output_tokens = random.randint(80, 160)

    base_ms = (
        120
        + 0.9 * input_tokens
        + 1.2 * output_tokens
    )

    time.sleep(jitter(base_ms, variance=0.25) / 1000)

    return "Latency in LLM systems is the end-to-end time from request to response."


# ----------------------------
# Main request handler
# ----------------------------

def handle_request(query: str) -> Dict:
    """
    End-to-end RAG request with stage-level latency tracking.
    """
    metrics: Dict[str, float] = {}

    with latency_timer("preprocessing", metrics):
        clean_query = preprocess(query)

    with latency_timer("retrieval", metrics):
        docs = retrieve_documents(clean_query)

    with latency_timer("prompt_build", metrics):
        prompt = build_prompt(clean_query, docs)

    with latency_timer("llm_inference", metrics):
        answer = call_llm(prompt)

    metrics["total"] = round(sum(metrics.values()), 2)

    return {
        "answer": answer,
        "latency_ms": metrics
    }
