import asyncio
import time
from input_guard import detect_pii, validate_topic
from output_guard import llama_guard_check

async def process_request(user_input):
    start_time = time.perf_counter()
    timings = {}

    # L1: Input Guards (Parallel)
    l1_start = time.perf_counter()
    pii_task = asyncio.to_thread(detect_pii, user_input)
    topic_task = asyncio.to_thread(validate_topic, user_input)
    
    pii, on_topic = await asyncio.gather(pii_task, topic_task)
    timings['input_guards_ms'] = (time.perf_counter() - l1_start) * 1000

    if pii:
        return f"Blocked: PII detected ({', '.join(pii)})", timings
    if not on_topic:
        return "Blocked: Off-topic question.", timings

    # L2: Mock RAG / LLM Call
    l2_start = time.perf_counter()
    # response = await call_llm(user_input)
    await asyncio.sleep(0.5) # Simulate LLM latency
    response = "This is a safe response about RAG."
    timings['llm_call_ms'] = (time.perf_counter() - l2_start) * 1000

    # L3: Output Guard
    l3_start = time.perf_counter()
    is_safe = await asyncio.to_thread(llama_guard_check, response)
    timings['output_guards_ms'] = (time.perf_counter() - l3_start) * 1000

    if not is_safe:
        return "Blocked: Unsafe output generated.", timings

    timings['total_latency_ms'] = (time.perf_counter() - start_time) * 1000
    return response, timings

async def run_benchmark(num_requests=10):
    print(f"Running benchmark with {num_requests} requests...")
    latencies = []
    for i in range(num_requests):
        _, timings = await process_request("Tell me about RAG.")
        latencies.append(timings['total_latency_ms'])
        
    import pandas as pd
    df = pd.DataFrame(latencies, columns=['latency_ms'])
    print(f"P50: {df['latency_ms'].median():.2f}ms")
    print(f"P95: {df['latency_ms'].quantile(0.95):.2f}ms")
    df.to_csv("phase-c/latency_benchmark.csv", index=False)

if __name__ == "__main__":
    asyncio.run(run_benchmark())
