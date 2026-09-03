# 📘 BÀN GIAO DỰ ÁN — Trợ Lý Giáo Viên Ngữ Văn THCS

> **Dành cho session mới:** File này tóm tắt toàn bộ trạng thái dự án. Đọc xong là có thể tiếp tục ngay, không cần hỏi lại cô Thu.
> **Cập nhật lần cuối:** 2026-09-03 — Bỏ hẳn hướng Zalo, chuyển hoàn toàn sang "Lớp Học Kết Nối" (Firebase) + Cổng Lớp Học. Đã sửa xong cả 3 đợt lỗi từ báo cáo kiểm tra toàn diện (29 phát hiện).
>
> **🔴 Netlify đang ĐÓNG BĂNG kể từ 2026-09-03:** Team hết "operational credits", production deploy bị tạm dừng (site cũ vẫn chạy, không sập, nhưng KHÔNG tự build bản mới nữa). Bản đang chạy trên `trolygiaovien.netlify.app` dừng lại ở **29/8** — nghĩa là **CHƯA có** toàn bộ các bản vá từ 30/8 trở đi, kể cả bản vá RIÊNG TƯ quan trọng nhất (lộ điểm học sinh, xem mục "Đã hoàn thành"). GitHub Pages (`docs/`) thì build tự động qua GitHub Actions, KHÔNG phụ thuộc credit Netlify, nên đang có đủ bản mới nhất. **→ Cho đến khi Netlify resume (xem Team settings → Billing → Usage) hoặc cô Thu nâng cấp gói, dùng `thinhdv123456.github.io/tro-ly-giao-vien/` làm link CHÍNH, không phải link dự phòng nữa.** Khi Netlify build lại bình thường (kiểm tra: vào tab Deploys, thấy build khớp commit mới nhất = "Published"), gỡ ghi chú này.

---

## 👤 Người dùng

- **Tên:** Cô Thu (sinh 1979, ~47 tuổi)
- **Nghề:** Giáo viên Ngữ văn THCS
- **Email:** thinhdv1@gmail.com
- **Ngôn ngữ giao tiếp:** Tiếng Việt, xưng "tôi - cô"
- **Tính cách thiết kế:** Trung niên, nữ tính nhưng chuyên nghiệp — tránh màu chói, childish

---

## 🎨 Bảng màu đang dùng (Palette "Kem Hồng")

```css
--c-primary: #be185d;      /* Hồng đậm - chủ đạo */
--c-primary-soft: #ec4899; /* Hồng tươi */
--c-accent: #e11d48;       /* Hồng-đỏ - nhấn AI/chấm */
--c-accent-soft: #fb7185;  /* Đào/coral */
--c-gold: #d97706;         /* Vàng kem ấm */
--c-cream: #fff7f4;        /* Kem hồng nhạt */
--c-cream-deep: #fdeae2;   /* Kem đậm */
--c-ink: #4a2530;          /* Nâu mận ấm */
--c-ink-soft: #6a4552;     /* dùng biến này cho chữ mờ/phụ, KHÔNG hardcode hex */
--c-border: #f0dcd0;
--app-fs: 17px;            /* cỡ chữ do cô tự chỉnh qua nút "Aa" trên header */
```

❌ Không dùng: `indigo-*`, `violet-*`, `purple-*`, `fuchsia-*`

Chế độ "chữ đậm hơn" (bật qua nút Aa) toggle class `text-strong` trên `<html>`, tự làm đậm heading + làm đậm màu chữ mờ.

---

## 📂 Các file chính

| File | Mô tả | Trạng thái |
|------|-------|-----------|
| `TroLyGiaoVien_Phase4_REFACTORED.html` ⭐ | Chương trình chính cho GIÁO VIÊN — nguồn duy nhất, Netlify build tự copy thành `dist/index.html` | ✅ Sản xuất |
| `CongHocSinh.html` ⭐ | **Cổng Lớp Học** — cho HỌC SINH/PHỤ HUYNH, deploy ở đường dẫn `/cong` | ✅ Sản xuất |
| `trolygv_server.py` | Máy chủ nội bộ (chạy `python3 trolygv_server.py`, cổng 8765) — lưu dữ liệu ra file thật + proxy gọi Claude API (tránh CORS) khi mở app dạng file cục bộ | 🖥️ Tuỳ chọn, chạy trên máy cô |
| `netlify.toml` | Cấu hình build Netlify — copy 2 file HTML trên thành `dist/index.html` + `dist/cong.html`, định tuyến `/cong`, `/api/claude/message` | ⚙️ Build |
| `docs/index.html`, `docs/cong/index.html` | Host trên **GitHub Pages** (miễn phí, không giới hạn credit như Netlify) — **PHẢI đồng bộ tay** mỗi lần sửa file chính (xem Quy tắc #8) | 🚀 **Đang là link CHÍNH** (Netlify đóng băng từ 2026-09-03, xem cảnh báo đầu file) |

Các file `TroLyGiaoVien_Phase1/2/3.html`, `TroLyGiaoVien_Phase4_Groq_v2_UPDATED.html`, `deploy/` là bản cũ/lưu trữ, không dùng để deploy.

**⭐ Bỏ hẳn (2026-09-03):** Toàn bộ hướng tích hợp Zalo — `zalo_reader.py`, `ZALO_INTEGRATION_GUIDE.md`, `HUONG_DAN_BO_DOC_ZALO.md`, `BAN_GIAO_ZALO.md`, `zalo_reader_config.example.json` đã **xoá khỏi repo**. Trong code chính: xoá hẳn tab "Sổ điểm · Zalo" (`ClassesTab` và mọi component con: `ZaloMainView/ZaloSettingsView/ZaloMonitorView/ZaloCollectorView/ZaloRemindView/ZaloHistoryView`, `GradingTabView` và cây con chấm bài rule-based cũ `chamBaiTuDong`, OCR qua `localhost:3000` đã hỏng). Tab "Tin nhắn" cũ tên `ZaloChatTab` đã đổi tên thành **`ClassMessagesTab`** (bản chất là nhắn tin qua Firebase thời gian thực, không liên quan Zalo, giữ lại và đổi route từ `zalo-chat` → `class-messages`). **Toàn bộ quản lý lớp giờ chỉ còn 1 hệ thống duy nhất: "Lớp Học Kết Nối" (`OnlineClassTab`, các component `Oc*`), dùng Firebase.**

---

## 🧱 Kiến trúc kỹ thuật

**Stack:** 1 file HTML độc lập mỗi chương trình (không cần build/npm)
- React 18 + Babel standalone (JSX chạy thẳng trong trình duyệt) qua CDN
- Tailwind CSS qua CDN
- **Firebase** (Auth + Firestore) — nguồn dữ liệu CHÍNH cho "Lớp Học Kết Nối" + Cổng Lớp Học; LocalStorage chỉ là cache/dự phòng cho phần soạn bài/ra đề (không đăng nhập vẫn dùng được, nhưng không đồng bộ đa thiết bị)
- Claude API (chất lượng cao, đọc được ảnh — bắt buộc cho chấm bài chụp tay) / Groq API (nhanh, miễn phí, gọi thẳng từ trình duyệt) / Ollama (local, offline) — chọn trong "Cài đặt AI"
- Export Word: Blob + HTML trick; Export PDF: html2pdf.js/jsPDF; nút xuất slide ở LessonModal ghi đúng là **"Xuất Slide (PDF)"** — thực chất xuất PDF trình bày dạng slide, không phải .pptx thật (đã sửa nhãn cho khớp thực tế ở Đợt 3, xem mục "Việc còn tồn đọng" nếu sau này cần .pptx thật)

**Quy trình đưa lên mạng (đầy đủ):**
1. Sửa code → parse thử bằng **Babel THẬT** (xem lệnh mẫu ở Quy tắc #4, không chỉ đếm ngoặc) → chỉ push khi "BABEL PARSE OK"
2. `cp TroLyGiaoVien_Phase4_REFACTORED.html docs/index.html` + `cp CongHocSinh.html docs/cong/index.html` (đồng bộ GitHub Pages)
3. `git add` + `git commit` + `git push origin main`
4. Netlify tự build từ `main` (qua `netlify.toml`) → `trolygiaovien.netlify.app`. GitHub Pages tự build từ thư mục `docs/` trên `main` → `thinhdv123456.github.io/tro-ly-giao-vien/`. **Netlify có credit build giới hạn theo tháng, từng hết nhiều lần** (hết hẳn từ 2026-09-03, xem cảnh báo đầu file) — khi hết, Netlify **không báo lỗi gì**, chỉ âm thầm ngừng build và tiếp tục phục vụ bản cũ, nên đừng mặc định "đã push thì Netlify chắc chắn có bản mới" — luôn kiểm tra tab Deploys trên Netlify khớp đúng commit trước khi báo cô Thu là "đã lên bản mới". GitHub Pages build qua GitHub Actions riêng, không dùng chung credit này nên luôn đáng tin hơn để xác nhận đã deploy thành công.
5. **Firebase yêu cầu domain phải nằm trong "Authorized domains"** (Firebase Console → Authentication → Settings) mới hoạt động được — Netlify domain đã được cấp, **GitHub Pages domain (`thinhdv123456.github.io`) phải tự thêm tay 1 lần** nếu chưa có, nếu không Firestore sẽ báo lỗi 400 âm thầm (đã từng xảy ra + đã hướng dẫn cô Thu thêm).

**Các menu/tab chính (MENU_ITEMS trong code):**
- `online` (ghim đầu menu) → **`OnlineClassTab`** = "Lớp Học Kết Nối" — quản lý lớp/giao bài/chấm bài/báo cáo, DUY NHẤT còn lại, dùng Firebase. Các component: `OcNewClass, OcClassDetail, OcNewAsg, OcSubmissions, OcGrade, OcMessages`...
- `dashboard` → `Dashboard` (trang chủ, hero + widget "Lớp Học Kết Nối" rút gọn)
- `planning` → `PlanningTab` (kế hoạch bài dạy), `lesson` → `LessonTab` (giáo án)
- `exam` → `ExamTab`, 5 sub-tab: **Đề kiểm tra** (`ExamModal`) · **🤖 Ra Đề Tự Động** (`AutoGenExamView`) · **📚 Kho Ngữ Liệu** (`KhoNguLieuTab`) · **Ma trận đề** (`MatrixModal`) · **Ngân hàng câu hỏi** (`QuestionBankModal`)
- `library` → `LibraryTab` (thư viện tài liệu tham khảo)
- `settings` → `SettingsTab` (Cài đặt AI, xuất/nhập dữ liệu, đăng nhập đám mây)
- Route riêng (không trong MENU_ITEMS, mở qua icon "Tin nhắn"): `class-messages` → `ClassMessagesTab`

**Ra đề bằng AI — đã hợp nhất cách xử lý lỗi (2026-09-03):** 3 nơi AI sinh đề (`generateFullExamAI`, `generateQuestionsFromPassageAI` trong `ExamModal`; `AutoGenExamView.generateExam`; lệnh `/sinh-đề` trong Trợ Lý AI) đều dùng chung `parseAIExamJson()`/`parseAINestedObject()` (gần `callGroqAPI`) — nếu AI trả JSON lỗi định dạng, KHÔNG được đổ JSON thô ra đề, phải báo lỗi rõ ràng cho cô. **Nếu thêm nơi mới sinh đề bằng AI, PHẢI dùng lại 2 hàm này**, đừng viết `JSON.parse` riêng. Cũng có bộ chọn "Loại câu hỏi Đọc hiểu" (`QUESTION_TYPE_OPTIONS`, `buildQuestionTypeInstruction`) — Kết hợp/Toàn trắc nghiệm/Toàn tự luận, hiện trước nút tạo đề.

**Bảo vệ dữ liệu đa tài khoản (2026-09-03):** localStorage lưu theo TRÌNH DUYỆT, không theo tài khoản Firebase — nếu không cẩn thận, dữ liệu tài khoản A có thể bị đẩy nhầm lên tài khoản B khi B đăng nhập lần đầu trên cùng máy. Đã chặn bằng `LAST_CLOUD_UID_KEY` trong `App`'s `onAuthStateChanged` — chỉ đẩy dữ liệu local lên cloud nếu UID khớp lần đăng nhập trước trên chính máy đó.

**Cổng Lớp Học (`CongHocSinh.html`) — cấu trúc học sinh (2026-09-03, viết lại):**
- `StudentHome` — **5 tab**: Chat | Tài liệu (mới, collection Firestore `materials`) | **Bài tập** (trung tâm, nút tròn nổi) | Thi & Kiểm tra (bài tập có `kind:'kiemtra'`, chọn lúc giao bài) | Kết quả
- `DoAssignment` — bắt buộc chọn 1 trong 2 cách làm bài TRƯỚC khi bắt đầu: **Làm trực tiếp** (mỗi câu 1 ô + đếm từ) hoặc **Nộp bằng ảnh chụp** (mở thẳng camera, tối đa 10 ảnh, tự kiểm tra độ nét bằng phương sai Laplacian — `isImageBlurry()` — cảnh báo nếu mờ nhưng vẫn cho dùng nếu HS xác nhận)
- ⚠️ Biết nhưng CHƯA sửa (xem báo cáo kiểm tra toàn diện đã gửi cô Thu 2026-09-03): chưa có nút thoát màn làm bài mà không nộp; chưa đổi lại được cách làm bài (type/photo) sau khi đã chọn.

---

## ✅ Đã hoàn thành (tóm tắt, xem lịch sử git để biết chi tiết)

- Soạn giáo án + kế hoạch bài dạy, ra đề (ma trận Bloom, kho ngữ liệu GDPT 2018, trắc nghiệm + tự luận, rubric)
- Chấm bài AI (kể cả ảnh chụp tay qua Claude Vision)
- **Lớp Học Kết Nối** (Firebase): tạo lớp, giao bài, nộp/chấm/trả bài, nhắn tin thời gian thực, báo cáo
- **Cổng Lớp Học**: 5 tab, 2 cách làm bài, PWA cài được trên điện thoại
- Cài đặt AI đa nguồn (Claude/Groq/Ollama), model mặc định `claude-sonnet-5`
- Nút "Aa" chỉnh cỡ chữ (14-24px) + chế độ chữ đậm hơn
- Trợ Lý AI trong app hiểu được toàn bộ chương trình (`APP_HELP_CONTEXT`, tự lấy menu từ code)
- Host dự phòng GitHub Pages (`docs/`) song song Netlify
- **2026-09-03: Bỏ hẳn Zalo**, dọn ~3000 dòng code hệ thống quản lý lớp cũ không dùng
- **2026-09-03: Đã sửa xong cả 3 đợt** từ báo cáo kiểm tra toàn diện (29 phát hiện qua mô phỏng 3 vai: giáo viên máy tính/điện thoại, học sinh Cổng điện thoại) — gồm lỗi RIÊNG TƯ nghiêm trọng (nút "Gửi tất cả" từng làm lộ điểm học sinh ra cả lớp, đã sửa thành gửi riêng), các lỗi hiển thị điện thoại (bảng tràn màn hình, modal bị bàn phím che nút Lưu), và các lỗi nhỏ (thiếu xác nhận trước khi xóa/ghi đè, đồng hồ đếm giờ chạy trước khi học sinh chọn cách làm bài, nút "PowerPoint" ghi sai vì thực chất xuất PDF...)

---

## 🚀 Việc còn tồn đọng / hướng mở rộng tiếp

Chủ động **bỏ qua, không sửa** 2 mục sau từ báo cáo cũ — rủi ro sửa sai cao hơn lợi ích, cần cô Thu tự trải nghiệm trên điện thoại thật rồi quyết định phạm vi cụ thể trước khi làm:
- Đóng modal (nút X) không cảnh báo mất nội dung chưa lưu — lặp lại ở *hầu hết* modal soạn thảo trong app, sửa đúng sẽ phải chạm rất nhiều nơi.
- Vài nút bấm nhỏ hơn khuyến nghị cho ngón tay chạm (<40px) — cần nhìn trên điện thoại thật mới biết chỗ nào thực sự đáng sửa.

Học sinh phải bấm "Vào lớp" mỗi lần mở app (không tự đăng nhập lại) là **chủ đích**, không phải lỗi — code có ghi chú rõ: tránh tự vào nhầm lớp/nhầm tên khi nhiều anh chị em dùng chung 1 điện thoại. Mã lớp + tên đã tự điền sẵn từ lần trước, chỉ cần bấm xác nhận 1 lần.

Hướng khác:
1. **Multi-teacher / phân quyền** — nhiều giáo viên dùng chung 1 trường
2. **Thống kê nâng cao** — biểu đồ tiến bộ HS theo thời gian, so sánh lớp
3. **PowerPoint thật** — nút "Outline PowerPoint" hiện xuất file PDF trình bày dạng slide (đã sửa nhãn cho đúng thực tế, KHÔNG còn ghi nhầm "PowerPoint"); nếu sau này cô Thu cần đúng file .pptx thật, phải cài lại `pptxgenjs` (đã gỡ vì trước đó có tải mà không dùng) và viết code build slide bằng thư viện đó thay vì jsPDF.
4. Dọn tiếp code trùng lặp còn sót (không phải Zalo) nếu tìm thấy — bài học từ vụ Zalo: mỗi khi thêm tính năng, tránh viết lại từ đầu một luồng đã có sẵn ở nơi khác trong app.

---

## 📋 Quy tắc làm việc (đã thống nhất với cô Thu)

1. **Luôn tiếng Việt**, xưng "tôi - cô"
2. **Emoji hoa cỏ/🌸** ở cuối câu để ấm áp (vừa phải, không lạm dụng)
3. **Không dùng** màu indigo/violet/purple/fuchsia trong UI
4. **Verify bằng Babel THẬT** sau mỗi lần sửa file lớn — KHÔNG chỉ đếm ngoặc (dễ báo nhầm vì string/emoji chứa ký tự ngoặc). Lệnh mẫu (cần `@babel/standalone` cài sẵn cục bộ, ví dụ trong thư mục scratchpad):
   ```js
   const Babel = require('<path>/node_modules/@babel/standalone/babel.min.js');
   const script = fs.readFileSync('TroLyGiaoVien_Phase4_REFACTORED.html','utf8').split('<script type="text/babel">')[1].split('</script>')[0];
   Babel.transform(script, { presets: ['react'] }); // throw nếu lỗi cú pháp thật
   ```
5. **Tránh lặp lại công việc đã làm** — đọc file hiện tại trước khi sửa. Cảnh giác với việc code có 2 nơi làm cùng 1 việc (nguồn gốc phần lớn lỗi từng tìm thấy, ví dụ vụ Zalo vs Lớp Học Kết Nối).
6. **⭐ Cập nhật `APP_HELP_CONTEXT_DETAILS`** (trong `TroLyGiaoVien_Phase4_REFACTORED.html`, gần `GROQ_MODEL`) mỗi khi thêm/đổi tính năng lớn. Danh sách menu (`APP_MENU_SUMMARY`) đã tự lấy từ `MENU_ITEMS` nên không cần sửa tay, chỉ thêm id vào `MENU_IMPLEMENTED_IDS` khi 1 tab code xong.
7. **Đồng bộ `docs/`** (GitHub Pages dự phòng) mỗi khi push thay đổi lớn cho `TroLyGiaoVien_Phase4_REFACTORED.html` hoặc `CongHocSinh.html` — copy đè `docs/index.html` + `docs/cong/index.html`, push cùng lúc.
8. **Hạn chế push nhiều lần liên tiếp cho sửa nhỏ** — mỗi push khiến Netlify tự build tốn credit/tháng (đã từng hết credit giữa tháng). Gom nhiều sửa nhỏ, test kỹ, rồi push 1 lần.
9. **Không cần hỏi lại** việc đã quyết định rõ trong file này (ví dụ: đã bỏ Zalo hẳn, không hỏi lại có nên quay lại Zalo không).

Chúc cô Thu dạy tốt! 🌸
