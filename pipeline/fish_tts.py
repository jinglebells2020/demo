#!/usr/bin/env python3
"""Synthesize every VO line of pipeline/script.json with the Fish Audio TTS API.

Usage:  FISH_API_KEY=sk-... python3 pipeline/fish_tts.py [--out voiceover] [--only 3,7]
Writes voiceover/sNN.mp3 and voiceover/durations.json (seconds per scene, measured with ffmpeg).
"""
import json, os, re, subprocess, sys, time, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, "pipeline", "script.json")
OUT = os.path.join(ROOT, "voiceover")
only = None
args = sys.argv[1:]
if "--out" in args: OUT = args[args.index("--out") + 1]
if "--only" in args: only = {int(x) for x in args[args.index("--only") + 1].split(",")}
os.makedirs(OUT, exist_ok=True)

key = os.environ.get("FISH_API_KEY")
if not key: sys.exit("FISH_API_KEY is not set")
MODEL_OVERRIDE = args[args.index("--model") + 1] if "--model" in args else None
FALLBACK_MODEL = "s2.1-pro-free"   # used only when the paid model answers 402 (no API credit)

def ffmpeg():
    try:
        import imageio_ffmpeg; return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return "ffmpeg"

def duration(path):
    p = subprocess.run([ffmpeg(), "-i", path], capture_output=True, text=True)
    m = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", p.stderr)
    return round(int(m[1]) * 3600 + int(m[2]) * 60 + float(m[3]), 3) if m else None

cfg = json.load(open(SCRIPT, encoding="utf-8"))
voice = cfg["voice"]
model = MODEL_OVERRIDE or voice["model"]
durations = {}
for sc in cfg["scenes"]:
    n, text = sc["n"], sc.get("tts") or sc.get("text") or ""
    if only and n not in only: continue
    dst = os.path.join(OUT, f"s{n:02d}.mp3")
    if not text.strip():
        durations[str(n)] = 0.0; continue
    body = json.dumps({
        "text": text, "reference_id": voice["reference_id"], "format": "mp3", "mp3_bitrate": 192,
        "sample_rate": 44100, "normalize": True, "latency": "normal", "temperature": 0.6, "top_p": 0.7,
        "prosody": {"speed": voice.get("speed", 1.0), "volume": 0, "normalize_loudness": True},
    }).encode()
    for attempt in range(4):
        req = urllib.request.Request("https://api.fish.audio/v1/tts", data=body, method="POST", headers={
            "Authorization": f"Bearer {key}", "Content-Type": "application/json", "model": model})
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                open(dst, "wb").write(r.read())
            break
        except urllib.error.HTTPError as e:
            if e.code == 402 and model != FALLBACK_MODEL:
                print(f"scene {n}: model {model} -> HTTP 402 (no API credit on this key); falling back to {FALLBACK_MODEL}. "
                      f"Add API credit at https://fish.audio/app/developers and re-run with --model {model}.", file=sys.stderr)
                model = FALLBACK_MODEL; continue
            print(f"scene {n}: attempt {attempt+1} failed: HTTP {e.code} {e.read()[:120]!r}", file=sys.stderr); time.sleep(3 * (attempt + 1))
        except Exception as e:  # 503 overload, network
            print(f"scene {n}: attempt {attempt+1} failed: {e}", file=sys.stderr); time.sleep(3 * (attempt + 1))
    else:
        sys.exit(f"scene {n}: giving up")
    d = duration(dst); durations[str(n)] = d
    print(f"scene {n:02d}  {d:6.2f}s  {text[:60]}")
prev = {}
dpath = os.path.join(OUT, "durations.json")
if os.path.exists(dpath): prev = json.load(open(dpath))
prev.update(durations)
prev["_meta"] = {"model_used": model, "reference_id": voice["reference_id"], "speed": voice.get("speed", 1.0)}
json.dump(prev, open(dpath, "w"), indent=1, ensure_ascii=False)
print("model used:", model)
print("total VO", round(sum(v for k, v in prev.items() if not k.startswith("_") and v), 1), "s")
