"""
Retrieved Context
        ↓
Model Answer
        ↓
Claim Extraction (LLM)
        ↓
Claim Verification (LLM Judge)
        ↓
Faithfulness Score + Failure Reasons

"""
import json
from typing import List, Literal, Optional
from pydantic import BaseModel, ValidationError


# -----------------------------
# Pydantic Schemas
# -----------------------------

VerdictType = Literal[
    "supported",
    "partially_supported",
    "not_supported",
    "contradicted",
]


class Claim(BaseModel):
    claim: str
    verdict: VerdictType
    evidence: Optional[str]
    importance: float  # 0.0 – 1.0


class FaithfulnessResult(BaseModel):
    claims: List[Claim]
    faithfulness_score: float
    is_faithful: bool


# -----------------------------
# Utility: Safe JSON Parse
# -----------------------------

def safe_json_load(text: str):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON from LLM:\n{text}")


# -----------------------------
# Step 1: Claim Extraction
# -----------------------------

def extract_claims(answer: str, client, model="gpt-4o-mini") -> List[str]:
    prompt = f"""
You are an expert linguistic analyst.

Extract all ATOMIC factual claims from the answer below.
Each claim must be a single, verifiable statement.

Answer:
\"\"\"{answer}\"\"\"

Return ONLY valid JSON:
{{ "claims": ["claim1", "claim2", "..."] }}
"""

    response = client.chat.completions.create(
        model=model,
        temperature=0,
        messages=[{"role": "user", "content": prompt}],
    )

    data = safe_json_load(response.choices[0].message.content)
    return data.get("claims", [])


# -----------------------------
# Step 2: Claim Importance
# -----------------------------

def score_claim_importance(claim: str, question: str, client, model="gpt-4o-mini") -> float:
    prompt = f"""
You are evaluating how important a claim is for answering the user's question.

Question:
\"\"\"{question}\"\"\"

Claim:
\"\"\"{claim}\"\"\"

Score importance from 0 to 1:
- 1.0 = central to answering the question
- 0.5 = useful detail
- 0.1 = minor or background info

Return ONLY valid JSON:
{{ "importance": 0.0 }}
"""

    response = client.chat.completions.create(
        model=model,
        temperature=0,
        messages=[{"role": "user", "content": prompt}],
    )

    data = safe_json_load(response.choices[0].message.content)
    return float(data.get("importance", 0.5))


# -----------------------------
# Step 3: Claim Verification (NLI-style)
# -----------------------------

def verify_claim(claim: str, context: str, client, model="gpt-4o-mini"):
    prompt = f"""
You are a strict faithfulness evaluator using natural language inference.

Context:
\"\"\"{context}\"\"\"

Claim:
\"\"\"{claim}\"\"\"

Classify the claim as:
- supported: directly stated or clearly entailed
- partially_supported: some support but missing details or weaker wording
- not_supported: not stated or cannot be inferred
- contradicted: context explicitly says the opposite

Return ONLY valid JSON:
{{
  "verdict": "supported | partially_supported | not_supported | contradicted",
  "evidence": "exact supporting or contradicting text from context, or null"
}}
"""

    response = client.chat.completions.create(
        model=model,
        temperature=0,
        messages=[{"role": "user", "content": prompt}],
    )

    return safe_json_load(response.choices[0].message.content)


# -----------------------------
# Step 4: Final Faithfulness Evaluation
# -----------------------------

VERDICT_SCORE = {
    "supported": 1.0,
    "partially_supported": 0.5,
    "not_supported": 0.0,
    "contradicted": -0.5,
}


def evaluate_faithfulness(
    answer: str,
    context: str,
    question: str,
    client,
    model="gpt-4o-mini",
    strict: bool = False,
) -> FaithfulnessResult:

    claims_text = extract_claims(answer, client, model)

    claims: List[Claim] = []
    weighted_score_sum = 0.0
    weight_sum = 0.0

    for c in claims_text:
        verdict_data = verify_claim(c, context, client, model)

        verdict = verdict_data.get("verdict", "not_supported")
        evidence = verdict_data.get("evidence")

        importance = score_claim_importance(c, question, client, model)

        score = VERDICT_SCORE.get(verdict, 0.0)

        weighted_score_sum += score * importance
        weight_sum += importance

        try:
            claims.append(
                Claim(
                    claim=c,
                    verdict=verdict,
                    evidence=evidence,
                    importance=importance,
                )
            )
        except ValidationError as e:
            print("Validation error:", e)

    final_score = weighted_score_sum / max(weight_sum, 1e-6)

    if strict:
        is_faithful = all(c.verdict == "supported" for c in claims)
    else:
        is_faithful = final_score >= 0.85

    return FaithfulnessResult(
        claims=claims,
        faithfulness_score=round(final_score, 4),
        is_faithful=is_faithful,
    )


"""
context = LangChain integrates with FAISS and Pinecone as vector stores for document retrieval.

answer = LangChain uses FAISS, Pinecone, and Weaviate for vector-based retrieval.

Output:
{
  "claims": [
    {
      "claim": "LangChain uses FAISS for vector-based retrieval",
      "supported": true,
      "evidence": "integrates with FAISS"
    },
    {
      "claim": "LangChain uses Pinecone for vector-based retrieval",
      "supported": true,
      "evidence": "integrates with Pinecone"
    },
    {
      "claim": "LangChain uses Weaviate for vector-based retrieval",
      "supported": false,
      "evidence": null
    }
  ],
  "faithfulness_score": 0.6667,
  "is_faithful": false
}







"""