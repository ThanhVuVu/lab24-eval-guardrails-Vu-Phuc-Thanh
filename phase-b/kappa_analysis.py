import pandas as pd
from sklearn.metrics import cohen_kappa_score

def calculate_calibration():
    # Load human labels and LLM judge scores
    # Expected columns: sample_id, human_score, llm_score (e.g. 1-5 or Binary)
    human_file = "phase-b/human_labels.csv"
    llm_file = "phase-b/absolute_scores.csv"

    if not os.path.exists(human_file) or not os.path.exists(llm_file):
        print("Required files (human_labels.csv, absolute_scores.csv) not found for calibration.")
        # Create a template for the user
        if not os.path.exists(human_file):
            pd.DataFrame({"sample_id": range(1, 11), "human_label": [0]*10}).to_csv(human_file, index=False)
            print(f"Created template: {human_file}")
        return

    df_human = pd.read_csv(human_file)
    df_llm = pd.read_csv(llm_file)

    # Merge or align data
    # Assuming both have 'sample_id'
    try:
        # Example alignment logic
        y_human = df_human['human_label']
        y_llm = df_llm['llm_label'] # Or a mapped version of absolute scores
        
        kappa = cohen_kappa_score(y_human, y_llm)
        print(f"Cohen's Kappa Score: {kappa:.3f}")
        
        # Interpretation
        if kappa < 0: interpretation = "No agreement"
        elif kappa <= 0.2: interpretation = "Slight agreement"
        elif kappa <= 0.4: interpretation = "Fair agreement"
        elif kappa <= 0.6: interpretation = "Moderate agreement"
        elif kappa <= 0.8: interpretation = "Substantial agreement"
        else: interpretation = "Almost perfect agreement"
        
        print(f"Interpretation: {interpretation}")
        
    except Exception as e:
        print(f"Error calculating Kappa: {e}")

if __name__ == "__main__":
    import os
    calculate_calibration()
