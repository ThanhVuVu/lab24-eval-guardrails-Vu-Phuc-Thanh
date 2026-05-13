# Step B.3: Human Calibration

## Cohen's Kappa Score: 0.259

### Interpretation: Fair agreement

### Root Cause Analysis (Kappa < 0.6)
1. **Ambiguous Rubric**: Các tiêu chí đánh giá về độ chính xác thực tế có thể quá cảm tính đối với người chấm nhãn.
2. **Model Limitation**: LLM Judge có thể thiếu kiến thức chuyên sâu về tên miền để phân biệt các lỗi nhỏ.
3. **Stochastic Variation**: Kích thước mẫu nhỏ (n=10) có thể dẫn đến phương sai cao trong các chỉ số đồng thuận.
