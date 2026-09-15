# ИС ОТО — Platform Overview (Harvey-style script)

Target: 3:45–3:55, 16:9, 1920×1080, 30 fps. One narrator (Russian), music bed, no on-camera people. Same act structure as Harvey: proof → flagship chapter → integrations → three shorter pillars → proof → tagline. All numbers come from the project's own README and demo data set (`jinglebells2020/kuis-oto`); the ones marked ⚠ are demo-stand figures and must be replaced with pilot figures before the video is published.

Voice: Fish Audio, model `s2.1-pro`, reference voice `2a1036d645634680b3cc69aeeb60375b` ("Спокойный женский голос", calm narration), speed 1.0. Machine-readable version of the VO lines: `pipeline/script.json`.

Legend for the "Asset" column: **UI** = real screenshot/recording of the live app (Playwright), **HF-img** = Higgsfield image, **HF-vid** = Higgsfield video, **native** = Higgsedit composition (text, icons, shapes, counters).

---

## Act A — Hook & proof (0:00–0:32)

| # | Harvey beat | VO (ru) | On screen | Motion | Asset |
|---|---|---|---|---|---|
| 1 | wordmark | Добро пожаловать в ИС ОТО. | Clay mark + «ИС ОТО» wordmark centered on paper #f6f4ef | hold 1.2 s, cut | native |
| 2 | world map | Двадцать регионов, восемнадцать департаментов и семьдесят восемь учреждений уголовно-исполнительной системы — в едином контуре организации труда осуждённых. ⚠ | Flat map of Kazakhstan on a faint grid; regions fill from light grey to ink one by one; three serif numerals appear beside: 20 · 18 · 78 with captions | staggered region fills (60 ms apart), slow zoom-out 1.06→1.0 | native (SVG regions) |
| 3 | practice-area grid | Система ускоряет работу по всем направлениям: от подбора персонала и договоров до табеля, зарплаты и отчётности. | Sage panel; 4×3 grid of rounded-square line icons with labels: Осуждённые, Договоры, Подбор, Табель, Зарплата, Отчётность, Охрана труда, Обучение, Площадки, Кабинет, Face ID, Магазин | cards pop in staggered 50 ms, panel slides left to reveal next | native (Lucide) |
| 4 | "25 hours saved" | Трудозанятость по системе — семьдесят процентов. Целевой показатель, по которому оценивают руководителей, виден каждый день. ⚠ | Huge serif «70,0 %» counting up from 41,1; small caption «трудозанятость по системе» beside it; a thin target line at 70 | counter 1.2 s, caption fades after the number lands | native |
| 5 | access anywhere (fragments) | Система доступна везде: | White UI fragments float in around the clay mark: a KPI card, a status chip, a nav item | slide-ins from edges, ease-out 400 ms | native + UI crops |
| 6 | desktop / mobile / MS | в браузере на планшете сотрудника, в приложении для Android и на киосках Face ID. | Three device frames on sage: tablet (dashboard), phone (staff app / kiosk), kiosk tablet (dark) | frames settle into a layered stack | native frames + UI |
| 7 | compliance icons | Она построена по требованиям силового ведомства: | Row of four circular icons: Суверенный контур · Права на уровне запроса · Журнал аудита · RU / KK | stagger left→right | native |
| 8 | 3D cube | суверенный контур без единого внешнего обращения, права на уровне запроса к базе, журнал аудита каждого действия и двуязычный интерфейс. | Clay «О» cube rotating slowly, white satellite cubes orbit it | continuous rotation 5 s | HF-img → HF-vid |

## Act B — Flagship: Панель руководителя → Подбор (0:32–1:42)

| # | Harvey beat | VO (ru) | On screen | Motion | Asset |
|---|---|---|---|---|---|
| 9 | "Assistant" pill | Панель руководителя отвечает на главный вопрос: дотягиваем ли до цели. | Sage panel; pill «▣ Панель руководителя» | pill scales in | native |
| 10 | prompt box + sources | Все цифры считаются из базы в момент открытия страницы — динамика за двенадцать месяцев, рейтинг учреждений, отстающие, истекающие договоры и незакрытые расследования. | Real dashboard (admin): dark KPI card, 12-month chart with the target line, ranking table, «Отстающие», chips | push-in 1.0→1.25 to the KPI card, then scroll recording | UI (shot + recording) |
| 11 | "for example, as a litigator…" | Например, руководитель видит учреждение с занятостью сорок один процент, резерв незанятых трудоспособных — и свободные площадки этого же учреждения. | Click on a lagging institution → facility catalog cards with photos, area, 380 V, heating | cursor path, cut to catalog, slow pan | UI |
| 12 | upload complaint | Работодатель создаёт запрос на подбор: швея, двадцать пять человек, разряд не ниже третьего. | Employer role: «Создать запрос» form; fields fill: Швея · 25 · разряд 3 | typing into fields | UI (recruitment-new) |
| 13 | "improve prompt" | Он видит только свои данные — ограничение действует на уровне запроса к базе, а не пункта меню. | Employer navigation with only 2 sections, versus admin's full sidebar | side-by-side nav comparison, highlight | UI crops, native |
| 14 | 100 model calls diagram | Подбор — ключевой момент. Система ранжирует кандидатов по шести критериям: профессия, разряд, медицинские ограничения, инструктаж по охране труда, дисциплина и остаток срока — и объясняет каждый балл. | Split: left = candidate list sorted by score (real UI); right = grey card with the six-criteria breakdown 40 / 20 / 15 / 10 / 8 / 7 drawing on | bars grow, numbers count | UI + native |
| 15 | citations / versions | Осуждённые без действующего инструктажа и с медицинскими ограничениями исключаются полностью, а не понижаются в рейтинге. Проверка встроена в операцию. | Zoom to «Сводка исключённых»; two rows highlighted in warning tint | push-in, highlight paint | UI + native |
| 16 | follow-up draft | Договор оформляется пошаговым мастером: проект, согласование, подписание, действие. | Contract stepper: проект → согласование → согласован → подписан → действует | stepper advances step by step | UI (contracts, signing) |
| 17 | editable document | Каждая версия и каждая подпись сохраняются с меткой времени; типовой трудовой договор печатается в двух языках. | Signing page with the certificate dialog (keep the «ИМИТАЦИЯ» plate visible), then the bilingual A4 contract, kk and ru columns | dialog, cut to A4 slow pan | UI |

## Act C — Integrations: учёт (1:42–2:24)

| # | Harvey beat | VO (ru) | On screen | Motion | Asset |
|---|---|---|---|---|---|
| 18 | Harvey + Microsoft lockup | ИС ОТО работает как модуль расширения над ЦАБД УИС и связывает реестр осуждённых, события СКУД и электронную подпись в одном контуре. | «ИС ОТО» → «ИС ОТО + ЦАБД УИС»; then three rows: ЦАБД УИС · СКУД / Face ID · ЭЦП НУЦ РК | lockup build, icons stagger | native |
| 19 | Word demo | В табеле — месячная сетка: строки — люди, колонки — дни, ячейки — часы и статус. Рядом — события проходов через КПП. | Timesheet grid (staff); SKUD event panel | pan across the grid, push-in on the panel | UI |
| 20 | playbook flags | Расхождение показаний СКУД и ручного ввода не скрывается: система требует обоснование и не сохранит корректировку без него. | Discrepancy row highlighted; «Обоснование» field with the save blocked | highlight paints in, field outline | UI + native |
| 21 | Outlook summaries | Импорт ведомости зачисляет зарплату на лицевые счета в той же транзакции, а закрытие периода само формирует распоряжения на перевод. | Payroll import → personal accounts → transfers register | three quick cuts | UI |

## Act D — Отчётность (dark chapter) (2:24–2:42)

| # | Harvey beat | VO (ru) | On screen | Motion | Asset |
|---|---|---|---|---|---|
| 22 | "Vault" dark card | Отчётность. | Black (ops-bg #14120d) card; pill «▤ Отчётность» in ops-glow | hard cut to dark | native |
| 23 | folders grid | Пятнадцать отчётов и семь типовых форм ДУИС считаются из тех же данных: рейтинг трудозанятости, травматизм по кварталам, иски и погашение. | Reports list; report 6 ranking with color scale and deltas; report 9 quarterly injuries | grid, then two cuts | UI |
| 24 | sync with DMS / 100k files | Экспорт в XLSX — числа остаются числами. Печатная форма — А4 с реквизитами и подписями. | Hover «Экспорт XLSX»; A4 print form | hover, cut to A4 slow pan | UI |

## Act E — Кабинет, Face ID, магазин (2:42–3:20)

| # | Harvey beat | VO (ru) | On screen | Motion | Asset |
|---|---|---|---|---|---|
| 25 | "Review tables" wide | Личный кабинет осуждённого превращает учёт в сервис. | Pill «Кабинет осуждённого»; tablet frame with the cabinet home | wide reveal | native + UI |
| 26 | select files / build columns | Лицевой счёт с выпиской, заявления о распределении зарплаты, документы с подписью PIN-кодом и отклики на вакансии — на планшете, крупным шрифтом. | Cabinet finance (statement), documents (PIN sign), vacancies | three tablet cuts with slight push-ins | UI |
| 27 | cells fill + 96 % stat | Киоски Face ID фиксируют проходы, не сохраняя ни одного изображения: в систему уходит только необратимый дескриптор. Магазин учреждения держит лимит на виду, а выдачу — под контролем сотрудника. | Phone frame: kiosk checkpoint (dark); Face ID admin panel (coverage, fleet, live feed); shop queue | phone frame, cut to panel, cut to shop | UI |
| 28 | export / open in assistant | И всё это проверяется при каждой сборке: сто семь сквозных сценариев подтверждают изоляцию данных и отсутствие внешних обращений. | Stat card over the UI: «107» сквозных сценариев · «0» внешних обращений (serif numerals) | card pops over, numerals count | native |

## Act F — Витрина и вывод на работу (3:20–3:38)

| # | Harvey beat | VO (ru) | On screen | Motion | Asset |
|---|---|---|---|---|---|
| 29 | "Workflows" gallery | Наконец, витрина свободных мощностей открывает производственные площади предпринимателям без входа в систему. | Pill «Витрина мощностей»; public /catalog cards | cards stagger | native + UI |
| 30 | description → flow graph | Регион, тип помещения, площадь — и запрос, который ложится в очередь учреждения. А вывод на работу проходит тот же маршрут, что и на бумаге: от инспектора до начальника. | Catalog detail + «Запросить площадку» form; then the workforce request route: инспектор → работодатель → пять виз → начальник as a node chain drawing on | form, then nodes/edges draw on | UI + native |

## Act G — Proof & close (3:38–3:52)

| # | Harvey beat | VO (ru) | On screen | Motion | Asset |
|---|---|---|---|---|---|
| 31 | 700+ deployments + client cards | Двадцать модулей, семь ролей, два языка и ноль внешних обращений. ИС ОТО построена по Правилам организации труда осуждённых — приказу МВД Республики Казахстан номер семьсот тридцать пять. | Dark card «20 модулей»; then 2×2 cards: «7» ролей · «2» языка · «0» внешних обращений · «№ 735» приказ МВД РК | dark card, cards stagger | native |
| 32 | "AI Tailored for Law" | (music only) | «Труд осуждённых — в цифровом контуре.» (serif) above the ИС ОТО wordmark; small line «ТОО «AltaiLabs» · КУИС МВД РК»; fade to black | hold 5 s, fade 1 s | native |

---

## Style transfer rules (Harvey → ИС ОТО)

- **Paper, not white.** Base #f6f4ef (the app's `--paper`), panels #efebe2 / #e8e3d8, dark chapters #14120d (`--ops-bg`). Cards white with 1 px #e6e1d6 hairline, no shadows except device frames.
- **Two type voices.** Serif for editorial (numerals, section words, tagline): Spectral (the app's own `--font-serif`). Sans for UI and captions: Manrope 400/600 (the app's body font). Sentence case only.
- **One accent.** Clay #d9613f for the mark, pills, highlight bars; clay-ink #a8401f for accent text. Red only for the SKUD discrepancy.
- **Real UI only.** Every product shot is a capture of the live demo stand; nothing is mocked. «ИМИТАЦИЯ» plates stay visible where the app shows them.
- **Motion.** Ease-out 300–500 ms, staggers 50–80 ms, push-ins ≤ 1.3×, one continuous 3D rotation, two hard cuts to dark. No bounces.
- **Numbers.** Always a serif numeral with a small sans caption beside it, never a bare number in prose.

---

## Build notes (Higgsedit in the Higgsfield sandbox)

The sandbox is ephemeral, so every run re-fetches its inputs. `pipeline/build_edit.py` writes `build/edit.jsx`
(timeline, map paths and asset sizes baked in) and `build/fetch.sh` (one `curl` per asset). The run is:

```bash
higgsedit new proj --size 1920x1080 --fps 30 && cd proj
curl -o fetch.sh <fetch.sh URL> && bash fetch.sh            # screenshots, recordings, generated clips, mix.mp3, TTFs
curl -o edit.jsx <edit.jsx URL>
higgsedit fonts add . "Manrope:400" "Manrope:500" "Manrope:600" "Spectral:400" "Spectral:500"
# Google Fonts delivers Latin-only subsets (218 glyphs) -> swap in full Cyrillic files built from the upstream TTFs
pip install fonttools brotli && python3 - <<'PY'
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
def w2(t, out): t.flavor='woff2'; t.save(out)
for w in (400,500,600): w2(instancer.instantiateVariableFont(TTFont('fonts-src/Manrope[wght].ttf'), {'wght': w}), f'fonts/manrope-{w}.woff2')
w2(TTFont('fonts-src/Spectral-Regular.ttf'), 'fonts/spectral-400.woff2'); w2(TTFont('fonts-src/Spectral-Medium.ttf'), 'fonts/spectral-500.woff2')
PY
higgsedit build edit.jsx                                    # frames | draft | final, per --mode
```

Findings that shaped the generator:

- Higgsedit's native shaping path (`typography.fontAssetId`) is single-script per text node and rejects common
  punctuation (·, —) inside a Cyrillic paragraph, so the edit uses the legacy `fontFamily` path with the font files
  replaced as above. The built-in Inter and Playfair Display also carry Cyrillic (Inter even the Kazakh letters) and
  are the fallback: `build_edit.py --sans Inter --serif "Playfair Display"`.
- Media nodes get explicit geometry (no `fit`), which is the only way to guarantee the screenshot's top-left is what
  the window shows; push-ins are `scale` on a wrapper frame with `origin="center"`, pans are `offsetY` on the media.
- The audio spine is one pre-mixed file (`audio/mix.mp3`), cut once at 0; every picture element is a `compose` overlay.
- Word-by-word text reveals (`motion.by = "word"`) work with `fontFamily` text; counters need a fixed-size
  `layout="none"` frame with a single static text template.
