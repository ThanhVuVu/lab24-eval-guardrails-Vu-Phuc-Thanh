# Lab 24: Full Evaluation & Guardrail System - Final Project Documentation

**Phiên bản:** AICB-P2T3 Ngày 24 Tháng 5, 2026 

**Mục tiêu:** Xây dựng hệ thống đánh giá (Evaluation) và rào chắn (Guardrail) sẵn sàng cho môi trường sản xuất (production-ready) cho RAG pipeline.

---

## ⚙️ 1. Chuẩn bị (Prerequisites)

* 
**Môi trường:** Python $\ge 3.10$.


* 
**Thư viện chính:** `ragas`, `presidio-analyzer`, `guardrails-ai`, `transformers`, `langchain`.


* 
**Tài khoản & API:** OpenAI (Judge), Groq (Llama Guard), Hugging Face (Model access), LangSmith/Langfuse (Logging).



---

## 🧪 2. Phase A: RAGAS Evaluation (30 điểm)

Mục tiêu là xây dựng quy trình đánh giá tự động để đo lường chất lượng thực tế của hệ thống.

### Task A.1 - Synthetic Test Set Generation

Tạo bộ dữ liệu 50 câu hỏi với tỷ lệ 50% đơn giản, 25% suy luận và 25% đa ngữ cảnh.

```python
from ragas.testset import TestsetGenerator
from ragas.testset.evolutions import simple, reasoning, multi_context
from langchain_community.document_loaders import DirectoryLoader
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# Load documents
loader = DirectoryLoader("./docs", glob="**/*.md")
documents = loader.load()

# Setup generator
generator = TestsetGenerator.from_langchain(
    generator_llm=ChatOpenAI(model="gpt-4o-mini"),
    critic_llm=ChatOpenAI(model="gpt-4o-mini"),
    embeddings=OpenAIEmbeddings()
)

# Generate test set (50 items)
testset = generator.generate_with_langchain_docs(
    documents=documents,
    test_size=50,
    distributions={simple: 0.5, reasoning: 0.25, multi_context: 0.25}
)
testset.to_pandas().to_csv("phase-a/testset_v1.csv", index=False)

```

### Task A.2 - Run RAGAS 4 Metrics

Chạy đánh giá dựa trên 4 chỉ số: Faithfulness, Answer Relevancy, Context Precision và Context Recall.

```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from datasets import Dataset

# Dữ liệu kết quả từ RAG pipeline (cần tự triển khai kết nối)
# results_data = [...]

dataset = Dataset.from_list(results_data)
scores = evaluate(
    dataset,
    metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
    llm=ChatOpenAI(model="gpt-4o-mini")
)
scores.to_pandas().to_csv("phase-a/ragas_results.csv", index=False)

```

---

## ⚖️ 3. Phase B: LLM-as-Judge & Calibration (25 điểm)

Sử dụng LLM để đánh giá các khía cạnh định tính và khử các loại bias hệ thống.

### Task B.1 - Pairwise Judge (Swap-and-Average)

Kỹ thuật tráo đổi thứ tự câu trả lời để loại bỏ "Position Bias".

```python
def pairwise_judge_with_swap(question, ans1, ans2, judge_llm):
    """Giảm thiểu position bias bằng cách chạy 2 lần với thứ tự đảo ngược."""
    # Run 1: ans1, ans2
    # Run 2: ans2, ans1 (Swap)
    # Aggregate: Nếu cả hai lần đều chọn một kết quả -> Thắng. Ngược lại -> Hòa (Tie)
    pass

```

### Task B.2 - Absolute Scoring với Rubric

```python
ABSOLUTE_PROMPT = """Score 1-5 trên 4 tiêu chí: 
1. Factual accuracy, 2. Relevance, 3. Conciseness, 4. Helpfulness."""
# Triển khai hàm absolute_score để lưu vào absolute_scores.csv

```

---

## 🛡️ 4. Phase C: Guardrails Stack (35 điểm)

Thiết kế hệ thống phòng thủ đa tầng cho cả đầu vào và đầu ra.

### Task C.1 - Input Guard (PII Redaction)

Loại bỏ thông tin định danh cá nhân (PII) bằng Presidio và Regex cho ngữ cảnh Việt Nam.

```python
VN_PII = {
    "cccd": r"\b\d{12}\b",
    "phone_vn": r"(\+84|0)\d{9,10}",
    "tax_code": r"\b\d{10}(-\d{3})?\b"
}

# Sử dụng Presidio kết hợp Regex để xử lý văn bản

```

### Task C.5 - Full Stack Integration (Async)

Tích hợp các lớp bảo vệ song song để tối ưu hóa độ trễ (Latency Budget) .

```python
async def guarded_pipeline(user_input):
    # L1: Input Guards Parallel (PII + Topic)
    # L2: RAG Pipeline (LLM Call)
    # L3: Output Guard Parallel (Llama Guard 3)
    # L4: Audit Log Async (Fire-and-forget)
    return answer, timings

```

---

📊 5. Rubric Chấm điểm & Self-Assessment (100 điểm)

### Phase A: RAGAS (30đ)
* **A.1 Testset (8đ):** $\ge 50$ dòng; đủ 4 cột (question, ground_truth, contexts, evolution_type); có ghi chú manual review.
* **A.2 Metrics (10đ):** Đủ 4 metrics; có file summary JSON.
* **A.3 Failure (8đ):** Bảng Bottom 10; $\ge 2$ clusters lỗi kèm giải pháp kỹ thuật.
* **A.4 CI/CD (4đ):** Workflow `.yml` hợp lệ, có threshold gate chặn merge.

### Phase B: LLM-Judge (25đ)
* **B.1 Pairwise (10đ):** Triển khai thành công swap-and-average.
* **B.2 Absolute (5đ):** Chấm điểm 4 chiều độc lập theo rubric.
* **B.3 Calibration (8đ):** $\ge 10$ human labels; tính đúng Cohen's Kappa.
* **B.4 Bias Report (2đ):** Định lượng ít nhất 2 loại bias (vị trí/độ dài).

### Phase C: Guardrails (35đ)
* **C.1 PII (8đ):** Recall $\ge 80\%$; Latency P95 < 50ms.
* **C.2 Topic (6đ):** Accuracy $\ge 75\%$ trên 20 mẫu; có fallback message.
* **C.3 Adversarial (6đ):** Detection rate $\ge 70\%$ trên 20 mẫu tấn công.
* **C.4 Llama Guard (8đ):** Phát hiện $\ge 80\%$ unsafe outputs; FP $\le 20\%$.
* **C.5 Integration (7đ):** Chạy full stack; benchmark $\ge 100$ requests; báo cáo P50/P95/P99.

### Phase D: Blueprint (10đ)
* **D.1 (2đ):** $\ge 5$ SLOs kèm threshold cảnh báo.
* **D.2 (3đ):** Sơ đồ kiến trúc 4 lớp chi tiết.
* **D.3 (3đ):** 3 kịch bản Playbook ứng phó sự cố.
* **D.4 (2đ):** Bảng dự toán chi phí vận hành hàng tháng.

---

## 🌟 6. Bonus Points (Tối đa +15)
* **Kỹ thuật:** SelfCheckGPT (+4đ), Semantic Entropy (+4đ).
* **Địa phương hóa:** Custom VN Classifier (Fine-tune Llama Guard cho tiếng Việt) (+5đ).
* **Công cụ:** Streamlit/Gradio Dashboard (+3đ), Blog post chia sẻ learnings (+2đ).

---

**Pass Threshold:** 60/100.
**Excellent:** $\ge 90/100$.