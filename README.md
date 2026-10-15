# maksimshevchenko.ru

Личный сайт Максима Шевченко.

## Устройство

- `src/page.html` — исходник страницы на двух языках. Элементы для одного языка помечены атрибутами `data-ru` или `data-en`.
- `tools/build.py` собирает из исходника две страницы: `index.html` (русская, `/`) и `en/index.html` (английская, `/en/`). Для каждой убирается текст другого языка, проставляются SEO-теги, `hreflang` и разметка schema.org.
- Сборка: `python3 tools/build.py` (нужен пакет `beautifulsoup4`). Собранные страницы коммитятся вместе с исходником.
- `robots.txt`, `sitemap.xml`, `404.html`, `CNAME` — служебные файлы GitHub Pages.

Шрифт Onest распространяется по лицензии SIL Open Font License (`fonts/OFL.txt`).
