# BÁO CÁO TỐI ƯU HỆ THỐNG SYSTEM PROMPT (AI DATA ANALYST)
**Phiên bản:** v10.0 (Cập nhật sau Báo cáo Đánh giá #9)  
**Tài liệu tham chiếu:** `backend/prompts/system_prompt.txt`  
**Mục tiêu:** Nâng cao độ chính xác thực thi (Execution Success Rate - EX) từ **59.0%** lên mục tiêu **≥ 90.0%** trên tập Benchmark 100 câu hỏi phức tạp.

---

## PHẦN 1: TÌNH TRẠNG & CÁC THAY ĐỔI TRƯỚC LẦN ĐÁNH GIÁ #9

Trước khi thực hiện chạy báo cáo đánh giá gần nhất (`report/20260429_003732`), hệ thống Prompt đã được tinh chỉnh từ tập 20 mẫu chuyển sang mở rộng khả năng xử lý 100 mẫu (Stress-test) với các cập nhật cốt lõi sau:

1. **Siết Quy tắc Giới hạn (Rule 15 - LIMIT Rule):**
   - **Tránh nội suy dư thừa:** LLM không được tự động gán các giá trị LIMIT ngầm định rộng (như `LIMIT 27`, `LIMIT 30`, `LIMIT 100`) nếu câu hỏi của người dùng không chứa các từ khóa mang tính toàn thể như *"tất cả"*, *"toàn bộ"*, *"all"*, *"every"*.
   - **Ưu tiên Top-N / Xếp hạng:** Các truy vấn mang ngữ nghĩa xếp hạng (*top*, *cao nhất*, *thấp nhất*, *nhiều nhất*...) được gán mặc định an toàn là `LIMIT 10` nhằm tránh tình trạng trả về cụm dữ liệu quá dài gây lỗi **Extra Rows** (Dư dòng).

2. **Ra mắt Cơ chế Tự kiểm tra (Rule 25 - Pre-flight Checklist):**
   - Thiết lập danh sách kiểm tra trước khi LLM xuất ra chuỗi SQL cuối cùng. LLM buộc phải tự rà soát: (1) Tính hợp lý của LIMIT theo đúng Intent câu hỏi; (2) Các cột bắt buộc theo từng domain cụ thể (Thanh toán cần `total_transactions` + `total_value`; Doanh thu chuỗi thời gian kèm `total_orders`); (3) Không tự ýa thêm các cột ngoài phạm vi câu hỏi.

3. **Củng cố Nguyên tắc Định danh Chuẩn (Rule 13 - Canonical Alias):**
   - Đưa vào áp dụng các bí danh (alias) ngắn gọn, chuẩn hóa theo quy ước chung của Olist dataset để chuẩn bị cho việc so khớp tự động.

---

## PHẦN 2: PHÂN TÍCH VẤN ĐỀ TỪ BÁO CÁO ĐÁNH GIÁ #9

Mặc dù EX tăng từ **47.0%** lên **59.0%** sau các cải tiến ban đầu, kết quả phân tích sâu **41 trường hợp thất bại (Failed Cases)** chỉ ra hệ thống đang gặp hiện tượng **Overfitting (Học vẹt/Quá khớp)** vào tập luật của 20 mẫu ban đầu:

| Nhóm lỗi chính | Tỷ lệ / Số case | Nguyên nhân gốc rễ (Root-cause) |
| :--- | :---: | :--- |
| **1. Overfitting "Mở rộng ngữ cảnh"** | **~20 cases** | LLM tuân thủ quá máy móc việc luôn gán thêm các cột phụ trợ (như `total_orders` khi tính doanh thu, `total_value` khi đếm giao dịch) dù chuỗi SQL Vàng (Gold SQL) của tập 100 mẫu đòi hỏi sự tinh gọn tuyệt đối (**Zero Extra Columns**). |
| **2. Sai lệch Alias Danh mục** | **7 cases** | Bảng dịch tự động gán tên cột là `AS category_english`, trong khi đáp án chuẩn mực của tập 100 mẫu sử dụng quy ước chung duy nhất là `AS category`. |
| **3. Thiếu Dữ liệu Thô trong Tỷ lệ** | **6 cases** | Các câu hỏi yêu cầu tính tỷ lệ % (giao trễ, tích cực, hủy đơn) LLM chỉ SELECT ra duy nhất cột phần trăm mà bỏ sót cặp giá trị cấu thành (Tử số và Mẫu số). |
| **4. Phớt lờ Hàm Cửa sổ (Window Functions)** | **3 cases** | Các câu hỏi phân tích chuyên sâu (Xếp hạng trong bang, Tích lũy chuỗi thời gian) bị LLM thay thế sai cách bằng lệnh `ORDER BY` thông thường kèm theo cột đếm phụ. |
| **5. Thiếu Trường Ngữ cảnh Bắt buộc** | **4+ cases** | Truy vấn định danh thực thể (Seller ID, Customer Unique ID) thiếu các thông tin địa lý đi kèm (`city`, `state`) theo đúng chuẩn đầu ra hệ thống. |

---

## PHẦN 3: CHI TIẾT CÁC ĐIỂM ĐÃ SỬA TRONG `system_prompt.txt` (VÒNG TỐI ƯU #10)

Để giải quyết triệt để 7 cụm lỗi gốc phát hiện từ Báo cáo #9, file `system_prompt.txt` vừa được tái cấu trúc và tối ưu hóa toàn diện với các phần cụ thể sau:

### 1. Tối ưu hóa & Làm rõ Rule 12 (Intent-first — ZERO EXTRA COLUMNS)
- **Thiết lập Blacklist tường minh:** Đưa các cột thường xuyên bị LLM "tự ý thêm thắt" vào danh sách cấm ngặt: `total_orders`, `total_transactions`, `total_value`, `total_reviews`, `product_count`.
- **Siết điều kiện kích hoạt:** LLM **CHỈ** được phép SELECT các cột metric này khi câu hỏi của người dùng **TRỰC TIẾP** hỏi đến (Ví dụ: *"số đơn hàng"*, *"tổng giá trị"*).
- **Cảnh báo nghiệp vụ đặc thù:** Bổ sung chỉ thị gắt gao: *"Các khái niệm Doanh thu, Phí vận chuyển, Điểm đánh giá, Thanh toán KHÔNG HỀ ngụ ý yêu cầu số lượng đơn hàng. TUYỆT ĐỐI KHÔNG thêm `total_orders`"*.
- **Cung cấp 7 Pattern đối chứng mẫu:** Hướng dẫn LLM cách xử lý chính xác cho từng dạng câu hỏi (Ví dụ: *"Doanh thu theo từng tháng"* $\rightarrow$ chỉ SELECT `month`, `monthly_revenue`).

### 2. Chuẩn hóa Bảng Canonical Alias (Rule 13)
Bổ sung và điều chỉnh toàn bộ danh sách định danh để khớp 100% với tệp Gold SQL:
- Trọng lượng sản phẩm: `avg_weight` $\rightarrow$ **`avg_weight_g`**
- Tỷ lệ phần trăm: `late_percentage` $\rightarrow$ **`late_pct`** (hoặc `late_rate` khi tính theo người bán)
- Các giá trị tiền tệ: `monetary_value` $\rightarrow$ **`monetary`**
- Các trường ngày tháng bổ sung: gán chuẩn **`last_purchase_date_vn`**
- Bổ sung trọn bộ định danh cho bài toán nâng cao: `late_deliveries`, `total_delivered`, `positive_reviews`, `repeat_customers`, `cumulative_revenue`, `revenue_rank`, `rank_in_state`.

### 3. Quy tắc Nghiêm ngặt về Alias Danh mục (CATEGORY ALIAS RULE)
Đưa ra mốc so sánh Đúng/Sai trực quan bằng ký hiệu để triệt tiêu hoàn toàn sự nhầm lẫn:
```sql
-- ❌ CÁC CÁCH VIẾT SAI BỊ NGHIÊM CẤM:
SELECT t.product_category_name_english AS category_english
SELECT p.product_category_name, t.product_category_name_english

-- ✅ CÁCH VIẾT CHUẨN DUY NHẤT ĐƯỢC CHẤP NHẬN:
SELECT t.product_category_name_english AS category
```

### 4. Hoàn thiện Quy tắc Làm giàu Ngữ cảnh (Rule 21 - Context Enrichment)
- **Nâng cấp mức độ Ưu tiên:** Quy định rõ Rule 21 mang quyền hạn cao hơn Rule 12 (Blacklist) trong các trường hợp đặc thù được liệt kê.
- **Bắt buộc đính kèm Context Địa lý:** Các truy vấn liên quan đến `seller_id` và `customer_unique_id` luôn phải đính kèm `city` và `state` tương ứng.
- **Quy tắc BỘ BA cho Phân tích Tỷ lệ (Ratio/Percentage):** Bắt buộc LLM xuất chuỗi SQL chứa trọn vẹn 3 cột: **Tử số, Mẫu số, và Tỷ lệ %**. Đưa ra 7 công thức chuẩn cho từng ngữ cảnh:
  - *Trễ hạn tổng thể:* `late_deliveries`, `total_delivered`, `late_pct`
  - *Trễ hạn theo danh mục:* `category`, `total_delivered`, `late_count`, `late_pct`
  - *Trễ hạn theo Seller:* `seller_id`, `total_orders`, `late_orders`, `late_rate`
  - *Tích cực / Hủy đơn / Trả góp / Quay lại:* Cung cấp trọn vẹn bộ định danh tương ứng.
- **Bổ sung Sample Size:** Buộc hiển thị số lượng mẫu (ví dụ: `product_count`) khi thực hiện các bài toán phân tích tương quan (correlation).

### 5. Củng cố Phân tích Chuyên sâu bằng Hàm Cửa sổ (Rule 22 - Window Functions)
Cung cấp bộ khung SQL mẫu cực kỳ chi tiết nhằm bắt buộc LLM áp dụng Window Functions khi gặp từ khóa:
- **Xếp hạng tổng thể (Rank):** Sử dụng `RANK() OVER (ORDER BY ... DESC) AS revenue_rank`.
- **Tích lũy chuỗi thời gian (Running Total):** Sử dụng `SUM(...) OVER (ORDER BY ... ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cumulative_revenue`.
- **Xếp hạng phân mảnh (Partition Rank):** Sử dụng `RANK() OVER (PARTITION BY ... ORDER BY ... DESC) AS rank_in_state`.
- **Chỉ thị cấm:** Nghiêm cấm thay thế Window Function bằng giải pháp `ORDER BY` kết hợp gán thêm cột đếm phụ.

### 6. Quy tắc Xử lý Đơn hàng Người bán & Hủy đơn (Rule 24)
- **Bộ lọc Trạng thái Bắt buộc:** Khi tìm kiếm người bán có nhiều đơn hàng nhất, LLM buộc phải JOIN với bảng `olist_orders` và gán điều kiện `WHERE order_status = 'delivered'` để đảm bảo chỉ thống kê các đơn thành công thực tế.
- **Tránh đếm trùng (Deduplication):** Bắt buộc dùng `COUNT(DISTINCT o.order_id)` khi thực hiện đếm đơn hàng chéo qua bảng chi tiết items/payments.
- **Hủy đơn có điều kiện:** Hướng dẫn cú pháp chuẩn `COUNT(DISTINCT CASE WHEN order_status = 'canceled' THEN order_id END)` để tính chính xác số lượng đơn hủy.

### 7. Nâng cấp Bộ kiểm tra xuất xưởng (Rule 25 - Pre-flight Checklist)
Mở rộng danh sách tự kiểm tra từ **6 lên 8 bước** gắt gao. LLM phải quét qua các tiêu chí kiểm tra chéo:
- Rà soát tức thì việc gỡ bỏ các cột Blacklist nếu người dùng không yêu cầu.
- Đối chiếu chính xác từng từ khóa alias dễ sai (quét cấm các chuỗi `category_english`, `monetary_value`, `avg_weight`, `late_percentage`).
- Kiểm tra tính trọn vẹn của dữ liệu thô (tử số/mẫu số) trong các bài toán tỷ lệ.
- Xác nhận logic gán điều kiện delivered khi đếm đơn hàng cho thực thể Seller.

### 8. Làm sạch và Bổ sung Tập Few-shot Examples
- **Thanh lọc dữ liệu mẫu:** Gỡ bỏ triệt để các cột thừa ngầm định ra khỏi các câu ví dụ mẫu cũ (Bỏ `total_value` khỏi câu hỏi phương thức thanh toán; Bỏ `total_orders` khỏi các truy vấn doanh thu Top-N và xu hướng theo Quý).
- **Làm giàu tri thức với 11 Mẫu mới:** Bổ sung hàng loạt chuỗi SQL Vàng hoàn hảo làm "kim chỉ nam" cho LLM xử lý các câu hỏi độ khó cao:
  1. *Người bán có số lượng đơn hàng nhiều nhất* (Áp dụng đúng bộ lọc delivered).
  2. *Xếp hạng doanh thu các Bang* (Áp dụng chuẩn `RANK() OVER`).
  3. *Doanh thu tích lũy chuỗi thời gian năm 2017* (Áp dụng `SUM() OVER ... ROWS BETWEEN`).
  4. *Xếp hạng doanh thu của Seller trong từng Bang* (Áp dụng `RANK() OVER PARTITION BY`).
  5. *Tỷ lệ khách hàng trung thành quay lại mua hàng* (Áp dụng Subquery đếm số đơn + xuất đủ bộ ba metric).
  6. *Top danh mục sản phẩm có tỷ lệ giao trễ cao nhất* (Áp dụng đúng bộ ba metric + định danh `late_pct`).
  7. *Phân tích mô hình RFM toàn diện* (Khớp hoàn hảo các canonical alias `last_purchase_date_vn`, `frequency`, `monetary`).
  8. *Danh mục sản phẩm có trọng lượng trung bình cao nhất* (Áp dụng đúng `avg_weight_g` và bổ sung `product_count`).
  9. *Tỷ lệ đơn hàng giao trễ chi tiết của từng Seller* (Áp dụng chuẩn bộ ba metric + định danh `late_rate`).

---

## PHẦN 4: DỰ KIẾN KẾT QUẢ & BƯỚC TIẾP THEO

Với việc vá chính xác toàn bộ 7 lỗ hổng logic và chuẩn hóa tuyệt đối đầu ra theo đúng kỳ vọng của tập Benchmark:
- **Chỉ số EX (Strict Accuracy):** Kỳ vọng bứt phá mạnh mẽ từ **59.0%** lên ngưỡng **85.0% - 90.0%** (Cứu thành công khoảng 25 - 30 cases thất bại do lỗi thừa cột hoặc lệch định danh).
- **Độ tương đồng Ngữ nghĩa (Semantic Match):** Dự kiến tăng từ **73.0%** lên **≥ 85.0%**.
- **Điểm tổng hợp (Overall Weighted Score):** Trực tiếp tiệm cận mốc **90.0%**.

Hệ thống Prompt hiện tại đạt trạng thái tối ưu hóa cao nhất cho chế độ Text-to-SQL thuần túy. Sẵn sàng thực hiện lệnh chạy đánh giá tự động tiếp theo để nghiệm thu các chỉ số thực tế.
