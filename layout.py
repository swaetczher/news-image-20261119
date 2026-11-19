"""Konstanta layout + pembungkus teks untuk poster berita 19 Nov 2026.

Kanvas 1024 x 1024 (batas keras kompetisi: maks 1024x1024 px, <=1 MiB).
Syarat juri: terbaca di lebar ~300 px — font tubuh minimal 22 px,
headline panel minimal 27 px, tanggal dan judul jauh lebih besar.
Semua teks dibungkus berdasarkan lebar piksel nyata (Pillow textlength),
bukan perkiraan jumlah karakter.
"""

W, H = 1024, 1024
MARGIN = 36
GUTTER = 16

# Palet poster koran: navy pekat + emas + merah bata + kertas hangat
NAVY = (10, 25, 60)
NAVY_MID = (22, 44, 92)
GOLD = (255, 205, 80)
RED = (190, 30, 30)
PAPER = (248, 246, 240)
INK = (20, 20, 24)
MUTED = (84, 84, 92)
RULE = (204, 200, 190)
CARD_BG = (255, 255, 255)
CARD_BORDER = (220, 216, 208)

# Warna ilustrasi
SKY_DAY = (168, 204, 232)
SKY_NIGHT = (18, 32, 66)
SEA = (44, 90, 138)
SEA_DEEP = (28, 64, 106)
FLAME = (232, 116, 28)
FLAME_YELLOW = (244, 178, 44)
LEAF = (72, 128, 80)

# Font (DejaVu tersedia di VM; fallback ke font default Pillow)
FONT_SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT_SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# Geometri vertikal poster
HEADER_H = 188
HERO_TOP = HEADER_H + 14
HERO_H = 300
ROW_TOP = HERO_TOP + HERO_H + GUTTER
ROW_H = 300
STRIP_TOP = ROW_TOP + ROW_H + GUTTER
STRIP_H = 104
FOOTER_Y = H - 46


def wrap_text(draw, text, font, max_width):
    """Bungkus teks menjadi baris-baris yang muat dalam max_width piksel."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines
