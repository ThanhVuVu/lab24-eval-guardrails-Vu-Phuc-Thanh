import streamlit as st
import pandas as pd
import os
import json

st.set_page_config(page_title="Lab 24: Eval & Guardrails", layout="wide")

st.title("🛡️ Lab 24: Evaluation & Guardrail System")

tab1, tab2, tab3 = st.tabs(["Phase A: RAGAS", "Phase B: LLM-Judge", "Phase C: Guardrails"])

with tab1:
    st.header("RAGAS Evaluation Results")
    if os.path.exists("phase-a/ragas_summary.json"):
        with open("phase-a/ragas_summary.json") as f:
            summary = json.load(f)
        
        cols = st.columns(4)
        cols[0].metric("Faithfulness", summary.get("mean_faithfulness"))
        cols[1].metric("Answer Relevance", summary.get("mean_answer_relevance"))
        cols[2].metric("Context Precision", summary.get("mean_context_precision"))
        cols[3].metric("Context Recall", summary.get("mean_context_recall"))
        
    if os.path.exists("phase-a/ragas_results.csv"):
        df_a = pd.read_csv("phase-a/ragas_results.csv")
        st.dataframe(df_a)

with tab2:
    st.header("LLM-as-Judge Comparison")
    if os.path.exists("phase-b/pairwise_results.csv"):
        df_b = pd.read_csv("phase-b/pairwise_results.csv")
        st.dataframe(df_b)
        
    if os.path.exists("phase-b/human_calibration.md"):
        st.markdown("### Human Calibration (Cohen's Kappa)")
        with open("phase-b/human_calibration.md", "r", encoding="utf-8") as f:
            st.markdown(f.read())

with tab3:
    st.header("Guardrails & Latency")
    if os.path.exists("phase-c/latency_benchmark.csv"):
        df_c = pd.read_csv("phase-c/latency_benchmark.csv")
        st.line_chart(df_c['latency'])
        st.write(f"P95 Latency: {df_c['latency'].quantile(0.95):.4f}s")
    
    st.subheader("Live Guardrail Test")
    user_input = st.text_input("Test input for Guardrails:")
    if user_input:
        st.info("Wait, you need to run the pipeline script to see live results.")
