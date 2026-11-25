# -*- coding: utf-8 -*-
import re
from pathlib import Path
from html import unescape

html = Path(r"d:\skill\sources\archmage-fp.html").read_text(encoding="utf-8")
# split articles
parts = re.split(r'<article class="card-module__[^"]*__card [^"]*" id="(skill-\d+)">', html)
# parts[0] preamble, then id, body, id, body...
out = []
for i in range(1, len(parts), 2):
    sid = parts[i].replace("skill-", "")
    body = parts[i + 1]
    end = body.find("</article>")
    body = body[:end] if end >= 0 else body

    def text_of(pattern, src=body):
        m = re.search(pattern, src, re.S)
        if not m:
            return ""
        t = re.sub(r"<[^>]+>", "", m.group(1))
        t = unescape(re.sub(r"\s+", " ", t)).strip()
        return t

    name = text_of(r'class="card-module__[^"]*__name"[^>]*>(.*?)</h4>')
    master = text_of(r'class="card-module__[^"]*__headMaster">(.*?)</span>')
    desc = text_of(r'class="card-module__[^"]*__headDesc"[^>]*>(.*?)</p>')
    req = text_of(r"前置技能：(.*?)</p>")
    comment = text_of(r'class="card-module__[^"]*__comment">(.*?)</p>')
    icon = ""
    im = re.search(r'<img src="([^"]+)"', body)
    if im:
        icon = im.group(1)
    tags = re.findall(r'class="b4-module__[^"]*__chip[^"]*">(新增|刪除|調整|修改|特效調整|數值調整)', body)
    # unique preserve order, only header tags roughly first few
    seen = []
    for t in tags:
        if t not in seen:
            seen.append(t)
    # after values: label + after cell
    rows = re.findall(
        r'<span class="table-module__[^"]*__label">(.*?)</span></th><td class="table-module__[^"]*__before[^"]*">(.*?)</td><td class="table-module__[^"]*__after">(.*?)</td>',
        body,
        re.S,
    )
    changes = []
    for label, before, after in rows:
        def clean(x):
            x = re.sub(r"<[^>]+>", "", x)
            return unescape(re.sub(r"\s+", " ", x)).strip()
        changes.append((clean(label), clean(before), clean(after)))
    grade = sid[:3]
    out.append((sid, grade, name, master, " ".join(seen), req, desc, icon, comment, changes))

Path(r"d:\skill\sources\archmage-fp.txt").write_text(
    "\n\n".join(
        f"ID {sid} grade {grade}\nNAME {name}\nMASTER {master}\nTAGS {tags}\nREQ {req}\nDESC {desc}\nICON {icon}\nCOMMENT {comment}\n"
        + "\n".join(f"  {a} | {b} -> {c}" for a, b, c in changes)
        for sid, grade, name, master, tags, req, desc, icon, comment, changes in out
    ),
    encoding="utf-8",
)
print(len(out))
for sid, grade, name, master, tags, req, desc, icon, comment, changes in out:
    print(f"{sid}\t{tags}\t{name}\t{master}")
