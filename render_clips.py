import json, subprocess, sys
from pathlib import Path

source,tpath,cpath,outdir=sys.argv[1:5]
Path(outdir).mkdir(parents=True,exist_ok=True)
data=json.load(open(tpath,encoding="utf-8"))
clips=json.load(open(cpath,encoding="utf-8")).get("clips",[])
segs=data.get("segments",[])

def srt_time(sec):
    ms=int(round(sec*1000)); h=ms//3600000; ms%=3600000; m=ms//60000; ms%=60000; s=ms//1000; ms%=1000
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

for i,c in enumerate(clips,1):
    start,end=float(c["start"]),float(c["end"])
    srt=Path(outdir)/f"clip_{i:02d}.srt"
    mp4=Path(outdir)/f"clip_{i:02d}.mp4"
    rows=[]; n=1
    for seg in segs:
        a=max(float(seg["start"]),start); b=min(float(seg["end"]),end)
        if b>a and seg["text"].strip():
            rows.append(f"{n}\n{srt_time(a-start)} --> {srt_time(b-start)}\n{seg['text'].strip()}\n"); n+=1
    srt.write_text("\n".join(rows),encoding="utf-8")
    vf=f"""[0:v]split=2[bg][fg];[bg]scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,boxblur=18:6[bg2];[fg]scale=720:1280:force_original_aspect_ratio=decrease[fg2];[bg2][fg2]overlay=(W-w)/2:(H-h)/2,subtitles={srt}:force_style='FontName=Arial,FontSize=18,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2,Alignment=2,MarginV=90'"""
    cmd=["ffmpeg","-y","-ss",str(start),"-i",source,"-t",str(end-start),"-vf",vf,
         "-c:v","libx264","-preset","veryfast","-crf","28","-maxrate","4M","-bufsize","8M",
         "-c:a","aac","-b:a","128k","-movflags","+faststart",str(mp4)]
    subprocess.run(cmd,check=True)
    if mp4.stat().st_size>49_000_000:
        cmd[cmd.index("-crf")+1]="31"
        subprocess.run(cmd,check=True)
    print(mp4)
