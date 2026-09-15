#!/usr/bin/env python3
"""Mix the per-scene VO files and the music into one stereo track aligned to pipeline/timing.json.

  python3 pipeline/mix_audio.py                       # audio/music-orchestral.mp3, looped once so its natural ending
                                                      # lands on the last frame, envelope ducking under the voice
  python3 pipeline/mix_audio.py --music audio/music_bed.wav --no-loop --music-db -11.7   # the generated bed (v2)

The ducking is an explicit gain envelope computed from the voice (not a compressor): the music sits at --music-db
when nobody speaks and at --music-db + --duck-db while the narrator talks, with 150 ms attack / 900 ms release.
Nothing in the chain pumps or limits: the voice is normalised to --vo-peak and the sum stays below full scale.
"""
import argparse, json, os, subprocess
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
try:
    import imageio_ffmpeg; FF = imageio_ffmpeg.get_ffmpeg_exe()
except Exception: FF = "ffmpeg"
SR = 44100

ap = argparse.ArgumentParser()
ap.add_argument("--music", default=None)
ap.add_argument("--music-db", type=float, default=-12.0, help="music level (dB) between lines")
ap.add_argument("--duck-db", type=float, default=-9.0, help="extra attenuation while the narrator speaks")
ap.add_argument("--vo-peak", type=float, default=0.72, help="voice peak after normalisation (linear)")
ap.add_argument("--loop-at", type=float, default=None, help="film time where the second music pass starts (default: auto)")
ap.add_argument("--no-loop", action="store_true")
ap.add_argument("--xfade", type=float, default=6.0)
ap.add_argument("--music-end", type=float, default=None)
ap.add_argument("--edge-fade", type=float, default=0.015, help="fade in/out (s) applied to every VO clip")
ap.add_argument("--out", default=os.path.join(ROOT, "audio", "mix.mp3"))
a = ap.parse_args()

def decode(path, stereo=True):
    """Any audio file -> float32 array (n, 2) at 44.1 kHz."""
    raw = subprocess.run([FF, "-v", "error", "-i", path, "-f", "f32le", "-ac", "2" if stereo else "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, dtype=np.float32)
    return x.reshape(-1, 2) if stereo else x

T = json.load(open(os.path.join(ROOT, "pipeline", "timing.json")))
total = T["total"]; N = int(round(total * SR))
music = a.music or next((p for p in (os.path.join(ROOT, "audio", "music-orchestral.mp3"), os.path.join(ROOT, "audio", "music_bed.wav")) if os.path.exists(p)), None)
if not music: raise SystemExit("no music file: put the track at audio/music-orchestral.mp3 or run make_music.py")

# ---- voice: every clip at its slot, gentle edge fades, normalised as a whole ----
vo = np.zeros((N, 2), dtype=np.float32)
ef = int(a.edge_fade * SR); ramp = np.linspace(0, 1, ef, dtype=np.float32)[:, None]
for s in T["scenes"]:
    f = next((c for c in (os.path.join(ROOT, "voiceover", f"s{s['n']:02d}.{e}") for e in ("wav", "mp3")) if os.path.exists(c)), "")
    if s["vo"] <= 0 or not os.path.exists(f): continue
    x = decode(f).copy()
    if len(x) > 2 * ef: x[:ef] *= ramp; x[-ef:] *= ramp[::-1]
    at = int(round(s["vo_at"] * SR)); n = min(len(x), N - at)
    vo[at:at + n] += x[:n]
vo *= a.vo_peak / max(1e-6, np.abs(vo).max())

# ---- music: one pass, optionally crossfaded into a second pass so the real ending lands on the last frame ----
m = decode(music)
env_m = np.abs(m).max(axis=1)
above = np.nonzero(env_m > 10 ** (-45 / 20))[0]
end = a.music_end or (above[-1] / SR if len(above) else len(m) / SR)
loop = not a.no_loop and end < total
if loop:
    loop_at = a.loop_at if a.loop_at is not None else round(total - end - 0.2, 2)
    xf = int(a.xfade * SR); la = int(loop_at * SR)
    out = np.zeros((max(N, la + len(m)), 2), dtype=np.float32)
    first = m[:la + xf].copy()
    fade = np.sqrt(np.linspace(1, 0, xf, dtype=np.float32))[:, None]      # equal-power crossfade
    first[la:la + xf] *= fade
    second = m.copy(); second[:xf] *= np.sqrt(np.linspace(0, 1, xf, dtype=np.float32))[:, None]
    out[:len(first)] += first; out[la:la + len(second)] += second
    m = out[:N]
    print(f"music {os.path.basename(music)}: ends at {end:.2f} s, second pass at {loop_at:.2f} s (crossfade {a.xfade} s), natural ending at {loop_at + end:.2f} of {total} s")
else:
    m = np.concatenate([m, np.zeros((max(0, N - len(m)), 2), dtype=np.float32)])[:N]
m = m / max(1e-6, np.abs(m).max())                     # music peak-normalised, then placed with --music-db
fi = int(1.0 * SR); m[:fi] *= np.linspace(0, 1, fi, dtype=np.float32)[:, None]
fo = int(1.2 * SR); m[-fo:] *= np.linspace(1, 0, fo, dtype=np.float32)[:, None]

# ---- ducking envelope from the voice: RMS (20 ms) -> attack 150 ms / release 900 ms -> gain between the two levels ----
hop = int(0.02 * SR); frames = N // hop
rms = np.sqrt((vo[:frames * hop].mean(axis=1) ** 2).reshape(frames, hop).mean(axis=1))
speech = np.clip(rms / (0.25 * a.vo_peak), 0, 1)        # 0 = silence, 1 = full speech level
sm = np.zeros_like(speech); att = np.exp(-hop / (0.15 * SR)); rel = np.exp(-hop / (0.9 * SR)); y = 0.0
for i, v in enumerate(speech):
    y = v + (y - v) * (att if v > y else rel); sm[i] = y
gain_db = a.music_db + a.duck_db * sm
g = np.interp(np.arange(N), np.arange(frames) * hop + hop / 2, 10 ** (gain_db / 20)).astype(np.float32)
mix = vo + m * g[:, None]
peak = np.abs(mix).max()
if peak > 0.98: mix *= 0.98 / peak
tmp = a.out + ".f32"
mix.astype(np.float32).tofile(tmp)
subprocess.run([FF, "-y", "-loglevel", "error", "-f", "f32le", "-ac", "2", "-ar", str(SR), "-i", tmp, "-b:a", "320k", a.out], check=True)
os.remove(tmp)
print(f"wrote {a.out} {os.path.getsize(a.out)} bytes; total {total} s; music {a.music_db} dB, duck {a.duck_db} dB, voice peak {a.vo_peak}, mix peak {peak:.2f}")
