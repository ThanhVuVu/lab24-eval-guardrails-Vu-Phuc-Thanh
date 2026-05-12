# Lab 24 — Detailed Rubric

# Tổng điểm

| Phase | Điểm |
|---|---|
| Phase A | 30 |
| Phase B | 25 |
| Phase C | 35 |
| Phase D | 10 |
| Bonus | +15 |

Pass threshold: 60  
Excellent: >= 90

---

# Phase A — RAGAS Evaluation (30đ)

## A.1 — Synthetic Test Set (8đ)

| Hạng mục | Điểm |
|---|---|
| >= 50 rows | 1 |
| Đúng 4 columns | 1 |
| Distribution 50/25/25 | 2 |
| Manual review >= 10 | 2 |
| Có edit ít nhất 1 câu | 2 |

### Mất điểm thường gặp

- Questions vô nghĩa
- Không review thủ công
- Distribution lệch

---

## A.2 — RAGAS Metrics (10đ)

| Hạng mục | Điểm |
|---|---|
| Chạy đủ 4 metrics | 4 |
| Save CSV + JSON | 2 |
| Cost logging | 1 |
| Analysis metric yếu | 3 |

---

## A.3 — Failure Analysis (8đ)

| Hạng mục | Điểm |
|---|---|
| Bottom 10 table | 2 |
| >= 2 clusters | 2 |
| Root cause đúng | 2 |
| Proposed fix technical | 2 |

### Mất điểm

- Chỉ viết "improve prompt"
- Không quantify

---

## A.4 — CI/CD Eval Gate (4đ)

| Hạng mục | Điểm |
|---|---|
| YAML valid | 1 |
| Threshold gate | 2 |
| Artifact upload | 1 |

---

# Phase B — LLM-as-Judge (25đ)

## B.1 — Pairwise Judge (10đ)

| Hạng mục | Điểm |
|---|---|
| Swap-and-average | 4 |
| Robust parsing | 2 |
| >= 30 samples | 2 |
| CSV đúng format | 2 |

---

## B.2 — Absolute Scoring (5đ)

| Hạng mục | Điểm |
|---|---|
| 4 dimensions | 2 |
| Overall average đúng | 1 |
| Save CSV | 2 |

---

## B.3 — Human Calibration (8đ)

| Hạng mục | Điểm |
|---|---|
| Human labels đầy đủ | 2 |
| Compute kappa | 2 |
| Interpretation đúng | 2 |
| Root cause analysis | 2 |

### Kappa guide

| Kappa | Chất lượng |
|---|---|
| <0.2 | Poor |
| 0.2-0.4 | Weak |
| 0.4-0.6 | Moderate |
| >=0.6 | Production-ready |

---

## B.4 — Bias Report (2đ)

| Hạng mục | Điểm |
|---|---|
| >= 2 quantified biases | 1 |
| Có chart/table | 1 |

---

# Phase C — Guardrails (35đ)

## C.1 — PII Guardrail (8đ)

| Hạng mục | Điểm |
|---|---|
| 10 test inputs | 2 |
| Detection >= 80% | 2 |
| P95 < 50ms | 2 |
| Edge cases | 2 |

---

## C.2 — Topic Validator (6đ)

| Hạng mục | Điểm |
|---|---|
| Implement thành công | 2 |
| Accuracy >= 75% | 2 |
| Refuse handling tốt | 2 |

---

## C.3 — Adversarial Testing (6đ)

| Hạng mục | Điểm |
|---|---|
| 20 attacks | 2 |
| Detection >= 70% | 2 |
| FP <= 10% | 2 |

---

## C.4 — Output Guardrail (8đ)

| Hạng mục | Điểm |
|---|---|
| Llama Guard chạy | 2 |
| Test safe/unsafe | 2 |
| Detection >= 80% | 2 |
| Latency benchmark | 2 |

---

## C.5 — Full Stack Benchmark (7đ)

| Hạng mục | Điểm |
|---|---|
| End-to-end chạy | 2 |
| >=100 requests benchmark | 2 |
| P50/P95/P99 | 2 |
| Overhead analysis | 1 |

---

# Phase D — Blueprint (10đ)

## D.1 — SLO Definition (2đ)

>= 5 SLOs với:

- target
- threshold
- severity

---

## D.2 — Architecture Diagram (3đ)

Phải có:

- 4 layers
- data flow
- latency annotation

---

## D.3 — Alert Playbook (3đ)

>= 3 incidents với:

- detection
- root cause
- investigation
- resolution

---

## D.4 — Cost Analysis (2đ)

- monthly projection
- breakdown
- optimization ideas

---

# Submission Checklist

| Hạng mục | Bắt buộc |
|---|---|
| README.md | ✓ |
| requirements.txt | ✓ |
| prompts.md | ✓ |
| Demo video | ✓ |
| Repo structure đúng | ✓ |
| Commit history | ✓ |

---

# Bonus (+15)

| Bonus | Điểm |
|---|---|
| Cross-judge protocol | +3 |
| SelfCheckGPT | +4 |
| Semantic entropy | +4 |
| NeMo Guardrails | +3 |
| Prompt Guard | +2 |
| Custom VN classifier | +5 |
| Eval dashboard | +3 |
| Blog post | +2 |

---

# Checklist để tối đa điểm

## Quan trọng nhất

- Full stack chạy end-to-end
- Metrics đầy đủ
- Benchmark thật
- Failure analysis sâu
- Bias analysis
- Async benchmark
- Production thinking

---

# Điều giúp đạt Excellent (>=90)

## Technical depth

- Failure clusters chất lượng
- Root cause analysis thật
- Guardrails robust

## Engineering quality

- Clean repo
- Reproducible
- CI/CD
- Logging

## Production mindset

- Latency budget
- Cost analysis
- Monitoring
- Alert playbook
