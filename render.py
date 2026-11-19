"""Renderer poster berita 19 Nov 2026 (Pillow, hanya saat build).

Satu fungsi publik: render_image(path) -> (width, height).
Deterministik: tanpa network, tanpa jam, tanpa acak — koordinat dan
font tetap, dua run menulis byte yang identik.
Ilustrasi bergaya kartun editorial / siluet — tanpa wajah fotorealistis
tokoh nyata (tiga pemimpin hanya siluet di meja bundar + bendera).
Semua teks diukur dulu dengan textlength, jadi tidak ada teks yang
keluar kanvas atau menumpuk.
"""

import os

from PIL import Image, ImageDraw, ImageFont

import layout
import news_data


def _font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except (OSError, IOError):
        return ImageFont.load_default()


def _fit_font(draw, text, path, start_size, max_width, min_size=18):
    """Perkecil font sampai teks muat dalam max_width."""
    size = start_size
    while size > min_size:
        font = _font(path, size)
        if draw.textlength(text, font=font) <= max_width:
            return font
        size -= 2
    return _font(path, min_size)


def _flag_us(draw, x, y, w=44, h=28):
    for i in range(5):
        draw.rectangle(
            [x, y + i * h // 5, x + w, y + (i + 1) * h // 5],
            fill=(178, 34, 34) if i % 2 == 0 else (255, 255, 255),
        )
    draw.rectangle([x, y, x + w * 0.45, y + h * 0.55], fill=(30, 50, 110))


def _flag_cn(draw, x, y, w=44, h=28):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 40, 40))
    draw.ellipse([x + 6, y + 5, x + 18, y + 17], fill=(255, 220, 60))


def _flag_ru(draw, x, y, w=44, h=28):
    for i, col in enumerate(((255, 255, 255), (30, 70, 180), (200, 40, 40))):
        draw.rectangle(
            [x, y + i * h // 3, x + w, y + (i + 1) * h // 3], fill=col
        )


# ---------------------------------------------------------------- ilustrasi
def _draw_summit(draw, x, y, w, h):
    """Meja bundar KTT: tiga siluet + tiga bendera, skyline Shenzhen."""
    draw.rectangle([x, y, x + w, y + h], fill=layout.SKY_DAY)
    # skyline Shenzhen: menara-menara gelap
    towers = [(0.04, 0.42, 0.10), (0.16, 0.30, 0.12), (0.30, 0.48, 0.09),
              (0.68, 0.34, 0.11), (0.82, 0.44, 0.10)]
    for fx, fh, fw in towers:
        tx = x + int(w * fx)
        th = int(h * fh)
        tw = int(w * fw)
        draw.rectangle([tx, y + h - th - 96, tx + tw, y + h - 96],
                       fill=(96, 116, 140))
    draw.rectangle([x, y + h - 96, x + w, y + h], fill=(58, 64, 74))
    # spanduk APEC
    draw.rectangle([x + 14, y + 12, x + 118, y + 40], fill=layout.NAVY)
    draw.text((x + 66, y + 26), "APEC 2026",
              font=_font(layout.FONT_SANS_BOLD, 18),
              fill=(255, 255, 255), anchor="mm")
    # tiga siluet duduk di belakang meja bundar
    table_y = y + h - 34
    for i, (fx, suit, tie) in enumerate((
        (0.22, (28, 28, 34), (178, 34, 34)),
        (0.50, (34, 34, 40), (30, 60, 140)),
        (0.78, (30, 30, 36), (200, 40, 40)),
    )):
        sx = x + int(w * fx)
        head_y = table_y - 118
        draw.ellipse([sx - 16, head_y, sx + 16, head_y + 32],
                     fill=(232, 196, 160))
        draw.rounded_rectangle(
            [sx - 30, head_y + 30, sx + 30, table_y + 6],
            radius=12, fill=suit,
        )
        draw.polygon(
            [(sx - 5, head_y + 32), (sx + 5, head_y + 32), (sx, head_y + 58)],
            fill=tie,
        )
    # meja bundar
    draw.ellipse([x + 24, table_y, x + w - 24, table_y + 34],
                 fill=(96, 58, 32))
    draw.ellipse([x + 24, table_y, x + w - 24, table_y + 16],
                 fill=(128, 78, 44))
    # tiga bendera kecil di depan meja (satu di bawah tiap kursi)
    for fx, flag in ((0.22, _flag_us), (0.50, _flag_cn), (0.78, _flag_ru)):
        flag(draw, x + int(w * fx) - 18, table_y + 8, 36, 22)


def _draw_hague(draw, x, y, w, h):
    """Peace Palace Den Haag + timbangan keadilan."""
    draw.rectangle([x, y, x + w, y + h], fill=layout.SKY_DAY)
    base_y = y + h - 26
    # gedung utama + menara
    draw.rectangle([x + 30, base_y - 52, x + w - 30, base_y],
                   fill=(196, 172, 132))
    draw.polygon(
        [(x + 30, base_y - 52), (x + w - 30, base_y - 52),
         (x + w - 62, base_y - 78), (x + 62, base_y - 78)],
        fill=(150, 60, 50),
    )
    draw.rectangle([x + w // 2 - 14, base_y - 108, x + w // 2 + 14, base_y - 72],
                   fill=(176, 150, 110))
    draw.polygon(
        [(x + w // 2 - 18, base_y - 108), (x + w // 2 + 18, base_y - 108),
         (x + w // 2, base_y - 132)],
        fill=(150, 60, 50),
    )
    # jendela lengkung (lewati dua di tengah: tempat timbangan)
    for wx in range(x + 44, x + w - 44, 34):
        if abs((wx + 8) - (x + w // 2)) < 48:
            continue
        draw.rounded_rectangle([wx, base_y - 40, wx + 16, base_y - 10],
                               radius=6, fill=layout.NAVY)
    # timbangan keadilan di depan gedung
    cx = x + w // 2
    cy = base_y - 6
    draw.line([cx, cy - 44, cx, cy], fill=(60, 48, 20), width=4)
    draw.line([cx - 34, cy - 44, cx + 34, cy - 44], fill=(60, 48, 20), width=3)
    for sx in (cx - 34, cx + 34):
        draw.line([sx, cy - 44, sx, cy - 22], fill=(60, 48, 20), width=2)
        draw.polygon([(sx - 14, cy - 22), (sx + 14, cy - 22), (sx, cy - 8)],
                     fill=(255, 205, 80))
    draw.ellipse([cx - 5, cy - 52, cx + 5, cy - 42], fill=(255, 205, 80))


def _draw_hormuz(draw, x, y, w, h):
    """Tanker terbakar + ranjau di Selat Hormuz."""
    draw.rectangle([x, y, x + w, y + h], fill=layout.SKY_DAY)
    sea_y = y + int(h * 0.58)
    draw.rectangle([x, sea_y, x + w, y + h], fill=layout.SEA)
    # matahari redup berasap
    draw.ellipse([x + w - 62, y + 12, x + w - 22, y + 52], fill=(255, 214, 90))
    # tanker: lambung + anjungan
    hx, hy = x + 18, sea_y + 8
    draw.polygon(
        [(hx, hy), (hx + 190, hy), (hx + 176, hy + 26), (hx + 12, hy + 26)],
        fill=(28, 28, 34),
    )
    draw.rectangle([hx + 140, hy - 22, hx + 172, hy], fill=(240, 240, 244))
    draw.rectangle([hx + 20, hy - 8, hx + 60, hy], fill=(200, 60, 60))
    # api di geladak
    draw.polygon(
        [(hx + 76, hy - 2), (hx + 88, hy - 34), (hx + 100, hy - 2)],
        fill=layout.FLAME,
    )
    draw.polygon(
        [(hx + 96, hy - 2), (hx + 106, hy - 26), (hx + 116, hy - 2)],
        fill=layout.FLAME_YELLOW,
    )
    # asap
    draw.ellipse([hx + 78, hy - 52, hx + 100, hy - 34], fill=(120, 120, 124))
    draw.ellipse([hx + 96, hy - 62, hx + 116, hy - 44], fill=(140, 140, 144))
    # ranjau laut berduri
    mx, my = x + w - 72, sea_y + 26
    for ang in range(0, 360, 45):
        import math
        dx = int(13 * math.cos(math.radians(ang)))
        dy = int(13 * math.sin(math.radians(ang)))
        draw.line([mx, my, mx + dx, my + dy], fill=(20, 20, 26), width=3)
    draw.ellipse([mx - 9, my - 9, mx + 9, my + 9], fill=(20, 20, 26))
    # kapal perang kecil di kejauhan
    wx, wy = x + 16, sea_y - 34
    draw.rectangle([wx, wy, wx + 64, wy + 10], fill=(70, 72, 78))
    draw.rectangle([wx + 14, wy - 12, wx + 30, wy], fill=(70, 72, 78))


def _draw_ukraine(draw, x, y, w, h):
    """Langit malam Kyiv: drone + Jembatan Kerch dengan rel putus."""
    draw.rectangle([x, y, x + w, y + h], fill=layout.SKY_NIGHT)
    # bintang
    for sx, sy in ((0.12, 0.14), (0.30, 0.08), (0.55, 0.18), (0.78, 0.10),
                   (0.90, 0.22), (0.42, 0.26)):
        draw.ellipse([x + int(w * sx), y + int(h * sy),
                      x + int(w * sx) + 3, y + int(h * sy) + 3],
                     fill=(255, 255, 255))
    # dua drone quad kecil
    for dx, dy in ((x + 44, y + 22), (x + 128, y + 34)):
        draw.line([dx - 9, dy - 7, dx + 9, dy + 7], fill=(220, 220, 224), width=3)
        draw.line([dx - 9, dy + 7, dx + 9, dy - 7], fill=(220, 220, 224), width=3)
        draw.rectangle([dx - 4, dy - 3, dx + 4, dy + 3], fill=(255, 205, 80))
    # skyline Kyiv gelap
    base_y = y + h - 30
    for fx, fh, fw in ((0.06, 0.20, 0.12), (0.24, 0.30, 0.10),
                       (0.62, 0.24, 0.12), (0.80, 0.32, 0.11)):
        bx = x + int(w * fx)
        draw.rectangle([bx, base_y - int(h * fh), bx + int(w * fw), base_y],
                       fill=(40, 48, 72))
    # Jembatan Kerch: bentang rel dengan celah putus di tengah
    by = base_y - 6
    draw.rectangle([x + 12, by, x + 118, by + 8], fill=(200, 200, 204))
    draw.polygon(
        [(x + 168, by - 14), (x + 190, by - 14), (x + 186, by + 8),
         (x + 172, by + 8)],
        fill=(232, 116, 28),
    )
    draw.rectangle([x + 196, by, x + w - 12, by + 8], fill=(200, 200, 204))
    # tiang jembatan
    for px in (x + 40, x + 150, x + 226):
        draw.rectangle([px, by + 8, px + 8, base_y + 26], fill=(150, 150, 156))
    # percikan api di celah
    draw.polygon(
        [(x + 178, by - 14), (x + 184, by - 30), (x + 190, by - 14)],
        fill=layout.FLAME_YELLOW,
    )


def _draw_cyclone(draw, x, y, w, h):
    """Pusaran siklon di Teluk Benggala menuju pantai India."""
    draw.rectangle([x, y, x + w, y + h], fill=(24, 68, 120))
    # daratan India di kanan
    draw.polygon(
        [(x + w - 52, y), (x + w, y), (x + w, y + h),
         (x + w - 66, y + h), (x + w - 78, y + int(h * 0.55)),
         (x + w - 58, y + int(h * 0.30))],
        fill=layout.LEAF,
    )
    # pusaran: busur konsentris putih
    cx, cy = x + int(w * 0.42), y + int(h * 0.52)
    for r, wd in ((58, 7), (44, 7), (30, 7), (16, 6)):
        draw.arc(
            [cx - r, cy - r, cx + r, cy + r],
            start=20, end=300, fill=(255, 255, 255), width=wd,
        )
    draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=layout.GOLD)
    # panah ke daratan (landfall Friday)
    ay = cy + 6
    draw.line([cx + 62, ay, x + w - 72, ay], fill=layout.GOLD, width=5)
    draw.polygon(
        [(x + w - 72, ay), (x + w - 88, ay - 9), (x + w - 88, ay + 9)],
        fill=layout.GOLD,
    )


ART = {
    "summit": _draw_summit,
    "hague": _draw_hague,
    "hormuz": _draw_hormuz,
    "ukraine": _draw_ukraine,
    "cyclone": _draw_cyclone,
}


# ---------------------------------------------------------------- render utama
def render_image(out_path):
    img = Image.new("RGB", (layout.W, layout.H), layout.PAPER)
    draw = ImageDraw.Draw(img)

    # --- Header navy: tanggal BESAR dulu, lalu judul ---
    draw.rectangle([0, 0, layout.W, layout.HEADER_H], fill=layout.NAVY)
    draw.rectangle(
        [0, layout.HEADER_H - 6, layout.W, layout.HEADER_H], fill=layout.RED
    )
    date_font = _font(layout.FONT_SANS_BOLD, 40)
    title_font = _fit_font(
        draw, news_data.TITLE, layout.FONT_SERIF_BOLD,
        62, layout.W - 2 * layout.MARGIN,
    )
    sub_font = _font(layout.FONT_SANS, 25)

    y = 14
    draw.text(
        (layout.W / 2, y), news_data.DATE_LINE, font=date_font,
        fill=layout.GOLD, anchor="ma",
    )
    y += 52
    draw.text(
        (layout.W / 2, y), news_data.TITLE, font=title_font,
        fill=(255, 255, 255), anchor="ma",
    )
    y += 72
    draw.text(
        (layout.W / 2, y), news_data.SUBTITLE, font=sub_font,
        fill=(214, 222, 240), anchor="ma",
    )

    # --- Panel hero: seni kiri, teks kanan ---
    x0 = layout.MARGIN
    card_w = layout.W - 2 * layout.MARGIN
    hy = layout.HERO_TOP
    draw.rounded_rectangle(
        [x0, hy, x0 + card_w, hy + layout.HERO_H],
        radius=12, fill=layout.CARD_BG,
        outline=layout.CARD_BORDER, width=2,
    )
    art_w = 400
    ART[news_data.HERO["art"]](draw, x0 + 2, hy + 2, art_w - 2, layout.HERO_H - 4)
    tx = x0 + art_w + 26
    tw = card_w - art_w - 52
    tag_font = _font(layout.FONT_SANS_BOLD, 24)
    head_font = _font(layout.FONT_SERIF_BOLD, 38)
    body_font = _font(layout.FONT_SANS, 26)
    ty = hy + 24
    draw.text((tx, ty), news_data.HERO["tag"], font=tag_font, fill=layout.RED)
    ty += 38
    for line in layout.wrap_text(draw, news_data.HERO["headline"], head_font, tw)[:2]:
        draw.text((tx, ty), line, font=head_font, fill=layout.INK)
        ty += 46
    ty += 8
    for line in layout.wrap_text(draw, news_data.HERO["body"], body_font, tw)[:3]:
        draw.text((tx, ty), line, font=body_font, fill=layout.MUTED)
        ty += 35

    # --- Baris 3 panel ---
    pw = 306
    ptag_font = _font(layout.FONT_SANS_BOLD, 21)
    phead_font = _font(layout.FONT_SERIF_BOLD, 27)
    pbody_font = _font(layout.FONT_SANS, 21)
    for i, panel in enumerate(news_data.PANELS):
        px = x0 + i * (pw + layout.GUTTER)
        py = layout.ROW_TOP
        draw.rounded_rectangle(
            [px, py, px + pw, py + layout.ROW_H],
            radius=12, fill=layout.CARD_BG,
            outline=layout.CARD_BORDER, width=2,
        )
        ART[panel["art"]](draw, px + 2, py + 2, pw - 4, 96)
        ty = py + 102
        draw.text((px + 18, ty), panel["tag"], font=ptag_font, fill=layout.RED)
        ty += 28
        for line in layout.wrap_text(
            draw, panel["headline"], phead_font, pw - 36
        )[:2]:
            draw.text((px + 18, ty), line, font=phead_font, fill=layout.INK)
            ty += 32
        ty += 2
        for line in layout.wrap_text(
            draw, panel["body"], pbody_font, pw - 36
        )[:4]:
            draw.text((px + 18, ty), line, font=pbody_font, fill=layout.MUTED)
            ty += 25

    # --- Strip bawah: dua kolom (Akvan + GTA VI) ---
    sy = layout.STRIP_TOP
    draw.rounded_rectangle(
        [x0, sy, x0 + card_w, sy + layout.STRIP_H],
        radius=12, fill=layout.CARD_BG,
        outline=layout.CARD_BORDER, width=2,
    )
    stag_font = _font(layout.FONT_SANS_BOLD, 21)
    sbody_font = _font(layout.FONT_SANS, 22)
    col_w = (card_w - 60) // 2
    for i, (tag, text) in enumerate(news_data.STRIP):
        cx = x0 + 24 + i * (col_w + 36)
        if i == 1:
            draw.line(
                [cx - 18, sy + 16, cx - 18, sy + layout.STRIP_H - 16],
                fill=layout.RULE, width=2,
            )
        ty = sy + 15
        draw.text((cx, ty), tag, font=stag_font, fill=layout.RED)
        ty += 32
        for line in layout.wrap_text(draw, text, sbody_font, col_w)[:2]:
            draw.text((cx, ty), line, font=sbody_font, fill=layout.MUTED)
            ty += 27

    # --- Footer ---
    foot_font = _font(layout.FONT_SANS, 21)
    draw.text(
        (layout.W / 2, layout.FOOTER_Y), news_data.FOOTER,
        font=foot_font, fill=layout.MUTED, anchor="ma",
    )

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    img.save(out_path, "PNG")
    return img.size


if __name__ == "__main__":
    import sys

    target = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    print("rendered", target, render_image(target))
