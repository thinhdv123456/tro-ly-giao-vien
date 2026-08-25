#!/bin/bash
# ════════════════════════════════════════════
#  Trợ Lý Giáo Viên — Deploy lên Netlify
#  Bấm đúp vào file này để cập nhật website
# ════════════════════════════════════════════

# Chuyển vào thư mục chứa file
cd "$(dirname "$0")"

echo "🌸 Trợ Lý Giáo Viên — Đang chuẩn bị deploy..."
echo ""

# Đồng bộ file mới nhất vào thư mục deploy
echo "📋 Bước 1: Sao chép file mới nhất vào thư mục deploy..."
cp "TroLyGiaoVien_Phase4_REFACTORED.html" "deploy/index.html"
echo "   ✅ Đã cập nhật deploy/index.html"
echo ""

# Kiểm tra Netlify CLI
echo "🔍 Bước 2: Kiểm tra Netlify CLI..."
if ! command -v netlify &> /dev/null; then
    echo "   ⚙️  Chưa có Netlify CLI — đang cài (1 lần duy nhất)..."
    npm install -g netlify-cli
    if [ $? -ne 0 ]; then
        echo ""
        echo "   ❌ Cài Netlify CLI thất bại."
        echo "   👉 Cô vào app.netlify.com → trolygiaovien → kéo thả thư mục 'deploy' nhé."
        read -p "   Nhấn Enter để đóng..."
        exit 1
    fi
    echo "   ✅ Đã cài Netlify CLI"
else
    echo "   ✅ Netlify CLI đã sẵn sàng"
fi
echo ""

# Deploy
echo "🚀 Bước 3: Đang deploy lên https://trolygiaovien.netlify.app ..."
echo ""
netlify deploy --prod --dir="deploy" --site="5eceaac6-dd84-44a3-a8e0-c44319fc325b"

if [ $? -eq 0 ]; then
    echo ""
    echo "════════════════════════════════════════════"
    echo "✅  DEPLOY THÀNH CÔNG!"
    echo "🔗  https://trolygiaovien.netlify.app"
    echo "════════════════════════════════════════════"
    echo ""
    echo "   Cô mở điện thoại truy cập link trên là thấy bản mới nhất rồi nhé 🌸"
else
    echo ""
    echo "❌ Deploy thất bại. Có thể cần đăng nhập Netlify."
    echo "👉 Chạy lần đầu: netlify login"
fi

echo ""
read -p "Nhấn Enter để đóng cửa sổ này..."
