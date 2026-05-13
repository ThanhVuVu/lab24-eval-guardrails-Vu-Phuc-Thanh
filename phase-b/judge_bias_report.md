# Step B.4: Bias Reporting

## Verbosity Bias Analysis
- Tổng số mẫu: 30
- Số lượt thắng (không tính hòa): 24
- Số lượt câu trả lời dài hơn thắng: 24
- Tỉ lệ định kiến độ dài: 100.00%

### Đánh giá:
LLM ưu tiên câu trả lời dài hơn trong 100.00% các trường hợp. Điều này cho thấy định kiến độ dài rất cao.

## Position Bias Mitigation
- **Phương pháp**: Triển khai Swap-and-Average.
- **Kết quả**: Bằng cách chạy hai hoán vị và chỉ trao chiến thắng nếu LLM nhất quán, định kiến vị trí đã được trung hòa.
