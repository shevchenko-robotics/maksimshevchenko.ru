"""Render data/records.json into bilingual HTML fragments (data-ru / data-en) for the site and the CV."""
import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
NBSP = " "


def load():
    return json.loads((ROOT / "data" / "records.json").read_text(encoding="utf-8"))


def typo(text, lang):
    """Escape and glue short words and initials to the next word with non-breaking spaces."""
    t = html.escape(text, quote=False)
    t = re.sub(r"(?<=\b[A-ZА-ЯЁ]\.) ", NBSP, t)              # initials: А. В. Пешнин
    t = re.sub(r"\b(RU) (\d)", "\\1" + NBSP + "\\2", t)      # RU 2869712
    t = re.sub(r"(\d) (C1)\b", "\\1" + NBSP + "\\2", t)       # 2869712 C1
    if lang == "ru":
        t = re.sub(r"(^|\s)([а-яА-ЯёЁ]{1,2}) ", lambda m: m.group(1) + m.group(2) + NBSP, t)  # в, с, по, на, и ...
    return t


def site_records():
    out = ['<ul class="records">']
    for r in load()["records"]:
        out.append("  <li>")
        out.append('    <span class="kind">' + "".join(
            f'<span data-{l}>{typo(r["kind"][l], l)}, {r["year"]}</span>' for l in ("ru", "en")) + "</span>")
        for field in ("title", "meta"):
            for l in ("ru", "en"):
                out.append(f'    <div class="{field}" data-{l}>{typo(r[field][l], l)}</div>')
        out.append("  </li>")
    out.append("</ul>")
    return "\n".join(out)


def site_mentions():
    out = ['<ul class="mentions">']
    for m in load()["mentions"]:
        text = "".join(f"<span data-{l}>{typo(m['text'][l], l)}</span>" for l in ("ru", "en"))
        src = "".join(f"<span data-{l}>{typo(m['source'][l], l)}</span>" for l in ("ru", "en"))
        out.append(f'  <li>\n    <a href="{html.escape(m["url"])}" target="_blank" rel="noopener">{text}</a>\n    <span class="src">{src}</span>\n  </li>')
    out.append("</ul>")
    return "\n".join(out)


def cv_records():
    out = []
    for r in load()["records"]:
        if not r.get("cv"):
            continue
        kind = "".join(f'<span class="t" data-{l}>{typo(r["cv_kind"][l], l)}.</span>' for l in ("ru", "en"))
        meta = r.get("cv_meta")
        body = "".join(
            f'<span data-{l}>{typo(r["title"][l], l)}.' + (f" {typo(meta[l], l)}" if meta else "") + "</span>"
            for l in ("ru", "en"))
        out.append(f'<div class="item small"><span class="y">{r["year"]}</span>{kind} {body}</div>')
    return "\n".join(out)
