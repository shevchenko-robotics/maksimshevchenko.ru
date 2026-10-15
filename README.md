# maksimshevchenko.ru

Личный сайт Максима Шевченко.

## Устройство

- `src/page.html` — исходник страницы на двух языках. Элементы для одного языка помечены атрибутами `data-ru` или `data-en`.
- `tools/build.py` собирает из исходника две страницы: `index.html` (русская, `/`) и `en/index.html` (английская, `/en/`). Для каждой убирается текст другого языка, проставляются SEO-теги, `hreflang` и разметка schema.org.
- Сборка: `python3 tools/build.py` (нужен пакет `beautifulsoup4`). Собранные страницы коммитятся вместе с исходником.
- `src/cv.html` — резюме на двух языках; `python3 tools/cv.py` (нужен `playwright`) печатает его в `cv/shevchenko-cv-ru.pdf` и `cv/shevchenko-cv-en.pdf`.
- Адрес почты на страницах хранится в перевёрнутом виде и собирается скриптом, чтобы его не находили спам-боты.
- `data/records.json` — патенты, публикации и упоминания. Из него собираются разделы сайта и список в резюме: после правки запустите `python3 tools/build.py` и `python3 tools/cv.py`.
- `.github/workflows/links.yml` — раз в месяц проверяет все внешние ссылки на сайте и заводит задачу (issue), если какие-то перестали открываться.
- `robots.txt`, `sitemap.xml`, `404.html`, `CNAME` — служебные файлы GitHub Pages.

Шрифт Onest распространяется по лицензии SIL Open Font License (`fonts/OFL.txt`).
