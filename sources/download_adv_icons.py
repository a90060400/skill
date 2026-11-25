# -*- coding: utf-8 -*-
import urllib.request
from pathlib import Path

root = Path(r"d:\skill\sources\adventurer-patch.txt")
text = root.read_text(encoding="utf-8")
job = None
items = []
for line in text.splitlines():
    if line.startswith("########"):
        job = line.strip("# ").strip()
        continue
    if line.startswith("  ICON ") and job:
        src = line.strip()
        src = src[len("ICON "):].strip() if src.startswith("ICON ") else src
        items.append((job, src, last_id, last_tag))
    elif line and line[0].isdigit() and "\t" in line:
        parts = line.split("\t")
        last_id, last_tag = parts[0], parts[1]

base = "https://artale.live"
ok = 0
for job, src, sid, tag in items:
    if tag == "刪除":
        continue
    if src.startswith("http"):
        url = src
    else:
        url = base + src
    dest_dir = Path(r"d:\skill\icons") / job
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"{sid}.png"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        data = urllib.request.urlopen(req, timeout=30).read()
    except Exception as exc:
        print("FAIL", job, sid, url, exc)
        continue
    i = data.find(b"IEND")
    if i >= 0:
        data = data[: i + 8]
    dest.write_bytes(data)
    ok += 1
    print(job, sid, len(data), data[:4])
print("saved", ok)
