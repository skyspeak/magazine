"""Renders the parents' episode for Issue No. 01 from script.txt.
Outputs audio/no-01-dog-parents.wav; encode to .m4a with the afconvert line in the README.
Chapter offsets live in src/chapters.json and are pasted into the published HTML."""
import subprocess, wave, math, struct, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))     # src/
BASE = os.path.dirname(HERE)                          # repo root
TMP  = os.path.join(BASE, "audio", "parts")
os.makedirs(TMP, exist_ok=True)
SR = 22050

VOICES = {"N": "Samantha", "D": "Daniel", "K": "Karen"}

def silence(ms):
    return b"\x00\x00" * int(SR * ms / 1000)

def render_line(i, voice, rate, text):
    path = os.path.join(TMP, f"{i:03d}.wav")
    subprocess.run(["say", "-v", voice, "-r", str(rate), "-o", path,
                    "--data-format=LEI16@%d" % SR, text], check=True)
    with wave.open(path) as w:
        return w.readframes(w.getnframes())

def sting(seconds=4.6, outro=False):
    """Warm plucked arpeggio: additive sines with exponential decay."""
    n = int(SR * seconds)
    buf = [0.0] * n
    # A minor 9 -> F major feel; frequencies in Hz
    seq = [(220.0, 0.00), (329.63, 0.18), (440.0, 0.36), (587.33, 0.54),
           (659.25, 0.72), (440.0, 0.90), (349.23, 1.14), (523.25, 1.32),
           (698.46, 1.50), (880.0, 1.68), (659.25, 1.92), (587.33, 2.16)]
    if outro:
        seq = [(220.0, 0.0), (329.63, 0.2), (440.0, 0.4), (659.25, 0.62), (880.0, 0.86)]
    for f, t0 in seq:
        s0 = int(t0 * SR)
        dur = int(1.9 * SR)
        for k in range(dur):
            idx = s0 + k
            if idx >= n: break
            env = math.exp(-3.1 * k / SR)
            tt = k / SR
            v = (math.sin(2*math.pi*f*tt) * 0.55
                 + math.sin(2*math.pi*f*2*tt) * 0.20 * math.exp(-7*tt)
                 + math.sin(2*math.pi*f*3*tt) * 0.07 * math.exp(-11*tt))
            buf[idx] += v * env * 0.20
    # low sustained pad under it
    for k in range(n):
        tt = k / SR
        env = min(tt / 0.25, 1.0) * math.exp(-0.55 * tt)
        buf[k] += (math.sin(2*math.pi*110.0*tt) * 0.10
                   + math.sin(2*math.pi*164.81*tt) * 0.055) * env
    # fade tail
    fade = int(0.5 * SR)
    for k in range(fade):
        buf[n-fade+k] *= (1 - k/fade)
    out = bytearray()
    for v in buf:
        s = max(-1.0, min(1.0, v))
        out += struct.pack("<h", int(s * 32767))
    return bytes(out)

lines = []
with open(os.path.join(HERE, "script.txt")) as f:
    for raw in f:
        raw = raw.rstrip("\n")
        if not raw.strip(): continue
        spk, rate, text = raw.split("::", 2)
        lines.append((spk, int(rate), text))

frames = bytearray()
prev = None
for i, (spk, rate, text) in enumerate(lines):
    if i == 3:                       # theme sting after the cold open
        frames += silence(150) + sting() + silence(250)
        prev = None
    if prev is not None:
        frames += silence(400 if spk != prev else 220)
    frames += render_line(i, VOICES[spk], rate, text)
    prev = spk
    if i % 15 == 0: print(f"  line {i}/{len(lines)}", flush=True)

frames += silence(300) + sting(3.2, outro=True)

master = os.path.join(BASE, "audio", "no-01-dog-parents.wav")
with wave.open(master, "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(bytes(frames))

secs = len(frames) / 2 / SR
print(f"master: {master}  {int(secs//60)}m{int(secs%60):02d}s  {os.path.getsize(master)/1e6:.1f} MB")
