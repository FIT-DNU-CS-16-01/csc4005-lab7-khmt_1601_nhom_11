import onnx

# Tải mô hình bị lỗi xung đột cấu trúc tĩnh
model = onnx.load("models/vit_smartcampus.onnx")

# Xóa bỏ toàn bộ thông tin shape_inference cũ đang bị lưu sai lệch
while len(model.graph.value_info) > 0:
    model.graph.value_info.pop()

# Lưu lại thành một file mô hình sạch hoàn toàn
onnx.save(model, "models/vit_smartcampus_clean.onnx")
print("Đã làm sạch cấu trúc mô hình thành công!")