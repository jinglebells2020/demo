# ИС ОТО — platform overview video, in the style of Harvey's "Platform Overview"

Reference: https://youtu.be/ydIT4EdLK54 (Harvey, 3:52). Target: the same kind of narrated product tour for
**ИС ОТО** (информационная система организации труда осуждённых, КУИС МВД РК · AltaiLabs), built from the
live demo stand at https://kuis-oto-app-production.up.railway.app.

| Folder | What is in it |
|---|---|
| `docs/01-harvey-breakdown.md` | Full breakdown of the reference: acts, 32 scenes, visual language, motion grammar, audio, copy patterns, and a Harvey → ИС ОТО mapping table |
| `docs/02-is-oto-script.md` | The ИС ОТО script: 32 scenes, Russian voice-over, on-screen plan, motion, asset type per scene, style-transfer rules |
| `docs/03-chatcut-setup.md` | ChatCut plugin install log and the browser step that still has to be done by a person |
| `pipeline/script.json` | Machine-readable VO lines (display text + TTS text with spelled-out abbreviations) and the voice settings |
| `pipeline/fish_tts.py` | Fish Audio TTS: `FISH_API_KEY=… python3 pipeline/fish_tts.py` → `voiceover/sNN.mp3` + `durations.json` (model `s2.1-pro`, automatic fallback to `s2.1-pro-free` on HTTP 402) |
| `pipeline/timing.py` | Scene timeline from measured VO durations → `pipeline/timing.json` |
| `pipeline/mix_audio.py` | VO + music bed → `audio/mix.mp3` |
| `pipeline/build_edit.py` | Generates the Higgsedit edit script (`build/edit.jsx`) and the sandbox fetch list; modes `frames` / `draft` / `final` |
| `pipeline/map/kz_oblasts.json` | 17 oblast outlines + 3 city markers of Kazakhstan (2022 divisions) as absolute SVG paths, for the "map fills in" scene |
| `pipeline/assets.json`, `pipeline/asset_sizes.json` | Higgsfield storage URLs and pixel sizes of every asset the edit uses |
| `voiceover/` | Final VO (male voice `7312c38557eb4fb384e3874e8e9cea67`, speed 1.1); `voiceover-v1-…`, `voiceover-v2-…` are the earlier takes |
| `audio/` | Synthesized ambient bed (`music_bed.wav`, ffmpeg-generated placeholder) and the final `mix.mp3` |
| `build/` | Generated `edit.jsx` + `fetch.sh` for the Higgsfield sandbox |
| `renders/` | Storyboard sheet and the rendered video (see below) |

## How the video is made (Harvey's recipe, our tools)

1. **Real product only.** 49 screenshots and two screen recordings were captured from the live demo stand with
   Playwright (admin, staff, employer, convict-cabinet and kiosk roles, 1600×1000 @2×, tablet 1024×768, phone 390×844).
2. **Brand graphics** (rotating 3D clay "О" mark, the cube cluster for the security beat, the device lineup) were
   generated with Higgsfield (`gpt_image_2_5` + `seedance_2_5` image-to-video).
3. **Voice-over** is Fish Audio (`s2.1-pro`; the key had no API credit at build time, so the delivered take used the
   free tier — re-run `fish_tts.py --model s2.1-pro` after topping up at fish.audio/app/developers).
4. **Motion graphics and assembly** are native Higgsedit compositions: paper background, Spectral serif numerals,
   Manrope UI captions, module grid, KPI counter, map fill-in, pills, stepper, criteria bars, dark chapter cards,
   window push-ins and pans over the real UI, screen recordings for the scroll moments.
5. **Music** is a synthesized ambient pad (placeholder — swap `audio/music_bed.wav` for a licensed track and re-run
   `mix_audio.py`).

## Reproduce

```bash
FISH_API_KEY=sk-… python3 pipeline/fish_tts.py            # 1. voice-over
python3 pipeline/timing.py && python3 pipeline/mix_audio.py # 2. timeline + audio mix
python3 pipeline/build_edit.py --mode final --fonts family   # 3. edit.jsx for Higgsedit
# 4. in the Higgsfield sandbox: fetch.sh → fonts add + Cyrillic font swap → higgsedit build edit.jsx
```

The sandbox steps (asset fetch, `higgsedit fonts add`, replacing the Latin-only Google subsets with full
Cyrillic woff2 files built from the upstream TTFs via fontTools, `higgsedit build`) are listed verbatim in
`docs/02-is-oto-script.md` → "Build notes".

## Caveats to fix before publishing

- Numbers marked ⚠ in the script (20 regions · 18 departments · 78 institutions · 70,0 %) are demo-stand figures.
- The signing dialog and the ЦАБД/СКУД/ЭЦП beats describe the architecture; on the demo stand they are imitations and
  the app's own «ИМИТАЦИЯ» plates stay visible in the footage.
- Kiosk footage is the phone-size checkpoint screen; the bilingual labor contract print page returned 404 on the
  stand at capture time, so scene 17 uses a report print form instead.
