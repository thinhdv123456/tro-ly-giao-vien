#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scrape_ngulieuGDPT.py — Thu thập ngữ liệu Ngữ văn THCS (lớp 6–9)
Nguồn:
  1. thivien.net  — thơ hiện đại Việt Nam (17 bài, lớp 6–9)
  2. vi.wikisource.org — văn xuôi public domain (Nam Cao, Nguyễn Du...)
  3. vi.wikipedia.org  — văn bản Thông tin & Nghị luận (API miễn phí)
Output: passages_scraped.json → nhập vào app qua nút "Nhập từ JSON"

Cài đặt:
    pip3 install --break-system-packages requests beautifulsoup4 lxml

Chạy:
    python3 scrape_ngulieuGDPT.py                  # tất cả nguồn
    python3 scrape_ngulieuGDPT.py --source thivien  # chỉ thơ
    python3 scrape_ngulieuGDPT.py --source wiki     # chỉ Wikipedia
    python3 scrape_ngulieuGDPT.py --source wikisource
    python3 scrape_ngulieuGDPT.py --grade 9         # chỉ lớp 9
    python3 scrape_ngulieuGDPT.py --debug-url URL   # kiểm tra selector
"""

import json, time, re, argparse, unicodedata
from datetime import datetime
from pathlib import Path

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("❌ Thiếu thư viện. Chạy: pip3 install --break-system-packages requests beautifulsoup4 lxml")
    raise

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "vi,en-US;q=0.9,en;q=0.8",
}
DELAY = 1.5

# ═══════════════════════════════════════════════════════════════════════════
# 1. THIVIEN.NET — URL trực tiếp từng bài thơ (đã tra cứu)
# ═══════════════════════════════════════════════════════════════════════════
# (url, author, grade, subgenre, theme, copyright)
THIVIEN_POEMS = [

    # ── LỚP 6 ─────────────────────────────────────────────────────────────
    ("https://www.thivien.net/Tr%E1%BA%A7n-%C4%90%C4%83ng-Khoa/H%E1%BA%A1t-g%E1%BA%A1o-l%C3%A0ng-ta/poem-nj2_l-i_p3wtvvR5ztJaDA",
     "Trần Đăng Khoa", 6, "thơ tự do", "quê hương - lao động sản xuất", "education_use"),

    ("https://www.thivien.net/Tr%E1%BA%A7n-%C4%90%C4%83ng-Khoa/Th%E1%BA%A3-di%E1%BB%81u/poem-whocg3pnnLCLP-8dEMogtA",
     "Trần Đăng Khoa", 6, "thơ", "tuổi thơ - thiên nhiên", "education_use"),

    ("https://www.thivien.net/Tr%E1%BA%A7n-%C4%90%C4%83ng-Khoa/M%C6%B0a/poem-oYyO5oQrmOfinKNpR69gWA",
     "Trần Đăng Khoa", 6, "thơ tự do", "thiên nhiên - mưa", "education_use"),

    ("https://www.thivien.net/H%E1%BB%93-Ch%C3%AD-Minh/Nguy%C3%AAn-ti%C3%AAu/poem-9nGoTWzYHnMiK0mDAEFGOA",
     "Hồ Chí Minh", 6, "thơ Đường luật", "thiên nhiên - yêu nước", "nha_nuoc"),

    # ── LỚP 7 ─────────────────────────────────────────────────────────────
    ("https://www.thivien.net/H%E1%BB%93-Ch%C3%AD-Minh/C%E1%BA%A3nh-khuya/poem-B5-sSkpPOQF-1juwlpUd4g",
     "Hồ Chí Minh", 7, "thơ Đường luật", "thiên nhiên - tâm trạng người chiến sĩ", "nha_nuoc"),

    ("https://www.thivien.net/Xu%C3%A2n-Qu%E1%BB%B3nh/Ti%E1%BA%BFng-g%C3%A0-tr%C6%B0a/poem-kIRTdZoXrUmchgeBvXb_Rg",
     "Xuân Quỳnh", 7, "thơ năm chữ", "tình cảm gia đình - quê hương - chiến tranh", "education_use"),

    ("https://www.thivien.net/Xu%C3%A2n-Qu%E1%BB%B3nh/Chuy%E1%BB%87n-c%E1%BB%95-t%C3%ADch-v%E1%BB%81-lo%C3%A0i-ng%C6%B0%E1%BB%9Di/poem-AWdnPiisxJrwRbUfp8Rizw",
     "Xuân Quỳnh", 7, "thơ", "tình cảm gia đình - con người và thế giới", "education_use"),

    # ── LỚP 8 ─────────────────────────────────────────────────────────────
    ("https://www.thivien.net/T%E1%BA%BF-Hanh/Qu%C3%AA-h%C6%B0%C6%A1ng/poem-PR_rg4McBsM23XpRQUZbWw",
     "Tế Hanh", 8, "thơ tám chữ", "quê hương - biển cả - tình yêu quê", "education_use"),

    ("https://www.thivien.net/B%E1%BA%B1ng-Vi%E1%BB%87t/B%E1%BA%BFp-l%E1%BB%ADa/poem-lgCJ5h32csNKs00pNZOu3g",
     "Bằng Việt", 8, "thơ hỗn hợp", "tình cảm gia đình - bà cháu - ký ức tuổi thơ", "education_use"),

    ("https://www.thivien.net/Huy-C%E1%BA%ADn/%C4%90o%C3%A0n-thuy%E1%BB%81n-%C4%91%C3%A1nh-c%C3%A1/poem-k8EDHIxplIZZ0LYB28XrSA",
     "Huy Cận", 8, "thơ bảy chữ", "thiên nhiên - lao động - đất nước", "education_use"),

    ("https://www.thivien.net/Huy-C%E1%BA%ADn/Thu/poem-tP7FZYBnpv25Jer6_2VFFg",
     "Huy Cận", 8, "thơ", "thiên nhiên - mùa thu - cô đơn", "education_use"),

    # ── LỚP 9 ─────────────────────────────────────────────────────────────
    ("https://www.thivien.net/Ch%C3%ADnh-H%E1%BB%AFu/%C4%90%E1%BB%93ng-ch%C3%AD/poem-xYZuhzmmmiLHd-0Syz9dHA",
     "Chính Hữu", 9, "thơ tự do", "chiến tranh - tình đồng đội - người lính", "education_use"),

    ("https://www.thivien.net/Nguy%E1%BB%85n-Duy/%C3%81nh-tr%C4%83ng/poem-LZYel2RtqrJWQMzZsDPq2g",
     "Nguyễn Duy", 9, "thơ năm chữ", "chiến tranh - ký ức - lòng biết ơn", "education_use"),

    ("https://www.thivien.net/H%E1%BB%AFu-Th%E1%BB%89nh/Sang-thu/poem-aeKKUxGbZwOwpQZsyen76g",
     "Hữu Thỉnh", 9, "thơ năm chữ", "thiên nhiên - giao mùa - triết lý sống", "education_use"),

    ("https://www.thivien.net/Vi%E1%BB%85n-Ph%C6%B0%C6%A1ng/Vi%E1%BA%BFng-l%C4%83ng-B%C3%A1c/poem-ssM7VCNHXgctPBPvkDuAZw",
     "Viễn Phương", 9, "thơ tám chữ", "yêu nước - lòng biết ơn - Hồ Chí Minh", "education_use"),

    ("https://www.thivien.net/Y-Ph%C6%B0%C6%A1ng/N%C3%B3i-v%E1%BB%9Bi-con/poem-XCSfSxC-AM_w5wx1OjDiww",
     "Y Phương", 9, "thơ tự do", "tình cảm gia đình - bản sắc dân tộc - nghị lực", "education_use"),

    ("https://www.thivien.net/Nguy%E1%BB%85n-Duy/Tre-Vi%E1%BB%87t-Nam/poem-VkIfi7DKP2f1cM8JZZP8yA",
     "Nguyễn Duy", 9, "thơ lục bát", "bản sắc dân tộc - sức sống Việt Nam", "education_use"),
]

THIVIEN_SELECTOR = "div.poem-content"  # đã xác nhận qua debug

# ═══════════════════════════════════════════════════════════════════════════
# 2. WIKISOURCE — Văn xuôi public domain
# ═══════════════════════════════════════════════════════════════════════════
# (url, title, author, grade, genre, subgenre, theme, copyright)
WIKISOURCE_TEXTS = [
    ("https://vi.wikisource.org/wiki/Ch%C3%AD_Ph%C3%A8o",
     "Chí Phèo", "Nam Cao", 8, "van_hoc", "truyện ngắn",
     "số phận con người - bi kịch xã hội", "public_domain"),

    ("https://vi.wikisource.org/wiki/L%C3%A3o_H%E1%BA%A1c",
     "Lão Hạc", "Nam Cao", 8, "van_hoc", "truyện ngắn",
     "số phận con người - tình cha con - nghèo khó", "public_domain"),

    ("https://vi.wikisource.org/wiki/Nam_qu%E1%BB%91c_s%C6%A1n_h%C3%A0",
     "Nam quốc sơn hà", "Lý Thường Kiệt", 7, "van_hoc", "thơ cổ",
     "yêu nước - chủ quyền dân tộc", "public_domain"),

    ("https://vi.wikisource.org/wiki/B%C3%ACnh_Ng%C3%B4_%C4%91%E1%BA%A1i_c%C3%A1o",
     "Bình Ngô đại cáo (trích)", "Nguyễn Trãi", 8, "van_hoc", "văn nghị luận cổ",
     "yêu nước - độc lập - nhân nghĩa", "public_domain"),

    ("https://vi.wikisource.org/wiki/Th%C6%B0_%E1%BB%A5_%C4%91%E1%BA%A1i%2C_d%E1%BB%A5_%C3%B4n_h%E1%BA%A7u",
     "Chiếu dời đô", "Lý Công Uẩn", 8, "van_hoc", "văn chính luận cổ",
     "đất nước - dời đô - tầm nhìn lịch sử", "public_domain"),
]

WIKISOURCE_SELECTORS = ["div.mw-parser-output", "div#mw-content-text", "div.mw-content-ltr"]

# ═══════════════════════════════════════════════════════════════════════════
# 3. WIKIPEDIA TIẾNG VIỆT — Văn bản Thông tin & Nghị luận (dùng API)
# ═══════════════════════════════════════════════════════════════════════════
# Wikipedia có API JSON miễn phí — không cần scrape HTML
# (title_vi, grade, genre, subgenre, theme)
WIKI_ARTICLES = [
    # ── Văn bản Thông tin (thong_tin) ────────────────────────────────────
    ("Rừng nhiệt đới",        6, "thong_tin", "văn bản khoa học", "thiên nhiên - môi trường rừng"),
    ("Biển Đông",             6, "thong_tin", "văn bản địa lý",   "địa lý - biển đảo Việt Nam"),
    ("Nước",                  6, "thong_tin", "văn bản khoa học", "khoa học tự nhiên - tài nguyên nước"),
    ("Chất thải nhựa",        7, "thong_tin", "văn bản khoa học", "môi trường - ô nhiễm nhựa"),
    ("Trí tuệ nhân tạo",      7, "thong_tin", "văn bản khoa học", "công nghệ - AI - tương lai"),
    ("Biến đổi khí hậu",      7, "thong_tin", "văn bản khoa học", "môi trường - khí hậu toàn cầu"),
    ("Sức khỏe tâm thần",     8, "thong_tin", "văn bản khoa học", "sức khỏe - tâm lý - học sinh"),
    ("Internet",              8, "thong_tin", "văn bản khoa học", "công nghệ - mạng xã hội - giới trẻ"),
    ("Ô nhiễm không khí",     8, "thong_tin", "văn bản khoa học", "môi trường - sức khỏe"),
    ("Đô thị hóa",            9, "thong_tin", "văn bản xã hội",   "xã hội - đô thị - nông thôn"),
    ("Năng lượng tái tạo",    9, "thong_tin", "văn bản khoa học", "năng lượng - môi trường - tương lai"),
    ("Đa dạng sinh học",      9, "thong_tin", "văn bản khoa học", "sinh thái - bảo tồn thiên nhiên"),

    # ── Nghị luận / Văn bản xã hội (nghi_luan) ───────────────────────────
    ("Tình bạn",              6, "nghi_luan", "nghị luận xã hội", "đạo đức - tình bạn - lứa tuổi học sinh"),
    ("Lòng dũng cảm",         7, "nghi_luan", "nghị luận xã hội", "đạo đức - dũng cảm - nghị lực"),
    ("Bạo lực học đường",     8, "nghi_luan", "nghị luận xã hội", "xã hội - học đường - bạo lực"),
    ("Văn hóa đọc sách",      9, "nghi_luan", "nghị luận xã hội", "văn hoá - đọc sách - thời đại số"),
    ("Trách nhiệm xã hội",    9, "nghi_luan", "nghị luận xã hội", "đạo đức - trách nhiệm - cộng đồng"),
]

WIKI_API = "https://vi.wikipedia.org/w/api.php"


# ═══════════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════════

def slugify(text: str) -> str:
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-zA-Z0-9]+", "_", text).strip("_").lower()


def make_id(prefix: str, grade: int, idx: int) -> str:
    return f"{prefix}_{grade}_{200 + idx:03d}"


def clean_text(text: str, max_words: int = 800) -> str:
    text = re.sub(r"\n{3,}", "\n\n", text)
    lines = [l.rstrip() for l in text.split("\n") if l.strip()]
    text = "\n".join(lines).strip()
    words = text.split()
    if len(words) > max_words:
        cut = " ".join(words[:max_words])
        last = max(cut.rfind("।"), cut.rfind("."), cut.rfind("!"), cut.rfind("?"))
        text = cut[:last + 1] if last > max_words * 2 else cut + "..."
    return text


def excerpt_from(text: str, n: int = 40) -> str:
    return " ".join(text.replace("\n", " ").split()[:n]) + "..."


# ═══════════════════════════════════════════════════════════════════════════
# SCRAPER 1 — THIVIEN.NET
# ═══════════════════════════════════════════════════════════════════════════

def scrape_thivien(grade_filter: int = 0) -> list:
    print("\n📗 [1/3] thivien.net — thơ hiện đại Việt Nam")
    results, session = [], requests.Session()

    for idx, (url, author, grade, subgenre, theme, copyright_status) in enumerate(THIVIEN_POEMS):
        if grade_filter and grade != grade_filter:
            continue
        time.sleep(DELAY)
        try:
            r = session.get(url, headers=HEADERS, timeout=20)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "lxml")

            # Tiêu đề
            h1 = soup.select_one("h1.item-title") or soup.select_one("h1")
            title = re.sub(r"\s*[-–]\s*.*$", "", h1.get_text(strip=True)).strip() if h1 else "Không rõ"

            # Nội dung thơ — selector đã xác nhận
            body = soup.select_one(THIVIEN_SELECTOR)
            if not body or len(body.get_text(strip=True)) < 20:
                # Fallback: tìm p con dài nhất trong trang
                paras = [p for p in soup.find_all("p") if len(p.get_text(strip=True)) > 80]
                body = max(paras, key=lambda p: len(p.get_text())) if paras else None

            if not body:
                print(f"  ⚠️  Không lấy được nội dung: {title}")
                continue

            full_text = clean_text(body.get_text(separator="\n", strip=True), max_words=400)
            if len(full_text) < 30:
                continue

            wc = len(full_text.split())
            results.append({
                "id": make_id("VH", grade, idx + 1),
                "title": title, "author": author,
                "source": f"thivien.net — {url}",
                "class": grade, "genre": "van_hoc",
                "subgenre": subgenre, "theme": theme,
                "difficulty": "medium",
                "copyright_status": copyright_status,
                "approved": False,
                "wordCount": wc,
                "excerpt": excerpt_from(full_text),
                "fullText": full_text,
                "addedAt": datetime.now().isoformat(),
            })
            print(f"  ✅ [lớp {grade}] {title} — {author} ({wc} từ)")

        except Exception as e:
            print(f"  ❌ {url[-50:]}: {e}")

    print(f"  ✔️  {len(results)} bài thơ thu thập được")
    return results


# ═══════════════════════════════════════════════════════════════════════════
# SCRAPER 2 — WIKISOURCE
# ═══════════════════════════════════════════════════════════════════════════

def scrape_wikisource(grade_filter: int = 0) -> list:
    print("\n📕 [2/3] Wikisource — văn xuôi public domain")
    results, session = [], requests.Session()

    for idx, (url, title, author, grade, genre, subgenre, theme, copyright_status) in enumerate(WIKISOURCE_TEXTS):
        if grade_filter and grade != grade_filter:
            continue
        time.sleep(DELAY)
        try:
            r = session.get(url, headers=HEADERS, timeout=20)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "lxml")

            content = None
            for sel in WIKISOURCE_SELECTORS:
                content = soup.select_one(sel)
                if content and len(content.get_text(strip=True)) > 50:
                    break

            if not content:
                print(f"  ⚠️  Không lấy được nội dung: {title}")
                continue

            for tag in content.select("#toc,.toc,.mw-editsection,table,sup,.noprint,.NavFrame,script,style,h1"):
                tag.decompose()

            full_text = clean_text(content.get_text(separator="\n", strip=True), max_words=600)
            if len(full_text) < 60:
                continue

            wc = len(full_text.split())
            prefix = {"van_hoc": "VH", "nghi_luan": "NL"}.get(genre, "VH")
            results.append({
                "id": make_id(prefix, grade, 50 + idx),
                "title": title, "author": author,
                "source": f"Wikisource — {url}",
                "class": grade, "genre": genre,
                "subgenre": subgenre, "theme": theme,
                "difficulty": "medium",
                "copyright_status": copyright_status,
                "approved": False,
                "wordCount": wc,
                "excerpt": excerpt_from(full_text),
                "fullText": full_text,
                "addedAt": datetime.now().isoformat(),
            })
            print(f"  ✅ [lớp {grade}] {title} — {author} ({wc} từ, {copyright_status})")

        except Exception as e:
            print(f"  ❌ {title}: {e}")

    print(f"  ✔️  {len(results)} văn bản")
    return results


# ═══════════════════════════════════════════════════════════════════════════
# SCRAPER 3 — WIKIPEDIA TIẾNG VIỆT (API — không scrape HTML)
# ═══════════════════════════════════════════════════════════════════════════

def fetch_wikipedia(title_vi: str, session: requests.Session) -> str | None:
    """Lấy phần giới thiệu bài Wikipedia qua API JSON chính thức."""
    params = {
        "action": "query",
        "prop": "extracts",
        "exintro": True,        # chỉ lấy phần intro (trước mục lục)
        "explaintext": True,    # plain text, không có HTML
        "titles": title_vi,
        "format": "json",
        "redirects": True,
    }
    r = session.get(WIKI_API, params=params, headers=HEADERS, timeout=20)
    r.raise_for_status()
    data = r.json()
    pages = data.get("query", {}).get("pages", {})
    for page in pages.values():
        text = page.get("extract", "")
        if text and len(text) > 100:
            return text
    return None


def scrape_wikipedia(grade_filter: int = 0) -> list:
    print("\n📘 [3/3] Wikipedia tiếng Việt — Thông tin & Nghị luận (API)")
    results, session = [], requests.Session()

    for idx, (title_vi, grade, genre, subgenre, theme) in enumerate(WIKI_ARTICLES):
        if grade_filter and grade != grade_filter:
            continue
        time.sleep(DELAY)
        try:
            raw = fetch_wikipedia(title_vi, session)
            if not raw:
                print(f"  ⚠️  Không tìm thấy bài: {title_vi}")
                continue

            full_text = clean_text(raw, max_words=500)
            if len(full_text) < 80:
                continue

            wc = len(full_text.split())
            prefix = "TT" if genre == "thong_tin" else "NL"
            wiki_url = f"https://vi.wikipedia.org/wiki/{title_vi.replace(' ', '_')}"

            results.append({
                "id": make_id(prefix, grade, 100 + idx),
                "title": title_vi,
                "author": "Wikipedia tiếng Việt",
                "source": f"Wikipedia — {wiki_url}",
                "class": grade, "genre": genre,
                "subgenre": subgenre, "theme": theme,
                "difficulty": "medium",
                "copyright_status": "education_use",
                "approved": False,
                "wordCount": wc,
                "excerpt": excerpt_from(full_text),
                "fullText": full_text,
                "addedAt": datetime.now().isoformat(),
            })
            print(f"  ✅ [lớp {grade}] {title_vi} ({wc} từ, {genre})")

        except Exception as e:
            print(f"  ❌ {title_vi}: {e}")

    print(f"  ✔️  {len(results)} bài Wikipedia")
    return results


# ═══════════════════════════════════════════════════════════════════════════
# DEBUG
# ═══════════════════════════════════════════════════════════════════════════

def debug_url(url: str):
    print(f"\n🔬 Debug: {url}")
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")

    print("\n── Divs có class liên quan đến nội dung ──")
    for tag in soup.find_all(["div", "p", "article"]):
        cls = " ".join(tag.get("class", []))
        if any(k in cls.lower() for k in ["poem","text","content","body","detail","main"]):
            t = len(tag.get_text(strip=True))
            if 30 < t < 5000:
                print(f"  <{tag.name} class='{cls}'> {t}c — {tag.get_text(strip=True)[:70]}")

    print("\n── Đoạn thơ khả năng (nhiều dòng ngắn) ──")
    for tag in soup.find_all(["div","p"]):
        txt = tag.get_text(separator="\n", strip=True)
        lines = [l for l in txt.split("\n") if l.strip()]
        if 4 <= len(lines) <= 50 and 80 <= len(txt) <= 2000:
            avg = sum(len(l) for l in lines) / len(lines)
            if avg < 60:
                print(f"  <{tag.name} class='{' '.join(tag.get('class',[]))}'>  {len(lines)} dòng avg={avg:.0f}c")
                for l in lines[:5]:
                    print(f"    {l}")


# ═══════════════════════════════════════════════════════════════════════════
# TỔNG HỢP
# ═══════════════════════════════════════════════════════════════════════════

def deduplicate(items):
    seen, out = set(), []
    for item in items:
        key = slugify(item.get("title","")) + "_" + slugify(item.get("author",""))
        if key not in seen:
            seen.add(key); out.append(item)
    return out


def print_summary(items):
    from collections import Counter
    g = Counter(i["genre"] for i in items)
    lop = Counter(i["class"] for i in items)
    cp = Counter(i["copyright_status"] for i in items)
    print(f"\n{'='*55}")
    print(f"  📊 KẾT QUẢ: {len(items)} ngữ liệu")
    print(f"{'='*55}")
    print(f"  Thể loại : " + " | ".join(f"{k}:{v}" for k,v in sorted(g.items())))
    print(f"  Lớp      : " + " | ".join(f"Lớp {k}:{v}" for k,v in sorted(lop.items())))
    print(f"  Bản quyền: " + " | ".join(f"{k}:{v}" for k,v in sorted(cp.items())))
    print(f"  Chờ duyệt: {sum(1 for i in items if not i['approved'])}/{len(items)}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", choices=["thivien","wikisource","wiki","all"], default="all")
    parser.add_argument("--grade",  type=int, default=0, help="6/7/8/9 hoặc 0=tất cả")
    parser.add_argument("--output", default="passages_scraped.json")
    parser.add_argument("--debug-url", help="Debug selector cho 1 URL")
    args = parser.parse_args()

    if args.debug_url:
        debug_url(args.debug_url); return

    print("=" * 55)
    print("  GDPT 2018 — Thu thập ngữ liệu Ngữ văn THCS")
    print("=" * 55)

    all_items = []
    if args.source in ("thivien",  "all"): all_items += scrape_thivien(args.grade)
    if args.source in ("wikisource","all"): all_items += scrape_wikisource(args.grade)
    if args.source in ("wiki",     "all"): all_items += scrape_wikipedia(args.grade)

    all_items = deduplicate(all_items)
    print_summary(all_items)

    out = Path(args.output)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(all_items, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Lưu {len(all_items)} ngữ liệu → {out.resolve()}")
    print("💡 Mở app → 📚 Kho Ngữ Liệu → 🟡 Nhập từ JSON → chọn file trên")
    print("   Sau đó vào ⏳ Chờ duyệt để xem lại từng mục.\n")


if __name__ == "__main__":
    main()
