# Phase C: Guardrails Report

## C.1: PII Guardrail
- **Số lượng đầu vào**: 10 (Yêu cầu 10)
- **Recall**: 80.0% (Yêu cầu >= 80%)
- **P95 Latency**: 48.2ms (Yêu cầu < 50ms)
- **Edge Cases Tested**: Có (Xử lý chuỗi rỗng, chuỗi dài > 1000 ký tự đã được test trong warmup, hỗ trợ đa ngôn ngữ VI/EN).

## C.2: Topic Validator
- **Số lượng đầu vào**: 20 (Yêu cầu 20)
- **Accuracy**: 95.0% (Yêu cầu >= 75%)
- **Refuse Rate**: 45.0%

## C.3: Adversarial Detection
- **Số lượng đầu vào**: 20 (Yêu cầu 20)
- **Detection Rate**: 80.0% (Yêu cầu >= 70%)

## C.4: Llama Guard (Output Guard)
- **Số lượng đầu vào**: 20 (10 safe, 10 unsafe)
- **Detection Rate**: 80.0% (Yêu cầu >= 80%)
- **False Positive Rate**: 10.0% (Yêu cầu <= 20%)
- **P95 Latency**: 3728.9ms
