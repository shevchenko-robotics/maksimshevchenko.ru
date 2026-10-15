#!/usr/bin/env python3
"""Build the Russian (/) and English (/en/) pages from the bilingual source src/page.html.

In the source, language-specific elements carry data-ru or data-en. For each language the
build removes the other language's elements, sets <html lang>, the SEO tags and the
schema.org description, and writes:
    index.html      Russian page
    en/index.html   English page
Run from the repository root:  python3 tools/build.py
"""
import json
import pathlib
from bs4 import BeautifulSoup

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://maksimshevchenko.ru"

META = {
    "ru": {
        "path": "/",
        "out": ROOT / "index.html",
        "title": "Максим Шевченко — инженер-робототехник и преподаватель",
        "og_title": "Максим Шевченко",
        "description": "Инженер-робототехник и преподаватель. Космическая, промышленная и мобильная робототехника, инженерное образование.",
        "og_description": "Инженер-робототехник и преподаватель",
        "locale": "ru_RU",
        "arm_label": "Робот-манипулятор следует за курсором",
        "name": "Максим Шевченко",
        "job": "Инженер-робототехник, преподаватель",
        "alt_names": ["Шевченко Максим Юрьевич", "Maksim Shevchenko"],
        "orgs": ["МГТУ им. Н. Э. Баумана", "МГТУ «СТАНКИН»"],
        "knows": ["Робототехника", "Промышленные роботы", "Мобильные роботы", "ROS 2", "Космическая робототехника", "Инженерное образование"],
    },
    "en": {
        "path": "/en/",
        "out": ROOT / "en" / "index.html",
        "title": "Maksim Shevchenko — robotics engineer and lecturer",
        "og_title": "Maksim Shevchenko",
        "description": "Robotics engineer and lecturer. Space, industrial and mobile robotics, engineering education.",
        "og_description": "Robotics engineer and lecturer",
        "locale": "en_US",
        "arm_label": "Robot arm following the cursor",
        "name": "Maksim Shevchenko",
        "job": "Robotics engineer, lecturer",
        "alt_names": ["Maksim Yurevich Shevchenko", "Максим Шевченко"],
        "orgs": ["Bauman Moscow State Technical University", "Moscow State University of Technology STANKIN"],
        "knows": ["Robotics", "Industrial robots", "Mobile robots", "ROS 2", "Space robotics", "Engineering education"],
    },
}


def seo_block(lang):
    m = META[lang]
    other = "en" if lang == "ru" else "ru"
    url = SITE + m["path"]
    person = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": m["name"],
        "alternateName": m["alt_names"],
        "jobTitle": m["job"],
        "url": url,
        "image": SITE + "/photo.jpg",
        "sameAs": ["https://github.com/shevchenko-robotics", "https://t.me/m_shevchenko"],
        "affiliation": [{"@type": "CollegeOrUniversity", "name": n} for n in m["orgs"]],
        "alumniOf": {"@type": "CollegeOrUniversity", "name": m["orgs"][0]},
        "knowsAbout": m["knows"],
    }
    tags = [
        f'<title>{m["title"]}</title>',
        f'<meta name="description" content="{m["description"]}">',
        f'<link rel="canonical" href="{url}">',
        f'<link rel="alternate" hreflang="{lang}" href="{url}">',
        f'<link rel="alternate" hreflang="{other}" href="{SITE + META[other]["path"]}">',
        f'<link rel="alternate" hreflang="x-default" href="{SITE}/">',
        f'<meta property="og:type" content="website">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:title" content="{m["og_title"]}">',
        f'<meta property="og:description" content="{m["og_description"]}">',
        f'<meta property="og:image" content="{SITE}/og.jpg">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        f'<meta property="og:locale" content="{m["locale"]}">',
        f'<meta property="og:locale:alternate" content="{META[other]["locale"]}">',
        '<meta name="twitter:card" content="summary_large_image">',
        '<meta name="yandex-verification" content="43ca04fe0772f251">',
        '<meta name="google-site-verification" content="JADMEylQvh-CYF1Jxu9lgDvbK0sg6NzI1zcbGTFCxfQ">',
        '<script type="application/ld+json">' + json.dumps(person, ensure_ascii=False) + "</script>",
    ]
    return "\n".join(tags)


def build(lang):
    src = (ROOT / "src" / "page.html").read_text(encoding="utf-8")
    src = src.replace("<!--SEO-->", seo_block(lang), 1)
    soup = BeautifulSoup(src, "html.parser")
    other = "en" if lang == "ru" else "ru"
    for el in soup.select(f"[data-{other}]"):
        el.decompose()
    for el in soup.select(f"[data-{lang}]"):
        del el[f"data-{lang}"]
    soup.html["lang"] = lang
    for a in soup.select("[data-lang-link]"):
        if a["data-lang-link"] == lang:
            a["aria-current"] = "page"
        del a["data-lang-link"]
    arm = soup.find(id="arm")
    if arm is not None:
        arm["aria-label"] = META[lang]["arm_label"]
    out = META[lang]["out"]
    out.parent.mkdir(parents=True, exist_ok=True)
    html = "<!doctype html>\n" + str(soup).split("\n", 1)[1] if str(soup).lower().startswith("<!doctype") else str(soup)
    out.write_text(html, encoding="utf-8")
    print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    for language in ("ru", "en"):
        build(language)
