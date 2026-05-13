import asyncio
import time
import pandas as pd
from guardrails import guarded_pipeline

async def run_benchmark(n=100):
    print(f"Starting benchmark for {n} requests...")
    latencies = []
    
    # Load real questions from testset for variety
    try:
        testset = pd.read_csv("phase-a/testset_v1.csv")
        # Repeat or shuffle to get n samples
        inputs = testset['question'].tolist()
        while len(inputs) < n:
            inputs.extend(testset['question'].tolist())
        inputs = inputs[:n]
    except Exception as e:
        print(f"Warning: Could not load testset, using fallback inputs. Error: {e}")
        inputs = ["What is RAG?", "How to use guardrails?", "Explain LLM evaluation."] * (n // 3 + 1)
        inputs = inputs[:n]
    
    for i, text in enumerate(inputs):
        if (i + 1) % 10 == 0:
            print(f"Benchmarking request {i+1}/{n}...")
        
        try:
            # Note: guarded_pipeline handles LLM calls which might hit rate limits.
            # If it fails, we catch it here to keep benchmarking.
            _, meta = await guarded_pipeline(text)
            latencies.append({
                'total': meta['latency'],
                'l1': meta.get('l1_latency', 0),
                'l3': meta.get('l3_latency', 0)
            })
        except Exception as e:
            print(f"Request {i+1} failed: {e}")
            time.sleep(2) # Backoff
            
        # Small sleep to be polite to the API
        await asyncio.sleep(0.5)
        
    if not latencies:
        print("Error: No latency data collected.")
        return

    df = pd.DataFrame(latencies)
    stats = {
        "Total P50": df['total'].quantile(0.5),
        "Total P95": df['total'].quantile(0.95),
        "Total P99": df['total'].quantile(0.99),
        "L1 P95": df['l1'].quantile(0.95),
        "L3 P95": df['l3'].quantile(0.95)
    }
    
    print("\nLatency Benchmark Results:")
    for k, v in stats.items():
        print(f"{k}: {v:.4f}s")
    
    df.to_csv("phase-c/latency_benchmark.csv", index=False)
    
    # Save results to a report
    with open("phase-c/benchmark_report.md", "w", encoding="utf-8") as f:
        f.write("# Phase C: Latency Benchmark Report\n\n")
        f.write(f"Benchmark performed on {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"- **Total Requests**: {len(latencies)}\n")
        f.write(f"- **Total Latency P50**: {stats['Total P50']:.4f}s\n")
        f.write(f"- **Total Latency P95**: {stats['Total P95']:.4f}s\n")
        f.write(f"- **Total Latency P99**: {stats['Total P99']:.4f}s\n")
        f.write(f"- **L1 Latency P95 (Input Guard)**: {stats['L1 P95'] * 1000:.1f}ms\n")
        f.write(f"- **L3 Latency P95 (Output Guard)**: {stats['L3 P95'] * 1000:.1f}ms\n\n")
        f.write("*Note: This benchmark includes Input Guard (PII + Topic) and Output Guard (Llama Guard).*\n")
        
if __name__ == "__main__":
    asyncio.run(run_benchmark())
