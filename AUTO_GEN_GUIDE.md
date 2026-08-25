# 📚 Hướng dẫn Ra Đề Tự Động (Auto-Generate Exam)

## ✨ Tính Năng Mới - Phiên Bản 4.3

Trợ Lý Giáo Viên Ngữ Văn hiện hỗ trợ **tạo đề kiểm tra tự động** bằng AI, kết hợp với **kho bài văn** được chuẩn bị sẵn.

---

## 🎯 Các Tính Năng Chính

### 1. **Kho Bài Văn (Passages Bank)**
- 30+ bài văn được lựa chọn từ các tác giả nổi tiếng Việt Nam
- Sắp xếp theo **lớp học** (6, 7, 8, 9)
- Phân loại theo **chủ đề**:
  - 👨‍👩‍👧‍👦 **Gia đình và tình yêu thương** (gia_dinh)
  - 🌿 **Thiên nhiên và mùa** (thienhien)
  - 💫 **Giá trị và ý nghĩa** (giaTri)
  - 🌟 **Hy vọng và sống** (hy_vong)
  - 💼 **Lao động và tìm kiếm** (lao_dong)
- Mỗi bài văn có:
  - Tiêu đề, tác giả
  - Trích dẫn ngắn (excerpt)
  - Toàn văn (fullText)
  - Mức độ khó: dễ (de), trung bình (vua), khó (kho), rất khó (ratKho)

### 2. **Tạo Đề Tự Động (Auto-Generate Exam)**

#### Quy Trình:
1. Chọn **Lớp học** (6, 8, 9)
2. Chọn **Chủ đề** (từ danh sách các chủ đề có sẵn cho lớp đó)
3. Chọn **Loại đề**:
   - Kiểm tra 45 phút (10 điểm)
   - Kiểm tra giữa kỳ 90 phút
   - Kiểm tra cuối kỳ 90 phút
   - Học sinh giỏi 120 phút (20 điểm)
4. Nhấn **"🤖 Tạo Đề"**

#### Kết Quả:
- AI tự động sinh **câu hỏi đọc hiểu** từ bài văn đã chọn
- Tạo **bài viết** yêu cầu học sinh bày tỏ cảm nghĩ
- Cung cấp **gợi ý đáp án** cho từng câu hỏi
- Hiển thị **xem trước** dề thi hoàn chỉnh
- Cho phép **lưu đề** vào danh sách "Đề kiểm tra"

---

## 📖 Cách Sử Dụng

### Bước 1: Vào Tab "Ra Đề Tự Động"
- Trong tab **"Đánh giá - Kiểm tra"**
- Nhấn vào sub-tab **"🤖 Ra Đề Tự Động"**

### Bước 2: Chọn Tham Số
```
Lớp học:  [Lớp 6 / 8 / 9]  ← Chọn lớp cần tạo đề
Chủ đề:   [Danh sách chủ đề] ← Tùy theo lớp đã chọn
Loại đề:  [Kiểm tra 45' / Giữa kỳ / Cuối kỳ / HSG]
```

### Bước 3: Tạo Đề
- Nhấn nút **"🤖 Tạo Đề"**
- Chỉ mất **vài giây** để AI sinh câu hỏi

### Bước 4: Xem & Lưu
- Nhấn **"Xem trước"** để kiểm tra đề (định dạng in ấn)
- Nếu hài lòng, nhấn **"Lưu đề"** để lưu vào danh sách
- Đề sẽ xuất hiện trong tab **"Đề kiểm tra"**

---

## 🎓 Ví Dụ Thực Tế

### Ví dụ 1: Tạo đề cho Lớp 6
1. Chọn **Lớp 6**
2. Chọn chủ đề **"Gia đình và tình yêu thương"**
3. Chọn loại đề **"Kiểm tra 45 phút"**
4. Nhấn **"🤖 Tạo Đề"**
5. AI sẽ tạo đề với:
   - Bài văn "Lão Học" - Nam Cao
   - 2-3 câu hỏi đọc hiểu đơn giản
   - 1 bài viết ngắn về tình cảm gia đình

### Ví dụ 2: Tạo đề cho Lớp 9
1. Chọn **Lớp 9**
2. Chọn chủ đề **"Giá trị và ý nghĩa"**
3. Chọn loại đề **"Kiểm tra học sinh giỏi"** (120 phút, 20 điểm)
4. AI tạo đề:
   - Bài văn mức độ cao (tác phẩm kinh điển)
   - Câu hỏi phân tích sâu sắc
   - Bài viết dài yêu cầu luận lập

---

## 🤖 Cách Hoạt Động

### Quy Trình AI:
1. **Chọn bài văn** từ kho dựa vào lớp + chủ đề
2. **Sinh prompt** chi tiết cho AI:
   - Bài văn cần phân tích
   - Mục tiêu học tập
   - Cấu trúc đề mong muốn
3. **Gọi Groq API** (hoặc Ollama nếu dùng local)
4. **Nhận kết quả**: Câu hỏi + gợi ý đáp án
5. **Định dạng lại** thành đề tiêu chuẩn

### Yêu Cầu:
- **Groq API Key** phải được cấu hình trong **"⚙️ Cài đặt AI"**
- Hoặc sử dụng **Ollama** chạy local

---

## 📊 Dữ Liệu Kho Bài Văn

| Lớp | Bài Văn | Tác Giả | Chủ Đề | Độ Khó |
|-----|---------|--------|--------|--------|
| 6 | Lão Học | Nam Cao | Gia đình | Dễ |
| 6 | Những Đứa Con Trong Gia Đình | SGK | Gia đình | Dễ |
| 7 | Chí Phèo | Nam Cao | Gia đình | Trung bình |
| 7 | Người Thợ May | SGK | Lao động | Dễ |
| 8 | Vợ Chồng A Phủ | Tô Hoài | Gia đình | Khó |
| 8 | Chiếc Lá Cuối Cùng | O. Henry | Hy vọng | Trung bình |
| 9 | Áo Cũ | Nguyễn Quang Thiều | Gia đình | Rất khó |
| 9 | Thu Về Một Nửa | Hữu Thỉnh | Thiên nhiên | Khó |
| 9 | Tôi Ước Mình Là Cái Cây | Trần Quốc Vượng | Giá trị | Trung bình |

---

## 💡 Tips & Lưu Ý

✅ **Nên làm:**
- Kiểm tra kỹ đề trước khi in
- Điều chỉnh câu hỏi nếu cần phù hợp với tiến độ lớp
- Sử dụng các chủ đề khác nhau để tạo đa dạng đề kiểm tra
- Tham khảo "Gợi ý đáp án" của AI để chuẩn bị khóa đáp án

❌ **Không nên:**
- Sử dụng đề AI 100% mà không xem trước
- Dùng cùng một bài văn + chủ đề nhiều lần (học sinh dễ nhớ)
- Bỏ qua việc cấu hình Groq API Key

---

## 🔧 Cấu Hình Groq API

1. Vào **"⚙️ Cài đặt AI"**
2. Phần **"Groq Cloud API"**
3. Nhập **Groq API Key** (lấy từ https://console.groq.com)
4. Nhấn **"Kiểm tra"** để xác minh
5. Khi thấy ✅ **"Cấu hình"**, có thể sử dụng auto-gen

---

## 📈 Phát Triển Tiếp Theo (Phase 5+)

- [ ] Thêm thêm bài văn vào kho (mục tiêu 100+ bài)
- [ ] Cho phép tùy chỉnh số lượng câu hỏi
- [ ] Thêm tính năng "Lưu template" để tái sử dụng
- [ ] Kết nối thực với API Zalo để gửi đề trực tiếp
- [ ] Thêm chức năng "Học sinh làm bài online + chấm AI"

---

**Phiên bản:** 4.3  
**Ngày cập nhật:** 27/04/2026  
**Trạng thái:** ✅ Sản xuất

Chúc cô Thu dạy tốt! 🌸
