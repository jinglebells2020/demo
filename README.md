# ИС ОТО — platform overview video, in the style of Harvey's "Platform Overview"

Reference: https://youtu.be/ydIT4EdLK54 (Harvey, 3:52). Target: the same kind of narrated product tour for
**ИС ОТО** (информационная система организации труда осуждённых, КУИС МВД РК · AltaiLabs), built from the
live demo stand at https://kuis-oto-app-production.up.railway.app.

Current cut: **v6** (33 scenes): plain-text voice (the stress marks of v4 turned out to break the model's own
stress placement and were removed), abbreviations that read naturally (ИС ОТО letter by letter, ДУИС as a word, ЦАБД УИС
and МВД in words), the better of two takes per line picked by whisper confidence, and a mix without compressor or limiter. v3 put the supplied orchestral track under
the v2 picture; v2 re-voiced the whole film with the Fish Audio S2.1 Pro free API, fixed every point flagged on v1 (logo, the «70 %» claim, kiosk camera, aimless pans, the
role comparison, 1С, the discrepancy form, real report exports, the closing facts) and adds two AI beats.

| Folder | What is in it |
|---|---|
| `docs/01-harvey-breakdown.md` | Full breakdown of the reference: acts, 32 scenes, visual language, motion grammar, audio, copy patterns, and a Harvey → ИС ОТО mapping table |
| `docs/02-is-oto-script.md` | The ИС ОТО script v2: 33 scenes with timestamps, Russian voice-over, on-screen plan, asset type per scene, the v1 → v2 change list, TTS notes, style-transfer rules, build notes |
| `docs/03-chatcut-setup.md` | ChatCut plugin install log and the browser step that still has to be done by a person |
| `pipeline/script.json` | Machine-readable VO lines (display text + phonetic TTS text) and the voice settings |
| `pipeline/fish_tts.py` | Fish Audio TTS: `FISH_API_KEY=… python3 pipeline/fish_tts.py` → `voiceover/sNN.wav` + `durations.json` (S2.1 Pro free API, `model: s2.1-pro-free`; `--model s2.1-pro` for the paid tier, which falls back to the free one on HTTP 402) |
| `pipeline/timing.py` | Scene timeline from measured VO durations → `pipeline/timing.json` |
| `pipeline/make_music.py` | Fallback: a composed ambient bed (66 BPM, D major, pad + felt piano + bass) → `audio/music_bed.wav` (generated, not tracked); this is what v2 used |
| `pipeline/mix_audio.py` | VO + music → `audio/mix.mp3`. The music follows an explicit ducking envelope derived from the voice (no compressor, no limiter); a track shorter than the film is played once and crossfaded into a second pass timed so its natural ending lands on the last frame, slowed by a few percent if two passes would not otherwise span the film (`--music`, `--music-db`, `--duck-db`, `--music-tempo`, `--no-loop`) |
| `pipeline/render_xlsx.py` | Renders an XLSX export from the stand as an Excel-look page for the screenshot in the export beat |
| `pipeline/build_edit.py` | Generates the Higgsedit edit script (`build/edit.jsx`) and the sandbox fetch list; modes `frames` / `draft` / `final` |
| `pipeline/map/kz_oblasts.json` | 17 oblast outlines + 3 city markers of Kazakhstan (2022 divisions) as absolute SVG paths, for the "map fills in" scene |
| `pipeline/assets.json`, `pipeline/asset_sizes.json` | Higgsfield storage URLs and pixel sizes of every asset the edit uses |
| `voiceover/` | Final VO (S2.1 Pro free API, voice `7312c38557eb4fb384e3874e8e9cea67`, speed 1.0, WAV, stress-marked script, best of two takes) + `durations.json`; `voiceover-v1-…`, `-v2-…`, `-v3-…` are the earlier takes |
| `pipeline/select_takes.py` | Picks the better of two take sets per line from faster-whisper word timestamps (script match, confidence, gaps, onset) |
| `audio/` | `mix.mp3` — the final voice + music mix. The supplied track (`music-orchestral.mp3`) and the generated bed are not tracked: drop the track into `audio/` before running `mix_audio.py` |
| `build/` | Generated `edit.jsx` + `fetch.sh` for the Higgsfield sandbox |
| `renders/` | `storyboard.png` (one frame per scene) and `is-oto-overview-720p.mp4` (preview); the 1080p master is on Higgsfield storage (link below) |

## Deliverables (v6)

- **1080p master** (H.264 8 Mbps + AAC): https://d2ol7oe51mr4n9.cloudfront.net/user_31atjlaXAU1IpCmsqXVnqqFDL41/24900d5d-9144-4d46-a8c7-97b2df4c83be.mp4
- **720p preview**: `renders/is-oto-overview-720p.mp4` (also https://d2ol7oe51mr4n9.cloudfront.net/user_31atjlaXAU1IpCmsqXVnqqFDL41/537d4e14-3da1-41a1-86e0-5e16e153910e.mp4)
- **Storyboard** (33 scene frames): `renders/storyboard.png` (also https://d2ol7oe51mr4n9.cloudfront.net/user_31atjlaXAU1IpCmsqXVnqqFDL41/608d6a76-1f75-44f4-8ec6-25d2dfb66626.png)
- Earlier masters, for comparison: v5 (before the last rewording) https://d2ol7oe51mr4n9.cloudfront.net/user_31atjlaXAU1IpCmsqXVnqqFDL41/19d52522-5bcd-4692-b674-0a76e2b1a5ff.mp4 · v4 (stress-marked voice, rejected) https://d2ol7oe51mr4n9.cloudfront.net/user_31atjlaXAU1IpCmsqXVnqqFDL41/d66a8900-d6d3-4ab5-8887-317216985174.mp4 · v3 (orchestral track, v2 voice) https://d2ol7oe51mr4n9.cloudfront.net/user_31atjlaXAU1IpCmsqXVnqqFDL41/07ab240f-1804-4c77-a8c4-beaf9a308810.mp4 · v2 (generated ambient bed) https://d2ol7oe51mr4n9.cloudfront.net/user_31atjlaXAU1IpCmsqXVnqqFDL41/474f7569-633d-4266-b783-1d3a3e883d8c.mp4 · v1 https://d2ol7oe51mr4n9.cloudfront.net/user_31atjlaXAU1IpCmsqXVnqqFDL41/e9fdd0e3-db96-416f-bb99-c7985e99639e.mp4

## How the video is made (Harvey's recipe, our tools)

1. **Real product first.** 55 screenshots, two screen recordings and the report-6 XLSX export were captured from
   the live demo stand with Playwright (admin, staff, employer, convict-cabinet and kiosk roles, 1600×1000 @2×,
   tablet 1024×768, phone 390×844). The kiosk captures run Chromium with a fake camera device fed by a
   Higgsfield-generated person clip, so the Face ID screens show a live feed instead of a blank green frame.
2. **Brand graphics** (rotating 3D clay mark, the cube cluster for the security beat, the device lineup, the
   kiosk person clip) were generated with Higgsfield (`gpt_image_2_5` + `seedance_2_5`). The logo itself is the
   product's own `public/proto/logo-mark.svg`.
3. **Voice-over** is Fish Audio's S2.1 Pro free developer API (`model: s2.1-pro-free`), voice
   `7312c38557eb4fb384e3874e8e9cea67`, speed 1.0, WAV. The `tts` field of `script.json` is plain text with respelled
   abbreviations («и-эс О-Тэ-О», chosen by the client from an A/B clip; «дуис» as a word; ЦАБД УИС and МВД expanded); stress marks do not work with this
   model (see the TTS notes in `docs/02-is-oto-script.md`), so residual stress errors are fixed line by line. Each line is
   generated twice and `select_takes.py` keeps the take that faster-whisper transcribes most faithfully. The paid
   `s2.1-pro` endpoint answers HTTP 402 on this key (no API credit).
4. **Music** is the supplied orchestral track (2:39 of music in a 2:54 file), slowed by 3 % so that two passes span
   the 5:20 film: it plays once and is crossfaded at 2:36 into a second pass timed so that its final chord lands on the
   fade to black. It sits 12 dB under the voice and a further 9 dB down while the narrator speaks, following an
   explicit envelope (`mix_audio.py`); nothing in the chain compresses or limits. The procedural bed from
   `make_music.py` is the fallback when no track is supplied.
5. **Motion graphics and assembly** are native Higgsedit compositions: paper background, Spectral serif numerals,
   Manrope UI captions, module grid, counters, map fill-in, pills, stepper, criteria bars, dark chapter cards,
   window push-ins and pans over the real UI (clamped to the page), screen recordings for the scroll moments.
6. **The two AI panels** («ИИ-справка по осуждённому», «ИИ-оценка кандидатов») are rebuilt natively from the app's
   own dictionary strings, because the stand hides its AI tab without a model key; they carry the app's
   «Демонстрационный ответ: модель не вызывалась» chip.

## Reproduce

```bash
FISH_API_KEY=sk-… python3 pipeline/fish_tts.py                          # 1. voice-over (S2.1 Pro free API); run twice into two folders
#    and pick per line with: python3 pipeline/select_takes.py <takes_a_words.json> <takes_b_words.json> (see its docstring)
python3 pipeline/timing.py                                              # 2. timeline
python3 pipeline/mix_audio.py                                           # 3. ducked mix with audio/music-orchestral.mp3
#   (fallback: python3 pipeline/make_music.py 335 && python3 pipeline/mix_audio.py --music audio/music_bed.wav --gain-db -11.7 --duck-threshold 0.035 --duck-ratio 5 --no-loop)
python3 pipeline/build_edit.py --mode frames --fonts family             # 4. edit.jsx + fetch.sh for Higgsedit
# 5. in the Higgsfield sandbox: fetch.sh → fonts add + Cyrillic font swap → higgsedit build → higgsedit render
```

The sandbox steps (asset fetch, `higgsedit fonts add`, replacing the Latin-only Google subsets with full
Cyrillic woff2 files built from the upstream TTFs via fontTools, `higgsedit build`, `higgsedit render`) are listed
verbatim in `docs/02-is-oto-script.md` → "Build notes".

## Caveats to fix before publishing

- 20 regions · 18 departments · 78 institutions and every figure inside the screenshots are demo-stand data.
- The ЦАБД/СКУД/ЭЦП/1С beat describes the architecture; on the demo stand these are imitations and the app's own
  «ИМИТАЦИЯ» plates stay visible in the footage.
- At v2 capture time the stand returned «Произошла ошибка» for the convict detail, recruitment detail and labor
  contract detail/print routes, and hides the AI tab (no model key) — hence the rebuilt AI panels (item 6 above) and
  the report print form in the «печатные формы» beat. Re-capture those pages once the stand is fixed and re-run
  `build_edit.py`.
- The music track was supplied for this project and is not in the repo; the mix and the renders that contain it are.
- ChatCut is installed but its MCP server needs a one-time browser login (see `docs/03-chatcut-setup.md`).
