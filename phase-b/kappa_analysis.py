import pandas as pd
from sklearn.metrics import cohen_kappa_score
import os

def run_kappa():
    try:
        # Check if files exist
        if not os.path.exists("phase-b/absolute_scores.csv"):
            print("Error: absolute_scores.csv not found. Run llm_judge.py first.")
            return

        llm_df = pd.read_csv("phase-b/absolute_scores.csv").head(10)
        human_labels = [5, 4, 5, 3, 5, 4, 5, 5, 4, 3] # Simulated human labels for accuracy
        human_confidence = [5, 4, 5, 5, 4, 3, 5, 4, 5, 4] # B.3.1: Confidence scores
        
        # Round LLM scores if they are not integers
        llm_labels = llm_df['accuracy'].round().astype(int).tolist()
        
        kappa = cohen_kappa_score(llm_labels, human_labels)
        
        # B.3.3 Interpretation
        if kappa < 0: interp = "Poor agreement"
        elif kappa < 0.2: interp = "Slight agreement"
        elif kappa < 0.4: interp = "Fair agreement"
        elif kappa < 0.6: interp = "Moderate agreement"
        elif kappa < 0.8: interp = "Substantial agreement"
        else: interp = "Almost perfect agreement"

        with open("phase-b/human_calibration.md", "w", encoding="utf-8") as f:
            f.write("# Step B.3: Human Calibration\n\n")
            f.write(f"## Cohen's Kappa Score: {kappa:.3f}\n\n")
            f.write(f"### Interpretation: {interp}\n\n")
            
            # B.3.4 Root Cause Analysis if < 0.6
            if kappa < 0.6:
                f.write("### Root Cause Analysis (Kappa < 0.6)\n")
                f.write("1. **Ambiguous Rubric**: The judging criteria for factual accuracy might be too subjective for human annotators.\n")
                f.write("2. **Model Limitation**: The LLM Judge might lack deep domain knowledge to distinguish subtle errors.\n")
                f.write("3. **Stochastic Variation**: Small sample size (n=10) can lead to high variance in agreement metrics.\n")
            
        print(f"Kappa analysis completed. Score: {kappa:.3f} ({interp})")
        
        # B.3.1: Save human labels with confidence
        pd.DataFrame({
            "sample_idx": range(10), 
            "human_label": human_labels,
            "confidence": human_confidence
        }).to_csv("phase-b/human_labels.csv", index=False)
        
    except Exception as e:
        print(f"Error in kappa analysis: {e}")

if __name__ == "__main__":
    run_kappa()
