#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================
#  MÁY CHỦ NỘI BỘ — TRỢ LÝ GIÁO VIÊN
#  Vừa phục vụ trang web, vừa TỰ LƯU toàn bộ dữ liệu vào 1 file thật trên máy.
#  Không gửi đi đâu cả — chỉ chạy trên chính máy này (localhost).
# ============================================================
import http.server
import os
import json
import shutil
import datetime
import urllib.request
import urllib.error
from http.server import ThreadingHTTPServer

PORT = 8765
# Model Claude mặc định cho tác vụ nặng (chấm bài, sinh đề...). Có thể đổi ở app.
CLAUDE_MODEL_DEFAULT = "claude-sonnet-5"
CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"
BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE, "DuLieu")
DATA_FILE = os.path.join(DATA_DIR, "TroLyGiaoVien_DuLieu.json")
BAK_FILE = os.path.join(DATA_DIR, "TroLyGiaoVien_DuLieu.bak.json")
SNAP_DIR = os.path.join(DATA_DIR, "SaoLuu_TheoNgay")
# Hộp thư đến từ Zalo: bộ đọc Zalo (zalo_reader.py) đẩy bài HS vào đây,
# app đọc ra rồi đưa vào thư viện chấm bài.
INBOX_FILE = os.path.join(DATA_DIR, "ZaloInbox.json")
IMG_DIR = os.path.join(DATA_DIR, "ZaloAnh")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(SNAP_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)


def _load_inbox():
    if os.path.exists(INBOX_FILE):
        try:
            with open(INBOX_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def _save_inbox(items):
    tmp = INBOX_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    os.replace(tmp, INBOX_FILE)


def _call_claude(prompt, max_tokens, api_key, model):
    """Gọi Anthropic Messages API phía máy chủ (tránh CORS của trình duyệt).
    Trả về (text, error). API key lấy từ app (localStorage) hoặc biến môi trường."""
    key = (api_key or os.environ.get("ANTHROPIC_API_KEY")
           or os.environ.get("CLAUDE_API_KEY") or "").strip()
    if not key:
        return None, "Chưa có Claude API Key (nhập trong Cài đặt AI hoặc đặt biến ANTHROPIC_API_KEY)"

    body = json.dumps({
        "model": model or CLAUDE_MODEL_DEFAULT,
        "max_tokens": int(max_tokens or 1024),
        "messages": [{"role": "user", "content": prompt or ""}],
    }).encode("utf-8")

    req = urllib.request.Request(
        CLAUDE_API_URL,
        data=body,
        method="POST",
        headers={
            "content-type": "application/json",
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        # Ghép các khối text trong content lại
        parts = [b.get("text", "") for b in data.get("content", []) if b.get("type") == "text"]
        return ("".join(parts).strip() or "(Claude không trả về nội dung)"), None
    except urllib.error.HTTPError as e:
        try:
            err = json.loads(e.read().decode("utf-8"))
            msg = err.get("error", {}).get("message", str(e))
        except Exception:
            msg = "HTTP %s" % e.code
        return None, "Claude API lỗi: %s" % msg
    except Exception as e:
        return None, "Lỗi kết nối Claude: %s" % e


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE, **kwargs)

    def _send_json(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/api/health":
            return self._send_json(200, {"ok": True, "mode": "server", "file": DATA_FILE})
        if self.path == "/api/data":
            if os.path.exists(DATA_FILE):
                try:
                    with open(DATA_FILE, "r", encoding="utf-8") as f:
                        return self._send_json(200, {"ok": True, "data": json.load(f)})
                except Exception as e:
                    return self._send_json(200, {"ok": True, "data": None, "error": str(e)})
            return self._send_json(200, {"ok": True, "data": None})
        # App gọi vào đây để lấy các bài Zalo đang chờ đưa vào chấm bài
        if self.path == "/api/zalo/inbox":
            items = _load_inbox()
            return self._send_json(200, {"ok": True, "count": len(items), "items": items})
        return super().do_GET()

    def do_POST(self):
        if self.path == "/api/data":
            try:
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length)
                payload = json.loads(raw.decode("utf-8"))

                # 1) Giữ bản trước đó làm dự phòng nhanh (.bak)
                if os.path.exists(DATA_FILE):
                    try:
                        shutil.copy2(DATA_FILE, BAK_FILE)
                    except Exception:
                        pass

                # 2) Ghi an toàn: ghi ra file tạm rồi thay thế (tránh hỏng nếu mất điện giữa chừng)
                tmp = DATA_FILE + ".tmp"
                with open(tmp, "w", encoding="utf-8") as f:
                    json.dump(payload, f, ensure_ascii=False, indent=2)
                os.replace(tmp, DATA_FILE)

                # 3) Mỗi ngày lưu thêm 1 ảnh chụp (snapshot) để lỡ có gì còn lần ngược lại được
                try:
                    today = datetime.date.today().isoformat()
                    snap = os.path.join(SNAP_DIR, "DuLieu_" + today + ".json")
                    if not os.path.exists(snap):
                        shutil.copy2(DATA_FILE, snap)
                        # chỉ giữ 30 bản gần nhất
                        snaps = sorted(
                            [p for p in os.listdir(SNAP_DIR) if p.endswith(".json")]
                        )
                        for old in snaps[:-30]:
                            try:
                                os.remove(os.path.join(SNAP_DIR, old))
                            except Exception:
                                pass
                except Exception:
                    pass

                return self._send_json(200, {"ok": True})
            except Exception as e:
                return self._send_json(500, {"ok": False, "error": str(e)})

        # 🤖 Cửa trung gian gọi Claude API (app gửi prompt + key -> máy chủ gọi hộ)
        if self.path == "/api/claude/message":
            try:
                length = int(self.headers.get("Content-Length", 0))
                payload = json.loads(self.rfile.read(length).decode("utf-8"))
                text, err = _call_claude(
                    payload.get("prompt"),
                    payload.get("maxTokens", 1024),
                    payload.get("apiKey"),
                    payload.get("model"),
                )
                if err:
                    return self._send_json(502, {"error": err})
                return self._send_json(200, {"text": text})
            except Exception as e:
                return self._send_json(500, {"error": str(e)})

        # 📥 Bộ đọc Zalo đẩy bài HS vào hộp thư đến
        if self.path == "/api/zalo":
            try:
                length = int(self.headers.get("Content-Length", 0))
                item = json.loads(self.rfile.read(length).decode("utf-8"))
                items = _load_inbox()
                # Chống trùng: bỏ qua nếu đã có cùng id
                new_id = item.get("id")
                if new_id and any(x.get("id") == new_id for x in items):
                    return self._send_json(200, {"ok": True, "duplicate": True, "count": len(items)})
                item.setdefault("receivedAt", datetime.datetime.now().isoformat())
                items.append(item)
                _save_inbox(items)
                return self._send_json(200, {"ok": True, "count": len(items)})
            except Exception as e:
                return self._send_json(500, {"ok": False, "error": str(e)})

        # 🧹 App báo đã nhập xong -> xoá hộp thư đến
        if self.path == "/api/zalo/clear":
            try:
                _save_inbox([])
                return self._send_json(200, {"ok": True})
            except Exception as e:
                return self._send_json(500, {"ok": False, "error": str(e)})

        return self._send_json(404, {"ok": False, "error": "not found"})

    def log_message(self, *args):
        pass  # chạy im lặng cho gọn


if __name__ == "__main__":
    os.chdir(BASE)
    try:
        with ThreadingHTTPServer(("127.0.0.1", PORT), Handler) as httpd:
            print("=" * 52)
            print("  ✅ May chu Tro Ly Giao Vien dang chay")
            print("  🌐 Dia chi : http://localhost:%d" % PORT)
            print("  💾 Du lieu : %s" % DATA_FILE)
            print("  (Dong cua so nay se tat may chu)")
            print("=" * 52)
            httpd.serve_forever()
    except OSError as e:
        # Cong da co server chay san -> khong sao, thoat nhe nhang
        print("ℹ️  Co ve may chu da chay san o cong %d (%s)." % (PORT, e))
    except KeyboardInterrupt:
        pass
