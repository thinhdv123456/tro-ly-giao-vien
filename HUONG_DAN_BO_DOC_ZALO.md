# 🤖 Hướng dẫn Bộ Đọc Zalo — Trợ Lý Giáo Viên

> Bộ đọc này chạy **trên máy của cô** (Mac hoặc Windows). Nó **chỉ đọc các nhóm cô cho phép**, tải bài học sinh, rồi đưa vào app để chấm. **Dữ liệu chỉ ở máy cô**, không gửi đi đâu.

---

## ⚠️ Đọc trước khi dùng (quan trọng)
- Việc tự động đọc Zalo **vẫn có rủi ro bị Zalo khoá số**. Bộ đọc đã chạy **chậm, giống người thật** để giảm rủi ro, nhưng **không phải 0%**.
- Nên cân nhắc dùng **số Zalo phụ** cho an toàn (cô chọn số chính thì vẫn được, cứ chạy chậm).
- **Phiên đăng nhập Zalo** được lưu trong `DuLieu/zalo_browser_profile/` và đã được `.gitignore` — **không bao giờ** bị đẩy lên GitHub.

---

## 1️⃣ Cài đặt (làm 1 lần)

### Bước A — Cần có Python 3
- **Mac:** thường có sẵn. Kiểm tra: mở **Terminal**, gõ `python3 --version`.
- **Windows:** tải ở python.org, khi cài **nhớ tích “Add Python to PATH”**. Kiểm tra ở **PowerShell**: `python --version`.

### Bước B — Vào thư mục dự án
- **Mac (Terminal):**
  ```bash
  cd ~/Documents/tro-ly-giao-vien
  ```
- **Windows (PowerShell):**
  ```powershell
  cd $HOME\Documents\tro-ly-giao-vien
  ```
  *(nếu dự án nằm chỗ khác, sửa lại đường dẫn cho đúng)*

### Bước C — Cài thư viện
- **Mac:**
  ```bash
  pip3 install -r requirements.txt
  python3 -m playwright install chromium
  ```
- **Windows:**
  ```powershell
  pip install -r requirements.txt
  python -m playwright install chromium
  ```

---

## 2️⃣ Khai báo các nhóm muốn đọc (danh sách trắng)

1. Chạy bộ đọc lần đầu để nó tạo file cấu hình:
   - Mac: `python3 zalo_reader.py`  ·  Windows: `python zalo_reader.py`
2. Nó tạo file **`zalo_reader_config.json`**. Mở file đó bằng trình soạn thảo, sửa mục `groups` thành **đúng tên nhóm** của cô:
   ```json
   "groups": [
     "Ngữ văn 7A - Cô Thu",
     "Phụ huynh 8B"
   ],
   ```
   > Tên phải khớp với tên hiển thị của nhóm trong Zalo. Muốn thêm/bớt nhóm, cứ sửa danh sách này.

---

## 3️⃣ Chạy bộ đọc

1. **Mở app Trợ Lý bằng nút “▶️ Mở Trợ Lý (lưu trên máy)”** trước — để máy chủ nội bộ (`localhost:8765`) chạy (nơi nhận bài).
2. Chạy bộ đọc:
   - Mac: `python3 zalo_reader.py`  ·  Windows: `python zalo_reader.py`
3. Lần đầu sẽ hiện **cửa sổ trình duyệt + mã QR**. Cô **mở Zalo trên điện thoại → quét QR** để đăng nhập. (Chỉ cần 1 lần, các lần sau nhớ luôn.)
4. Bộ đọc sẽ lần lượt vào từng nhóm trong danh sách, lấy tin mới + tải ảnh bài, rồi gửi vào app. Cứ vài phút quét lại một lần.

**Chạy thử 1 vòng rồi dừng** (để kiểm tra): thêm `--once`
```
python3 zalo_reader.py --once
```

---

## 4️⃣ Nếu Zalo đổi giao diện (bộ đọc không lấy được tin)

Zalo Web thỉnh thoảng đổi cấu trúc, khiến bộ đọc “không thấy” tin. Khi đó chạy **chế độ hiệu chỉnh**:
```
python3 zalo_reader.py --calibrate
```
Nó lưu 2 file vào `DuLieu/`: `zalo_calibrate.png` (ảnh màn hình) và `zalo_calibrate.html` (mã trang).
→ **Gửi 2 file này cho phiên Claude chạy trên máy** (mở `claude` trong Terminal), bảo *“chỉnh SELECTORS trong zalo_reader.py cho khớp Zalo hiện tại”*. Đây là bước cần làm **trên máy thật** vì phải nhìn thấy Zalo Web đang đăng nhập.

---

## 5️⃣ Dữ liệu đi đâu?
- Bài + ảnh HS → gửi vào **hộp thư đến** trên máy chủ nội bộ (`DuLieu/ZaloInbox.json`, ảnh ở `DuLieu/ZaloAnh/`).
- Trong app, phần **“Nhận bài từ Zalo”** (sẽ dựng ở bước sau) sẽ lấy các bài này đưa vào **thư viện chấm bài**.
- Mọi thứ **nằm trong máy cô**. (Dữ liệu lớp/điểm chính vẫn đồng bộ đa thiết bị qua Firebase như thường.)

---

## ❓ Lỗi thường gặp
| Hiện tượng | Cách xử lý |
|---|---|
| `command not found: python3` | Cài Python 3 (Bước A) |
| `No module named playwright` | Chạy lại Bước C |
| “Không gửi được về máy chủ” | Mở app bằng nút “▶️ Mở Trợ Lý” trước cho máy chủ chạy |
| Không lấy được tin | Chạy `--calibrate` rồi nhờ Claude trên máy chỉnh selector |
| Hiện lại QR mỗi lần | Đừng xoá thư mục `DuLieu/zalo_browser_profile/` |
