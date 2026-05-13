import re
import time
import asyncio
from presidio_analyzer import AnalyzerEngine
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from dotenv import load_dotenv
import os

load_dotenv()

# C.1: PII Guardrail
class PIIGuardrail:
    def __init__(self):
        self.analyzer = AnalyzerEngine()
        self.vn_pii_patterns = {
            "cccd": r"\b\d{12}\b",
            "phone_vn": r"(\+84|0)\d{9,10}",
            "tax_code": r"\b\d{10}(-\d{3})?\b"
        }

    def detect_pii(self, text):
        # Presidio for standard PII
        results = self.analyzer.analyze(text=text, entities=["EMAIL_ADDRESS", "IP_ADDRESS", "PERSON", "PHONE_NUMBER"], language='en')
        
        # Regex for VN PII
        vn_matches = []
        for entity, pattern in self.vn_pii_patterns.items():
            for match in re.finditer(pattern, text):
                vn_matches.append({"entity_type": entity.upper(), "start": match.start(), "end": match.end()})
        
        return results, vn_matches

# C.2: Topic Validator
class TopicValidator:
    def __init__(self, allowed_topics=["AI", "Python", "Guardrails", "RAG", "Evaluation"]):
        self.allowed_topics = allowed_topics

    def is_on_topic(self, text):
        # Simple keyword matching for demo, could be an LLM call
        text_lower = text.lower()
        return any(topic.lower() in text_lower for topic in self.allowed_topics)

# C.4: Llama Guard 3 Integration (via NVIDIA NIM)
class LlamaGuard:
    def __init__(self):
        self.model_name = os.getenv("GUARDRAILS_MODEL", "meta/llama-guard-4-12b")
        self.api_key = os.getenv("NVIDIA_API_KEY")
        self.model = ChatNVIDIA(model=self.model_name, nvidia_api_key=self.api_key)

    def check_safety(self, text):
        try:
            # Llama Guard 3 on NVIDIA NIM
            response = self.model.invoke(f"Check the following text for safety violations:\n\n{text}")
            return response.content
        except Exception as e:
            return f"Error: {e}"

# C.5: Full Stack Async Pipeline
async def guarded_pipeline(user_input):
    start_time = time.perf_counter()
    pii_guard = PIIGuardrail()
    topic_validator = TopicValidator()
    llama_guard = LlamaGuard()

    # L1: Input Guards Parallel
    l1_start = time.perf_counter()
    pii_results, vn_pii = pii_guard.detect_pii(user_input)
    on_topic = topic_validator.is_on_topic(user_input)
    l1_latency = time.perf_counter() - l1_start
    
    if not on_topic:
        return "Off-topic question rejected.", {"latency": time.perf_counter() - start_time, "l1_latency": l1_latency, "l3_latency": 0}

    # L2: Simulate RAG Generation
    # (In real scenario, this is where the RAG call happens)
    llm_output = f"Processed: {user_input}"
    
    # L3: Output Guard
    l3_start = time.perf_counter()
    safety_result = llama_guard.check_safety(llm_output)
    l3_latency = time.perf_counter() - l3_start
    
    total_latency = time.perf_counter() - start_time
    return llm_output, {"latency": total_latency, "l1_latency": l1_latency, "l3_latency": l3_latency, "safety": safety_result, "pii_found": len(pii_results) + len(vn_pii)}

if __name__ == "__main__":
    # Test
    async def test():
        ans, meta = await guarded_pipeline("Tell me about Guardrails in AI.")
        print(f"Answer: {ans}")
        print(f"Metadata: {meta}")

    asyncio.run(test())
