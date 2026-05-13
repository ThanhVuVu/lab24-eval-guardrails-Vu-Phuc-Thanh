import pandas as pd
import json

df = pd.read_csv("phase-a/ragas_results.csv")

# Calculate average score per row
df['avg_score'] = df[['faithfulness', 'answer_relevancy', 'context_precision', 'context_recall']].mean(axis=1)

# Get bottom 10
bottom_10 = df.sort_values('avg_score').head(10)

# Save bottom 10 to a markdown table
markdown_table = bottom_10[['question', 'faithfulness', 'answer_relevancy', 'context_precision', 'context_recall', 'avg_score']].to_markdown(index=False)

with open("phase-a/failure_analysis.md", "w", encoding="utf-8") as f:
    f.write("# Phase A: Failure Analysis\n\n")
    f.write("## Bottom 10 Lowest-Scoring Samples\n\n")
    f.write(markdown_table)
    f.write("\n\n## Failure Clusters\n\n")
    f.write("### 1. Retrieval Noise (Context Precision Low)\n")
    f.write("- **Symptom**: The system retrieves multiple documents but only a small portion is relevant.\n")
    f.write("- **Example**: \"What are the different types of guardrails used in LLMs...\" (Sample ID 37)\n")
    f.write("- **Technical Solution**: Implement Re-ranking (e.g., Cohere Rerank) or optimize chunking strategy.\n\n")
    f.write("### 2. Context Ignored (Faithfulness Low)\n")
    f.write("- **Symptom**: The model generates answers based on internal knowledge rather than retrieved context.\n")
    f.write("- **Example**: \"What happend if LLM dont have PII detecion...\" (Sample ID 38)\n")
    f.write("- **Technical Solution**: Refine system prompt to strictly enforce answering only from provided context.\n\n")
    f.write("### 3. Incomplete Answers (Context Recall Low)\n")
    f.write("- **Symptom**: The answer is factually correct but misses key secondary details from the ground truth.\n")
    f.write("- **Example**: \"What are the primary functions of LLM Guardrails...\" (Sample ID 8)\n")
    f.write("- **Technical Solution**: Increase the number of retrieved chunks (top_k) or use a recursive retrieval strategy.\n")

print("Failure analysis completed.")
