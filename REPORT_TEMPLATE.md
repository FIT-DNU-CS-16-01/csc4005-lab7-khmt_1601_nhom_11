# CSC4005 Lab 7 Report – Compression: KD + Quantization Trade-offs

## 1. Thông tin

- Họ tên:
- Mã sinh viên:
- Lớp:
- Link GitHub repo:
- Kỹ thuật chọn: Quantization / Knowledge Distillation / Cả hai
- Link W&B nếu dùng KD:
- Link model nếu không commit trực tiếp:

## 2. Mô tả baseline model

| Nội dung | Giá trị |
|---|---|
| Bài toán | Smart Campus Scene Classification |
| Dataset | MIT Indoor Scenes 67 subset |
| Số lớp | 5 |
| Baseline model | Vision Transformer (ViT) |
| Baseline format | ONNX |
| Baseline checkpoint/ONNX | models/vit_smartcampus.onnx |
| Baseline model size | 327.36 MB MB |

## 3. Kỹ thuật nén đã chọn

### Nếu chọn Quantization

| Thông tin | Giá trị |
|---|---|
| Loại quantization | Dynamic / Static |
| Input model | models/vit_smartcampus_clean.onnx |
| Output model | UINT8 |
| Dạng dữ liệu sau nén | INT8 |
| Công cụ | onnxruntime.quantization |

Mô tả ngắn:

```Mô hình Vision Transformer đã được nén bằng kỹ thuật Dynamic Quantization của ONNX Runtime. Quá trình quantization chuyển trọng số từ dạng FP32 sang UINT8 nhằm giảm kích thước mô hình và cải thiện tốc độ suy luận trên CPU. Trước khi quantize, mô hình ONNX được làm sạch thông tin shape inference để tránh lỗi khi thực hiện quantization.
...
```

### Nếu chọn Knowledge Distillation

| Thông tin | Giá trị |
|---|---|
| Teacher model | ... |
| Student model | ... |
| alpha | ... |
| temperature | ... |
| epochs | ... |
| batch size | ... |
| optimizer | ... |

Công thức loss sử dụng:

```text
loss = alpha * CE(student_logits, labels) + (1 - alpha) * KD_loss(student_logits, teacher_logits, T)
```

## 4. Kết quả đánh giá

| Model | Accuracy | Macro-F1 | Model size (MB) |
|---|---:|---:|---:|
| Baseline | 0.970849 | 0.962329 | 327.36 |
| Compressed | 0.970849 | 0.961822 | 82.73 |

Nhận xét:

- Accuracy giảm bao nhiêu? Accuracy giảm 0%.
- Macro-F1 giảm bao nhiêu? Macro-F1 giảm khoảng 0.000507 điểm (~0.05%).
- Mức giảm này có chấp nhận được không? Vì sao? Mức giảm rất nhỏ và gần như không ảnh hưởng đến chất lượng phân loại.

## 5. Kết quả benchmark

| Model | Batch size | Mean latency (ms) | P95 latency (ms) | Throughput (img/s) | Size (MB) |
|---|---:|---:|---:|---:|---:|
| Baseline | 1 | 272.33 | 331.59 | 3.67 | 327.36 |
| Compressed | 1 | 105.46 | 125.52 | 9.48 | 82.73 |
| Baseline | 4 | ... | ... | ... | 327.36 |
| Compressed | 4 | ... | ... | ... | 82.73 |
| Baseline | 8 | ... | ... | ... | 327.36 |
| Compressed | 8 | ... | ... | ... | 82.73 |

## 6. Bảng trade-off

| Model | Accuracy | Macro-F1 | Mean latency @bs=1 | Throughput @bs=1 | Size | Nhận xét |
|---|---:|---:|---:|---:|---:|---|
| Baseline | 0.970849 | 0.962329 | 272.33 | 3.67 img/s | 327.36 MB | Accuracy cao nhưng kích thước lớn và suy luận chậm hơn |
| Compressed | 0.970849 | 0.961822 | 105.46 ms | 9.48 img/s | 82.73 MB | Accuracy gần như giữ nguyên, nhỏ hơn nhiều và chạy nhanh hơn |

## 7. Phân tích

Trả lời:

1. Mô hình sau nén nhỏ hơn bao nhiêu phần trăm? Model size giảm từ 327.36 MB xuống 82.73 MB, tương đương giảm khoảng 74.73%.
2. Latency giảm hay tăng? Latency giảm từ 272.33 ms xuống 105.46 ms, giảm khoảng 61.27%.
3. Throughput thay đổi thế nào? Throughput tăng từ 3.67 ảnh/giây lên 9.48 ảnh/giây, tăng khoảng 158%.
4. Accuracy/F1 giảm nhiều không? Accuracy không thay đổi. Macro-F1 chỉ giảm khoảng 0.05%, mức giảm không đáng kể.
5. Nếu triển khai trên CPU hoặc edge device, bạn có chọn compressed model không? Có. Compressed model giữ nguyên accuracy trong khi giảm đáng kể kích thước và latency. Điều này giúp tiết kiệm bộ nhớ và tăng tốc độ xử lý trên CPU hoặc thiết bị biên.
6. Nếu không chọn, lý do là gì? Không áp dụng vì compressed model cho thấy hiệu quả tốt hơn baseline ở hầu hết các tiêu chí quan trọng.

## 8. Khi nào chọn KD, khi nào chọn Quantization?

Viết nhận xét ngắn:

- Khi nào quantization phù hợp? Quantization phù hợp khi đã có mô hình được huấn luyện tốt và muốn giảm kích thước mô hình hoặc tăng tốc suy luận mà không cần huấn luyện lại.
- Khi nào KD phù hợp? Knowledge Distillation phù hợp khi muốn xây dựng một mô hình nhỏ hơn hoàn toàn bằng cách học từ teacher model. Phương pháp này thường cho khả năng giảm kích thước mạnh hơn nhưng cần thời gian huấn luyện lại.   
- Nếu được làm lại, bạn sẽ chọn kỹ thuật nào cho hệ thống Smart Campus? Đối với hệ thống Smart Campus, quantization là lựa chọn phù hợp vì triển khai đơn giản, không cần huấn luyện lại và vẫn đạt được hiệu quả rất tốt về kích thước và tốc độ xử lý.

## 9. Kết luận

Tóm tắt 5–8 dòng:

- Kỹ thuật nén đã dùng;
- Kết quả chính;
- Trade-off quan trọng nhất;
- Bài học rút ra.
Trong bài thực hành này, kỹ thuật Dynamic Quantization đã được áp dụng cho mô hình Vision Transformer dưới định dạng ONNX. Kết quả cho thấy kích thước mô hình giảm từ 327.36 MB xuống còn 82.73 MB, tương đương giảm khoảng 74.73%. Đồng thời latency giảm từ 272.33 ms xuống 105.46 ms và throughput tăng từ 3.67 lên 9.48 ảnh mỗi giây. Accuracy được giữ nguyên ở mức 97.08% và Macro-F1 chỉ giảm rất nhỏ. Kết quả này cho thấy quantization là một phương pháp nén hiệu quả, giúp cải thiện khả năng triển khai mô hình trên CPU và các thiết bị có tài nguyên hạn chế mà vẫn duy trì chất lượng dự đoán. Bài học quan trọng rút ra là cần đánh giá đồng thời Accuracy, Latency và Model Size để lựa chọn mô hình phù hợp cho môi trường triển khai thực tế.
