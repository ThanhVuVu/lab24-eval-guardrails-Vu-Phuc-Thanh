import os
import pandas as pd
import json
import time
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from dotenv import load_dotenv

load_dotenv()

# Configuration from .env
JUDGE_MODEL = os.getenv("JUDGE_MODEL", "meta/llama-3.1-8b-instruct")
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

# Khởi tạo model NVIDIA
model = ChatNVIDIA(model=JUDGE_MODEL, nvidia_api_key=NVIDIA_API_KEY)

def invoke_with_retry(prompt, max_retries=5, delay=2):
    for i in range(max_retries):
        try:
            return model.invoke(prompt).content.strip()
        except Exception as e:
            if "429" in str(e) and i < max_retries - 1:
                wait_time = delay * (2 ** i)
                print(f"Rate limited. Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise e

def pairwise_judge_with_swap(question, ans1, ans2):
    """Giảm thiểu position bias bằng cách chạy 2 lần với thứ tự đảo ngược."""
    prompt_template = """Question: {question}

Model A: {ans1}
Model B: {ans2}

Which answer is better? Respond only with 'A', 'B', or 'Tie'."""

    # Run 1
    response1 = invoke_with_retry(prompt_template.format(question=question, ans1=ans1, ans2=ans2))

    # Run 2 (Swap)
    response2_raw = invoke_with_retry(prompt_template.format(question=question, ans1=ans2, ans2=ans1))
    
    # Normalize response 2
    response2 = response2_raw
    if response2_raw == 'A': response2 = 'B'
    elif response2_raw == 'B': response2 = 'A'

    winner = 'Tie'
    if response1 == response2:
        winner = response1
        
    return response1, response2_raw, winner

def absolute_scoring(question, answer):
    prompt = f"""Score 1-5 trên 4 tiêu chí: 1. Factual accuracy, 2. Relevance, 3. Conciseness, 4. Helpfulness.
Question: {question}
Answer: {answer}

Respond strictly in JSON format: {{"accuracy": x, "relevance": x, "conciseness": x, "helpfulness": x}}"""
    
    response = invoke_with_retry(prompt)
    try:
        # Extract JSON from response if needed
        data = json.loads(response[response.find("{"):response.rfind("}")+1])
        # B.2.2: Overall = average of 4
        data['overall'] = sum([data['accuracy'], data['relevance'], data['conciseness'], data['helpfulness']]) / 4
        return data
    except:
        return {"accuracy": 0, "relevance": 0, "conciseness": 0, "helpfulness": 0, "overall": 0}

# Load some data for testing (30 samples)
if os.path.exists("phase-a/testset_v1.csv"):
    df = pd.read_csv("phase-a/testset_v1.csv").head(30)
    
    pairwise_results = []
    absolute_results = []
    
    for idx, row in df.iterrows():
        print(f"Judging sample {idx+1}/30...")
        # Simulate two models (e.g., GPT-4o-mini vs a slightly worse version or just the same for demo)
        q = row['question']
        a1 = row['ground_truth']
        a2 = a1[:int(len(a1)*0.8)] # Simulate a slightly less complete answer
        
        # Pairwise
        run1, run2, winner = pairwise_judge_with_swap(q, a1, a2)
        pairwise_results.append({
            "question": q,
            "run1": run1,
            "run2": run2,
            "winner": winner
        })
        
        # Absolute
        scores = absolute_scoring(q, a1)
        scores['question'] = q
        absolute_results.append(scores)
        
        # Thêm delay nhỏ giữa các sample để tránh Rate Limit
        time.sleep(1)
        
    pd.DataFrame(pairwise_results).to_csv("phase-b/pairwise_results.csv", index=False)
    pd.DataFrame(absolute_results).to_csv("phase-b/absolute_scores.csv", index=False)
    print("Phase B evaluation completed.")
else:
    print("Testset not found.")
