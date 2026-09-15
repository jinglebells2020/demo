# ИС ОТО — Platform Overview (Harvey-style script), v2

Target: 5:08, 16:9, 1920×1080, 30 fps. One narrator (Russian), composed music bed ducked under the voice, no
on-camera people. Same act structure as Harvey: proof → flagship chapter → integrations → three shorter pillars →
proof → tagline. Every number in the narration is a product fact (module count, roles, number of typical forms and
reports, Order № 735) or a demo-stand figure that the app itself shows on screen.

Voice: Fish Audio **S2.1 Pro free developer API** (`model: s2.1-pro-free`, fish.audio/blog/s2-1-pro-free-api),
reference voice `7312c38557eb4fb384e3874e8e9cea67` («Мужской Профессиональный»), speed 1.0, WAV 44.1 kHz.
Machine-readable VO lines with their phonetic TTS forms: `pipeline/script.json`.

Legend for the "Asset" column: **UI** = real screenshot/recording of the live demo stand (Playwright),
**HF-img** = Higgsfield image, **HF-vid** = Higgsfield video, **native** = Higgsedit composition (text, icons,
shapes, counters, cards). "t" is the scene start in the delivered cut.

---

## Act A — Hook & proof (0:00–0:54)

| # | t | Harvey beat | VO (ru) | On screen | Asset |
|---|---|---|---|---|---|
| 1 | 0:00 | wordmark | Добро пожаловать в ИС ОТО. | The product's own mark (`public/proto/logo-mark.svg`) + «ИС ОТО» wordmark + kicker «ОРГАНИЗАЦИЯ ТРУДА ОСУЖДЁННЫХ», centered on paper #f6f4ef | native |
| 2 | 0:03 | world map | Двадцать регионов, восемнадцать департаментов и семьдесят восемь учреждений уголовно-исполнительной системы — в едином контуре организации труда осуждённых. | Kazakhstan oblast map fills in region by region; three serif counters 20 · 18 · 78 with sans captions | native |
| 3 | 0:14 | practice-area grid | Система ускоряет работу по всем направлениям: от подбора персонала и договоров до табеля, зарплаты и отчётности. | Sage panel; 4×3 grid of module cards (icon + name) staggering in | native |
| 4 | 0:23 | "25 hours saved" | Семь типовых форм ДУИС и пятнадцать отчётов формируются из тех же данных, что и табель, — без ручного свода. | Two serif numerals «7 типовых форм ДУИС» · «15 отчётов» with the sans line under them | native |
| 5 | 0:32 | access anywhere (fragments) | Система доступна везде: | White UI fragments (the dashboard KPI card, a status chip, nav items) float in around the real mark | native + UI crops |
| 6 | 0:34 | desktop / mobile / MS | в браузере на планшете сотрудника, в приложении для Android и на киосках Face ID. | Tablet with the dashboard, phone with the kiosk checkpoint (live camera feed), device lineup | UI + HF-vid + HF-img |
| 7 | 0:41 | compliance icons | Она построена по требованиям силового ведомства: | Row of four circular icons: Суверенный контур · Права на уровне запроса · Журнал аудита · RU/KZ | native |
| 8 | 0:44 | 3D cube | суверенный контур без единого внешнего обращения, права на уровне запроса к базе, журнал аудита каждого действия и двуязычный интерфейс. | Rotating clay cube cluster with the mark, captions per requirement | HF-vid |

## Act B — Flagship: Панель руководителя → Подбор → ИИ → Договор (0:54–2:53)

| # | t | Harvey beat | VO (ru) | On screen | Asset |
|---|---|---|---|---|---|
| 9 | 0:54 | "Assistant" pill | Панель руководителя отвечает на главный вопрос: дотягиваем ли до цели. | Sage panel; pill «▣ Панель руководителя» | native |
| 10 | 0:59 | prompt box + sources | Все цифры считаются из базы в момент открытия страницы — динамика за двенадцать месяцев, рейтинг учреждений, отстающие, истекающие договоры и незакрытые расследования. | Admin dashboard push-in, then the screen recording scrolling the dashboard | UI |
| 11 | 1:12 | "for example, as a litigator…" | Например, руководитель видит учреждение с занятостью сорок один процент, резерв незанятых трудоспособных — и свободные площадки этого же учреждения. | Facilities catalog window, push-in clamped to the page (no empty scroll) | UI |
| 12 | 1:23 | upload complaint | Работодатель создаёт запрос на подбор: швея, двадцать пять человек, разряд не ниже третьего. | Employer role: filled «Создать запрос» form; side card «Запрос на подбор» with the three values | UI + native |
| 13 | 1:30 | "improve prompt" | Он видит только своих работников, кандидатов и договоры — ограничение действует на уровне запроса к базе, а не пункта меню. | Employer dashboard; card «Представитель работодателя · Видит только своё» listing the employer's two sections against the admin's full menu | UI + native |
| 14 | 1:39 | 100 model calls diagram | Подбор — ключевой момент. Система ранжирует кандидатов по шести критериям: профессия, разряд, медицинские ограничения, инструктаж по охране труда, дисциплина и остаток срока — и объясняет каждый балл. | Staff recruitment ranking; card «Почему этот кандидат» with six criteria bars summing to 100 | UI + native |
| 15 | 1:54 | citations / versions | Осуждённые без действующего инструктажа и с медицинскими ограничениями исключаются полностью, а не понижаются в рейтинге. Проверка встроена в операцию. | Readiness registry; card «Сводка исключённых» | UI + native |
| 16 | 2:06 | follow-up draft | В системе есть и помощник на основе искусственного интеллекта. Справка по осуждённому собирает трудовой профиль из данных системы и даёт итог: сильные стороны, риски и готовность к трудоустройству по пятибалльной шкале. | Convict registry behind the «ИИ-справка по осуждённому» panel: Итог · Сильные стороны · Риски · Рекомендации · Готовность 4 из 5 · «Демонстрационный ответ» chip | UI + native |
| 17 | 2:21 | editable document | Оценка кандидатов читает свободный текст требований работодателя и сопоставляет его с обезличенными профилями: соответствие по каждому и кого предлагать первым. Это подсказка сотруднику, а не решение: персональные данные наружу не передаются. | Recruitment page behind the «ИИ-оценка кандидатов» panel: three anonymised candidates with fit meters, «На что обратить внимание» | UI + native |
| 18 | 2:38 | workflow stepper | Договор оформляется пошаговым мастером: проект, согласование, подписание, действие. | Labor contracts list; stepper проект → согласование → подписание → действие | UI + native |
| 19 | 2:45 | editable document | Каждая версия и каждая подпись сохраняются с меткой времени; типовой трудовой договор печатается в двух языках. | Signing page, then the A4 print form; card «Печатные формы» (казахская и русская колонки, 13 разделов) | UI + native |

## Act C — Integrations: учёт (2:53–3:34)

| # | t | Harvey beat | VO (ru) | On screen | Asset |
|---|---|---|---|---|---|
| 20 | 2:53 | Harvey + Microsoft lockup | ИС ОТО работает как модуль расширения над ЦАБД УИС и связывает реестр осуждённых, события СКУД, электронную подпись и обмен с 1С в одном контуре. | Wordmark «модуль расширения» over ЦАБД УИС; four rows: реестр осуждённых · СКУД · ЭЦП · **1С (обмен по кадрам и заработной плате)** | native |
| 21 | 3:06 | Word demo | В табеле — месячная сетка: строки — люди, колонки — дни, ячейки — часы и статус. Рядом — события проходов через КПП. | Full timesheet grid, slow pan across the month | UI |
| 22 | 3:16 | playbook flags | Расхождение показаний СКУД и ручного ввода не скрывается: система требует обоснование и не сохранит корректировку без него. | Discrepancies page, then the real cell form in its error state with the app's message «Укажите обоснование корректировки — без него запись не сохраняется» anchored to the form | UI + native |
| 23 | 3:25 | Outlook summaries | Импорт ведомости зачисляет зарплату на лицевые счета в той же транзакции, а закрытие периода само формирует распоряжения на перевод. | Payroll page → transfers page | UI |

## Act D — Отчётность (dark chapter) (3:34–3:55)

| # | t | Harvey beat | VO (ru) | On screen | Asset |
|---|---|---|---|---|---|
| 24 | 3:34 | "Vault" dark card | Отчётность. | Black (ops-bg #14120d) card; pill «▤ Отчётность» | native |
| 25 | 3:36 | folders grid | Рейтинг трудозанятости, травматизм по кварталам, иски и погашение — каждый отчёт считается из той же базы, что и табель, в момент открытия. | Reports list → report 6 → report 9 | UI |
| 26 | 3:47 | sync with DMS / 100k files | Экспорт в Excel — числа остаются числами и суммируются. Печатная форма — А4 с реквизитами и подписями. | The real `report-6.xlsx` exported from the stand, rendered as a spreadsheet (chip «выгрузка с демонстрационного стенда»), then the A4 print form | UI (derived) |

## Act E — Кабинет, Face ID, магазин (3:55–4:25)

| # | t | Harvey beat | VO (ru) | On screen | Asset |
|---|---|---|---|---|---|
| 27 | 3:55 | "Review tables" wide | Личный кабинет осуждённого превращает учёт в сервис. | Pill «Кабинет осуждённого»; tablet frame with the cabinet home | native + UI |
| 28 | 4:00 | select files / build columns | Лицевой счёт с выпиской, заявления о распределении зарплаты, документы с подписью PIN-кодом и отклики на вакансии — на планшете, крупным шрифтом. | Tablet: cabinet tabs (счёт, заявления, документы, вакансии) | UI |
| 29 | 4:10 | cells fill + 96 % stat | Киоски Face ID фиксируют проходы, не сохраняя ни одного изображения: в систему уходит только необратимый дескриптор. Магазин учреждения держит лимит на виду, а выдачу — под контролем сотрудника. | Face ID settings page, phone with the kiosk in its «Лицо считано» state (live camera feed), shop page | UI + HF-vid |

## Act F — Витрина и вывод на работу (4:25–4:46)

| # | t | Harvey beat | VO (ru) | On screen | Asset |
|---|---|---|---|---|---|
| 30 | 4:25 | "Workflows" gallery | Наконец, витрина свободных мощностей открывает производственные площади предпринимателям без входа в систему. | Pill «Витрина свободных мощностей»; public catalog | native + UI |
| 31 | 4:32 | description → flow graph | Регион, тип помещения, площадь — и запрос, который ложится в очередь учреждения. А вывод на работу проходит тот же маршрут, что и на бумаге: от инспектора до начальника. | Public catalog → workforce route page; card «Вывод на работу · маршрут — как на бумаге» | UI + native |

## Act G — Proof & close (4:46–5:08)

| # | t | Harvey beat | VO (ru) | On screen | Asset |
|---|---|---|---|---|---|
| 32 | 4:46 | 700+ deployments + client cards | Двадцать модулей, семь ролей, два языка и ноль внешних обращений. ИС ОТО построена по Правилам организации труда осуждённых — приказу МВД Республики Казахстан номер семьсот тридцать пять. | Four fact cards: 20 модулей · 7 ролей · 2 языка · 0 внешних обращений, then the Order № 735 line | native |
| 33 | 5:01 | "AI Tailored for Law" | (music only) | «Труд осуждённых — в цифровом контуре.» (serif) above the wordmark; «ТОО «AltaiLabs» · КУИС МВД Республики Казахстан · 2026»; fade to black | native |

---

## What changed from v1 (by the v1 timestamps that were flagged)

| v1 time | Problem | v2 |
|---|---|---|
| 0:00 | wrong logo | The real mark from the app (`public/proto/logo-mark.svg` rendered to PNG) in scenes 1, 5, 20 and 33 |
| 0:25 | «70 %» is not our fact | Beat replaced with a product fact: seven typical ДУИС forms and fifteen reports (scene 4) |
| 0:29 | wrong logo | Same real mark behind the floating fragments (scene 5) |
| 0:33 | kiosk camera view is green | Kiosk checkpoint re-captured with a live camera feed (Playwright fake device fed with a Higgsfield person clip) (scene 6) |
| 1:18 | page scrolls to nowhere | Every push-in / pan is clamped to the media size (`fit()` in the generator), so a window never leaves the page (scene 11 and all others) |
| 1:29 | the "comparison" showed two identical pictures | Scene 13 now shows the employer dashboard with a card that lists the employer's two sections against the admin's full menu |
| 2:04 | right element scrolls into nowhere | Same clamp; the signing page and the print form are held, not panned past their end (scene 19) |
| 2:17 | add 1С | Integration row «1С — обмен по кадрам и заработной плате» and the VO line names it (scene 20) |
| 2:31 | red box in the wrong place | The real timesheet cell form in its error state, with the app's own validation message anchored to the form (scene 22) |
| 3:06 | export examples | The actual `report-6.xlsx` exported from the stand with the given data, rendered as a spreadsheet, then the print form (scene 26) |
| 3:22 | kiosk cam view | Re-captured kiosk in the «Лицо считано» state on the phone (scene 29) |
| 3:38 | «107 сценариев / 0 обращений» is not relevant | Removed; the closing facts are 20 modules · 7 roles · 2 languages · 0 external calls + Order № 735 (scene 32) |
| — | mention the AI features | Two new beats: ИИ-справка по осуждённому and ИИ-оценка кандидатов (scenes 16–17), with their own VO lines |
| whole | voice quality | Re-voiced with the S2.1 Pro free API, natural speed, phonetic abbreviations (see below); composed music bed with sidechain ducking |

## TTS notes (why the lines in `script.json` have a `tts` twin)

Verified with faster-whisper on the generated takes: the model reads hyphenated **uppercase** Cyrillic
abbreviations («И-С О-Т-О») as English letter names, and «ИИ» collapses into one sound. Abbreviations are therefore
written as lowercase syllables (и-эс о-тэ-о, цэ-а-бэ-дэ у-и-эс, дэ-у-и-эс, ка-пэ-пэ, эм-вэ-дэ, скуд, один-эс, фейс-айди,
пин-кодом, эксель, а-четыре) and «ИИ» is spoken as «искусственный интеллект». Speed 1.1 made the voice sound clipped;
the delivered take is speed 1.0, WAV 44.1 kHz, then padded per scene by `timing.py` (0.55 s between lines, longer
holds after pills and before chapter cuts).

## Style transfer rules (Harvey → ИС ОТО)

- **Paper, not white.** Base #f6f4ef (the app's `--paper`), panels #efebe2 / #e8e3d8, dark chapters #14120d (`--ops-bg`). Cards white with 1 px #e6e1d6 hairline, no shadows except device frames.
- **Two type voices.** Serif for editorial (numerals, section words, tagline): Spectral (the app's own `--font-serif`). Sans for UI and captions: Manrope 400/500/600/700 (the app's body font). Sentence case only.
- **One accent.** Clay #d9613f for the mark, pills, highlight bars; clay-ink #a8401f for accent text. Red only for the СКУД discrepancy.
- **Real UI first.** Every product shot is a capture of the live demo stand. The two AI panels are the exception: the stand hides the AI tab without a model key (and the convict/contract detail routes currently error), so they are rebuilt from the app's own dictionary strings (`lib/i18n/dictionaries/ru/ai.ts`) and carry the app's «Демонстрационный ответ: модель не вызывалась» chip. «ИМИТАЦИЯ» plates stay visible where the app shows them.
- **Motion.** Ease-out 300–500 ms, staggers 50–80 ms, push-ins ≤ 1.2×, pans clamped to the page, one continuous 3D rotation, two hard cuts to dark. No bounces.
- **Numbers.** Always a serif numeral with a small sans caption beside it, never a bare number in prose.
- **Music.** A composed ambient bed (`pipeline/make_music.py`: 66 BPM, D major, pad + felt piano + bass, fade-in, swell into the tagline, fade-out), mixed at −12 dB under the voice with sidechain ducking (`mix_audio.py`).

---

## Build notes (Higgsedit in the Higgsfield sandbox)

The sandbox is ephemeral, so every run re-fetches its inputs. `pipeline/build_edit.py` writes `build/edit.jsx`
(timeline, map paths and asset sizes baked in) and `build/fetch.sh` (one `curl` per asset). The run that produced v2:

```bash
higgsedit new proj --size 1920x1080 --fps 30 && cd proj
SHA=<commit>   # the edit is fetched from the pushed commit so the sandbox and the repo never drift
curl -o fetch.sh https://raw.githubusercontent.com/jinglebells2020/demo/$SHA/build/fetch.sh && bash fetch.sh
curl -o edit.jsx https://raw.githubusercontent.com/jinglebells2020/demo/$SHA/build/edit.jsx
higgsedit fonts add . "Manrope:400" "Manrope:500" "Manrope:600" "Manrope:700" "Spectral:400" "Spectral:500"
# Google Fonts delivers Latin-only subsets (218 glyphs) -> swap in full Cyrillic files built from the upstream TTFs
pip install fonttools brotli && python3 - <<'PY'
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
def w2(t, out): t.flavor='woff2'; t.save(out)
for w in (400,500,600,700): w2(instancer.instantiateVariableFont(TTFont('fonts-src/Manrope[wght].ttf'), {'wght': w}), f'fonts/manrope-{w}.woff2')
w2(TTFont('fonts-src/Spectral-Regular.ttf'), 'fonts/spectral-400.woff2'); w2(TTFont('fonts-src/Spectral-Medium.ttf'), 'fonts/spectral-500.woff2')
PY
higgsedit build edit.jsx                                    # frames mode: 33 storyboard frames + the recorded timeline
higgsedit render . --out renders/is-oto-overview.mp4 --bitrate 8M   # 9238 frames, ~35 ms/frame on 7 workers
ffmpeg -i renders/is-oto-overview.mp4 -vf scale=1280:720 -c:v libx264 -crf 23 -c:a aac -b:a 160k renders/is-oto-overview-720p.mp4
```

Findings that shaped the generator:

- Higgsedit's native shaping path (`typography.fontAssetId`) is single-script per text node and rejects common
  punctuation (·, —) inside a Cyrillic paragraph, so the edit uses the legacy `fontFamily` path with the font files
  replaced as above. The built-in Inter and Playfair Display also carry Cyrillic (Inter even the Kazakh letters) and
  are the fallback: `build_edit.py --sans Inter --serif "Playfair Display"`.
- Media nodes get explicit geometry (no `fit`), which is the only way to guarantee the screenshot's top-left is what
  the window shows; push-ins are `scale` on a wrapper frame with `origin="center"`, pans are `offsetY` on the media,
  and both are clamped to the asset's pixel size (`pipeline/asset_sizes.json`) so nothing pans past the page.
- The audio spine is one pre-mixed file (`audio/mix.mp3`) cut once at 0; it must be at least as long as the
  timeline (`mix_audio.py` pads it), otherwise `cut()` rejects it.
- Word-by-word text reveals (`motion.by = "word"`) work with `fontFamily` text; counters need a fixed-size
  `layout="none"` frame with a single static text template. Every animation has to end inside its node's lifetime.
- Chromium's form-validation bubble stays English even with `--lang=ru-RU`, so the discrepancy beat masks it with the
  app's own Russian message rendered natively.
