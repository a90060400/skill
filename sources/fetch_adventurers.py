# -*- coding: utf-8 -*-
import re
import urllib.request
from html import unescape
from pathlib import Path

jobs = [
    "hero", "paladin", "darkknight", "archmage-il", "bishop",
    "bowmaster", "marksman", "nightlord", "shadower", "viper", "captain",
]
root = Path(r"d:\skill\sources")
root.mkdir(exist_ok=True)


def clean(html):
    text = re.sub(r"<[^>]+>", "", html)
    text = unescape(re.sub(r"\s+", " ", text)).strip()
    return text


lines = []
for slug in jobs:
    url = f"https://artale.live/tw/patch-notes/cygnus-knights/{slug}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    html = urllib.request.urlopen(req).read().decode("utf-8")
    (root / f"{slug}.html").write_text(html, encoding="utf-8")
    parts = re.split(r'<article class="card-module__[^"]*__card [^"]*" id="(skill-\d+)">', html)
    lines.append(f"\n######## {slug} ########")
    count = 0
    for i in range(1, len(parts), 2):
        sid = parts[i].replace("skill-", "")
        body = parts[i + 1]
        end = body.find("</article>")
        body = body[:end] if end >= 0 else body
        head_end = body.find('class="card-module__')
        # header ends at comment or grid
        header = body.split('class="card-module__', 1)[0]
        # better: cut at first comment
        cut = body.find("__comment")
        header = body[:cut] if cut >= 0 else body[:1500]
        name = clean(re.search(r'__name"[^>]*>(.*?)</h4>', body, re.S).group(1)) if re.search(r'__name"', body) else "?"
        master = clean(re.search(r'__headMaster">(.*?)</span>', body, re.S).group(1)) if re.search(r'__headMaster', body) else ""
        desc_m = re.search(r'__headDesc"[^>]*>(.*?)</p>', body, re.S)
        desc = clean(desc_m.group(1)) if desc_m else ""
        req_m = re.search(r"前置技能：([^<]+)", body)
        req = clean(req_m.group(1)) if req_m else ""
        icon_m = re.search(r'<img src="([^"]+)"', body)
        icon = icon_m.group(1) if icon_m else ""
        tags = []
        for t in re.findall(r'__chip[^"]*"[^>]*>(新增|刪除|特效調整|數值調整|調整|修改)<', header):
            if t not in tags:
                tags.append(t)
        rows = []
        for label, before, after in re.findall(
            r'__label">(.*?)</span></th><td class="table-module__[^"]*__before[^"]*">(.*?)</td><td class="table-module__[^"]*__after">(.*?)</td>',
            body,
            re.S,
        ):
            rows.append((clean(label), clean(after)))
        count += 1
        lines.append(f"{sid}\t{'/'.join(tags) or '-'}\t{name}\t{master}\tREQ {req}")
        lines.append(f"  DESC {desc}")
        lines.append(f"  ICON {icon}")
        for label, after in rows:
            lines.append(f"  * {label} => {after}")
    lines.append(f"COUNT {count}")

out = root / "adventurer-patch.txt"
out.write_text("\n".join(lines), encoding="utf-8")
print("wrote", out, "chars", out.stat().st_size)
