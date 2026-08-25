#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================
#  🤖 BỘ ĐỌC ZALO — TRỢ LÝ GIÁO VIÊN  (chạy trên MÁY của cô: Mac / Windows)
# ============================================================
#  NGUYÊN TẮC AN TOÀN — đọc kỹ:
#   • CHỈ đọc các nhóm cô ghi trong "groups" của file cấu hình (danh sách trắng).
#     Không đụng tin nhắn riêng hay nhóm khác.
#   • Dữ liệu đọc được CHỈ gửi về máy chủ nội bộ trên chính máy này (localhost),
#     KHÔNG gửi ra ngoài, KHÔNG gửi cho ai khác.
#   • Đăng nhập Zalo bằng QR MỘT LẦN; phiên đăng nhập lưu trong DuLieu/ (đã được
#     .gitignore nên KHÔNG bao giờ bị đẩy lên GitHub).
#   • Chạy CHẬM, giống người thật, để giảm rủi ro Zalo khoá số. Không spam.
#
#  ⚠️ LƯU Ý KỸ THUẬT: Zalo Web đổi giao diện theo thời gian, nên các "selector"
#     ở mục SELECTORS bên dưới có thể cần tinh chỉnh TRÊN MÁY THẬT (xem README).
#     Chạy chế độ hiệu chỉnh:   python zalo_reader.py --calibrate
#     Nó sẽ lưu ảnh + mã trang vào DuLieu/ để dò đúng selector.
# ============================================================

import json
import os
import sys
import time
import random
import hashlib
import datetime
import urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parent
DATA_DIR = BASE / "DuLieu"
DATA_DIR.mkdir(exist_ok=True)
CONFIG_FILE = BASE / "zalo_reader_config.json"
EXAMPLE_FILE = BASE / "zalo_reader_config.example.json"
STATE_FILE = DATA_DIR / "zalo_reader_state.json"          # nhớ tin đã gửi (chống trùng)
PROFILE_DIR = DATA_DIR / "zalo_browser_profile"           # phiên đăng nhập Zalo (bí mật)
IMG_DIR = DATA_DIR / "ZaloAnh"
IMG_DIR.mkdir(exist_ok=True)

DEFAULT_CONFIG = {
    "server_url": "http://localhost:8765",
    "groups": [
        "Ngữ văn 7A - Cô Thu",
        "Phụ huynh 8B"
    ],
    "poll_seconds": 90,          # nghỉ giữa 2 vòng quét (chậm cho an toàn)
    "delay_min": 2.5,            # nghỉ tối thiểu giữa các thao tác (giây)
    "delay_max": 6.0,            # nghỉ tối đa giữa các thao tác (giây)
    "messages_per_group": 25,    # số tin gần nhất lấy mỗi nhóm
    "download_images": True,
    "headless": False            # để thấy cửa sổ trình duyệt (cần thấy để quét QR)
}

# ------------------------------------------------------------
#  SELECTORS — chỉnh ở đây nếu Zalo đổi giao diện (xem README)
# ------------------------------------------------------------
SELECTORS = {
    # Dấu hiệu ĐÃ đăng nhập (khung chat hiện ra)
    "logged_in": "#main, .chat-container, [class*='conversation']",
    # Ô tìm kiếm để mở đúng nhóm theo tên
    "search_box": "input[type='text'][placeholder*='m ki'], input#contact-search-input, input[placeholder*='Tìm']",
    # Một dòng tin nhắn trong khung chat
    "message_row": ".msg, [class*='message-'], [class*='chat-item']",
    # Trong 1 dòng tin: tên người gửi / nội dung / thời gian / ảnh
    "message_sender": "[class*='sender'], [class*='author'], [class*='name']",
    "message_text": "[class*='text'], [class*='content'] span",
    "message_time": "[class*='time'], time",
    "message_image": "img[src*='zalo'], img[src^='blob:'], img[src^='http']",
}


# ------------------------------------------------------------
#  Tiện ích
# ------------------------------------------------------------
def load_config():
    if not CONFIG_FILE.exists():
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, ensure_ascii=False, indent=2)
        print("📝 Đã tạo file cấu hình mẫu: %s" % CONFIG_FILE.name)
        print("   → Hãy MỞ file đó, sửa danh sách 'groups' đúng TÊN NHÓM của cô, rồi chạy lại.")
        sys.exit(0)
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    # bổ sung khoá thiếu bằng mặc định
    for k, v in DEFAULT_CONFIG.items():
        cfg.setdefault(k, v)
    return cfg


def load_state():
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except Exception:
            return set()
    return set()


def save_state(seen):
    tmp = str(STATE_FILE) + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(sorted(seen), f)
    os.replace(tmp, STATE_FILE)


def gentle_sleep(cfg):
    time.sleep(random.uniform(cfg["delay_min"], cfg["delay_max"]))


def msg_key(group, sender, text, tstamp):
    raw = "|".join([group, sender or "", text or "", tstamp or ""])
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16]


def simple_classify(text):
    """Phân loại thô (không cần AI). AI có thể nâng cấp sau ở phần 'trợ lý trực nhóm'."""
    t = (text or "").lower()
    if any(w in t for w in ["nộp bài", "bài làm", "em gửi bài", "bài tập của em"]):
        return "nop_bai"
    if any(w in t for w in ["xin nghỉ", "cho em nghỉ", "con nghỉ", "xin phép"]):
        return "xin_nghi"
    if "?" in t or any(w in t for w in ["cô ơi", "cho em hỏi", "hỏi cô", "khi nào", "ở đâu", "thế nào", "bao giờ"]):
        return "cau_hoi"
    if any(w in t for w in ["vâng", "dạ", "cảm ơn", "cám ơn", "ok", "đã nhận"]):
        return "xa_giao"
    return "khac"


def push_to_server(cfg, item):
    url = cfg["server_url"].rstrip("/") + "/api/zalo"
    body = json.dumps(item, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST",
                                 headers={"content-type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print("   ⚠️ Không gửi được về máy chủ (%s đang chạy chưa?): %s" % (cfg["server_url"], e))
        return None


# ------------------------------------------------------------
#  Thao tác trên Zalo Web (Playwright)
# ------------------------------------------------------------
def ensure_login(page):
    """Chờ tới khi đăng nhập xong (cô quét QR bằng điện thoại nếu cần)."""
    print("🔐 Đang mở Zalo Web... Nếu hiện mã QR, cô mở Zalo trên điện thoại để quét.")
    for _ in range(180):  # chờ tối đa ~6 phút
        try:
            if page.query_selector(SELECTORS["logged_in"]):
                print("✅ Đã đăng nhập Zalo.")
                return True
        except Exception:
            pass
        time.sleep(2)
    print("❌ Chưa đăng nhập được (hết thời gian chờ).")
    return False


def open_group(page, name, cfg):
    """Mở đúng 1 nhóm theo tên qua ô tìm kiếm."""
    box = page.query_selector(SELECTORS["search_box"])
    if not box:
        print("   ⚠️ Không thấy ô tìm kiếm — cần tinh chỉnh selector (chạy --calibrate).")
        return False
    box.click()
    gentle_sleep(cfg)
    box.fill("")
    box.type(name, delay=random.randint(40, 110))  # gõ như người
    gentle_sleep(cfg)
    # Nhấn Enter hoặc click kết quả đầu tiên khớp tên
    page.keyboard.press("Enter")
    gentle_sleep(cfg)
    return True


def read_recent_messages(page, group, cfg):
    """Đọc các tin gần nhất trong khung chat hiện tại."""
    out = []
    rows = page.query_selector_all(SELECTORS["message_row"])
    rows = rows[-cfg["messages_per_group"]:] if rows else []
    for row in rows:
        try:
            def pick(sel):
                el = row.query_selector(sel)
                return (el.inner_text().strip() if el else "")
            sender = pick(SELECTORS["message_sender"])
            text = pick(SELECTORS["message_text"]) or row.inner_text().strip()
            tstamp = pick(SELECTORS["message_time"])
            images = []
            if cfg["download_images"]:
                for img in row.query_selector_all(SELECTORS["message_image"]):
                    src = img.get_attribute("src")
                    if src:
                        images.append(src)
            out.append({"sender": sender, "text": text, "time": tstamp, "images": images})
        except Exception:
            continue
    return out


def download_image(page, src, dest):
    try:
        resp = page.request.get(src)
        if resp.ok:
            with open(dest, "wb") as f:
                f.write(resp.body())
            return True
    except Exception:
        pass
    return False


def calibrate(page):
    """Lưu ảnh + mã trang để dò đúng selector khi Zalo đổi giao diện."""
    shot = DATA_DIR / "zalo_calibrate.png"
    html = DATA_DIR / "zalo_calibrate.html"
    try:
        page.screenshot(path=str(shot), full_page=True)
        with open(html, "w", encoding="utf-8") as f:
            f.write(page.content())
        print("🔎 Đã lưu để hiệu chỉnh:\n   • %s\n   • %s" % (shot, html))
        print("   → Gửi 2 file này cho phiên Claude trên máy để chỉnh SELECTORS cho khớp.")
    except Exception as e:
        print("Lỗi calibrate:", e)


# ------------------------------------------------------------
#  Vòng chạy chính
# ------------------------------------------------------------
def main():
    calibrate_mode = "--calibrate" in sys.argv
    once_mode = "--once" in sys.argv
    cfg = load_config()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("❌ Chưa cài Playwright. Chạy:\n   pip install playwright\n   python -m playwright install chromium")
        sys.exit(1)

    print("=" * 56)
    print("  🤖 BỘ ĐỌC ZALO — Trợ Lý Giáo Viên")
    print("  📋 Nhóm theo dõi: %s" % ", ".join(cfg["groups"]))
    print("  🖥️  Gửi về: %s" % cfg["server_url"])
    print("  🔒 Chỉ đọc nhóm trong danh sách. Dữ liệu chỉ ở máy này.")
    print("=" * 56)

    seen = load_state()

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            headless=cfg["headless"],
            accept_downloads=True,
            viewport={"width": 1280, "height": 900},
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto("https://chat.zalo.me/", wait_until="domcontentloaded")

        if not ensure_login(page):
            ctx.close()
            return

        if calibrate_mode:
            calibrate(page)
            ctx.close()
            return

        while True:
            new_count = 0
            for group in cfg["groups"]:
                print("📂 Nhóm: %s" % group)
                if not open_group(page, group, cfg):
                    continue
                gentle_sleep(cfg)
                for m in read_recent_messages(page, group, cfg):
                    key = msg_key(group, m["sender"], m["text"], m["time"])
                    if key in seen:
                        continue
                    # tải ảnh (nếu có)
                    saved_imgs = []
                    for i, src in enumerate(m.get("images", [])):
                        dest = IMG_DIR / ("%s_%s_%d.jpg" % (key, datetime.date.today().isoformat(), i))
                        if download_image(page, src, dest):
                            saved_imgs.append(str(dest.name))
                    item = {
                        "id": key,
                        "group": group,
                        "sender": m["sender"],
                        "text": m["text"],
                        "time": m["time"],
                        "label": simple_classify(m["text"]),
                        "images": saved_imgs,
                    }
                    res = push_to_server(cfg, item)
                    if res and res.get("ok"):
                        seen.add(key)
                        new_count += 1
                save_state(seen)
                gentle_sleep(cfg)

            print("   ✔️ Vòng quét xong, %d tin mới." % new_count)
            if once_mode:
                break
            print("   ⏳ Nghỉ %d giây..." % cfg["poll_seconds"])
            time.sleep(cfg["poll_seconds"])

        ctx.close()


if __name__ == "__main__":
    main()
