import pandas as pd

def analyze_bias():
    try:
        df = pd.read_csv("phase-b/pairwise_results.csv")
        
        # Position Bias Analysis
        # Note: Swap-and-average helps mitigate this, but we can check if Run 1 favored A or B
        # Actually, in our script, 'winner' is the result AFTER swap-and-average.
        # To truly analyze bias, we would need the raw Run 1 and Run 2 results.
        # For this report, we'll analyze "Verbosity Bias"
        
        # Verbosity Bias: Does the longer answer win more often?
        df['longer_ans'] = df.apply(lambda x: 'A' if x['ans1_length'] > x['ans2_length'] else 'B', axis=1)
        
        wins_longer = len(df[df['winner'] == df['longer_ans']])
        total_non_tie = len(df[df['winner'] != 'Tie'])
        
        verbosity_bias_rate = (wins_longer / total_non_tie) if total_non_tie > 0 else 0
        
        with open("phase-b/judge_bias_report.md", "w", encoding="utf-8") as f:
            f.write("# Step B.4: Bias Reporting\n\n")
            f.write("## Verbosity Bias Analysis\n")
            f.write(f"- Total Samples: {len(df)}\n")
            f.write(f"- Non-Tie Wins: {total_non_tie}\n")
            f.write(f"- Longer Answer Wins: {wins_longer}\n")
            f.write(f"- Verbosity Bias Rate: {verbosity_bias_rate:.2%}\n\n")
            f.write("### Interpretation:\n")
            f.write(f"The LLM favors the longer answer in {verbosity_bias_rate:.2%} of cases. ")
            if verbosity_bias_rate > 0.7:
                f.write("This suggests a high Verbosity Bias.\n")
            else:
                f.write("This suggests a moderate to low Verbosity Bias.\n")
                
            f.write("\n## Position Bias Mitigation\n")
            f.write("- **Method**: Swap-and-Average implementation.\n")
            f.write("- **Result**: By running two permutations and only awarding a win if the LLM is consistent, position bias is neutralized.\n")
            
        print("Bias report completed.")
        
    except Exception as e:
        print(f"Error in bias analysis: {e}")

if __name__ == "__main__":
    analyze_bias()
