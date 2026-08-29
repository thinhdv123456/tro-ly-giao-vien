#!/bin/bash
# ============================================================
#  🔼 LƯU & ĐẨY LÊN — Trợ Lý Giáo Viên
#  Bấm đúp file này SAU KHI làm xong, để lưu mọi thay đổi
#  và đẩy lên GitHub (máy khác pull về là có ngay).
# ============================================================
cd "$(dirname "$0")" || exit 1

echo "============================================================"
echo "  🔼 ĐANG LƯU & ĐẨY THAY ĐỔI LÊN GITHUB..."
echo "============================================================"
echo ""

# Lấy bản mới trước cho an toàn (tránh xung đột khi đẩy)
git pull --no-edit

git add -A

if git diff --cached --quiet; then
  echo "ℹ️  Không có thay đổi nào mới để lưu."
else
  git commit -m "Cập nhật $(date '+%d/%m/%Y %H:%M')"
  git push
  if [ $? -eq 0 ]; then
    echo ""
    echo "✅ ĐÃ ĐẨY LÊN GITHUB XONG! Máy khác chỉ cần bấm '🔽 Lấy bản mới' là có."
  else
    echo ""
    echo "⚠️  Đẩy lên chưa được (xem dòng chữ ở trên). Chụp màn hình gửi Claude giúp cô."
  fi
fi
echo ""
read -n 1 -s -r -p "Bấm phím bất kỳ để đóng cửa sổ này..."
echo ""
