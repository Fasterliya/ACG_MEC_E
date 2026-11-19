# -*- coding: utf-8 -*-
"""
提瓦特主神条构建脚本
- 裁切 10 张源图 -> 41x41
- 读取母 Mod 的 hindu_deities_strip.dds（738x41 / 18 帧）
- 右侧追加 10 帧 -> 1148x41 / 28 帧
- 以母 Mod 文件 header 为模板写未压缩 A8R8G8B8 DDS（含 mip 链）
- 回读校验 + 生成预览图
"""
import os
import struct

from PIL import Image, ImageDraw

MOD = r"F:\Paradox Interactive\Europa Universalis IV\mod\ACG_MEC_E"
ACG1 = r"F:\SteamLibrary\steamapps\workshop\content\236850\2796854877"
SRC = r"F:\SITU\东方风云设计理念\政府改革\ACG风云立绘\新建文件夹"
SRC_ELEM = os.path.join(SRC, "七元素切图_128", "透明底_增强+")

FRAME = 41
FIRST_SPRITE = 19

ORDER = [
    ("acg_mec_e_deity_barbatos", os.path.join(SRC_ELEM, "风.png")),
    ("acg_mec_e_deity_morax", os.path.join(SRC_ELEM, "岩.png")),
    ("acg_mec_e_deity_baal", os.path.join(SRC_ELEM, "雷.png")),
    ("acg_mec_e_deity_buer", os.path.join(SRC_ELEM, "草.png")),
    ("acg_mec_e_deity_focalors", os.path.join(SRC_ELEM, "水.png")),
    ("acg_mec_e_deity_mavuika", os.path.join(SRC_ELEM, "火.png")),
    ("acg_mec_e_deity_washajia", os.path.join(SRC_ELEM, "冰.png")),
    ("acg_mec_e_deity_hengyue", os.path.join(SRC, "恒月.png")),
    ("acg_mec_e_deity_hongyue", os.path.join(SRC, "虹月.png")),
    ("acg_mec_e_deity_shuangyue", os.path.join(SRC, "霜月.png")),
]

BASE_STRIP = os.path.join(ACG1, "gfx", "interface", "hindu_deities_strip.dds")
# Same filename as vanilla / ACG1: a mod file with an identical path replaces the original one.
OUT_STRIP = os.path.join(MOD, "gfx", "interface", "hindu_deities_strip.dds")
OUT_ICONS = os.path.join(MOD, "analysis", "teyvat_icons")
OUT_PREVIEW = os.path.join(OUT_ICONS, "_preview_strip.png")


def crop_square(im, size=FRAME):
    im = im.convert("RGBA")
    alpha = im.getchannel("A")
    mask = alpha.point(lambda v: 255 if v > 4 else 0)
    bbox = mask.getbbox()
    if bbox:
        im = im.crop(bbox)
    w, h = im.size
    side = max(w, h)
    canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    canvas.paste(im, ((side - w) // 2, (side - h) // 2))
    out = canvas.resize((size, size), Image.LANCZOS)
    # 去白边：透明像素 RGB 清零
    px = out.load()
    for y in range(size):
        for x in range(size):
            r, g, b, a = px[x, y]
            if a < 10:
                px[x, y] = (0, 0, 0, 0)
    return out


def dds_levels(im):
    levels = [im.convert("RGBA")]
    w, h = im.size
    while w > 1 or h > 1:
        w = max(1, w // 2)
        h = max(1, h // 2)
        levels.append(levels[-1].resize((w, h), Image.LANCZOS))
    return levels


def write_dds(path, im, template):
    header = bytearray(open(template, "rb").read()[:128])
    w, h = im.size
    levels = dds_levels(im)
    struct.pack_into("<I", header, 12, h)
    struct.pack_into("<I", header, 16, w)
    struct.pack_into("<I", header, 20, w * 4)
    struct.pack_into("<I", header, 28, len(levels))
    flags = struct.unpack_from("<I", header, 8)[0] | 0x20000
    struct.pack_into("<I", header, 8, flags)
    out = bytearray(header)
    for lv in levels:
        r, g, b, a = lv.split()
        out += Image.merge("RGBA", (b, g, r, a)).tobytes()
    with open(path, "wb") as f:
        f.write(out)
    return len(levels), len(out)


def main():
    os.makedirs(os.path.dirname(OUT_STRIP), exist_ok=True)
    os.makedirs(OUT_ICONS, exist_ok=True)

    base = Image.open(BASE_STRIP)
    base.load()
    base = base.convert("RGBA")
    assert base.size == (738, 41), base.size

    frames = []
    for i, (key, src) in enumerate(ORDER):
        if not os.path.exists(src):
            raise SystemExit("missing source: " + src)
        icon = crop_square(Image.open(src))
        icon.save(os.path.join(OUT_ICONS, "%02d_%s.png" % (FIRST_SPRITE + i, key)))
        frames.append((key, icon))

    total = base.size[0] + FRAME * len(frames)
    strip = Image.new("RGBA", (total, FRAME), (0, 0, 0, 0))
    strip.paste(base, (0, 0))
    for i, (key, icon) in enumerate(frames):
        strip.paste(icon, (base.size[0] + i * FRAME, 0))

    mips, size = write_dds(OUT_STRIP, strip, BASE_STRIP)

    # 回读校验
    rb = Image.open(OUT_STRIP)
    rb.load()
    ok_size = rb.size == (total, FRAME)
    diff_max = 0
    for i in range(12 + 6):
        left = base.crop((i * FRAME, 0, (i + 1) * FRAME, FRAME))
        right = rb.crop((i * FRAME, 0, (i + 1) * FRAME, FRAME)).convert("RGBA")
        if list(left.getdata()) != list(right.getdata()):
            diff_max += 1
    for i, (key, icon) in enumerate(frames):
        x = base.size[0] + i * FRAME
        right = rb.crop((x, 0, x + FRAME, FRAME)).convert("RGBA")
        if list(icon.getdata()) != list(right.getdata()):
            diff_max += 1

    # 预览图（3 倍放大 + 帧号网格）
    scale = 3
    prev = strip.resize((strip.size[0] * scale, FRAME * scale), Image.NEAREST)
    bg = Image.new("RGBA", prev.size, (28, 28, 32, 255))
    bg.alpha_composite(prev)
    d = ImageDraw.Draw(bg)
    for idx in range(28):
        x = idx * FRAME * scale
        d.line([(x, 0), (x, bg.size[1])], fill=(255, 0, 0, 160), width=1)
        d.text((x + 3, 2), str(idx + 1), fill=(255, 255, 0, 255))
    bg.save(OUT_PREVIEW)

    print("dds:", OUT_STRIP)
    print("size:", rb.size, "frames:", total // FRAME, "mips:", mips, "bytes:", size)
    print("mismatched frames:", diff_max)
    print("preview:", OUT_PREVIEW)


if __name__ == "__main__":
    main()
