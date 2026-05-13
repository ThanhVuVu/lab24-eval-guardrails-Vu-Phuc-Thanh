# Lab 24 — Full Evaluation & Guardrail System

## Overview
Dự án này xây dựng một hệ thống đánh giá toàn diện và lớp bảo vệ (Guardrails) cho ứng dụng RAG. Hệ thống bao gồm quy trình đánh giá tự động bằng Ragas, chấm điểm bằng LLM-as-a-Judge, và các lớp kiểm soát đầu vào/đầu ra để đảm bảo an toàn dữ liệu và tính chính xác của phản hồi. Tôi đã tích hợp thành công NVIDIA NIM endpoints để tối ưu hóa hiệu năng và độ trễ cho các lớp bảo vệ.

## Setup
`ash
pip install -r requirements.txt
export OPENAI_API_KEY=your_key_here
export NVIDIA_API_KEY=your_key_here
`

## Results Summary

### Phase A (RAGAS)
- **Test set**: 50 câu hỏi (50% simple, 25% reasoning, 25% multi-context).
- **Metrics**: Faithfulness: 0.82 | Answer Relevance: 0.88 | Context Precision: 0.90 | Context Recall: 0.85
- **Total eval cost**: ~.05 (GPT-4o-mini).
- **Identified 3 failure clusters**: Retrieval Noise, Context Ignored, Incomplete Answers (xem phase-a/failure_analysis.md).

### Phase B (LLM-Judge)
- **Cohen's kappa vs human**: 0.259 (Fair agreement).
- **Position bias**: Đã giảm thiểu thông qua kỹ thuật swap-and-average trong llm_judge.py.
- **Length bias**: Ghi nhận xu hướng Judge ưu tiên các câu trả lời dài hơn dù thông tin tương đương.

### Phase C (Guardrails)
- **PII recall**: 80.0% (Phát hiện Email, CCCD, Số điện thoại VN).
- **Topic validator**: 95.0% accuracy (Chỉ cho phép các chủ đề AI/RAG/LLM).
- **Adversarial defense**: 80.0% (Ngăn chặn Prompt Injection và Jailbreak).
- **Llama Guard latency P95**: 48.2ms (Sau khi tối ưu warmup).

### Phase D (Blueprint)
- Chi tiết thiết kế hệ thống và vận hành: [blueprint.md](phase-d/blueprint.md)

## Lessons Learned
- Việc tinh chỉnh Localized PII (Regex cho Việt Nam) kết hợp với Presidio giúp tăng đáng kể độ chính xác so với việc chỉ dùng thư viện quốc tế.
- LLM-as-a-Judge rất nhạy cảm với vị trí của câu trả lời, việc sử dụng swap-and-average là bắt buộc để có kết quả khách quan.
- Tích hợp NVIDIA NIM giúp giảm độ trễ của các lớp bảo vệ (Llama Guard) xuống mức chấp nhận được cho môi trường sản xuất.

## Demo Video
[Link Video Demo hoặc Đường dẫn file local: demo/demo_video.mp4]

---
*Dự án được thực hiện bởi Thanh Vu - Lab 24.*
