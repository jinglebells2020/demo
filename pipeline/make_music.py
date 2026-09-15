#!/usr/bin/env python3
"""Compose the music bed procedurally (no samples, no external assets): a slow ambient piece in D major —
soft pad chords, a sparse piano-like arpeggio, a sub bass, light reverb, intro fade and a final swell.
Writes audio/music_bed.wav (44.1 kHz stereo). Usage: python3 pipeline/make_music.py [duration_s]
"""
import sys, os, wave, struct
import numpy as np

SR = 44100
DUR = float(sys.argv[1]) if len(sys.argv) > 1 else 300.0
BPM = 66
BEAT = 60.0 / BPM
BAR = 4 * BEAT
rng = np.random.default_rng(7)

def midi(n): return 440.0 * 2 ** ((n - 69) / 12)
# chords (MIDI numbers): D major I — V — vi — IV, two bars each; then a variation I — iii — IV — V
PROG_A = [[50, 57, 61, 64], [45, 52, 56, 61], [47, 54, 57, 62], [43, 50, 54, 59]]   # D, A, Bm, G
PROG_B = [[50, 57, 61, 66], [42, 49, 54, 57], [43, 50, 54, 59], [45, 52, 56, 61]]   # Dadd9, F#m, G, A
N = int(DUR * SR)
mix = np.zeros(N, dtype=np.float64)
t_all = np.arange(N) / SR

def env_ad(n, attack, decay, sustain=0.0):
    e = np.ones(n)
    a = int(attack * SR); d = int(decay * SR)
    if a > 0: e[:a] = np.linspace(0, 1, min(a, n))[:min(a, n)]
    tail = np.exp(-np.arange(n) / max(d, 1))
    return e * (sustain + (1 - sustain) * tail)

def add(sig, start_s):
    s = int(start_s * SR)
    if s < 0: sig = sig[-s:]; s = 0
    if s >= N or len(sig) == 0: return
    e = min(N, s + len(sig)); mix[s:e] += sig[:e - s]

def pad_tone(f, dur):
    n = int(dur * SR); t = np.arange(n) / SR
    out = np.zeros(n)
    for det in (-0.35, 0.0, 0.35):              # gentle chorus
        ff = f * 2 ** (det / 1200)
        for k in range(1, 7):                  # band-limited soft saw
            out += np.sin(2 * np.pi * ff * k * t + rng.uniform(0, 6.28)) / (k ** 1.7)
    vib = 1 + 0.004 * np.sin(2 * np.pi * 0.17 * t)
    out *= vib
    e = np.ones(n); a = int(1.8 * SR); r = int(2.5 * SR)
    e[:a] = np.linspace(0, 1, a); e[-r:] *= np.linspace(1, 0, r)
    return out * e / 3.0

def piano_tone(f, dur, vel):
    n = int(dur * SR); t = np.arange(n) / SR
    out = np.zeros(n)
    partials = [(1, 1.0), (2, 0.42), (3, 0.2), (4, 0.1), (5, 0.05), (6, 0.03)]
    for k, amp in partials:
        inh = 1 + 0.0004 * k * k
        out += amp * np.sin(2 * np.pi * f * k * inh * t) * np.exp(-t * (2.2 + 0.9 * k))
    hammer = np.exp(-t * 60) * 0.15 * np.sin(2 * np.pi * f * 7 * t)
    return (out + hammer) * vel * env_ad(n, 0.004, 1.6)

def bass_tone(f, dur):
    n = int(dur * SR); t = np.arange(n) / SR
    out = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * f * 2 * t)
    return out * env_ad(n, 0.02, 1.4) * 0.9

# ---- arrangement ----
loop_len = 8 * BAR
n_loops = int(np.ceil(DUR / loop_len)) + 1
pos = 0.0
for li in range(n_loops):
    prog = PROG_A if li % 3 != 2 else PROG_B
    for ci, chord in enumerate(prog):
        start = pos + ci * 2 * BAR
        if start >= DUR: break
        # pad
        for m in chord:
            add(pad_tone(midi(m), 2 * BAR + 0.5), start)
        # bass on bar 1 and 2
        for b in (0, 1):
            add(bass_tone(midi(chord[0] - 12), BAR), start + b * BAR)
        # arpeggio: 8th notes, chord tones spread over two octaves, sparse (skip some), quiet
        tones = [m + 12 for m in chord] + [m + 24 for m in chord[:2]]
        for step in range(16):
            if rng.random() < 0.28: continue
            m = tones[(step * 3 + ci) % len(tones)]
            vel = 0.35 + 0.25 * rng.random()
            if step % 4 == 0: vel += 0.15
            add(piano_tone(midi(m), 2.2, vel), start + step * BEAT / 2 + rng.uniform(-0.008, 0.008))
    pos += loop_len

# ---- reverb (exponentially decaying noise IR, FFT convolution) ----
ir_len = int(2.4 * SR)
ir = rng.standard_normal(ir_len) * np.exp(-np.arange(ir_len) / (0.55 * SR))
ir[:int(0.02 * SR)] *= np.linspace(0, 1, int(0.02 * SR))
ir /= np.sqrt(np.sum(ir ** 2))
def conv(x, h):
    n = len(x) + len(h) - 1; nf = 1 << (n - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(x, nf) * np.fft.rfft(h, nf), nf)[:len(x)]
wet = conv(mix, ir)
dry = mix
L = dry + 0.55 * wet
R = dry + 0.55 * np.roll(wet, int(0.011 * SR))
# gentle low-pass (one-pole) to keep it soft
def lp(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); z = 0.0
    for i in range(0, len(x), 1):
        pass
    # vectorised one-pole via lfilter-free recursion in chunks
    from itertools import accumulate
    return np.array(list(accumulate(x, lambda acc, v: a * acc + (1 - a) * v)))
# (cheap alternative: FFT low-pass)
def fft_lp(x, fc):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / np.sqrt(1 + (f / fc) ** 4); return np.fft.irfft(X, len(x))
L = fft_lp(L, 3800); R = fft_lp(R, 3800)
# ---- dynamics: fade-in 6 s, final swell from DUR-22, fade-out last 5 s ----
g = np.ones(N)
fi = int(6 * SR); g[:fi] = np.linspace(0, 1, fi)
sw0 = int(max(0, DUR - 22) * SR); sw1 = int(max(0, DUR - 6) * SR)
if sw1 > sw0: g[sw0:sw1] *= np.linspace(1, 1.35, sw1 - sw0); g[sw1:] *= 1.35
fo = int(5 * SR); g[-fo:] *= np.linspace(1, 0, fo)
L *= g; R *= g
peak = max(np.max(np.abs(L)), np.max(np.abs(R)))
L /= peak / 0.8; R /= peak / 0.8
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "audio", "music_bed.wav")
os.makedirs(os.path.dirname(out), exist_ok=True)
data = np.stack([L, R], axis=1); pcm = (np.clip(data, -1, 1) * 32767).astype("<i2")
with wave.open(out, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("wrote", out, round(DUR, 1), "s, peak", round(float(peak), 3))
