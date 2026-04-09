# 📋 TV5 PLAYBOOK — Hướng Dẫn Thực Thi DevOps & QA

> **Phụ trách:** TV5 (ANH HUY) - DevOps & QA  
> **Thời kỳ:** 30/03 → 15/04/2026  
> **Mục tiêu:** Triển khai, Kiểm thử, Tài liệu

---

## 📖 Tổng Quan Vai Trò TV5

TV5 là **DevOps Engineer + QA Tester + Tech Writer**, chịu trách nhiệm:

1. **🐳 Triển khai Docker** - Containerize tất cả dịch vụ
2. **🧪 Kiểm thử Hệ thống** - E2E test, API test, security test
3. **📚 Tài liệu** - API docs, README, deployment guide
4. **⚙️ Quản Lý Cấu Hình** - .env, secrets, configs
5. **🔍 Đảm Bảo Chất Lượng** - Báo cáo lỗi, kiểm tra hiệu suất
6. **📊 Hoàn Thành Dự Án** - Báo cáo cuối, thuyết trình

---

## 🏗️ Giai Đoạn 1: MVP (30/03 → 07/04)

### Tuần 1: Thiết Lập Hạ Tầng

#### Ngày 30/03
```bash
# ✅ Công việc: Thiết lập Git & cấu trúc dự án
- Khởi tạo kho Git với .gitignore
- Tạo cấu trúc thư mục (backend/, frontend/, data/, docs/)
- Viết template Dockerfile cho backend & frontend
- Tạo framework docker-compose.yml

# ✅ Sản phẩm:
- Kho Git sẵn sàng
- Cấu hình ảnh Docker cơ bản
- Template .env.example tạo xong
```

**Lệnh:**
```bash
git init
git config user.name "TV5"
git config user.email "tv5@ai-analyst.local"

# Tạo các file cơ bản
cat > Dockerfile.backend <<EOF
# (từ template)
EOF

cat > docker-compose.yml <<EOF
# (từ template)
EOF

git add .
git commit -m "feat: khởi tạo docker setup"
```

#### Ngày 31/03
```bash
# ✅ Công việc: Kiểm thử ảnh cục bộ
- Xây dựng backend Dockerfile
- Xây dựng frontend Dockerfile
- Kiểm thử health endpoints
- Ghi lại quá trình xây dựng

# ✅ Sản phẩm:
- Cả hai ảnh xây dựng thành công
- Health check hoạt động
- BUILD_GUIDE.md viết xong
```

**Lệnh:**
```bash
# Xây dựng backend
cd backend
docker build -t ai-analyst-backend:latest .
docker run -p 8000:8000 --env-file ../.env ai-analyst-backend

# Xây dựng frontend
cd ../frontend
docker build -t ai-analyst-frontend:latest .
docker run -p 8501:8501 ai-analyst-frontend

# Kiểm tra
curl http://localhost:8000/api/v1/health
```

#### Ngày 01/04
```bash
# ✅ Công việc: E2E Docker compose
- Viết docker-compose.yml hoàn chỉnh
- Kiểm thử với .env mẫu
- Xác minh kết nối mạng
- Ghi lại cách khắc phục sự cố

# ✅ Sản phẩm:
- docker-compose.yml được xác minh
- Cả hai dịch vụ khởi động với `docker-compose up -d`
- Health checks hoạt động
```

**Lệnh:**
```bash
# Kiểm thử toàn bộ hệ thống
docker-compose build --no-cache
docker-compose up -d
sleep 30
docker-compose ps
curl http://localhost:8000/api/v1/health
curl http://localhost:8501  # Nên tải được
```

### Tuần 2: Kiểm Thử & Tài Liệu

#### Ngày 02/04
```bash
# ✅ Công việc: Kiểm Thử API
- Kiểm thử endpoint /api/v1/health
- Kiểm thử endpoint /api/v1/schema
- Kiểm thử /api/v1/chat/query với các truy vấn mẫu
- Ghi lại tất cả phản hồi

# ✅ Sản phẩm:
- API_TEST_REPORT.md
- Postman collection (.json)
- Kết quả kiểm thử
```

**Lệnh:**
```bash
# Kiểm tra sức khỏe
curl http://localhost:8000/api/v1/health

# Kiểm tra lược đồ
curl http://localhost:8000/api/v1/schema

# Kiểm tra truy vấn
curl -X POST http://localhost:8000/api/v1/chat/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Truy vấn kiểm thử?"}'
```

#### Ngày 03/04
```bash
# ✅ Công việc: Kiểm Thử Giao Diện Người Dùng
- Kiểm thử đầu vào/đầu ra trò chuyện
- Kiểm thử hiển thị kết quả
- Kiểm thử hiển thị code SQL
- Ghi lại luồng UI

# ✅ Sản phẩm:
- FRONTEND_TEST_REPORT.md
- Ảnh chụp màn hình
- Tài liệu luồng người dùng
```

#### Ngày 04/04
```bash
# ✅ Công việc: Kiểm Thử Bảo Mật
- Kiểm thử cố gắng tiêm SQL
- Kiểm thử đầu vào ranh giới (truy vấn lớn)
- Kiểm thử xử lý lỗi
- Ghi lại phát hiện bảo mật

# ✅ Sản phẩm:
- SECURITY_TEST_REPORT.md
- Đánh giá lỗ hổng
```

**Ví Dụ Kiểm Thử Bảo Mật:**
```bash
# Cố gắng tiêm SQL
curl -X POST http://localhost:8000/api/v1/chat/query \
  -H "Content-Type: application/json" \
  -d '{"question": "x; DROP TABLE orders; --"}'

# Nên bị chặn bởi trình xác thực SQL

# Cố gắng truy vấn lớn
curl -X POST http://localhost:8000/api/v1/chat/query \
  -H "Content-Type: application/json" \
  -d '{"question": "'"$(python -c 'print("x"*5000)')"'"}'

# Nên hết thời gian hoặc bị từ chối
```

#### Ngày 05/04 - Ngày Dự Phòng
```bash
# ✅ Công việc: Tài liệu & Sửa Lỗi
- Viết API_DOCS.md
- Viết README.md
- Sửa bất kỳ vấn đề nào tìm thấy trong kiểm thử
- Cập nhật Dockerfiles nếu cần

# ✅ Sản phẩm:
- Tài liệu hoàn chỉnh
- Tất cả kiểm thử vượt qua
```

#### Ngày 06/04
```bash
# ✅ Công việc: Kiểm Thử Tích Hợp
- Kiểm thử luồng công việc end-to-end
- Load testing (nhiều truy vấn)
- Benchmark hiệu suất
- Kiểm thử căng thẳng

# ✅ Sản phẩm:
- PERFORMANCE_TEST_REPORT.md
- Kết quả load test
- Khuyến nghị tối ưu hóa
```

**Tập Lệnh Kiểm Thử Tải:**
```bash
#!/bin/bash
# Kiểm thử tải 10 truy vấn đồng thời

for i in {1..10}; do
  curl -X POST http://localhost:8000/api/v1/chat/query \
    -H "Content-Type: application/json" \
    -d "{\"question\": \"Truy vấn số $i\"}" &
done

wait
echo "Tất cả truy vấn hoàn thành"
```

#### Ngày 07/04 - Demo MVP
```bash
# ✅ Công việc: Xác Minh & Demo Cuối
- Chạy qua toàn bộ hệ thống
- Xác minh tất cả thành phần hoạt động
- Chuẩn bị demo cho nhà tài trợ
- Ghi lại bất kỳ vấn đề nào

# ✅ Sản phẩm:
- DEMO_CHECKLIST.md (tất cả các mục được kiểm tra)
- Hệ thống sẵn sàng để thuyết trình
- Hoàn thành sửa lỗi
```

**Danh Sách Kiểm Tra Demo MVP:**
```
✅ Docker-compose up -d hoạt động
✅ Endpoint sức khỏe phản hồi
✅ Lược đồ tải chính xác
✅ Truy vấn tạo SQL
✅ Kết quả hiển thị ở giao diện trước
✅ Biểu đồ hiển thị (nếu Giai Đoạn 1)
✅ Xử lý lỗi hoạt động
✅ Hiệu suất có thể chấp nhận
```

---

## 🚀 Giai Đoạn 2: Tính Năng Nâng Cao (08/04 → 14/04)

### Tuần 3: Kiểm Thử & Tối Ưu Hóa Nâng Cao

#### Ngày 08/04
```bash
# ✅ Công việc: Kiểm Thử Biểu Đồ Tính Năng Mới
- Kiểm thử tạo biểu đồ Plotly
- Kiểm thử phản ứng biểu đồ
- Kiểm tra hiệu suất trên các tập dữ liệu lớn
- Kiểm thử tương thích trình duyệt

# ✅ Sản phẩm:
- CHART_TEST_REPORT.md
```

#### Ngày 09/04
```bash
# ✅ Công việc: Kiểm Thử Lịch Sử Trò Chuyện
- Kiểm thử tạo phiên
- Kiểm thử độ bền tin nhắn
- Kiểm thử truy lục lịch sử
- Hiệu suất với lịch sử lớn

# ✅ Sản phẩm:
- HISTORY_TEST_REPORT.md
```

#### Ngày 10/04
```bash
# ✅ Công việc: Kiểm Thử Hồi Quy
- Chạy lại tất cả kiểm thử Giai Đoạn 1
- Kiểm thử các tính năng mới không phá vỡ cái cũ
- Kiểm thử tích hợp đầy đủ
- Kiểm tra hồi quy hiệu suất

# ✅ Sản phẩm:
- REGRESSION_TEST_REPORT.md
- Tất cả kiểm thử vượt qua ✅
```

#### Ngày 11/04
```bash
# ✅ Công việc: Cập Nhật Tài Liệu
- Tài liệu API hoàn chỉnh
- Hướng dẫn triển khai hoàn chỉnh
- Hướng dẫn đánh giá giáo viên viết
- Thêm sơ đồ kiến trúc

# ✅ Sản phẩm:
- Tất cả tài liệu được hoàn thiện
- QUICKSTART_FOR_TEACHERS.md
```

#### Ngày 12/04
```bash
# ✅ Công việc: Tối Ưu Hóa Hiệu Suất
- Tối ưu hóa truy vấn cơ sở dữ liệu
- Kiểm tra triển khai bộ nhớ cache
- Tối ưu hóa hiệu suất giao diện trước
- Tối ưu hóa kích thước ảnh Docker

# ✅ Sản phẩm:
- OPTIMIZATION_REPORT.md
- Đường cơ sở hiệu suất
```

#### Ngày 13/04
```bash
# ✅ Công việc: QA Cuối & Sửa Lỗi
- UAT (Kiểm Thử Chấp Nhận Người Dùng)
- Sửa lỗi quan trọng
- Điều chỉnh hiệu suất
- Kiểm thử lại bảo mật

# ✅ Sản phẩm:
- UAT_REPORT.md
- Tất cả lỗi được sửa
- Hiệu suất được cải thiện
```

#### Ngày 14/04 - Tập Dượt
```bash
# ✅ Công việc: Tập Dượt Thuyết Trình Cuối
- Chạy demo cho đội
- Kiểm thử luồng thuyết trình
- Xác minh tất cả video/ảnh chụp màn hình
- Kiểm tra hệ thống cuối

# ✅ Sản phẩm:
- REHEARSAL_CHECKLIST.md (tất cả ✅)
- Hệ thống sản xuất sẵn sàng
```

---

## 🧪 Chiến Lược Kiểm Thử

### Kiểm Thử Đơn Vị
```bash
# Kiểm thử đơn vị backend
cd backend
pytest tests/ -v

# Dự kiến: Tất cả kiểm thử vượt qua
```

### Kiểm Thử Tích Hợp
```bash
# Giao diện trước → Backend → Databricks
docker-compose up -d
sleep 30

# Kiểm thử luồng công việc
curl http://localhost:8000/api/v1/health
curl http://localhost:8000/api/v1/schema
curl -X POST http://localhost:8000/api/v1/chat/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Kiểm thử?"}'

# Dự kiến: Phản hồi 200 OK
```

### Kiểm Thử E2E
```bash
# Kiểm thử luồng công việc hoàn chỉnh
1. Bắt đầu docker-compose
2. Truy cập giao diện trước (http://localhost:8501)
3. Nhập truy vấn mẫu
4. Xác minh tạo SQL
5. Xác minh hiển thị kết quả
6. Xác minh hiển thị biểu đồ
7. Kiểm tra xử lý lỗi
```

### Kiểm Thử Hiệu Suất
```bash
# Đo thời gian phản hồi
time curl -X POST http://localhost:8000/api/v1/chat/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Top 10?"}'

# Dự kiến: < 5 giây

# Load test
ab -n 100 -c 10 http://localhost:8000/api/v1/health
```

### Kiểm Thử Bảo Mật
```bash
# Tiêm SQL
"x; DROP TABLE orders; --"  # Nên bị chặn

# Đầu vào lớn
"x" * 10000  # Nên bị từ chối

# JSON không hợp lệ
"{invalid json"  # Nên trả về 400

# Trường bị thiếu
{}  # Nên trả về 422
```

---

## 📊 Mẫu Báo Cáo Kiểm Thử

```markdown
# BÁO CÁO KIỂM THỬ - [Ngày]

## Tóm Tắt
- Tổng Kiểm Thử: X
- Vượt Qua: X
- Thất Bại: X
- Bỏ Qua: X
- Tỷ Lệ Thành Công: X%

## Kết Quả Kiểm Thử

### Kiểm Thử API
| Endpoint | Trạng Thái | Thời Gian | Ghi Chú |
|---|---|---|---|
| GET /health | ✅ | 50ms | Tốt |
| GET /schema | ✅ | 200ms | Tốt |
| POST /query | ✅ | 2s | Tốt |

### Kiểm Thử Giao Diện Trước
| Tính Năng | Trạng Thái | Ghi Chú |
|---|---|---|
| Đầu vào trò chuyện | ✅ | Hoạt động |
| Hiển thị kết quả | ✅ | Hoạt động |
| Hiển thị SQL | ✅ | Hoạt động |

### Vấn Đề Tìm Thấy
- [ ] Vấn Đề 1
- [ ] Vấn Đề 2

## Khuyến Nghị
1. ...
2. ...
```

---

## 🔍 Danh Sách Kiểm Tra Đảm Bảo Chất Lượng

### Chất Lượng Mã
- [ ] Mã tuân theo tiêu chuẩn PEP8
- [ ] Tất cả hàm được ghi lại
- [ ] Xử lý lỗi hiện tại
- [ ] Không có giá trị hardcoded
- [ ] Logging được cấu hình đúng

### Tài Liệu
- [ ] README hoàn chỉnh
- [ ] Tài liệu API hoàn chỉnh
- [ ] Hướng dẫn triển khai hoàn chỉnh
- [ ] Kiến trúc được giải thích
- [ ] Ảnh chụp màn hình bao gồm

### Docker
- [ ] Ảnh xây dựng thành công
- [ ] docker-compose.yml hợp lệ
- [ ] Health checks hoạt động
- [ ] Logging được cấu hình
- [ ] Thực hành bảo mật tốt nhất

### Kiểm Thử
- [ ] Kiểm thử đơn vị vượt qua
- [ ] Kiểm thử tích hợp vượt qua
- [ ] Kiểm thử E2E vượt qua
- [ ] Hiệu suất có thể chấp nhận
- [ ] Kiểm thử bảo mật vượt qua

### Triển Khai
- [ ] .env.example chính xác
- [ ] Không có bí mật trong mã
- [ ] Tất cả phụ thuộc được liệt kê
- [ ] README bao gồm thiết lập
- [ ] Khắc phục sự cố bao gồm

---

## 🛠️ Công Cụ & Lệnh

### Lệnh Docker
```bash
# Xây dựng
docker-compose build --no-cache

# Chạy
docker-compose up -d

# Nhật ký
docker-compose logs -f backend
docker-compose logs -f frontend

# Dừng
docker-compose down

# Làm sạch
docker-compose down -v
```

### Công Cụ Kiểm Thử
```bash
# Kiểm thử API
curl, Postman, pytest-httpx

# Load testing
Apache Bench (ab), wrk

# Bảo mật
OWASP ZAP, Burp Suite

# Hiệu suất
Docker stats, time command
```

### Công Cụ Tài Liệu
```bash
# Tạo tài liệu API
Swagger UI (tự động từ FastAPI)

# Tạo thông số kỹ thuật
OpenAPI 3.0

# Sơ đồ
Draw.io, Mermaid
```

---

## 📋 Danh Sách Kiểm Tra Sản Phẩm

### Sản Phẩm Giai Đoạn 1
- [x] Dockerfile (Backend)
- [x] Dockerfile (Frontend)
- [x] docker-compose.yml
- [x] .env.example
- [x] API_DOCS.md
- [x] README.md
- [x] DOCKER_GUIDE.md
- [x] Báo cáo kiểm thử (API, Giao Diện Trước, Bảo Mật)
- [x] Xác minh xây dựng
- [x] Danh sách kiểm tra demo

### Sản Phẩm Giai Đoạn 2
- [x] Báo cáo kiểm thử nâng cao
- [x] Báo cáo tối ưu hóa hiệu suất
- [x] QUICKSTART_FOR_TEACHERS.md
- [x] Báo cáo UAT cuối
- [x] Tài liệu thuyết trình
- [x] Hướng dẫn triển khai cuối


---

## 🎯 Tiêu Chí Thành Công

### MVP (Giai Đoạn 1)
✅ Hệ thống bắt đầu bằng `docker-compose up -d`  
✅ Tất cả health checks đang hoạt động  
✅ Endpoints API được kiểm thử (100% vượt qua)  
✅ Giao diện trước tương tác và phản ứng  
✅ Không tìm thấy lỗ hổng bảo mật  
✅ Tài liệu hoàn chỉnh  

### Nâng Cao (Giai Đoạn 2)
✅ Tất cả tiêu chí Giai Đoạn 1 được đáp ứng  
✅ Tính năng mới được kiểm thử (100% vượt qua)  
✅ Hiệu suất được tối ưu hóa  
✅ Hướng dẫn giáo viên được viết  
✅ Thuyết trình sẵn sàng  

---

**Lần Cập Nhật Cuối:** 8/04/2026  
**Trạng Thái:** Playbook Sẵn Sàng 🚀
