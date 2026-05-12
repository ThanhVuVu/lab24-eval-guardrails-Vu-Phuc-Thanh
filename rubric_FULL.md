# Rubric Chấm điểm Lab 24

## 1. Thang điểm tổng quát
- **Excellent (90 - 115):** Hệ thống hoàn thiện, đạt target metrics, có làm thêm Bonus.
- **Good (75 - 89):** Đầy đủ các phase, hoạt động ổn định.
- **Pass (60 - 74):** Có lỗi nhỏ hoặc thiếu một vài tiểu mục.
- **Fail (< 60):** Không đạt ngưỡng tối thiểu, phải nộp lại.

## 2. Tiêu chí chi tiết từng Phase 

### Phase A: RAGAS (30 điểm)
- [ ] **A.1 (8đ):** Test set 50 câu, đúng tỷ lệ 50/25/25, có manual review ít nhất 10 câu.
- [ ] **A.2 (10đ):** Chạy đủ 4 core metrics, có file `ragas_summary.json` và báo cáo API cost.
- [ ] **A.3 (8đ):** Bảng Bottom 10, phân tích được ít nhất 2 Failure Clusters với giải pháp technical.
- [ ] **A.4 (4đ):** File CI/CD `.yml` đúng syntax, có threshold gate để block merge.

### Phase B: LLM-Judge (25 điểm)
- [ ] **B.1 (10đ):** Pairwise pipeline có cơ chế swap-and-average, chạy trên >= 30 câu.
- [ ] **B.2 (5đ):** Absolute scoring trên 4 chiều, có lưu file `absolute_scores.csv`.
- [ ] **B.3 (8đ):** Tính được Cohen's Kappa, giải thích kết quả đúng theo thang Kappa scale.
- [ ] **B.4 (2đ):** Định lượng được ít nhất 2 biases (vị trí/độ dài) bằng số liệu/biểu đồ.

### Phase C: Guardrails (35 điểm)
- [ ] **C.1 (8đ):** PII Guardrail đạt Recall >= 80% (cả EN/VN), Latency P95 < 50ms.
- [ ] **C.2 (6đ):** Topic Validator đạt Accuracy >= 75%, có thông báo fallback lịch sự khi bị từ chối.
- [ ] **C.3 (6đ):** Vượt qua bài test với 20 Adversarial inputs, tỷ lệ chặn (Detection rate) >= 70%.
- [ ] **C.4 (8đ):** Llama Guard 3 hoạt động, phân biệt được Safe/Unsafe responses.
- [ ] **C.5 (7đ):** Full stack tích hợp chạy được Async/Parallel, báo cáo đầy đủ P50/P95/P99 latency.

### Phase D: Blueprint Document (10 điểm)
- [ ] **D.1 (2đ):** Định nghĩa ít nhất 5 SLOs kèm ngưỡng cảnh báo (Alert thresholds).
- [ ] **D.2 (3đ):** Sơ đồ kiến trúc 4 lớp (L1-L4) rõ ràng, có chú thích latency mỗi lớp.
- [ ] **D.3 (3đ):** Playbook cho 3 tình huống sự cố (vd: Faithfulness giảm, Latency tăng).
- [ ] **D.4 (2đ):** Dự toán chi phí hàng tháng dựa trên giả định 100k queries.

## 3. Bonus Points (Tối đa +15)
- **SelfCheckGPT (+4đ):** Phát hiện ảo giác dựa trên tính nhất quán.
- **Semantic Entropy (+4đ):** Implement phương pháp Farquhar 2024 (Nature).
- **Custom VN Classifier (+5đ):** Fine-tune Llama Guard cho tiếng Việt.
- **Eval Dashboard (+3đ):** Live dashboard bằng Streamlit/Gradio.
- **Blog Post (+2đ):** Bài viết chia sẻ trên Medium/Dev.to.

## ⚠️ Điểm trừ (Penalty)
- Thiếu `prompts.md`: **Vi phạm Academic Integrity**.
- Nộp muộn: **-10% mỗi ngày** (Tối đa 3 ngày).
- Không có Video Demo: **Không thể verify kết quả**.