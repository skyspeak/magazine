"""Renders the kids' episode for Issue No. 01 from script-kid.txt.
Outputs audio/no-01-dog-kids.wav and writes src/chapters-kid.json."""
import subprocess, wave, math, struct, os, json

HERE = os.path.dirname(os.path.abspath(__file__))     # src/
BASE = os.path.dirname(HERE)                          # repo root
TMP  = os.path.join(BASE, "audio", "kidparts")
os.makedirs(TMP, exist_ok=True)
SR = 22050
VOICES = {"N": "Samantha", "D": "Daniel"}
STING_AT = 2

def silence(ms): return b"\x00\x00" * int(SR * ms / 1000)

def render_line(i, voice, rate, text):
    path = os.path.join(TMP, f"{i:03d}.wav")
    subprocess.run(["say","-v",voice,"-r",str(rate),"-o",path,"--data-format=LEI16@%d"%SR,text], check=True)
    with wave.open(path) as w: return w.readframes(w.getnframes())

def sting(seconds=3.9, outro=False):
    """Bright, bouncy major arpeggio — the kid cut."""
    n = int(SR*seconds); buf=[0.0]*n
    seq = [(523.25,0.00),(659.25,0.13),(783.99,0.26),(1046.50,0.39),
           (880.00,0.55),(783.99,0.66),(1046.50,0.78),(1318.51,0.91),
           (1174.66,1.10),(987.77,1.22),(1318.51,1.34),(1567.98,1.50)]
    if outro:
        seq = [(523.25,0.0),(659.25,0.12),(783.99,0.24),(1046.50,0.38),(1318.51,0.56)]
    for f,t0 in seq:
        s0=int(t0*SR); dur=int(1.3*SR)
        for k in range(dur):
            idx=s0+k
            if idx>=n: break
            tt=k/SR; env=math.exp(-5.2*tt)
            v=(math.sin(2*math.pi*f*tt)*0.5
               + math.sin(2*math.pi*f*2*tt)*0.26*math.exp(-9*tt)
               + math.sin(2*math.pi*f*3*tt)*0.11*math.exp(-14*tt))
            buf[idx]+=v*env*0.19
    # bouncing bass pulse
    for beat in range(int(seconds/0.26)):
        s0=int(beat*0.26*SR); f=130.81 if beat%2==0 else 196.00
        for k in range(int(0.22*SR)):
            idx=s0+k
            if idx>=n: break
            tt=k/SR
            buf[idx]+=math.sin(2*math.pi*f*tt)*0.14*math.exp(-11*tt)
    fade=int(0.35*SR)
    for k in range(fade): buf[n-fade+k]*=(1-k/fade)
    out=bytearray()
    for v in buf:
        out+=struct.pack("<h", int(max(-1.0,min(1.0,v))*32767))
    return bytes(out)

lines=[]
for raw in open(os.path.join(HERE,"script-kid.txt")):
    raw=raw.rstrip("\n")
    if not raw.strip(): continue
    spk,rate,text=raw.split("::",2)
    lines.append((spk,int(rate),text))

frames=bytearray(); starts=[]; prev=None; t=0.0
for i,(spk,rate,text) in enumerate(lines):
    if i==STING_AT:
        pad=silence(150)+sting()+silence(300); frames+=pad
        t+=len(pad)/2/SR; prev=None
    if prev is not None:
        gap=400 if spk!=prev else 220
        frames+=silence(gap); t+=gap/1000
    starts.append(t)
    pcm=render_line(i,VOICES[spk],rate,text)
    frames+=pcm; t+=len(pcm)/2/SR; prev=spk
    if i%12==0: print(f"  {i}/{len(lines)}",flush=True)

tail=silence(300)+sting(2.6,outro=True); frames+=tail; t+=len(tail)/2/SR

master=os.path.join(BASE,"audio","no-01-dog-kids.wav")
with wave.open(master,"wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(bytes(frames))

CH=[(0,"Start here"),(2,"Why asking again backfires"),(7,"The four things they're actually scared of"),
    (14,"The magic question"),(17,"Mission: fourteen mornings"),(22,"Name what you're giving up"),
    (26,"Argue against yourself"),(31,"Four facts that make you sound like a pro"),
    (36,"The sad part"),(40,"If they say no - or not yet")]
chaps=[{"t":round(starts[i],1),"label":f"{int(starts[i]//60)}:{int(starts[i]%60):02d}","title":ti} for i,ti in CH]
json.dump(chaps, open(os.path.join(HERE,"chapters-kid.json"),"w"), indent=1)
for c in chaps: print(f"  {c['label']:>6}  {c['title']}")
print(f"master {int(t//60)}m{int(t%60):02d}s  {os.path.getsize(master)/1e6:.1f} MB")
