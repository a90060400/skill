# -*- coding: utf-8 -*-
import re
import urllib.request
from pathlib import Path

saved = Path(r"d:\skill\sources\archmage-fp.html").read_text(encoding="utf-8")
req = urllib.request.Request(
    "https://artale.live/tw/patch-notes/cygnus-knights/archmage-fp",
    headers={"User-Agent": "Mozilla/5.0"},
)
live = urllib.request.urlopen(req).read().decode("utf-8")
Path(r"d:\skill\sources\archmage-fp.html").write_text(live, encoding="utf-8")


def show(label, html):
    i = html.find('id="skill-2121001"')
    chunk = html[i:i + 5000]
    print("===", label, "idx", i, "===")
    name = re.search(r'__name"[^>]*>([^<]+)', chunk)
    print("NAME", name.group(1) if name else None)
    for src in re.findall(r'src="([^"]+)"', chunk)[:15]:
        print("SRC", src)
    tags = re.findall(r">(新增|刪除|特效調整|調整|修改)<", chunk)
    print("TAGS", tags[:8])


show("SAVED", saved)
show("LIVE", live)
print("SAME", saved == live)
