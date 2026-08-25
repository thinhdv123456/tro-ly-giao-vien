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
from http.server import ThreadingHTTPServer

PORT = 8765
BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE, "DuLieu")
DATA_FILE = os.path.join(DATA_DIR, "TroLyGiaoVien_DuLieu.json")
BAK_FILE = os.path.join(DATA_DIR, "TroLyGiaoVien_DuLieu.bak.json")
SNAP_DIR = os.path.join(DATA_DIR, "SaoLuu_TheoNgay")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(SNAP_DIR, exist_ok=True)


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
