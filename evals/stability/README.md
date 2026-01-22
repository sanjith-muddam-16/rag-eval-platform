# Prompt Stability Analysis

## What Prompt Stability Actually Means

Prompt Stability measures how robust and invariant an LLM’s output is when the prompt is perturbed, without changing the underlying intent.<br>
Let, <br>
P = original prompt<br>
{P1,P2,...,Pn} = semantically equivalent prompt variants<br>
f(P) = model output<br>
Stability(P)=Ei​[Similarity(f(P),f(Pi​))]<br>
Low stability ⇒ brittle system<br>
High stability ⇒ production-ready system<br>

---

Lexical Perturbations(Same meaning but different surface form)
"What is the capital of France?"
→ "France's capital city is?"
→ "Can you tell me the capital of France?"

---

Syntactic Perturbations(Grammar/Strucutre changes):
"Explain X briefly"
→ "Briefly explain X"
→ "X — explanation required"

---

Instructional Noise(Extra constraints that should not matter):
"Answer concisely"
"Answer as a teacher"
"Answer step by step"

---

Context Order Perturbations (CRITICAL for RAG):
[Query → Context]
[Context → Query]
[Context shuffled]

---

Adversarial Benign Perturbations
"Ignore previous formatting"
"Use different wording"

---
