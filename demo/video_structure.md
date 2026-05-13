# Demo Video Structure (5 Minutes)

## Section 1: Introduction (1:00)
- Briefly explain the RAG Evaluation & Guardrails project.
- Show the project goals and architecture (4 layers).

## Section 2: Evaluation Pipeline (1:30)
- Demonstrate the Ragas evaluation process.
- Show the `failure_analysis.md` and how we identified system weaknesses.
- Show the LLM-as-a-Judge pairwise comparison results.

## Section 3: Guardrails in Action (1:30)
- Run a live test or show recorded examples of PII detection.
- Show the Topic Validator blocking an off-topic question.
- Show Llama Guard blocking an unsafe response.

## Section 4: Operations & CI/CD (1:00)
- Show the `benchmark_report.md` with latency metrics.
- Show the GitHub Action (`eval-gate.yml`) acting as a quality gate.
- Conclusion and final results.
