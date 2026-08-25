# 📮 THƯ BÀN GIAO — Tích hợp đọc Zalo cho Trợ Lý Giáo Viên

> **Dành cho phiên Claude mới (đặc biệt là phiên chạy TRÊN Mac mini M4 của cô Thu).**
> Đọc file này + `CLAUDE.md` là nắm được toàn bộ bối cảnh, không cần cô Thu kể lại.
> **Viết ngày:** 2026-08-25 · **Người viết:** Claude (phiên trên mây) · **Người dùng:** Cô Thu (thinhdv1@gmail.com)

---

## 1. 🎯 Cô Thu đang muốn gì?

Cô Thu muốn app **Trợ Lý Giáo Viên** có thể **tự động đọc các nhóm Zalo cá nhân của cô** (nhóm lớp, nhóm phụ huynh), để việc quản lý lớp — nhận bài, theo dõi, nhắc nhở — diễn ra tự động thay vì copy-paste thủ công như hiện tại.

Đây là mong muốn cốt lõi. Mọi thứ dưới đây xoay quanh việc **làm được điều đó một cách thực tế và an toàn**.

---

## 2. 🧭 Bối cảnh cuộc trao đổi (tóm tắt để phiên sau hiểu)

Cô Thu và Claude (phiên trên mây) đã bàn kỹ qua nhiều câu hỏi. Các kết luận quan trọng:

### a) Vì sao app hiện tại (file HTML) KHÔNG tự đọc Zalo được
- App là trang web tĩnh chạy trong trình duyệt → bị **"bức tường" bảo mật trình duyệt** (Same-Origin Policy) chặn, không đọc được nội dung trang Zalo.
- **Nhúng Zalo Web vào iframe cũng vô ích:** Zalo cấm bị nhúng, và kể cả nhúng được thì trình duyệt vẫn cấm app đọc nội dung bên trong iframe khác nguồn gốc.
- Zalo **không có API chính thức** cho phép đọc nhóm chat cá nhân (API chính thức chỉ dành cho Official Account doanh nghiệp, và OA không đọc được nhóm cá nhân).

### b) Ba con đường khả thi (đã trình bày cho cô)
| Đường | Đọc được nhóm cá nhân? | Rủi ro | Ghi chú |
|------|----------------------|--------|---------|
| **A. OA + ZNS (chính thống)** | ❌ Không | ✅ An toàn, hợp pháp | Chỉ GỬI thông báo tới phụ huynh được |
| **B. Thư viện không chính thức** (`zca-js`) | ✅ Có | ⚠️ **Rất cao — có thể bị KHÓA số Zalo vĩnh viễn** | Giả mạo tín hiệu API |
| **C. Tự động hóa giao diện** (browser automation / extension / OCR) | ✅ Có | 🟡 Trung bình (thấp hơn B) | Bắt chước cô dùng máy như người thật |

### c) Kết luận quan trọng về "nơi chạy"
- **KHÔNG có cách nào đọc Zalo cá nhân mà không cần một chương trình chạy TRÊN máy của cô.** Không có "phép màu trên mây".
- Phiên Claude trên mây (nơi đã trao đổi với cô) chạy trên **máy Linux ở trung tâm dữ liệu** — KHÔNG ở trong Mac mini, KHÔNG chạm được Zalo của cô. Đã kiểm chứng bằng `uname -a` → `Linux x86_64`.
- **Mac mini M4 của cô là nơi lý tưởng** để đặt "trợ lý đọc Zalo": máy khỏe, bật 24/7, chạy nền êm.

### d) Quyết định đã chốt với cô Thu
➡️ **Đi theo hướng: cài Claude Code + dựng "trợ lý đọc Zalo" NGAY TRÊN Mac mini M4.**
Cô Thu cho biết **đã có Claude chạy trên Mac mini M4** — nên phiên đó chính là nơi làm việc thật. (Nếu chưa cài, xem mục 5.)

---

## 3. 🧱 Kiến trúc mục tiêu (tách 2 phần, đừng gộp)

```
┌─────────────────────────────────────────────────────────┐
│                    MAC MINI M4 (bật 24/7)                 │
│                                                          │
│   ┌──────────────────┐      ┌───────────────────────┐   │
│   │ TRỢ LÝ ĐỌC ZALO  │─────▶│  trolygv_server.py    │   │
│   │ (cần dựng mới)   │ đẩy  │  (ĐÃ CÓ SẴN!)         │   │
│   │ - Playwright HOẶC│ tin  │  localhost:8765       │   │
│   │   OCR màn hình   │      │  lưu vào file DuLieu/ │   │
│   └──────────────────┘      └───────────┬───────────┘   │
│                                          │ phục vụ        │
│                              ┌───────────▼───────────┐   │
│                              │ App Trợ Lý (HTML)     │   │
│                              │ mở trong trình duyệt  │   │
│                              └───────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

**Điểm mấu chốt:** App HTML **giữ nguyên**, chỉ **nhận thêm dữ liệu**. Không đập đi làm lại.

---

## 4. ⭐ Tin quan trọng: NỀN MÓNG ĐÃ CÓ SẴN

Trong dự án đã có **`trolygv_server.py`** — một máy chủ nội bộ chạy trên chính máy cô:
- Chạy ở `http://localhost:8765`
- Phục vụ file app HTML
- Có sẵn API: `GET /api/health`, `GET /api/data`, `POST /api/data`
- **Tự lưu toàn bộ dữ liệu vào file thật** `DuLieu/TroLyGiaoVien_DuLieu.json` + tự sao lưu theo ngày

➡️ **Đây chính là "cây cầu" để trợ lý đọc Zalo đưa dữ liệu vào app.** Chỉ cần **thêm một endpoint mới** (ví dụ `POST /api/zalo`) vào file này, rồi trợ lý đọc Zalo gọi vào đó. Không phải xây cầu từ đầu.

Cũng có sẵn file `▶️ Mở Trợ Lý (lưu trên máy).command` — kịch bản mở app kèm máy chủ nội bộ trên máy Mac.

---

## 5. 🛠️ Nếu cần cài Claude Code lên Mac mini (macOS 13+, chip Apple)

**Cách khuyên dùng (Native Install)** — mở Terminal, dán:
```bash
curl -fsSL https://claude.ai/install.sh | bash
```
Hoặc qua Homebrew:
```bash
brew install --cask claude-code
```
Kiểm tra: `claude --version` · Chẩn đoán: `claude doctor` · Khởi động: gõ `claude` trong thư mục dự án.
Đăng nhập: chạy `claude`, làm theo hướng dẫn trên trình duyệt (cần tài khoản Claude Pro/Max/Team/Enterprise).
Tài liệu: https://code.claude.com/docs/en/setup

---

## 6. ✅ VIỆC CẦN LÀM TIẾP (cho phiên trên Mac mini)

**Bước 0 — Xác nhận đang ở trong Mac mini:** chạy `uname -a`, phải thấy `Darwin` + `arm64`.

**Bước 1 — Lấy code mới nhất:**
```bash
git pull origin claude/teacher-assistant-project-extjm1
```

**Bước 2 — Đề xuất kỹ thuật đọc Zalo (nên chọn 1):**
- **Ưu tiên — Browser automation (Playwright + Python):** mở `chat.zalo.me`, cô đăng nhập QR 1 lần, chương trình đọc chữ trực tiếp từ trang → chính xác nhất. Chạy chậm, giống người thật để giảm rủi ro.
- **Phương án 2 — OCR màn hình app Zalo:** chụp màn hình + đọc chữ (tái dùng công nghệ OCR tiếng Việt app đã có). Đọc được mọi thứ hiện trên màn hình nhưng dễ sai hơn.
- **Phương án 3 — Extension trình duyệt:** đọc tab Zalo Web cô đang mở, gửi về server. Dễ dùng cho cô.

**Bước 3 — Nối vào app:**
- Thêm endpoint `POST /api/zalo` vào `trolygv_server.py` để nhận tin từ trợ lý đọc Zalo.
- Trợ lý đọc Zalo (Playwright/OCR) đẩy tin nhắn mới vào endpoint đó.
- App HTML đọc dữ liệu Zalo qua server và hiển thị trong các tab quản lý lớp (ClassesTab / zalo-main đã có sẵn).

**Bước 4 — Chạy thử an toàn:** cho chạy với 1 nhóm nhỏ trước, tốc độ chậm, quan sát vài ngày rồi mới mở rộng.

---

## 7. ⚠️ CẢNH BÁO PHẢI NHẮC LẠI VỚI CÔ THU

- Mọi cách "đọc thẳng nhóm Zalo cá nhân" (kể cả Playwright/OCR) đều **vi phạm điều khoản Zalo ở mức độ nào đó** và **có rủi ro bị khóa số**. Cách C (giao diện) rủi ro thấp hơn cách B (`zca-js`) nhưng **không phải 0%**.
- Cô Thu dùng số cá nhân để liên lạc phụ huynh → **mất số là mất mát lớn**. Luôn cho cô biết rõ rủi ro trước khi bật tính năng.
- **Khuyên dùng số Zalo phụ/dành riêng** cho việc tự động hóa nếu có thể, để bảo vệ số chính.
- Chạy **chậm, tự nhiên**, không spam, không gửi hàng loạt tốc độ cao.

---

## 8. 📌 Quy tắc làm việc với cô Thu (từ CLAUDE.md)

- Luôn **tiếng Việt**, xưng **"tôi - cô"**, thêm 🌸 ấm áp vừa phải.
- Không dùng màu indigo/violet/purple/fuchsia trong UI. Palette: Teal `#0f766e` + Rose `#be185d` + Cream `#fdfaf6`.
- Đọc file hiện tại trước khi sửa. Verify Babel (braces/parens/brackets cân bằng) sau mỗi lần sửa file lớn.
- File app chính: `TroLyGiaoVien_Phase4_REFACTORED.html`. Copy sang `deploy/index.html` trước khi deploy.
- Nhánh làm việc: `claude/teacher-assistant-project-extjm1`.

---

*Chúc phiên sau tiếp nối suôn sẻ. Cô Thu là người rất chịu khó tìm hiểu — hãy giải thích rõ ràng, thành thật về giới hạn kỹ thuật, đừng hứa hão. 🌸*
