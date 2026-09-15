#!/usr/bin/env python3
"""Acoustic stress check for Russian TTS takes.

For a word with known time span (from faster-whisper word timestamps) the syllable nuclei are found as peaks of the
250–3500 Hz energy envelope; the stressed syllable is the nucleus with the largest duration × energy product (Russian
stressed vowels are longer and louder than reduced unstressed ones). The predicted syllable index is compared with the
expected one (the vowel that carries the U+0301 mark in the reference spelling).

Usage as a library: predict(wav, start, end, n_vowels) -> (index, details)
"""
import subprocess, unicodedata, sys, json
import numpy as np
try:
    import imageio_ffmpeg; FF = imageio_ffmpeg.get_ffmpeg_exe()
except Exception: FF = "ffmpeg"
SR = 16000
VOWELS = "аеёиоуыэюя"

def load(path):
    raw = subprocess.run([FF, "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32)

def envelope(x, frame=0.02, hop=0.005):
    n = int(frame * SR); h = int(hop * SR); win = np.hanning(n)
    freqs = np.fft.rfftfreq(n, 1 / SR); band = (freqs >= 250) & (freqs <= 3500)
    e = []
    for i in range(0, max(1, len(x) - n), h):
        s = np.abs(np.fft.rfft(x[i:i + n] * win)) ** 2; e.append(s[band].sum())
    e = np.array(e) + 1e-12
    k = np.ones(5) / 5; e = np.convolve(e, k, mode="same")
    return e, h

def nuclei(e, min_dist=0.07, hop=0.005, prom=0.15):
    """Local maxima of the envelope with prominence >= prom * max, at least min_dist apart."""
    md = int(min_dist / hop); peaks = []
    for i in range(1, len(e) - 1):
        if e[i] >= e[i - 1] and e[i] > e[i + 1] and e[i] >= prom * e.max():
            if peaks and i - peaks[-1] < md:
                if e[i] > e[peaks[-1]]: peaks[-1] = i
            else: peaks.append(i)
    out = []
    for p in peaks:  # duration at half height
        l = p
        while l > 0 and e[l] > e[p] / 2: l -= 1
        r = p
        while r < len(e) - 1 and e[r] > e[p] / 2: r += 1
        out.append((p, (r - l) * hop, float(e[p])))
    return out

def predict(x, start, end, n_vowels):
    a = max(0, int((start - 0.02) * SR)); b = min(len(x), int((end + 0.02) * SR))
    seg = x[a:b]
    if len(seg) < int(0.05 * SR): return None, {"reason": "short"}
    e, h = envelope(seg); nu = nuclei(e)
    if not nu: return None, {"reason": "no nuclei"}
    if len(nu) > n_vowels:  # keep the strongest n_vowels nuclei, in time order
        nu = sorted(sorted(nu, key=lambda t: -t[1] * t[2])[:n_vowels], key=lambda t: t[0])
    scores = [d * en for _, d, en in nu]
    idx = int(np.argmax(scores))
    if len(nu) < n_vowels:
        # fewer nuclei than vowels: map by relative position inside the word
        pos = nu[idx][0] * h / max(1, len(seg)); idx = min(n_vowels - 1, int(pos * n_vowels))
    conf = (sorted(scores)[-1] / (sorted(scores)[-2] + 1e-9)) if len(scores) > 1 else 9.0
    return idx, {"nuclei": len(nu), "scores": [round(s / max(scores), 2) for s in scores], "conf": round(float(conf), 2)}

def strip_marks(w): return "".join(c for c in unicodedata.normalize("NFD", w) if unicodedata.category(c) != "Mn")
def expected_index(marked):
    """Index (0-based, among vowels) of the vowel carrying U+0301; ё counts as stressed if no mark."""
    d = unicodedata.normalize("NFD", marked.lower()); vi = -1; stressed = None
    for i, c in enumerate(d):
        if c in VOWELS: vi += 1
        if c == "́" and stressed is None: stressed = vi
    if stressed is None:
        nfc = unicodedata.normalize("NFC", marked.lower()); vs = [c for c in nfc if c in VOWELS]
        if "ё" in vs: stressed = vs.index("ё")
    return stressed, vi + 1
