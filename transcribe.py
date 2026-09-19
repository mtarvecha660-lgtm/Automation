import json, sys
from faster_whisper import WhisperModel

video, out = sys.argv[1:3]
model = WhisperModel("tiny", device="cpu", compute_type="int8")
segments, info = model.transcribe(video, beam_size=1, vad_filter=True, condition_on_previous_text=False)

rows = []
for s in segments:
    t = (s.text or "").strip()
    if t:
        rows.append({"start": round(float(s.start),2), "end": round(float(s.end),2), "text": t})

with open(out, "w", encoding="utf-8") as f:
    json.dump({"language": getattr(info, "language", None), "duration": rows[-1]["end"] if rows else 0, "segments": rows}, f, ensure_ascii=False, indent=2)
print(f"Transcript segments: {len(rows)}")
