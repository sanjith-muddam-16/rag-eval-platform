from typing import List,Tuple
import json
def binary_correctness_label(qa_pairs:List[Tuple[str,str]],client,model:str='gpt-4.1-nano')\
    ->List[int]:
    formatted_items = []
    for i,(q,a) in enumerate(qa_pairs,1):
        formatted_items.append(
            f"{i}.Question:{q}\n Answer:{a}"
        )
    joined = "\n\n".join(formatted_items)
    prompt = f"""You are a strict factual evaluator.For each Question Answer pair below, 
    decide whether the answer is completely factually correct.Return your response strictly in the following 
    JSON format:
    {{
        "results": [true/false, true/false, ...]
        }}
    Do not add any explanation.
    Pairs:
    {joined}"""
    response = client.chat.completions.create(model=model,messages=[{"role": "user", "content": prompt}],
        temperature=0)
    content = response.choices[0].message.content.strip()
    import json
    try:
        data = json.loads()
        bools = data['results']
        return [1 if x else 0 for x in bools]
    except Exception as e:
        print("Parssing Failed ",content)
        raise e
    
    """pairs = [("Who is the PM of India?", "Narendra Modi"),("Capital of Australia?", "Sydney"),
    ("2 + 2 = ?", "4")]
    scores = binary_correctness_batch(pairs, client)
    print(scores)   # [1, 0, 1]
    """

def scalar_correctness_batch(qa_pairs:List[Tuple[str,str]],client,model='gpt-4.1-nano')->List[int]:
    formatted = []
    for i,(q,a) in enumerate(qa_pairs,1):
        formatted.append(f'{i}.Question{q}\nAnswer{a}')
    joined = '\n\n'.join(formatted)
    prompt = f"""You are an expert factual evaluator.For each Question Answer pair below, rate factual correctness
    on a scale from 0.0 to 1.0 using this rubric:
    - 1.0 = fully correct
    - 0.75 = mostly correct, minor error
    - 0.5 = partially correct
    - 0.25 = mostly incorrect
    - 0.0 = completely incorrect
    Return ONLY valid JSON in this exact format:
    {{
        "scores": [number, number, ...]
    }}
    Do not include any explanation or extra text.
    Pairs:{joined}"""
    response = client.chat.completions.create(model=model,messages=[{"role": "user", "content": prompt}],
        temperature=0)
    content = response.choices[0].message.content.strip()
    try:
        data = json.loads(content)
        scores = data['scores']
        # Handling edge cases if any present
        cleaned = []
        for s in scores:
            s = float(s)
            if s<0.0:s=0.0
            if s>1.0:s=1.0
            cleaned.append(s)
        return cleaned
    except Exception as e:
        print("Failed to parse ",content)
        raise e
    
def extract_claims_batch(answers: List[str],client,model: str = "gpt-4o-mini") -> List[List[str]]:
    formatted = []
    for i,ans in enumerate(answers,1):
        formatted.append(f"{i}.{ans}")
    joined = "\n\n".join(formatted)
    prompt = f"""Extract all atomic factual claims from each answer below.Each claim must be independently
      verifiable.Return ONLY valid JSON in this exact format:
    {{
        "results": [
            ["claim1", "claim2", ...],
            ["claim1", ...],
        ]
    }}
    Answers:{joined}"""
    response = client.chat.completions.create(model=model,messages=[{"role": "user", "content": prompt}],
        temperature=0)
    content = response.choices[0].message.content.strip()
    try:
        data = json.loads(content)
        return data["results"]
    except Exception as e:
        print("Claim extraction parse failed:\n", content)
        raise e

def verify_claims_batch(q_claim_pairs: List[Tuple[str, str]],client,model: str = "gpt-4o-mini") -> List[bool]:
    formatted = []
    for i, (q, c) in enumerate(q_claim_pairs, 1):
        formatted.append(
            f"{i}. Question: {q}\n   Claim: {c}"
        )
    joined = "\n\n".join(formatted)
    prompt = f"""You are a strict factual verifier.For each Question - Claim pair, decide whether the claim is 
    factually correct.Return ONLY valid JSON in this exact format:
    {{
    "results": [true, false, true, ...]
    }}
    Pairs:{joined}
"""
    response = client.chat.completions.create(model=model,messages=[{"role": "user", "content": prompt}],
        temperature=0)
    content = response.choices[0].message.content.strip()
    try:
        data = json.loads(content)
        return data["results"]
    except Exception as e:
        print("Claim verification parse failed:\n", content)
        raise e

from typing import List, Tuple

def claim_level_correctness_batch(qa_pairs: List[Tuple[str, str]],client,model: str = "gpt-4o-mini") -> List[float]:
    questions = [q for q, _ in qa_pairs]
    answers = [a for _, a in qa_pairs]
    all_claims = extract_claims_batch(answers, client, model)
    flat_pairs = []
    index_map = [] 
    for i, (q, claims) in enumerate(zip(questions, all_claims)):
        for c in claims:
            flat_pairs.append((q, c))
            index_map.append(i)

    if not flat_pairs:
        return [0.0] * len(qa_pairs)
    results = verify_claims_batch(flat_pairs, client, model)
    total = [0] * len(qa_pairs)
    correct = [0] * len(qa_pairs)
    for res, idx in zip(results, index_map):
        total[idx] += 1
        if res:
            correct[idx] += 1
    scores = []
    for c, t in zip(correct, total):
        scores.append(c / t if t > 0 else 0.0)
    return scores

            
    


