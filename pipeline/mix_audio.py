#!/usr/bin/env python3
"""Mix the per-scene VO files and the music bed into one stereo track aligned to pipeline/timing.json."""
import json, os, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
try:
    import imageio_ffmpeg; FF = imageio_ffmpeg.get_ffmpeg_exe()
except Exception: FF = "ffmpeg"
T = json.load(open(os.path.join(ROOT, "pipeline", "timing.json")))
total = T["total"]
inputs, filters, labels = [], [], []
i = 0
for s in T["scenes"]:
    f = next((c for c in (os.path.join(ROOT, "voiceover", f"s{s['n']:02d}.{e}") for e in ("wav", "mp3")) if os.path.exists(c)), "")
    if s["vo"] <= 0 or not os.path.exists(f): continue
    inputs += ["-i", f]
    filters.append(f"[{i}:a]aformat=sample_rates=44100:channel_layouts=stereo,adelay={int(s['vo_at']*1000)}|{int(s['vo_at']*1000)},volume=1.0[v{i}]")
    labels.append(f"[v{i}]"); i += 1
music = os.path.join(ROOT, "audio", "music_bed.wav")
inputs += ["-i", music]
filters.append(f"[{i}:a]aformat=sample_rates=44100:channel_layouts=stereo,apad=whole_dur={total},atrim=0:{total},volume=0.26,afade=t=in:st=0:d=2.5,afade=t=out:st={total-4:.2f}:d=4[m]")
filters.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0,volume=1.15,apad=whole_dur={total}[vo]")
filters.append("[vo]asplit=2[vo1][vo2]")
# duck the music under speech: sidechain compressor keyed by the voice track
filters.append("[m][vo2]sidechaincompress=threshold=0.035:ratio=5:attack=60:release=700:makeup=1[md]")
filters.append(f"[vo1][md]amix=inputs=2:normalize=0,atrim=0:{total},alimiter=limit=0.95[out]")
out = os.path.join(ROOT, "audio", "mix.mp3")
cmd = [FF, "-y", "-loglevel", "error"] + inputs + ["-filter_complex", ";".join(filters), "-map", "[out]", "-ar", "44100", "-b:a", "320k", out]
subprocess.run(cmd, check=True)
print("wrote", out, os.path.getsize(out), "bytes; total", total, "s")
