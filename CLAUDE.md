# 📘 BÀN GIAO DỰ ÁN — Trợ Lý Giáo Viên Ngữ Văn THCS

> **Dành cho session mới:** File này tóm tắt toàn bộ trạng thái dự án. Đọc xong là có thể tiếp tục ngay, không cần hỏi lại cô Thu.
> **Cập nhật lần cuối:** 2026-05-01 — Giai đoạn A hoàn thành (Kho Ngữ Liệu GDPT 2018 + Trắc nghiệm + Rubric)

---

## 👤 Người dùng

- **Tên:** Cô Thu (sinh 1979, ~47 tuổi)
- **Nghề:** Giáo viên Ngữ văn THCS
- **Email:** thinhdv1@gmail.com
- **Ngôn ngữ giao tiếp:** Tiếng Việt, xưng "tôi - cô"
- **Tính cách thiết kế:** Trung niên, nữ tính nhưng chuyên nghiệp — tránh màu chói, childish

---

## 🎨 Bảng màu đã chọn (Palette "Cô Thu")

```css
--c-primary: #0f766e       /* Teal đậm */
--c-primary-soft: #14b8a6  /* Teal nhẹ */
--c-accent: #be185d        /* Rose đậm */
--c-accent-soft: #ec4899   /* Rose nhẹ */
--c-gold: #d97706          /* Gold ấm */
--c-cream: #fdfaf6         /* Kem trắng */
--c-cream-deep: #f5ede1    /* Kem đậm */
--c-ink: #3c2a21           /* Nâu đất ấm */
--c-border: #e7dcd0
```

**Font:** Be Vietnam Pro (body) + Playfair Display (heading decorative)

**Quy tắc mapping Tailwind:**
- `bg-teal-700` cho nút chính, `bg-rose-700` cho nút AI/chấm bài
- `bg-teal-50` + `text-teal-700` cho tag/pill
- `bg-rose-50` + `text-rose-700` cho AI tag/pill
- Gradient: `from-rose-* to-amber-*` (ấm), `from-teal-* to-cyan-*` (lạnh)
- ❌ Không dùng: `indigo-*`, `violet-*`, `purple-*`, `fuchsia-*` (đã purge hết)

**CSS utility classes đã tạo trong `<style>`:**
`.soft-card` `.cream-card` `.teal-card` `.rose-card` `.btn-primary` `.btn-accent` `.btn-gold` `.tab-chip` `.flourish-underline` `.glass-header` `.pill` `.gradient-bg`

---

## 📂 Các file chính

| File | Mô tả | Trạng thái |
|------|-------|-----------|
| `TroLyGiaoVien_Phase4_REFACTORED.html` ⭐ | **REFACTORED (đang dùng):** Gộp Grading vào Classes + Zalo tích hợp đầy đủ | ✅ Sản xuất |
| `TroLyGiaoVien_Phase4_Groq_v2_UPDATED.html` | Bản gốc Phase 4 (trước refactor) | 🗂️ Lưu trữ |
| `ZALO_INTEGRATION_GUIDE.md` | Hướng dẫn chi tiết 5 bước sử dụng Zalo (tiếng Việt) | 📖 Hướng dẫn |
| `deploy/index.html` | Copy của Phase 4 REFACTORED (sẵn deploy Netlify) | 🚀 Deploy |
| `TroLyGiaoVien_Phase1.html` | Phase 1: Soạn giáo án + Kế hoạch bài dạy | 🗂️ Lưu trữ |
| `TroLyGiaoVien_Phase2.html` | Phase 2: + Soạn đề + Ngân hàng câu hỏi | 🗂️ Lưu trữ |
| `TroLyGiaoVien_Phase3.html` | Phase 3: + Chấm bài AI + Portfolio HS | 🗂️ Lưu trữ |

---

## 🧱 Kiến trúc kỹ thuật

**Stack:** 1 file HTML độc lập (không cần build)
- React 18 + Babel standalone (JSX in-browser)
- Tailwind CSS qua CDN
- Tesseract.js (OCR chữ tay tiếng Việt)
- html2pdf.js (export PDF)
- LocalStorage (persistence, key: `tro_ly_gv_nguvan_thcs_v3`)
- Export Word: Blob + HTML trick
- Export Excel: SheetJS không dùng — dùng CSV tải xuống

**Trạng thái code hiện tại (Phase 4.3 — Giai đoạn A):**
- **6,642 dòng** (+663 so với Phase 4.2), ✅ Babel parse OK
- Version: 4.3 · Kho Ngữ Liệu GDPT 2018 + Trắc nghiệm + Rubric 🌸

**Các component lớn:**
- `Dashboard` — cream-card hero + 6 stat cards gradient + quick-start
- `PlanningTab` — soạn kế hoạch bài dạy
- `LessonTab` — soạn giáo án + export PPTX (jsPDF)
- **`ExamTab`** — 5 sub-tabs (MỚI: thêm tab Kho Ngữ Liệu):
  - **Đề kiểm tra** (`ExamModal`) — ma trận × Bloom, ngữ liệu từ kho, trắc nghiệm, rubric
  - **🤖 Ra Đề Tự Động** (`AutoGenExamView`) — lọc theo loại VB + chủ đề, prompt GDPT 2018
  - **📚 Kho Ngữ Liệu** (`KhoNguLieuTab`) — CRUD + duyệt + dán văn bản nhanh ⭐ MỚI
  - **Ma trận đề** (`MatrixModal`)
  - **Ngân hàng câu hỏi** (`QuestionBankModal`) — hỗ trợ tự luận + trắc nghiệm A/B/C/D ⭐ MỚI
- **`ClassesTab`** — 4 sub-tabs: classes | grading | zalo-main | report
- `ZaloSettingsView / ZaloMonitorView / ZaloCollectorView / ZaloRemindView / ZaloHistoryView`

**Hằng số quan trọng (MỚI thêm):**
```js
const LOAI_VAN_BAN = [
  { id: 'van_hoc', ten: 'Văn học', icon: '📖' },       // truyện, thơ, ký, kịch
  { id: 'thong_tin', ten: 'Thông tin', icon: '📰' },    // báo chí, hướng dẫn
  { id: 'nghi_luan', ten: 'Nghị luận', icon: '💬' },   // nghị luận xã hội/văn học
  { id: 'hanh_chinh', ten: 'Hành chính-Công vụ', icon: '📋' }, // đơn, thông báo
];
```

**PASSAGES_BANK v2** (20 ngữ liệu, metadata đầy đủ):
- Mỗi item: `{ id, title, author, source, class, genre, subgenre, theme, difficulty, copyright_status, approved, wordCount, excerpt, fullText }`
- ID format: `VH_6_001` (Văn học lớp 6), `TT_7_001` (Thông tin lớp 7), `NL_8_001` (Nghị luận lớp 8), `HC_6_001` (Hành chính lớp 6)
- copyright_status: `'public_domain'` | `'nha_nuoc'` | `'education_use'` | `'unknown'`

**Data model (`data`) — đã bổ sung `passages`:**
```js
{
  plans: [], lessons: [], exams: [], questionBank: [],
  gradings: [{id,title,grade,type,score,maxScore,feedback,annotations,...}],
  classes: [{id,name,grade,students:[{id,name,parentPhone,parentName,zaloName,note}]}],
  assignments: [], submissions: [],
  // ⭐ MỚI - Kho ngữ liệu do cô tự thêm (kho tĩnh PASSAGES_BANK không lưu ở đây)
  passages: [{
    id: 'USR_xxx', title, author, source, class, genre, subgenre, theme,
    difficulty, copyright_status, approved: true/false,
    wordCount, excerpt, fullText, addedAt
  }],
  zaloConfig: { phone, groups, apiKey, updatedAt },
  zaloSubmissions: [{ id, studentName, assignmentTitle, content, timestamp, status }]
}
```

**ExamModal — tính năng mới:**
- `passageGenre` field — lọc ngữ liệu theo loại VB
- `passageAuthor` field — hiển thị tác giả trong đề
- `rubric: [{cauSo, tienChi:[{y, diem, goi_y}]}]` — barem có cấu trúc cho phần Viết
- Preview 3 chế độ: Đề | Đáp án | **Rubric** (mới)
- Dropdown "Chọn từ kho ngữ liệu" lấy từ `[...PASSAGES_BANK, ...data.passages]`

**QuestionBankModal — tính năng mới:**
- `type: 'essay' | 'mc'` — chọn loại câu hỏi
- `options: ['','','','']` — 4 lựa chọn A/B/C/D
- `correctAnswer: 'A'|'B'|'C'|'D'` — đáp án đúng

**Key helpers:**
- `slugifyVN(str)` — NFD normalize + strip diacritics
- `chamBaiTuDong(text, config)` — engine chấm AI rule-based
- `buildAssignmentZaloMessage / buildReminderZaloMessage / buildFeedbackZaloMessage`
- Copy-paste workflow: `navigator.clipboard.writeText(msg)` + `window.open('https://chat.zalo.me/')`

---

## ✅ Đã hoàn thành

- [x] **Phase 1:** Soạn giáo án + kế hoạch bài dạy
- [x] **Phase 2:** Soạn đề + ngân hàng câu hỏi + tự động sinh đề
- [x] **Phase 3:** Chấm bài AI + OCR + sổ theo dõi HS + báo cáo lớp + phiếu phụ huynh
- [x] **Phase 4:** Quản lý lớp + giao/nộp/chấm/trả bài qua Zalo + đồng bộ ảnh→HS
- [x] **Phase 4 Refactored:** Gộp Grading vào Classes + Zalo integration đầy đủ
- [x] **Zalo Integration (Phase 4.2):** Settings / Monitor / Collector / Remind / History
- [x] **UI redesign:** bảng màu cô Thu (teal + rose + cream), font Be Vietnam Pro + Playfair
- [x] **Documentation:** Hướng dẫn sử dụng Zalo chi tiết (tiếng Việt)
- [x] **⭐ Giai đoạn A — GDPT 2018 (2026-05-01):**
  - [x] `LOAI_VAN_BAN` — 4 loại văn bản (Văn học, Thông tin, Nghị luận, Hành chính)
  - [x] `PASSAGES_BANK v2` — 20 ngữ liệu, metadata đầy đủ (genre, copyright, wordCount...)
  - [x] `THEMES` mở rộng 15 chủ đề phủ 4 loại văn bản
  - [x] `KhoNguLieuTab` — CRUD ngữ liệu, duyệt pending/approved, dán văn bản 2 bước
  - [x] `PassageModal` + `PastePassageModal` — thêm/sửa ngữ liệu với metadata
  - [x] `QuestionBankModal` — hỗ trợ tự luận + trắc nghiệm A/B/C/D
  - [x] `ExamModal` — chọn loại văn bản, chọn từ kho, trắc nghiệm, rubric cấu trúc
  - [x] `AutoGenExamView` — lọc theo loại VB + chủ đề, prompt AI chuẩn GDPT 2018

---

## 🚀 Các hướng mở rộng tiếp (Phase 5+ gợi ý)

1. **Backend Firebase/Supabase** — đồng bộ dữ liệu đa thiết bị (hiện LocalStorage chỉ 1 máy)
2. **Zalo Mini App** — push thông báo thật, không cần copy-paste
3. **AI thật (Claude API / Gemini)** — chấm bài chính xác hơn thay engine rule-based
4. **PWA** — cài như app trên điện thoại, offline-first
5. **Multi-teacher** — login + phân quyền nhiều giáo viên/1 trường
6. **Thống kê nâng cao** — chart tiến bộ từng HS theo thời gian, so sánh lớp

---

## 📋 Quy tắc làm việc (đã thống nhất với cô Thu)

1. **Luôn tiếng Việt**, xưng "tôi - cô"
2. **Emoji hoa cỏ/🌸** ở cuối câu để ấm áp (vừa phải, không lạm dụng)
3. **Không dùng** màu indigo/violet/purple/fuchsia trong UI
4. **Babel verify** sau mỗi lần sửa file lớn (dùng script kiểm tra braces/parens/brackets)
5. **Khi tạo file mới**, lưu vào `/sessions/youthful-quirky-turing/mnt/TRO LY GIAO VIEN/` và link `computer://` để cô mở
6. **Tránh lặp lại công việc đã làm** — đọc file hiện tại trước khi sửa

---

## 🔁 Lời nhắc cho Claude session mới

**Nếu cô Thu yêu cầu tiếp tục/sửa/mở rộng:**

1. ⭐ **File chính:** `TroLyGiaoVien_Phase4_REFACTORED.html` (không phải Phase4.html cũ)
2. **Hướng dẫn Zalo:** Đọc `ZALO_INTEGRATION_GUIDE.md` để hiểu quy trình copy-paste
3. **Tôn trọng cấu trúc:**
   - ClassesTab có 4 sub-tabs: classes | grading (GradingTabView) | zalo-main | report
   - Zalo có 5 sub-views: settings | monitor | collector | remind | history
   - Lưu dữ liệu vào `data.zaloConfig` + `data.zaloSubmissions`
4. **Palette + CSS:** Teal (#0f766e), Rose (#be185d), Cream (#fdfaf6) — không đổi
5. **Verify:** Node script kiểm tra braces/parens/brackets (phải balanced)
6. **Deploy:** Copy sang `deploy/index.html` trước khi lên Netlify

**Phase 5+ (API Zalo thực):**
- Kết nối Zalo API → tự động nhận/gửi tin (không copy-paste)
- Dùng file này làm base, thêm API handlers vào ZaloSettingsView
- Test kỹ trước deploy (API key sensitive)

Chúc cô Thu dạy tốt! 🌸
