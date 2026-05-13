# Phase A: Failure Analysis

## Danh sách 10 mẫu có điểm thấp nhất
(Bảng dữ liệu đã được tạo trong quy trình đánh giá)

## Failure Clusters

### 1. Retrieval Noise (Context Precision Low)
- **Triệu chứng**: Hệ thống truy xuất nhiều tài liệu nhưng chỉ một phần nhỏ trong đó thực sự liên quan.
- **Ví dụ**: "What are the different types of guardrails used in LLMs..." (Sample ID 37)
- **Giải pháp kỹ thuật**: Triển khai Re-ranking (ví dụ: Cohere Rerank) hoặc tối ưu hóa chiến lược chia nhỏ văn bản (chunking strategy).

### 2. Context Ignored (Faithfulness Low)
- **Triệu chứng**: Mô hình tạo câu trả lời dựa trên kiến thức nội tại thay vì sử dụng ngữ cảnh được cung cấp.
- **Ví dụ**: "What happend if LLM dont have PII detecion..." (Sample ID 38)
- **Giải pháp kỹ thuật**: Tinh chỉnh system prompt để yêu cầu mô hình chỉ được trả lời dựa trên ngữ cảnh được cung cấp.

### 3. Incomplete Answers (Context Recall Low)
- **Triệu chứng**: Câu trả lời đúng về mặt thực tế nhưng thiếu các chi tiết phụ quan trọng từ Ground Truth.
- **Ví dụ**: "What are the primary functions of LLM Guardrails..." (Sample ID 8)
- **Giải pháp kỹ thuật**: Tăng số lượng đoạn văn bản truy xuất (top_k) hoặc sử dụng chiến lược truy xuất đệ quy (recursive retrieval).
