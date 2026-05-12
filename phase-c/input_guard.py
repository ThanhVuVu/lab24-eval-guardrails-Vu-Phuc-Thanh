import re
import os
import spacy
from presidio_analyzer import AnalyzerEngine

# 1. Định nghĩa các mẫu PII đặc thù Việt Nam (Localized PII)
VN_PII_PATTERNS = {
    "phone_vn": r"\b(0|(\+84))(3|5|7|8|9)\d{8}\b",  # Định dạng số di động VN
    "cccd": r"\b\d{12}\b",                          # Căn cước công dân 12 số
    "tax_code": r"\b[1-9]\d{9}\b"                   # Mã số thuế 10 số (không bắt đầu bằng 0)
}

# 2. Khởi tạo Engine phân tích PII       
try:
    # Presidio mặc định dùng model spaCy để nhận diện thực thể (NER)
    analyzer = AnalyzerEngine()
except Exception:
    print("Warning: Presidio AnalyzerEngine failed to initialize. "
          "Please run 'python -m spacy download en_core_web_lg'")
    analyzer = None

def detect_pii(text, score_threshold=0.4):
    """
    Nhận diện PII đa lớp, kết hợp Presidio (Quốc tế) và Regex (Việt Nam).
    Ưu tiên các nhãn địa phương hóa (VN) khi có sự trùng lặp.
    """
    findings = []
    
    # --- Bước 1: Quét bằng Regex Việt Nam (Ưu tiên cao) ---
    for label, pattern in VN_PII_PATTERNS.items():
        for match in re.finditer(pattern, text):
            findings.append({
                "start": match.start(),
                "end": match.end(),
                "type": label,
                "score": 0.95  # Gán điểm tin cậy cao cho Regex chính xác
            })
    
    # --- Bước 2: Quét bằng Presidio (Các nhãn quốc tế: Email, IP, Card...) ---
    if analyzer:
        results = analyzer.analyze(text=text, entities=[], language='en', score_threshold=score_threshold)
        for res in results:
            # Kiểm tra xem vùng dữ liệu này đã được Regex VN nhận diện chưa
            is_overlap = False
            for f in findings:
                # Nếu vùng của Presidio nằm trong hoặc trùng với vùng Regex đã bắt
                if (res.start >= f["start"] and res.end <= f["end"]) or \
                   (f["start"] >= res.start and f["end"] <= res.end):
                    is_overlap = True
                    break
            
            if not is_overlap:
                # Lọc bỏ các nhãn US gây nhiễu nếu cần
                if res.entity_type in ["US_BANK_NUMBER", "US_DRIVER_LICENSE"]:
                    if res.score < 0.6: continue
                
                findings.append({
                    "start": res.start,
                    "end": res.end,
                    "type": res.entity_type,
                    "score": res.score
                })

    # --- Bước 3: Hợp nhất và trả về các nhãn duy nhất ---
    # Sắp xếp theo vị trí xuất hiện trong văn bản
    findings.sort(key=lambda x: x["start"])
    
    # Trả về danh sách các loại PII tìm thấy (không trùng lặp)
    return list(dict.fromkeys([f["type"] for f in findings]))

def validate_topic(text, allowed_topics=["RAG", "Guardrails", "AI", "LLM"]):
    """Kiểm tra xem câu hỏi có nằm trong chủ đề cho phép không."""
    text_lower = text.lower()
    return any(topic.lower() in text_lower for topic in allowed_topics)

if __name__ == "__main__":
    # Test cases bao gồm cả PII quốc tế và Việt Nam
    test_text = "Lien he qua 0912345678 hoac email test@example.com. Hoi ve RAG."
    
    print("--- Testing Input Guardrails ---")
    pii_found = detect_pii(test_text)
    is_on_topic = validate_topic(test_text)
    
    print(f"Input Text: {test_text}")
    print(f"PII Detected: {pii_found}")
    print(f"Is On Topic: {is_on_topic}")
