#!/bin/bash
# ============================================================
#  ▶️  MỞ TRỢ LÝ GIÁO VIÊN — chế độ LƯU TRÊN MÁY
#  Nhấp đúp file này để mở chương trình bằng trình duyệt qua localhost,
#  nhờ đó tính năng "Lưu tự động ra thư mục trên máy" mới chạy được.
# ============================================================

# Về đúng thư mục chứa file này
cd "$(dirname "$0")" || exit 1

FILE="TroLyGiaoVien_Phase4_REFACTORED.html"
PORT=8765
URL="http://localhost:${PORT}/${FILE}"

if [ ! -f "$FILE" ]; then
  echo "❌ Không tìm thấy $FILE trong thư mục này."
  echo "   Hãy đặt file .command này cùng thư mục với chương trình."
  read -r -p "Nhấn Enter để đóng..." _
  exit 1
fi

# Nếu máy chủ tự-lưu đã chạy thì dùng lại, không thì khởi động
if ! curl -s "http://localhost:${PORT}/api/health" >/dev/null 2>&1; then
  echo "🚀 Đang khởi động máy chủ tự-lưu ở cổng ${PORT}..."
  if command -v python3 >/dev/null 2>&1; then
    (python3 "trolygv_server.py" >/dev/null 2>&1 &)
  else
    echo "❌ Máy chưa có Python 3. Vui lòng cài Python hoặc báo để được hỗ trợ."
    read -r -p "Nhấn Enter để đóng..." _
    exit 1
  fi
  sleep 2
fi

echo "🌸 Đang mở Trợ Lý Giáo Viên bằng trình duyệt..."
# Ưu tiên mở bằng Chrome, không có thì Cốc Cốc, không có nữa thì trình duyệt mặc định
if open -a "Google Chrome" "$URL" 2>/dev/null; then
  :
elif open -a "CocCoc" "$URL" 2>/dev/null; then
  :
else
  open "$URL"
fi

echo ""
echo "✅ Xong! Cửa sổ trình duyệt đã mở."
echo "   Lần đầu: vào ⚙️ Cài đặt AI → mục '🛟 An toàn dữ liệu' → 'Chọn thư mục lưu trên máy'."
echo "   (Có thể đóng cửa sổ Terminal này lại.)"
