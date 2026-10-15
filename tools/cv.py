#!/usr/bin/env python3
"""Render the one-page CV (src/cv.html) to PDF in Russian and English.

Writes cv/shevchenko-cv-ru.pdf and cv/shevchenko-cv-en.pdf.
Needs beautifulsoup4 and playwright (Chromium). Run from the repository root:  python3 tools/cv.py
"""
import datetime
import pathlib
import tempfile
from bs4 import BeautifulSoup
import records
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
MONTHS_RU = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"]


def page_for(lang):
    src = (ROOT / "src" / "cv.html").read_text(encoding="utf-8").replace("<!--CV_RECORDS-->", records.cv_records(), 1)
    soup = BeautifulSoup(src, "html.parser")
    other = "en" if lang == "ru" else "ru"
    for el in soup.select(f"[data-{other}]"):
        el.decompose()
    for el in soup.select(f"[data-{lang}]"):
        del el[f"data-{lang}"]
    soup.html["lang"] = lang
    d = datetime.date.today()
    soup.select_one(".upd").string = (f"{d.day} {MONTHS_RU[d.month - 1]} {d.year}" if lang == "ru" else d.strftime("%B %Y"))
    return str(soup)


def main():
    out_dir = ROOT / "cv"
    out_dir.mkdir(exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for lang in ("ru", "en"):
            with tempfile.NamedTemporaryFile("w", suffix=".html", dir=ROOT / "src", delete=False, encoding="utf-8") as f:
                f.write(page_for(lang))
                tmp = pathlib.Path(f.name)
            try:
                page = browser.new_page()
                page.goto(tmp.as_uri())
                page.wait_for_load_state("networkidle")
                page.evaluate("document.fonts.ready")
                target = out_dir / f"shevchenko-cv-{lang}.pdf"
                page.pdf(path=str(target), format="A4", print_background=True, prefer_css_page_size=True)
                print("wrote", target.relative_to(ROOT))
            finally:
                tmp.unlink()
        browser.close()


if __name__ == "__main__":
    main()
