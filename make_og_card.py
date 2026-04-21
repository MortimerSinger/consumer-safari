"""
Compose purpose-built 1200x630 OG card for The Digital Recoil.
"""

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps
import os

WORKSPACE = '/home/user/workspace/morning-briefing'
FONTS = '/home/user/workspace/fonts'

VIOLET_DARK = (76, 29, 149)
LAVENDER = (221, 214, 254)
TITLE_BLUE = (196, 181, 253)

cover = Image.open(os.path.join(WORKSPACE, 'digital-recoil-cover.jpg'))
cover_bw = ImageOps.grayscale(cover).convert('RGB')

OG_W, OG_H = 1200, 630

# Clean mural face region ONLY: y=130 to y=440 (above the title overlay baked into cover)
# This avoids TCP mark (y<120) and the title block overlay on the face (y>450)
face_region = cover_bw.crop((0, 130, 1080, 450))

# We want to fit this into a 780x630 panel on the right side of OG
# Face region aspect: 1080/440 = 2.45 (very landscape)
# Right panel aspect: 780/630 = 1.238
# Since face region is wider than we need, we can crop width instead of stretching

# Scale by HEIGHT to 630, width becomes 1546
scale = 630 / face_region.height
new_w = int(face_region.width * scale)
scaled = face_region.resize((new_w, 630), Image.LANCZOS)

# Now crop horizontally - face is roughly center (x=540 in original, x=540*scale in scaled)
right_w = 780
face_x_scaled = int(540 * scale)
# Center face in the 780 frame
crop_x = max(0, min(face_x_scaled - right_w // 2, scaled.width - right_w))
final_right = scaled.crop((crop_x, 0, crop_x + right_w, 630))

# Create canvas and paste
og = Image.new('RGB', (OG_W, OG_H), VIOLET_DARK)
og.paste(final_right, (OG_W - right_w, 0))

# Violet gradient panel on left with soft fade into image
panel_w = 520
panel = Image.new('RGBA', (panel_w, OG_H), (0, 0, 0, 0))
pdraw = ImageDraw.Draw(panel)
for x in range(panel_w):
    if x < 380:
        alpha = 255
    else:
        alpha = int(255 * (1 - (x - 380) / 140))
    pdraw.line([(x, 0), (x, OG_H)], fill=(VIOLET_DARK[0], VIOLET_DARK[1], VIOLET_DARK[2], alpha))

og = og.convert('RGBA')
og.paste(panel, (0, 0), panel)
og = og.convert('RGB')

# Text overlays
draw = ImageDraw.Draw(og)

font_title = ImageFont.truetype(os.path.join(FONTS, 'playfair-sc-bold.ttf'), 72)
font_subtitle = ImageFont.truetype(os.path.join(FONTS, 'playfair-sc.ttf'), 30)
font_byline_label = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 13)
font_byline = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 15)
font_mono = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 14)

# Top-left: TCP monogram text block
draw.text((55, 48), "TRAUB", fill=LAVENDER, font=font_mono)
draw.text((55, 68), "CAPITAL", fill=LAVENDER, font=font_mono)
draw.text((55, 88), "PARTNERS", fill=LAVENDER, font=font_mono)

# Title
title_y = 260
draw.text((55, title_y), "Digital Recoil", fill=LAVENDER, font=font_title)

# Subtitle
subtitle_y = title_y + 85
draw.text((55, subtitle_y), "& The Analog", fill=TITLE_BLUE, font=font_subtitle)
draw.text((55, subtitle_y + 40), "Enthusiast Economy", fill=TITLE_BLUE, font=font_subtitle)

# Byline
byline_y = OG_H - 80
draw.text((55, byline_y), "CONSUMER SIGNAL SERIES · PAPER No. 01", fill=TITLE_BLUE, font=font_byline_label)
draw.text((55, byline_y + 24), "Mortimer Singer · Traub Capital Partners · April 2026", fill=(255, 255, 255), font=font_byline)

output_path = os.path.join(WORKSPACE, 'digital-recoil-og.jpg')
og.save(output_path, 'JPEG', quality=92, optimize=True)
size_kb = os.path.getsize(output_path) / 1024
print(f"Saved: {output_path}, {OG_W}x{OG_H}, {size_kb:.1f}KB")
