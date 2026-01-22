"""
answer_variance.py
Measures the variance in the computed answer.
Measure the semantic drift accross multiple LLM outputs using the embedings.

This module is intentionally:
1)Prompt Agnostic
2)Model Agnostic
3)RAG Agnostic

It only measures how different the answers are semantically
"""
from typing import List,Dict
import numpy as np
def cosine_similarity(vec_a:np.ndarray,vec_b:np.ndarray)->float:
    """
    Computes cosine similarity between two vectors and handles edge cases safely
    """
    denominator = (np.linalg.norm(vec_a)*np.linalg.norm(vec_b))
    if denominator == 0:
        return 0
    else:
        return float(np.dot(vec_a,vec_b)/denominator)
    
def embed_texts(texts:List[str],embed_fn)->np.ndarray:
    """
    Converts a list of texts into embedding vectors
    embed_fn Must accepts a List[str] and return List[List[int]] or np.ndarray
    This design makes the code usable accross a wide-span of embedders
    """
    embeddings = embed_fn(texts)
    return np.asarray(embeddings,dtype=np.float32)

def compute_similarity_matrix(embedding:np.ndarray)->np.ndarray:
    """
    Computes full pair wise cosine similarity and gives a similarity matrix
    Output shape will be (n,n)
    Diagonals will be 1 as cosine(a,a) = 1
    """
    n = embedding.shape(0)
    sim_matrix = np.zeros(shape=(n,n),dtype=np.float32)
    for i in range(n):
        for j in range(n):
            sim_matrix[i][j] = cosine_similarity(embedding[i],embedding[j])
    return sim_matrix

def compute_answer_variance(answers:List[str],embed_fn)->Dict[str,float]:
    """
    Computes semantic variance metrics across multiple answers.
    This is the PRIMARY metric used by:
    - prompt_stability.py
    - regression detection
    - robustness analysis

    Returns:
    {
        "mean_similarity":float
        "variance":float
        "std_dev":float
        "worst_case_similarity":float
    }
    """
    # Requires atleast two samples for evaluation

    if len(answers) < 2:
        raise ValueError(
            "Answer variance requires at least 2 answers."
        )
    
    # Embed answers
    embeddings = embed_texts(answers, embed_fn)

    # Compute similarity index 
    sim_matrix = compute_similarity_matrix(embeddings)

    # Compute upper triangle similarites and get a code
    similarities = []
    n = sim_matrix.shape[0]
    for i in range(n):
        for j in range(i + 1, n):
            similarities.append(sim_matrix[i, j])

    # Compute the feature indices
    similarities = np.array(similarities, dtype=np.float32)
    mean_similarity = float(np.mean(similarities))
    variance = float(np.var(similarities))
    std_dev = float(np.std(similarities))
    worst_case_similarity = float(np.min(similarities))

    # Return the statistics
    return {
        "mean_similarity": mean_similarity,
        "variance": variance,
        "std_dev": std_dev,
        "worst_case_similarity": worst_case_similarity
    }
