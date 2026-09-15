#!/usr/bin/env python3
"""Pick the better of two voice-over take sets, line by line, from faster-whisper word timestamps.

Workflow (the transcription runs wherever faster-whisper is installed, e.g. the Higgsfield sandbox):
  1. generate the lines twice: voiceover-v5a/sNN.wav and voiceover-v5b/sNN.wav (fish_tts.py --out …)
  2. concatenate each set with 0.8 s gaps into takes_a.mp3 / takes_b.mp3 and note the offsets (takes_a_offsets.json:
     {"1": {"start": 0.0, "end": 6.3, "dur": 6.3}, …})
  3. transcribe both with WhisperModel('medium').transcribe(word_timestamps=True) and dump the words as
     [[start, end, word, probability], …] into takes_a_words.json / takes_b_words.json
  4. python3 pipeline/select_takes.py --dir <folder with the four json files> [--apply]

Score per line = 3 × script similarity + mean word probability − 0.4 × low-confidence words − 0.5 × internal gaps > 0.6 s
− 0.3 if the clip starts with a hard onset. --apply copies the winners into voiceover/.
"""
import argparse, json, re, unicodedata, difflib, shutil, os, subprocess
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
try:
    import imageio_ffmpeg; FF = imageio_ffmpeg.get_ffmpeg_exe()
except Exception: FF = "ffmpeg"
ap = argparse.ArgumentParser(); ap.add_argument("--dir", required=True); ap.add_argument("--takes", default="a,b")
ap.add_argument("--apply", action="store_true"); a = ap.parse_args()
d = json.load(open(os.path.join(ROOT, "pipeline", "script.json")))
NUM = {'20': 'двадцать', '18': 'восемнадцать', '78': 'семьдесят восемь', '12': 'двенадцать', '41': 'сорок один', '25': 'двадцать пять',
       '7': 'семь', '15': 'пятнадцать', '6': 'шести', '2': 'два', '0': 'ноль', '735': 'семьсот тридцать пять', '1с': 'один эс', '4': 'четыре'}
def norm(t):
    t = unicodedata.normalize('NFD', t); t = ''.join(c for c in t if unicodedata.category(c) != 'Mn').lower().replace('ё', 'е')
    out = []
    for w in re.sub(r'[^а-яa-z0-9 ]+', ' ', t).split(): out += NUM.get(w, w).split()
    return out
def onset(path):
    raw = subprocess.run([FF, "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", "44100", "-"], capture_output=True).stdout
    x = np.abs(np.frombuffer(raw, dtype=np.float32)); return float(x[:900].max())
res = {}
for take in a.takes.split(","):
    words = json.load(open(os.path.join(a.dir, f"takes_{take}_words.json"))); off = json.load(open(os.path.join(a.dir, f"takes_{take}_offsets.json")))
    for sc in d["scenes"]:
        n = sc["n"]
        if not sc.get("tts"): continue
        o = off[str(n)]; ws = [w for w in words if w[0] >= o["start"] - 0.3 and w[1] <= o["end"] + 0.3]
        heard = " ".join(w[2] for w in ws); probs = [w[3] for w in ws] or [0]
        sim = difflib.SequenceMatcher(None, norm(sc["text"]), norm(heard)).ratio()
        gaps = [round(ws[i + 1][0] - ws[i][1], 2) for i in range(len(ws) - 1) if ws[i + 1][0] - ws[i][1] > 0.6]
        on = onset(os.path.join(ROOT, f"voiceover-v5{take}", f"s{n:02d}.wav"))
        low = [w[2] for w in ws if w[3] < 0.4]
        score = 3 * sim + float(np.mean(probs)) - 0.4 * len(low) - 0.5 * len(gaps) - (0.3 if on > 0.35 else 0)
        res.setdefault(n, {})[take] = dict(sim=round(sim, 3), mean=round(float(np.mean(probs)), 3), low=low, gaps=gaps, onset=round(on, 2), score=round(score, 3), heard=heard.strip())
pick = {}
for n, r in sorted(res.items()):
    best = max(r, key=lambda t: r[t]["score"]); pick[n] = best
    print(f"{n:2d} pick {best}  " + " | ".join(f"{t}: sim={v['sim']} mean={v['mean']} low={v['low']} gaps={v['gaps']} on={v['onset']}" for t, v in r.items()))
if a.apply:
    for n, t in pick.items(): shutil.copy(os.path.join(ROOT, f"voiceover-v5{t}", f"s{n:02d}.wav"), os.path.join(ROOT, "voiceover", f"s{n:02d}.wav"))
    json.dump({"picked": pick, "scores": res}, open(os.path.join(a.dir, "selection.json"), "w"), ensure_ascii=False, indent=1)
    print("applied", pick)
