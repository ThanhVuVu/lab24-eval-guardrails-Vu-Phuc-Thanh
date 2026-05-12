# Dự án Đánh giá và Triển khai Guardrails cho LLM (Lab 24)

## Tổng quan dự án

Dự án này tập trung vào việc xây dựng một quy trình đánh giá toàn diện và triển khai các lớp bảo vệ (guardrails) cho các ứng dụng dựa trên mô hình ngôn ngữ lớn (LLM), đặc biệt là các hệ thống Retrieval-Augmented Generation (RAG). Mục tiêu chính là đảm bảo tính chính xác, an toàn và tin cậy của câu trả lời được tạo ra, đồng thời ngăn chặn các nội dung không phù hợp hoặc tấn công từ bên ngoài.

Trong giai đoạn đầu (Phase A), chúng tôi tập trung vào việc xây dựng bộ dữ liệu kiểm thử (testset) và sử dụng khung đánh giá Ragas để đo lường các chỉ số như tính trung thực (faithfulness), tính liên quan của câu trả lời (answer relevance) và tính liên quan của ngữ cảnh (context precision). Việc phân tích các trường hợp thất bại giúp xác định các điểm yếu trong kiến trúc RAG hiện tại. 

Giai đoạn B mở rộng việc đánh giá thông qua phương pháp so sánh cặp (pairwise) và chấm điểm tuyệt đối bằng cách sử dụng các "LLM Judge". Chúng tôi cũng thực hiện phân tích sự tương đồng với nhãn người (Human-LLM agreement) thông qua chỉ số Kappa để đảm bảo tính khách quan và tin cậy của quy trình đánh giá tự động. Ngoài ra, báo cáo về định kiến của quan tòa (Judge Bias) cũng được thực hiện để tinh chỉnh prompt cho Judge.

Giai đoạn C là bước quan trọng nhất trong việc triển khai thực tế, nơi các "Guardrails" được thiết lập ở cả đầu vào (Input Guard) và đầu ra (Output Guard). Chúng tôi kiểm thử khả năng phát hiện thông tin định danh cá nhân (PII), ngăn chặn các câu hỏi độc hại (Adversarial attacks) và đo lường độ trễ (latency) để đảm bảo hệ thống không chỉ an toàn mà còn hiệu quả về mặt hiệu năng. Toàn bộ pipeline được tích hợp để xử lý yêu cầu từ người dùng một cách an toàn nhất.

Cuối cùng, dự án cung cấp một bản thiết kế (Blueprint) chi tiết cho việc mở rộng hệ thống và một thư mục demo để trình bày cách thức hoạt động thực tế của toàn bộ pipeline đánh giá và bảo vệ này. Quy trình CI/CD cũng được thiết lập thông qua GitHub Workflows để tự động hóa việc kiểm tra chất lượng.
