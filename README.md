# Lab 24 — Full Evaluation & Guardrail System

## 1. Mục tiêu Lab

Lab này yêu cầu xây dựng một hệ thống đánh giá (evaluation) và guardrails hoàn chỉnh cho RAG pipeline theo hướng production-ready.

Bạn sẽ phải:

- Đánh giá chất lượng RAG bằng RAGAS
- Xây dựng hệ thống LLM-as-Judge
- Đo agreement với human bằng Cohen's Kappa
- Xây dựng input/output guardrails
- Benchmark latency toàn hệ thống
- Thiết kế blueprint vận hành production

---

# 2. Tổng quan Pipeline

```text
User Input
    ↓
[L1] Input Guardrails
    ├── PII Redaction
    ├── Topic Validator
    └── Injection Detection
    ↓
[L2] RAG Pipeline
    ├── Retrieval
    └── Generation
    ↓
[L3] Output Guardrails
    ├── Llama Guard 3
    └── Optional Hallucination Check
    ↓
[L4] Audit Logging
    ↓
Response to User
```

---

# 3. Repo Structure Bắt Buộc

```text
lab24-eval-guardrails-Vu-Phuc-Thanh/
├── README.md
├── requirements.txt
├── prompts.md
│
├── phase-a/
├── phase-b/
├── phase-c/
├── phase-d/
│
├── .github/workflows/
│
└── demo/
```

---

# 4. Setup Environment

## Python

```bash
python --version
```

Yêu cầu: Python >= 3.10

---

## Install dependencies

```bash
pip install -r requirements.txt
```

---

## API Keys

Cần:

- OpenAI API Key
- HuggingFace Token
- Groq API Key

```bash
export OPENAI_API_KEY=...
export HF_TOKEN=...
export GROQ_API_KEY=...
```

---

# 5. Phase A — RAGAS Evaluation (30 điểm)

## Task A.1 — Synthetic Test Set Generation (8đ)

### Việc cần làm

- Generate 50 questions
- 50% simple
- 25% reasoning
- 25% multi-context

### Output

```text
phase-a/
├── testset_v1.csv
└── testset_review_notes.md
```

### Acceptance checklist

- >= 50 rows
- Có:
  - question
  - ground_truth
  - contexts
  - evolution_type
- Manual review >= 10 câu
- Chỉnh sửa ít nhất 1 câu

---

## Task A.2 — Run RAGAS Metrics (10đ)

### Metrics

- Faithfulness
- Answer Relevancy
- Context Precision
- Context Recall

### Output

```text
phase-a/
├── ragas_results.csv
└── ragas_summary.json
```

### Benchmark targets

| Metric | Target | Min OK |
|---|---|---|
| Faithfulness | >= 0.85 | 0.75 |
| Answer Relevancy | >= 0.80 | 0.70 |
| Context Precision | >= 0.70 | 0.60 |
| Context Recall | >= 0.75 | 0.65 |

---

## Task A.3 — Failure Cluster Analysis (8đ)

### Việc cần làm

- Analyze bottom 10 questions
- Cluster failure patterns
- Root cause analysis
- Technical fixes

### Output

```text
phase-a/failure_analysis.md
```

---

## Task A.4 — CI/CD Eval Gate (4đ)

### Việc cần làm

Tạo:

```text
.github/workflows/eval-gate.yml
```

Pipeline phải:

- chạy evaluation
- fail nếu metric thấp
- upload artifact

---

# 6. Phase B — LLM-as-Judge (25 điểm)

## Task B.1 — Pairwise Judge (10đ)

### Việc cần làm

- Compare 2 RAG versions
- Swap-and-average
- Robust JSON parsing

### Output

```text
phase-b/pairwise_results.csv
```

---

## Task B.2 — Absolute Scoring (5đ)

### Chấm 4 dimensions

- accuracy
- relevance
- conciseness
- helpfulness

### Output

```text
phase-b/absolute_scores.csv
```

---

## Task B.3 — Human Calibration (8đ)

### Việc cần làm

- Human label 10 samples
- Compute Cohen's Kappa

### Output

```text
phase-b/
├── human_labels.csv
└── kappa_analysis.ipynb
```

### Interpretation

| Kappa | Ý nghĩa |
|---|---|
| <0.2 | Judge không reliable |
| 0.2-0.4 | Bias mạnh |
| 0.4-0.6 | Tạm dùng |
| >=0.6 | Production-ready |

---

## Task B.4 — Bias Report (2đ)

### Quantify ít nhất 2 biases

Ví dụ:

- Position bias
- Length bias

### Output

```text
phase-b/judge_bias_report.md
```

---

# 7. Phase C — Guardrails Stack (35 điểm)

## Task C.1 — PII Redaction (8đ)

### Detect:

- CCCD
- phone
- email
- tax code

### Output

```text
phase-c/pii_test_results.csv
```

### Targets

- Detection >= 80%
- P95 latency < 50ms

---

## Task C.2 — Topic Validator (6đ)

### Chọn 1 approach

- Embedding similarity
- LLM zero-shot
- Guardrails AI

### Targets

- Accuracy >= 75%

---

## Task C.3 — Adversarial Testing (6đ)

### Build 20 attacks

Bao gồm:

- DAN
- Roleplay
- Encoding
- Payload splitting
- Indirect injection

### Output

```text
phase-c/adversarial_test_results.csv
```

---

## Task C.4 — Output Guardrail (8đ)

### Deploy

Llama Guard 3

### Targets

- Unsafe detection >= 80%
- FP <= 20%

---

## Task C.5 — Full Stack Benchmark (7đ)

### Việc cần làm

- Integrate full stack
- Async pipeline
- Measure latency

### Output

```text
phase-c/latency_benchmark.csv
```

### Metrics

- P50
- P95
- P99

---

# 8. Phase D — Blueprint Document (10 điểm)

### Output

```text
phase-d/blueprint.md
```

### Bao gồm

- SLOs
- Architecture Diagram
- Alert Playbook
- Cost Analysis

---

# 9. Demo Video (Bắt buộc)

### Video 5 phút phải show

1. RAGAS evaluation
2. LLM Judge
3. Guardrail defense
4. Latency benchmark

---

# 10. Chiến lược đạt điểm cao

Ưu tiên:

1. Full stack chạy end-to-end
2. Benchmark đầy đủ
3. Failure analysis sâu
4. Blueprint thực tế
5. Demo video rõ ràng

```
lab24-eval-guardrails-Vu-Phuc-Thanh/
├── README.md                          # Overview 200-300 từ
├── requirements.txt
├── prompts.md                         # AI prompts đã dùng (academic integrity)
│
├── phase-a/
│   ├── testset_v1.csv
│   ├── testset_review_notes.md
│   ├── ragas_results.csv
│   ├── ragas_summary.json
│   └── failure_analysis.md
│
├── phase-b/
│   ├── pairwise_results.csv
│   ├── absolute_scores.csv
│   ├── human_labels.csv
│   ├── kappa_analysis.ipynb          # hoặc kappa_analysis.py + output
│   └── judge_bias_report.md
│
├── phase-c/
│   ├── input_guard.py
│   ├── output_guard.py
│   ├── full_pipeline.py
│   ├── pii_test_results.csv
│   ├── adversarial_test_results.csv
│   └── latency_benchmark.csv
│
├── phase-d/
│   └── blueprint.md                  # hoặc blueprint.pdf
│
├── .github/workflows/
│   └── eval-gate.yml
│
└── demo/
```
