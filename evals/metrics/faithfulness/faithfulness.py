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
from pydantic import BaseModel
from typing import List

class Claim(BaseModel):
    claim:str
    supported:bool
    evidence:str|None

class FaithfulnessResult(BaseModel):
    claims : List[Claim]
    faithfulness_score : float
    is_faithful : bool

"""
[
  {"claim": "...", "supported": true, "evidence": "..."},
  {"claim": "...", "supported": false, "evidence": null}
]

"""
def verify_claim(claim:str,context:str,client,model='gpt-4o-mini'):
    prompt = f"""You are a strict faithfulness evaluator
    Context:\"\"\"{context}\"\"\"
    Claim:\"\"\"{claim}\"\"\"
    Is the claim directly supported by the context?
    Answer only in JSON:
    {{
        "supported": true or false,
        "evidence": "exact supporting text or null"
    }} 
"""
    response = client.chat.completions.create( model=model,temperature=0,
        messages=[{"role": "user", "content": prompt}],
    )

    return eval(response.choices[0].message.content)

def extract_claims(answer:str,client,model='gpt-4o-mini'):
    prompt = f"""You are a linguistic expert.Extract all atomic factual claims from the answer below.
                Each claim must be a single verifiable statement.
                Answer:\"\"\"{answer}\"\"\".
                Return a JSON list of strings."""
    messages = [{'role':'user'},{'content':prompt}]
    response = client.chat.completions.create(model=model,temperature=0,messages=messages)
    return eval(response.choices[0].message.content)

def evaluate_faithfulness(answer:str,context:str,client,model='gpt-4o-mini',strict:bool=False):
    claims_text = extract_claims(answer, client, model)
    claims = []
    supported_count = 0
    for c in claims_text:
        verdict = verify_claim(c, context, client, model)
        supported = verdict["supported"]

        if supported:
            supported_count += 1

        claims.append(
            Claim(
                claim=c,
                supported=supported,
                evidence=verdict["evidence"],
            )
        )
    score = supported_count / max(len(claims), 1)
    return FaithfulnessResult(
        claims=claims,
        faithfulness_score=score,
        is_faithful=(score == 1.0) if strict else (score >= 0.85),
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