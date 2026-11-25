# -*- coding: utf-8 -*-
import urllib.request
from pathlib import Path

base = "https://artale.live"
out = Path(r"d:\skill\icons\archmage-fp")
out.mkdir(parents=True, exist_ok=True)
files = {
    "fp_mp_inc": "/assets/balance-patch/icons/2000001.png",
    "fp_poison_master1": "/assets/balance-patch/icons/game/2100001.png",
    "fp_fire_arrow": "/assets/balance-patch-v2/icons/2101004.png",
    "fp_poison_breath": "/assets/balance-patch-v2/icons/2101005.png",
    "fp_element_amp": "/assets/balance-patch-v2/icons/2110001.png",
    "fp_poison_master2": "/assets/balance-patch/icons/game/2110002.png",
    "fp_explosion": "/assets/balance-patch-v2/icons/2111002.png",
    "fp_poison_mist": "/assets/balance-patch-v2/icons/2111003.png",
    "fp_magic_comp": "/assets/balance-patch-v2/icons/2111006.png",
    "fp_poison_master3": "/assets/balance-patch/icons/game/2120000.png",
    "fp_big_bang": "/assets/balance-patch-v2/icons/2121001.png",
    "fp_fire_demon": "/assets/balance-patch-v2/icons/2121003.png",
    "fp_paralyze": "/assets/balance-patch-v2/icons/2121006.png",
    "fp_meteor": "/assets/balance-patch-v2/icons/2121007.png",
}
for name, path in files.items():
    dest = out / f"{name}.png"
    urllib.request.urlretrieve(base + path, str(dest))
    data = dest.read_bytes()
    print(name, len(data), data[:8])
