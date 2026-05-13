# Phase D: Blueprint

## 1. System Architecture (4 Layers)
`mermaid
graph TD
    User((Người dùng)) --> L1[L1: Input Guardrails]
    L1 -->|PII đã ẩn/Chủ đề hợp lệ| L2[L2: Retrieval Engine]
    L1 -->|Không hợp lệ| Rejection[Thông báo từ chối]
    L2 --> Context[Ngữ cảnh liên quan]
    Context --> L3[L3: Generation LLM]
    L3 --> Answer[Câu trả lời thô]
    Answer --> L4[L4: Output Guardrails]
    L4 -->|An toàn| Final[Câu trả lời an toàn cuối cùng]
    L4 -->|Không an toàn| Block[Thông báo chặn do vi phạm an toàn]
    Final --> User
`

## 2. Service Level Objectives (SLOs)
| Chỉ số | Threshold | Warning Level |
| :--- | :--- | :--- |
| P95 Latency | < 2.0s | > 1.5s |
| Faithfulness | > 0.85 | < 0.80 |
| PII Recall | > 95% | < 90% |
| Topic Accuracy | > 90% | < 85% |
| Safety Violation Rate | < 1% | > 2% |

## 3. Incident Response Playbook
### Scenario 1: Hallucination Rate Spikes
- **Hành động**: Tăng tần suất lấy mẫu 'Critic LLM' trong quy trình đánh giá RAGAS để xác nhận.
- **Cách khắc phục**: Cập nhật system prompt để thắt chặt quy tắc hoặc tăng độ chồng lấp (overlap) giữa các đoạn văn bản.

### Scenario 2: Latency Degradation
- **Hành động**: Kiểm tra trạng thái API của Groq/OpenAI.
- **Cách khắc phục**: Chuyển sang mô hình nhỏ hơn (ví dụ: Llama 3 8B thay vì 70B) hoặc tối ưu hóa chỉ mục (indexing) của Vector DB.

### Scenario 3: PII Leakage
- **Hành động**: Kiểm tra nhật ký Presidio và cập nhật các mẫu Regex tùy chỉnh.
- **Cách khắc phục**: Triển khai thêm một lớp xác thực PII bằng 'Small LLM' nếu phương pháp regex thất bại.

## 4. Estimated Operational Cost (100k queries/month)
- **OpenAI (GPT-4o-mini)**: ~ (Phí Input/Output tokens)
- **Groq (Llama Guard 3)**: Miễn phí (hiện tại) hoặc ~ (nếu sử dụng nhiều)
- **Vector DB (Pinecone/Milvus)**: ~ (Gói Standard)
- **Total**: **~/tháng**
