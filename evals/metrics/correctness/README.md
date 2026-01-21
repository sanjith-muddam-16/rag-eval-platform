# Correctness Evaluation

## What is Correctness?

**Correctness** answers one fundamental question:

> **Is the generated answer factually right in the real world?**

An answer is considered **correct** if it:

- Matches **true, real-world facts**
- Correctly answers the user’s question
- Remains correct **even if retrieved documents are wrong, incomplete, or misleading**

> Correctness is **independent of retrieval quality**.  
> A model can be correct even when retrieval fails — and incorrect even with perfect retrieval.

---

## Types of Correctness

### Reference-Based Correctness (Classic)

**Inputs required**

- Question
- Ground truth (reference) answer
- Model-generated answer

**How it works**

- Compare **semantic meaning**, not exact tokens

**Common methods**

- Embedding similarity
- LLM-based semantic equivalence
- Structured output comparison (JSON, SQL, etc.)

**Weaknesses**

- Requires gold/reference answers
- Fails when multiple correct answers exist
- Expensive to maintain at scale

---

### Reference-Free Correctness (LLM-as-Judge)

**Inputs required**

- Question
- Model-generated answer

**How it works**

- Provide the LLM with the question and answer
- Ask:
  > “Is this answer factually correct and complete?”

**Judgment type**

- Binary: `Correct / Incorrect`
- Scalar: score in range `[0, 1]`

**Why it’s powerful**

- No gold labels required
- Handles open-ended answers
- Works well for RAG systems and agents
- Scales to large datasets

**Limitations**

- Subjective without a strict rubric
- Judge quality matters

---

### Claim-Level Correctness (Best Practice)

Instead of judging the entire answer as a whole:

1. Break the answer into **atomic factual claims**
2. Verify each claim independently
3. Aggregate the results into a final score

**This avoids**

- One wrong sentence passing unnoticed
- One correct sentence masking multiple factual errors

This is the **most reliable correctness evaluation strategy** for LLM systems.

---

## Correctness Metrics (What You Actually Compute)

### Binary Correctness

**Values**

- `1` → Correct
- `0` → Incorrect

**Used when**

- There is only **one correct answer**
- Any error = failure

**Examples**

- Math problems
- Fact lookup questions
- Tool outputs

---

### Scalar Correctness

**Values**

- Continuous score in range `[0.0 – 1.0]`

**Used when**

- Answers are open-ended
- Partial correctness matters
- LLM answers contain multiple components

This is the **most common industry metric**.

---

### Claim-Averaged Correctness

Most scalar correctness scores are computed as:

```text
Correctness = (# correct claims) / (# total claims)

```

## Worked Example

### Question

**What are the benefits of the HTTP/2 protocol?**

---

### Model Answer

> HTTP/2 improves performance by enabling multiplexing, compressing headers, and reducing latency.  
> It also encrypts all traffic by default.

⚠️ **Important**  
The last sentence is incorrect — **HTTPS encrypts traffic, not HTTP/2 itself**.

---

## Method 1 — Reference-Based Correctness

### Inputs

- Question
- Gold reference answer
- Model answer

### Reference Answer (Ground Truth)

> HTTP/2 improves performance through multiplexing, header compression, and server push.  
> Encryption is provided by HTTPS, not HTTP/2 itself.

### Semantic Comparison

| Claim                       | Matches Reference |
| --------------------------- | ----------------- |
| Multiplexing                | ✅                |
| Header compression          | ✅                |
| Reduced latency             | ✅ (implied)      |
| Encrypts traffic by default | ❌                |

### Metric Output

- **Binary correctness:** `0` (incorrect)
- **Scalar correctness:** `0.75`

### Key Properties

- ✅ Objective
- ✅ Simple
- ❌ Requires gold answers
- ❌ Breaks when multiple valid answers exist

---

## Method 2 — Reference-Free Correctness (LLM-as-Judge)

### Inputs

- Question
- Model answer

### Evaluation Logic

The evaluator asks:

> _“Is this answer factually correct and complete?”_

### Implicit Reasoning

- First part → correct
- Final claim → incorrect
- Overall → mostly correct but contains an error

### Metric Output

- **Binary correctness:** `0`
- **Scalar correctness:** `0.75`

### Key Properties

- ✅ No labels needed
- ✅ Works for open-ended QA
- ⚠️ Subjective without a rubric
- ⚠️ Judge quality matters

---

## Method 3 — Claim-Level Correctness (Best Practice)

This method explains **where the score comes from**.

### Step 1: Extract Atomic Claims

| #   | Claim                                  |
| --- | -------------------------------------- |
| 1   | HTTP/2 enables multiplexing            |
| 2   | HTTP/2 compresses headers              |
| 3   | HTTP/2 reduces latency                 |
| 4   | HTTP/2 encrypts all traffic by default |

### Step 2: Verify Each Claim

| Claim | Correct |
| ----- | ------- |
| 1     | ✅      |
| 2     | ✅      |
| 3     | ✅      |
| 4     | ❌      |

### Step 3: Compute Final Score

```text
Correctness = 3 / 4 = 0.75
```

## Why Claim-Level Correctness Is Superior

- **Transparent scoring**  
  Each factual claim is evaluated independently, making it clear how the final score is derived.

- **Easy to debug failures**  
  Incorrect claims can be directly identified and inspected, enabling targeted fixes.

- **Fine-grained penalties**  
  Partial correctness is handled naturally without over-penalizing mostly correct answers.

- **Scales to long, complex answers**  
  Works reliably even when answers contain many factual components.

---

## Method Comparison

| Method          | What It Uses | Output | Insight                 |
| --------------- | ------------ | ------ | ----------------------- |
| Reference-based | Gold answer  | 0.75   | Objective but expensive |
| Reference-free  | Judge only   | 0.75   | Scalable but subjective |
| Claim-level     | Atomic facts | 0.75   | Most interpretable      |

---

## When to Use Which

- **Closed tasks** → Binary correctness
- **Open-ended QA** → Scalar correctness
- **RAG / LLM systems** → Claim-level correctness
