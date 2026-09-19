import json, re, sys, requests

tpath, opath, key, model = sys.argv[1:5]
data = json.load(open(tpath, encoding="utf-8"))
segs = data.get("segments", [])
if not segs: raise SystemExit("No transcript segments.")

transcript = "\n".join(f'{i}: [{s["start"]:.2f}-{s["end"]:.2f}] {s["text"]}' for i,s in enumerate(segs))
prompt = f"""Select up to 5 strong YouTube Shorts moments from this transcript.
Return ONLY JSON:
{{"clips":[{{"start":0.0,"end":30.0,"title":"hook title","reason":"one sentence"}}]}}
Rules: 20-60 seconds each; self-contained; strong hook, insight, story, conflict, surprise or punchline; avoid sponsor reads, intros, repetition and incomplete endings; do not overlap; timestamps must be from the transcript.
Transcript:
{transcript}"""

r = requests.post(
    f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
    params={"key": key},
    json={"contents":[{"parts":[{"text":prompt}]}]},
    timeout=120
)
r.raise_for_status()
text = r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.I)

try:
    obj = json.loads(text)
except json.JSONDecodeError:
    obj = json.loads(re.search(r"\{.*\}", text, re.S).group(0))

clips=[]
for c in obj.get("clips", []):
    try:
        s,e=float(c["start"]),float(c["end"])
        if e-s < 20: continue
        e=min(e, s+60)
        clips.append({"start":round(s,2),"end":round(e,2),
                      "title":str(c.get("title","AI selected clip"))[:120],
                      "reason":str(c.get("reason",""))[:240]})
    except Exception: pass

clips.sort(key=lambda x:x["start"])
clean=[]
for c in clips:
    if any(not (c["end"]<=x["start"] or c["start"]>=x["end"]) for x in clean): continue
    clean.append(c)

if not clean:
    dur=float(data.get("duration",0))
    cur=0
    while cur+25<=dur and len(clean)<5:
        clean.append({"start":round(cur,2),"end":round(min(cur+45,dur),2),"title":f"Clip {len(clean)+1}","reason":"Fallback selection"})
        cur+=55

json.dump({"clips":clean[:5]}, open(opath,"w",encoding="utf-8"), ensure_ascii=False, indent=2)
print(json.dumps({"clips":clean[:5]}, indent=2))
