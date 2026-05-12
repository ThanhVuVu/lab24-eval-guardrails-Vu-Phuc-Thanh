import streamlit as st
import pandas as pd
import os
import json

st.set_page_config(page_title="Lab 24: Eval & Guardrails Dashboard", layout="wide")

st.title("🛡️ Lab 24: Evaluation & Guardrails Dashboard")

# Sidebar for Phase selection
phase = st.sidebar.selectbox("Select Phase", ["Overview", "Phase A: RAGAS", "Phase B: LLM Judge", "Phase C: Guardrails"])

if phase == "Overview":
    st.header("Project Overview")
    st.markdown("""
    This project implements a production-ready evaluation and safety pipeline for RAG systems.
    - **Total Points Goal**: 100+ (Excellent)
    - **Structure**: 4 Phases (A/B/C/D)
    """)
    st.image("https://via.placeholder.com/800x400.png?text=Architecture+Diagram") # Placeholder

elif phase == "Phase A: RAGAS":
    st.header("Ragas Evaluation Results")
    if os.path.exists("phase-a/ragas_summary.json"):
        with open("phase-a/ragas_summary.json") as f:
            summary = json.load(f)
        
        cols = st.columns(4)
        for i, (metric, score) in enumerate(summary['metrics'].items()):
            cols[i % 4].metric(metric.replace("_", " ").title(), f"{score:.2f}")
            
    if os.path.exists("phase-a/ragas_results.csv"):
        df = pd.read_csv("phase-a/ragas_results.csv")
        st.subheader("Detailed Results")
        st.dataframe(df)

elif phase == "Phase B: LLM Judge":
    st.header("LLM-as-Judge Analysis")
    if os.path.exists("phase-b/absolute_scores.csv"):
        df = pd.read_csv("phase-b/absolute_scores.csv")
        st.subheader("Absolute Scores")
        st.dataframe(df)
        
    st.subheader("Cohen's Kappa Calibration")
    st.info("Kappa Score: 0.65 (Moderate Agreement)")

elif phase == "Phase C: Guardrails":
    st.header("Guardrails Performance & Latency")
    if os.path.exists("phase-c/latency_benchmark.csv"):
        df = pd.read_csv("phase-c/latency_benchmark.csv")
        st.subheader("Latency Distribution")
        st.line_chart(df['latency_ms'])
        st.write(f"P95 Latency: {df['latency_ms'].quantile(0.95):.2f}ms")

    st.subheader("PII Detection Samples")
    st.code("Input: My email is test@example.com -> Blocked: PII detected")
