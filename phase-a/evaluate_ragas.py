import os
import pandas as pd
import json
from datasets import Dataset
from ragas.metrics import Faithfulness, AnswerRelevancy, ContextPrecision, ContextRecall
from ragas import evaluate
from langchain_nvidia_ai_endpoints import ChatNVIDIA, NVIDIAEmbeddings
from dotenv import load_dotenv
import ast

load_dotenv()

# Configuration from .env
EVAL_MODEL = os.getenv("JUDGE_MODEL", "meta/llama-3.1-8b-instruct")
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

def run_evaluation():
    if not os.path.exists("phase-a/testset_v1.csv"):
        print("Testset not found.")
        return

    # Load and convert string representations of lists back to actual lists
    df = pd.read_csv("phase-a/testset_v1.csv")
    
    def parse_list(val):
        if isinstance(val, str) and val.startswith('['):
            try:
                return ast.literal_eval(val)
            except:
                return [val]
        return [val] if not isinstance(val, list) else val

    if 'response' not in df.columns:
        df['response'] = df['ground_truth']
    
    # Ensure contexts are lists of strings
    if 'retrieved_contexts' not in df.columns:
        df['retrieved_contexts'] = df['contexts'].apply(parse_list)
    else:
        df['retrieved_contexts'] = df['retrieved_contexts'].apply(parse_list)
        
    # Ánh xạ từ tên cột thực tế sang chuẩn Ragas để engine nhận diện được
    if 'contexts' in df.columns:
        df['contexts'] = df['contexts'].apply(parse_list)
    
    # Đảm bảo các cột khớp với chuẩn Ragas (question, contexts, ground_truth, answer)
    if 'answer' not in df.columns and 'ground_truth' in df.columns:
        df['answer'] = df['ground_truth']
    
    # Ragas needs specific columns in the Dataset
    dataset = Dataset.from_pandas(df[['question', 'contexts', 'ground_truth', 'answer']])
    
    # Dùng trực tiếp ChatNVIDIA (LangChain) cho các Legacy Metrics
    eval_llm = ChatNVIDIA(
        model=EVAL_MODEL, 
        nvidia_api_key=NVIDIA_API_KEY
    )
    eval_embeddings = NVIDIAEmbeddings(
        model="nvidia/nv-embedqa-e5-v5", 
        nvidia_api_key=NVIDIA_API_KEY
    )
    
    # Khôi phục đầy đủ metrics
    metrics = [
        Faithfulness(llm=eval_llm),
        AnswerRelevancy(llm=eval_llm, embeddings=eval_embeddings),
        ContextPrecision(llm=eval_llm),
        ContextRecall(llm=eval_llm)
    ]
    
    from ragas.run_config import RunConfig
    run_config = RunConfig(max_workers=1)
    
    print(f"Running RAGAS evaluation using NVIDIA NIM: {EVAL_MODEL} (max_workers=1)...")
    result = evaluate(
        dataset,
        metrics=metrics,
        llm=eval_llm,
        run_config=run_config
    )
    
    result_df = result.to_pandas()
    # Đổi tên cột về chuẩn rubric sau khi Ragas đã xử lý xong
    result_df = result_df.rename(columns={
        'user_input': 'question',
        'reference': 'ground_truth',
        'retrieved_contexts': 'contexts'
    })
    print(f"Standardized Columns: {result_df.columns.tolist()}")
    result_df.to_csv("phase-a/ragas_results.csv", index=False)
    
    summary = {
        "mean_faithfulness": result_df['faithfulness'].mean(),
        "mean_answer_relevance": result_df['answer_relevancy'].mean(),
        "mean_context_precision": result_df['context_precision'].mean(),
        "mean_context_recall": result_df['context_recall'].mean(),
        "total_samples": len(result_df)
    }
    
    with open("phase-a/ragas_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
        
    print("Evaluation completed. Results saved to phase-a/")

if __name__ == "__main__":
    run_evaluation()
