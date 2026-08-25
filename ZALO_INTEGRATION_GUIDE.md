# 📱 Hướng Dẫn Tích Hợp Zalo - Phần Quản Lý Lớp Học

## 🎯 Tổng Quan

Phần **💬 ZALO TƯƠNG TÁC** trong tab **Quản Lý Các Lớp Học** giúp cô:
- **Quản lý** các nhóm Zalo lớp học
- **Nhận bài** từ học sinh gửi qua Zalo
- **Đôn đốc** học sinh nộp bài
- **Theo dõi** lịch sử giao/nhận/chấm bài

---

## 📋 Các Bước Sử Dụng

### **Bước 1️⃣: Cài Đặt (⚙️ Settings)**

#### Điền thông tin Zalo cá nhân:
```
📱 Số điện thoại Zalo: 0912345678 (số Zalo của cô)
👥 Nhóm Zalo cần quản lý: 
   - Ngữ Văn 7A1
   - Ngữ Văn 7A2
   - Ngữ Văn 8A1
   (Cô có thể thêm/xóa nhóm bất kỳ lúc nào)
🔑 API Key: (để trống - tính năng Phase 5+)
```

**💾 Cách lưu:**
- Điền đầy đủ thông tin
- Nhấn nút **"Lưu Tất Cả Cài Đặt"**
- Sẽ hiển thị: ✅ Đã lưu cài đặt Zalo!

---

### **Bước 2️⃣: Giám Sát Nhóm (📬 Giám Sát Nhóm)**

**Mục đích:** Theo dõi các nhóm Zalo đang được quản lý

**Thông tin hiển thị:**
- Danh sách các nhóm Zalo đã thêm
- Trạng thái: "Đang giám sát" (sẵn sàng)
- Hướng dẫn: Copy-paste từ Zalo vào app

**Hiện tại (Phase 4):**
- Cô mở Zalo trên máy tính
- Xem tin nhắn trong các nhóm lớp
- Khi em gửi bài, cô copy → dán vào "📥 Nhận Bài"

---

### **Bước 3️⃣: Nhận Bài (📥 Nhận Bài)**

**Quy trình:**

1. **Cô mở Zalo** trên máy tính
2. **Em gửi bài** vào nhóm Zalo (ảnh bài làm + nội dung)
3. **Cô copy tin nhắn** (Ctrl+C hoặc chuột phải → Copy)
4. **Dán vào app:**
   - Tên học sinh: Nguyễn Văn A
   - Bài tập: Chọn từ danh sách
   - Nội dung: Dán ảnh/text từ Zalo
5. **Nhấn "Lưu Bài Nộp"**
6. ✅ Bài sẽ lưu vào danh sách "Danh sách bài đã nhận"

**📊 Danh sách bài nhận:**
- Hiển thị tất cả bài đã lưu
- Có thể **Chấm** (chuyển sang tab Chấm Bài)
- Có thể **Xóa** (nếu nhập sai)

---

### **Bước 4️⃣: Đôn Đốc (📤 Đôn Đốc)**

**Mục đích:** Gửi tin nhắn nhắc nhở học sinh nộp bài

**Quy trình:**

1. **Chọn bài tập** từ danh sách
   - App sẽ tự động điền hạn chót
2. **Chỉnh sửa tin nhắn** (nếu cần)
   - Viết thân thiện, khích lệ
   - Gợi ý: "Em yêu, cô mong em nộp bài..."
3. **Sao chép tin nhắn** (Ctrl+C auto hoặc nhấn nút)
   - ✅ Đã sao chép! Hãy dán vào nhóm Zalo.
4. **Mở Zalo** → nhấn "Mở Zalo" hoặc tự mở
5. **Dán vào nhóm** (Ctrl+V)
6. **Gửi tin** (Enter hoặc ✓)

**💡 Mẹo:**
- Cô có thể gửi cho **1 nhóm** (tất cả em)
- Hoặc **1 em cá nhân** (riêng tư)

---

### **Bước 5️⃣: Theo Dõi Lịch Sử (💬 Lịch Sử)**

**Hiển thị:**
- 📧 Các bài tập đã giao
- 📥 Bài nộp từ em
- 💬 Phản hồi đã trả (Phase 5+)

**Thống kê:**
- Bài tập giao: X cái
- Bài nộp nhận: Y bài
- Phản hồi gửi: Z lần

---

## 🔄 Quy Trình Hoàn Chỉnh (5 Bước)

```
┌─────────────────────────────────────────────────────────┐
│  1️⃣  Cô SOẠN BÀI TẬP (Tab: Bài Tập)                     │
│  ✍️  Tên bài, deadline, điểm, mô tả                     │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│  2️⃣  COPY TIN NHẮN → DÁN VÀO ZALO (Tab: Đôn Đốc)       │
│  📤  "Em yêu, nộp bài... [Tên bài]... Cảm ơn em! 🌸"   │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│  3️⃣  EM NỘP BÀI VÀO NHÓM ZALO                           │
│  📸 Em chụp ảnh bài làm → gửi vào nhóm                  │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│  4️⃣  CÔ DÁNSZ VÀOMÉN "NHẬN BÀI" (Tab: Nhận Bài)        │
│  📥 Copy tin từ Zalo → Dán vào app → Lưu               │
│  🤖 App: OCR chữ viết + Chấm tự động                   │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│  5️⃣  COPY PHẢN HỒI → DÁN VÀO ZALO TRẢ BÀI             │
│  💬 "Em yêu, cô xem bài em... [Nhận xét]... Cảm ơn! 🌸"│
└─────────────────────────────────────────────────────────┘
```

---

## 🎁 Ưu Điểm Của Phương Pháp Copy-Paste

✅ **An toàn 100%** - Không cần bất kỳ API key hay kết nối Zalo
✅ **Không bị ban** - Chỉ là copy-paste, không bot behavior
✅ **Nhanh gọn** - 2-3 click, vài giây để giao/nhận bài
✅ **Kiểm soát** - Cô kiểm tra trước khi gửi
✅ **Linh hoạt** - Gửi cho nhóm hoặc riêng tư em

---

## 🚀 Sắp Ra Mắt (Phase 5+)

Những tính năng nâng cao:
- ✨ **Kết nối API Zalo** → Tự động nhận/gửi tin
- 🔔 **Push notification** → Thông báo thực tế
- 📁 **Auto download ảnh** → Lưu bài làm tự động
- ⚡ **Bulk remind** → Đôn đốc nhiều em cùng lúc
- 📊 **Analytics** → Thống kê chi tiết theo em, lớp

---

## ❓ Câu Hỏi Thường Gặp

**❓ Làm sao biết em nộp bài hay chưa?**
- ✅ Bài nộp sẽ hiển thị trong "📥 Nhận Bài"

**❓ Có thể xóa bài đã nhận không?**
- ✅ Có, nhấn nút "Xóa" ở danh sách

**❓ Quên lưu cài đặt có sao không?**
- ⚠️ Nên lưu để app nhớ số Zalo và nhóm

**❓ Tại sao phải copy-paste?**
- 🛡️ Để an toàn 100%, không bị ban Zalo

**❓ Khi nào có API tự động?**
- 🚀 Phase 5+ (sau hoàn thành chấm bài, báo cáo)

---

## 📞 Hỗ Trợ

Nếu cô gặp vấn đề:
1. Kiểm tra cài đặt Zalo (⚙️)
2. Thử refresh trang (F5)
3. Kiểm tra dữ liệu đã lưu chưa

---

**🌸 Chúc cô thành công với học sinh! 🌸**

_Version 1.0 - Ngày cập nhật: 23/04/2026_
