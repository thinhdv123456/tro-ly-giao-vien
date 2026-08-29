#!/bin/bash
# ============================================================
#  🔽 LẤY BẢN MỚI — Trợ Lý Giáo Viên
#  Bấm đúp file này TRƯỚC KHI bắt đầu làm việc, để lấy bản
#  mới nhất từ GitHub về máy này (tránh làm trên bản cũ).
# ============================================================
cd "$(dirname "$0")" || exit 1

echo "============================================================"
echo "  🔽 ĐANG LẤY BẢN MỚI NHẤT TỪ GITHUB..."
echo "============================================================"
echo ""

git pull

echo ""
if [ $? -eq 0 ]; then
  echo "✅ XONG! Máy này đã có bản mới nhất. Cô có thể bắt đầu làm."
else
  echo "⚠️  Có trục trặc khi lấy bản mới (xem dòng chữ ở trên)."
  echo "    Nếu báo 'conflict' hoặc lỗi lạ, chụp màn hình gửi Claude giúp cô."
fi
echo ""
read -n 1 -s -r -p "Bấm phím bất kỳ để đóng cửa sổ này..."
echo ""
