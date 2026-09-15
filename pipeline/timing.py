#!/usr/bin/env python3
"""Derive the scene timeline from the measured voiceover durations.

Reads voiceover/durations.json (written by fish_tts.py) and writes pipeline/timing.json:
one entry per scene with `at` (timeline start, s) and `dur` (s). Pads are the breathing room after
each VO line, tuned to Harvey's rhythm (short inside split sentences, longer at chapter boundaries).
"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(os.path.join(ROOT, "voiceover", "durations.json")))
PAD_DEFAULT = 0.55
PAD = {1: 0.7, 5: 0.3, 7: 0.3, 9: 0.8, 24: 0.9, 27: 0.6, 30: 0.6, 32: 0.9}
MIN = {1: 2.0, 9: 2.6, 24: 2.2, 27: 3.2, 30: 3.4}
TAIL = 6.5  # scene 33: tagline + fade to black (no VO)
scenes = []
t = 0.0
for n in range(1, 34):
    vo = float(d.get(str(n)) or 0.0)
    dur = TAIL if n == 33 else max(vo + PAD.get(n, PAD_DEFAULT), MIN.get(n, 0))
    scenes.append({"n": n, "at": round(t, 3), "dur": round(dur, 3), "vo": round(vo, 3), "vo_at": round(t + 0.15, 3)})
    t += dur
out = {"total": round(t, 3), "fps": 30, "scenes": scenes}
json.dump(out, open(os.path.join(ROOT, "pipeline", "timing.json"), "w"), indent=1)
print(f"total {t:.1f}s ({int(t//60)}:{int(t%60):02d})")
for s in scenes: print(f"  s{s['n']:02d} at {s['at']:7.2f}  dur {s['dur']:5.2f}  vo {s['vo']:5.2f}")
