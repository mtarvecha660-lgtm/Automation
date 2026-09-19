import json, sys, requests
from pathlib import Path

cpath,outdir,token,chat=sys.argv[1:5]
clips=json.load(open(cpath,encoding="utf-8")).get("clips",[])

for i,c in enumerate(clips,1):
    p=Path(outdir)/f"clip_{i:02d}.mp4"
    if not p.exists(): continue
    caption=f"🎬 Clip {i}/{len(clips)}\n🔥 {c.get('title','AI selected clip')}\n\n{c.get('reason','')}"[:1024]
    with p.open("rb") as f:
        r=requests.post(f"https://api.telegram.org/bot{token}/sendVideo",
                         data={"chat_id":chat,"caption":caption,"supports_streaming":"true"},
                         files={"video":(p.name,f,"video/mp4")},timeout=180)
    r.raise_for_status()

requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
              data={"chat_id":chat,"text":f"✅ Done — {len(clips)} clip(s) sent."},timeout=30).raise_for_status()
