#!/usr/bin/env python3
"""Mix the per-scene VO files and the music bed into one stereo track aligned to pipeline/timing.json.

  python3 pipeline/mix_audio.py                       # orchestral track (audio/music-orchestral.mp3), looped once so its
                                                      # natural ending lands on the last frame, -14 dB under the voice
  python3 pipeline/mix_audio.py --music audio/music_bed.wav --gain-db -11.7 --duck-threshold 0.035 --duck-ratio 5 --no-loop
                                                      # the generated ambient bed used by v2

--loop-at is the film time at which a second pass of the track starts (equal-power crossfade of --xfade seconds);
the default places the track's natural ending (last sample above -45 dBFS) 0.2 s before the end of the timeline.
"""
import argparse, json, os, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
try:
    import imageio_ffmpeg; FF = imageio_ffmpeg.get_ffmpeg_exe()
except Exception: FF = "ffmpeg"

ap = argparse.ArgumentParser()
ap.add_argument("--music", default=None)
ap.add_argument("--gain-db", type=float, default=-14.0, help="music gain before ducking")
ap.add_argument("--loop-at", type=float, default=None, help="film time where the second pass starts (default: auto)")
ap.add_argument("--no-loop", action="store_true")
ap.add_argument("--xfade", type=float, default=6.0)
ap.add_argument("--music-end", type=float, default=None, help="where the music really ends (default: measured at -45 dBFS)")
ap.add_argument("--duck-threshold", type=float, default=0.05)
ap.add_argument("--duck-ratio", type=float, default=2.5)
ap.add_argument("--fade-out", type=float, default=None)
ap.add_argument("--out", default=os.path.join(ROOT, "audio", "mix.mp3"))
a = ap.parse_args()

T = json.load(open(os.path.join(ROOT, "pipeline", "timing.json")))
total = T["total"]
music = a.music or next((p for p in (os.path.join(ROOT, "audio", "music-orchestral.mp3"), os.path.join(ROOT, "audio", "music_bed.wav")) if os.path.exists(p)), None)
if not music: raise SystemExit("no music file: put the track at audio/music-orchestral.mp3 or run make_music.py")

def music_end(path):
    """Last moment above -45 dBFS (the track may carry trailing silence)."""
    import numpy as np
    raw = subprocess.run([FF, "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", "8000", "-"], capture_output=True).stdout
    x = np.abs(np.frombuffer(raw, dtype=np.float32)); idx = np.nonzero(x > 10 ** (-45 / 20))[0]
    return idx[-1] / 8000.0 if len(idx) else len(x) / 8000.0

loop = not a.no_loop
if loop:
    end = a.music_end or music_end(music)
    loop_at = a.loop_at if a.loop_at is not None else round(total - end - 0.2, 2)
    if loop_at <= a.xfade or end >= total:  # the track already covers the timeline
        loop = False
fade_out = a.fade_out if a.fade_out is not None else (1.2 if loop else 4.0)
gain = 10 ** (a.gain_db / 20)

inputs, filters, labels = [], [], []
i = 0
for s in T["scenes"]:
    f = next((c for c in (os.path.join(ROOT, "voiceover", f"s{s['n']:02d}.{e}") for e in ("wav", "mp3")) if os.path.exists(c)), "")
    if s["vo"] <= 0 or not os.path.exists(f): continue
    inputs += ["-i", f]
    filters.append(f"[{i}:a]aformat=sample_rates=44100:channel_layouts=stereo,adelay={int(s['vo_at']*1000)}|{int(s['vo_at']*1000)},volume=1.0[v{i}]")
    labels.append(f"[v{i}]"); i += 1
fmt = "aformat=sample_rates=44100:channel_layouts=stereo"
inputs += ["-i", music]
if loop:
    inputs += ["-i", music]
    filters.append(f"[{i}:a]{fmt},atrim=0:{loop_at + a.xfade:.3f}[m1]")
    filters.append(f"[{i+1}:a]{fmt}[m2]")
    filters.append(f"[m1][m2]acrossfade=d={a.xfade}:c1=tri:c2=tri[mm]")
    src = "[mm]"
    print(f"music {os.path.basename(music)}: ends at {end:.2f} s, second pass starts at {loop_at:.2f} s (crossfade {a.xfade} s), natural ending at {loop_at + end:.2f} s of {total} s")
else:
    filters.append(f"[{i}:a]{fmt}[mm]"); src = "[mm]"
filters.append(f"{src}apad=whole_dur={total},atrim=0:{total},volume={gain:.4f},afade=t=in:st=0:d=1.0,afade=t=out:st={total - fade_out:.2f}:d={fade_out}[m]")
filters.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0,volume=1.15,apad=whole_dur={total}[vo]")
filters.append("[vo]asplit=2[vo1][vo2]")
# duck the music under speech: sidechain compressor keyed by the voice track
filters.append(f"[m][vo2]sidechaincompress=threshold={a.duck_threshold}:ratio={a.duck_ratio}:attack=80:release=1200:makeup=1[md]")
filters.append(f"[vo1][md]amix=inputs=2:normalize=0,atrim=0:{total},alimiter=limit=0.95[out]")
cmd = [FF, "-y", "-loglevel", "error"] + inputs + ["-filter_complex", ";".join(filters), "-map", "[out]", "-ar", "44100", "-b:a", "320k", a.out]
subprocess.run(cmd, check=True)
print("wrote", a.out, os.path.getsize(a.out), "bytes; total", total, "s; music gain", a.gain_db, "dB; duck", a.duck_threshold, a.duck_ratio)
