"""
Telcoin — 30-Second Commercial: "What 6 Percent Costs"
Motion graphics video production script.
Renders to: design/output/telcoin-30s-what-6-percent-costs.mp4

Brand colors:
  Background: #0A0E1A  (10, 14, 26)
  Blue:       #0047FF  (0, 71, 255)
  Cyan:       #00D4FF  (0, 212, 255)
  White:      #FFFFFF  (255, 255, 255)
  Light gray: #B0B8C8  (176, 184, 200)
  Gold:       #C9A227  (201, 162, 39)
"""

import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ─── CONFIG ──────────────────────────────────────────────────────────────────
W, H = 1920, 1080
FPS = 24
DURATION = 30.0
TOTAL_FRAMES = int(FPS * DURATION)

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_FILE = os.path.join(OUT_DIR, "telcoin-30s-what-6-percent-costs.mp4")

# Fonts
FONT_DIR = "/usr/share/fonts/truetype/liberation"
FONT_REG  = os.path.join(FONT_DIR, "LiberationSans-Regular.ttf")
FONT_BOLD = os.path.join(FONT_DIR, "LiberationSans-Bold.ttf")

# ─── COLORS ──────────────────────────────────────────────────────────────────
BG    = (10, 14, 26)
BLUE  = (0, 71, 255)
CYAN  = (0, 212, 255)
WHITE = (255, 255, 255)
GRAY  = (176, 184, 200)
GOLD  = (201, 162, 39)
BLACK = (0, 0, 0)
RED_MUTED = (180, 60, 60)
GREEN_SOFT = (50, 200, 120)

# ─── FONT CACHE ──────────────────────────────────────────────────────────────
_font_cache = {}

def font(size, bold=False):
    key = (size, bold)
    if key not in _font_cache:
        path = FONT_BOLD if bold else FONT_REG
        _font_cache[key] = ImageFont.truetype(path, size)
    return _font_cache[key]


# ─── HELPERS ─────────────────────────────────────────────────────────────────

def eased(t, ease="inout"):
    """Normalize t to [0,1] with easing."""
    t = max(0.0, min(1.0, t))
    if ease == "in":
        return t * t
    elif ease == "out":
        return 1 - (1 - t) ** 2
    elif ease == "inout":
        if t < 0.5:
            return 2 * t * t
        return 1 - (-2 * t + 2) ** 2 / 2
    return t

def lerp(a, b, t):
    return a + (b - a) * t

def lerp_color(c1, c2, t):
    return tuple(int(lerp(a, b, t)) for a, b in zip(c1, c2))

def alpha_composite(base, overlay_color, alpha):
    """Blend overlay_color onto base with alpha [0..1]."""
    return lerp_color(base, overlay_color, max(0.0, min(1.0, alpha)))

def new_frame():
    return Image.new("RGB", (W, H), BG)

def text_center(draw, text, y, f, color=WHITE, anchor="mm"):
    draw.text((W // 2, y), text, font=f, fill=color, anchor=anchor)

def text_at(draw, text, x, y, f, color=WHITE, anchor="la"):
    draw.text((x, y), text, font=f, fill=color, anchor=anchor)

def fade_img(img, alpha):
    """Fade image toward black."""
    if alpha >= 1.0:
        return img
    overlay = Image.new("RGB", img.size, BLACK)
    return Image.blend(img, overlay, 1.0 - alpha)

def draw_rounded_rect(draw, x0, y0, x1, y1, r, fill=None, outline=None, width=2):
    draw.rounded_rectangle([x0, y0, x1, y1], radius=r, fill=fill, outline=outline, width=width)

def glow_dot(img, cx, cy, r, color, intensity=1.0):
    """Draw a glowing dot using compositing."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    # Outer glow
    for i in range(4, 0, -1):
        alpha = int(40 * intensity * (5 - i) / 4)
        d.ellipse([cx - r * i, cy - r * i, cx + r * i, cy + r * i],
                  fill=(*color, alpha))
    # Core dot
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*color, int(255 * intensity)))
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")

def draw_line_animated(img, x1, y1, x2, y2, progress, color, width=2):
    """Draw a line up to `progress` (0-1)."""
    if progress <= 0:
        return img
    px = int(x1 + (x2 - x1) * progress)
    py = int(y1 + (y2 - y1) * progress)
    draw = ImageDraw.Draw(img)
    draw.line([x1, y1, px, py], fill=color, width=width)
    return img


# ─── WORLD MAP DATA ───────────────────────────────────────────────────────────
# Simplified continent outlines as lat/lon polygon tuples
# Format: list of (lon, lat) points
CONTINENTS = {
    "north_america": [
        (-168,72),(-140,70),(-100,72),(-85,65),(-55,50),(-52,47),
        (-65,44),(-70,41),(-75,35),(-80,25),(-87,15),(-83,8),(-78,8),
        (-75,10),(-70,12),(-62,10),(-60,8),(-62,4),(-75,0),(-78,2),
        (-80,5),(-83,10),(-90,14),(-92,16),(-95,16),(-97,20),(-105,20),
        (-117,32),(-120,34),(-124,38),(-125,48),(-130,55),(-140,60),
        (-150,60),(-155,58),(-160,58),(-165,60),(-170,63),(-168,72)
    ],
    "south_america": [
        (-80,12),(-75,12),(-68,12),(-62,12),(-52,5),(-50,2),(-48,0),
        (-50,-5),(-38,-5),(-35,-8),(-35,-14),(-38,-20),(-40,-22),
        (-43,-23),(-44,-28),(-50,-29),(-52,-33),(-54,-35),(-58,-38),
        (-62,-42),(-65,-46),(-66,-50),(-68,-55),(-68,-55),(-68,-56),
        (-70,-55),(-72,-50),(-72,-45),(-70,-40),(-72,-30),(-70,-18),
        (-76,-14),(-78,-8),(-80,-2),(-80,5),(-80,12)
    ],
    "europe": [
        (-10,36),(-5,36),(5,36),(15,38),(22,37),(28,38),(30,42),
        (28,45),(30,48),(28,52),(22,55),(18,57),(15,58),(12,58),
        (8,57),(5,56),(3,53),(2,52),(0,50),(-2,48),(-5,44),
        (-8,42),(-10,38),(-10,36)
    ],
    "africa": [
        (-18,16),(-15,12),(-15,8),(-10,5),(-5,5),(-2,4),(4,5),
        (8,4),(10,2),(12,0),(14,-4),(16,-6),(20,-10),(24,-16),
        (28,-22),(30,-26),(32,-30),(30,-34),(26,-34),(22,-32),
        (18,-28),(16,-22),(14,-16),(12,-8),(8,-4),(2,0),(-2,4),
        (-2,8),(0,14),(2,18),(4,22),(8,24),(10,22),(14,22),
        (14,18),(16,14),(12,12),(8,14),(4,15),(0,15),(-4,14),
        (-8,14),(-12,14),(-16,14),(-18,16)
    ],
    "asia": [
        (26,72),(40,72),(60,70),(80,68),(100,68),(120,68),(140,68),
        (145,60),(145,52),(140,46),(136,42),(130,35),(126,32),(122,28),
        (120,22),(110,18),(105,12),(100,8),(100,2),(104,1),(108,2),
        (112,4),(118,4),(122,6),(125,8),(130,30),(134,34),(136,36),
        (130,42),(130,46),(134,50),(136,52),(134,56),(130,60),
        (120,62),(110,66),(100,68),(90,68),(80,68),(70,65),(60,62),
        (50,60),(40,56),(35,50),(30,48),(28,46),(30,42),(35,38),
        (38,36),(40,36),(42,36),(50,30),(60,22),(62,22),(64,24),
        (66,26),(68,24),(70,20),(72,22),(76,22),(80,10),(82,8),
        (84,4),(80,2),(72,4),(68,8),(64,8),(60,22),(52,24),
        (48,28),(42,36),(38,38),(30,42),(26,40),(26,36),(26,72)
    ],
    "australia": [
        (114,-22),(118,-20),(122,-18),(126,-16),(130,-12),(136,-12),
        (140,-14),(144,-14),(148,-18),(152,-22),(152,-28),(150,-32),
        (148,-36),(146,-38),(142,-38),(138,-36),(136,-34),(132,-34),
        (128,-32),(124,-28),(118,-26),(116,-24),(114,-22)
    ],
}

def lonlat_to_xy(lon, lat, mx, my, mw, mh):
    """Convert lon/lat to pixel coordinates within a map bounding box."""
    x = mx + (lon + 180) / 360.0 * mw
    y = my + (90 - lat) / 180.0 * mh
    return int(x), int(y)

# Remittance corridor cities: (name, lon, lat)
CITIES = [
    ("Manila",         121.0,  14.6),
    ("Dhaka",           90.4,  23.7),
    ("Nairobi",         36.8,  -1.3),
    ("Karachi",         67.0,  24.9),
    ("Jakarta",        106.8,  -6.2),
    ("Guatemala City", -90.5,  14.6),
]
HUB = ("New York", -74.0, 40.7)


# ─── SCENE RENDERERS ─────────────────────────────────────────────────────────

def render_scene1_hook(t):
    """0-3s: Dark hook — time + phone fee establishing."""
    img = new_frame()
    draw = ImageDraw.Draw(img)

    fade_in = eased(t / 0.8, "out")
    scene_alpha = 1.0 if t > 2.5 else fade_in

    # Subtle background texture — faint grid
    for gx in range(0, W, 80):
        a = int(12 * scene_alpha)
        draw.line([(gx, 0), (gx, H)], fill=(20, 28, 50, a), width=1)
    for gy in range(0, H, 80):
        a = int(12 * scene_alpha)
        draw.line([(0, gy), (W, gy)], fill=(20, 28, 50, a), width=1)

    # Time stamp — like a phone screen
    time_alpha = eased((t - 0.3) / 0.6, "out") if t > 0.3 else 0
    if time_alpha > 0:
        time_color = alpha_composite(BG, GRAY, time_alpha)
        # Small label
        draw.text((W // 2, 340), "17:47", font=font(96, bold=True),
                  fill=alpha_composite(BG, WHITE, time_alpha), anchor="mm")
        draw.text((W // 2, 420), "End of shift.", font=font(28),
                  fill=alpha_composite(BG, GRAY, time_alpha), anchor="mm")

    # Fee card — appears at t=1.2
    card_alpha = eased((t - 1.2) / 0.7, "out") if t > 1.2 else 0
    if card_alpha > 0:
        # Dim card
        cx, cy = W // 2, 600
        cw, ch = 480, 140
        card_bg = alpha_composite(BG, (18, 24, 44), card_alpha)
        draw_rounded_rect(draw, cx - cw // 2, cy - ch // 2,
                          cx + cw // 2, cy + ch // 2,
                          r=12, fill=card_bg,
                          outline=alpha_composite(BG, (40, 50, 80), card_alpha),
                          width=1)
        # Fee line — traditional app
        fa = alpha_composite(BG, GRAY, card_alpha * 0.7)
        draw.text((cx, cy - 28), "Transfer $200.00", font=font(22),
                  fill=alpha_composite(BG, GRAY, card_alpha), anchor="mm")
        # Fee amount — the gut punch
        fee_color = alpha_composite(BG, (200, 80, 80), card_alpha)
        draw.text((cx - 60, cy + 10), "Fee:", font=font(24),
                  fill=alpha_composite(BG, GRAY, card_alpha), anchor="lm")
        draw.text((cx + 60, cy + 10), "$12.50", font=font(28, bold=True),
                  fill=fee_color, anchor="rm")
        draw.text((cx, cy + 46), "Traditional transfer", font=font(18),
                  fill=alpha_composite(BG, (120, 130, 150), card_alpha), anchor="mm")

    # Fade to next scene
    if t > 2.5:
        fade_out = eased((t - 2.5) / 0.5, "in")
        img = fade_img(img, 1.0 - fade_out)

    return img


def render_scene2_problem(t):
    """3-10s: Problem stat card — 6.3%, $19 math."""
    # t here is local time within scene (0 to 7s)
    img = new_frame()
    draw = ImageDraw.Draw(img)

    fade_in = eased(t / 0.4, "out")

    # ── Big percentage number ──
    pct_appear = eased(t / 0.6, "out")

    # Animated number count-up for percentage (0 → 6.3%)
    if t < 0.8:
        pct_val = lerp(0.0, 6.3, eased(t / 0.8, "out"))
    else:
        pct_val = 6.3

    pct_text = f"{pct_val:.1f}%"

    # Large stat — centered upper
    pct_color = alpha_composite(BG, WHITE, pct_appear)
    draw.text((W // 2, 340), pct_text, font=font(180, bold=True),
              fill=pct_color, anchor="mm")

    # Underline in cyan
    if pct_appear > 0.1:
        line_w = int(320 * min(1.0, (pct_appear - 0.1) / 0.4))
        lx = W // 2 - line_w // 2
        draw.line([(lx, 455), (lx + line_w, 455)], fill=CYAN, width=3)

    # Source label
    src_alpha = eased((t - 0.5) / 0.5, "out") if t > 0.5 else 0
    if src_alpha > 0:
        draw.text((W // 2, 500), "World Bank global average per remittance transfer",
                  font=font(26), fill=alpha_composite(BG, GRAY, src_alpha), anchor="mm")

    # ── Second card: $19 math ── appears at t=2.5
    card_alpha = eased((t - 2.5) / 0.6, "out") if t > 2.5 else 0
    if card_alpha > 0:
        # Card background
        cx, cy = W // 2, 700
        cw, ch = 720, 140
        draw_rounded_rect(draw, cx - cw // 2, cy - ch // 2,
                          cx + cw // 2, cy + ch // 2,
                          r=16,
                          fill=alpha_composite(BG, (14, 20, 42), card_alpha),
                          outline=alpha_composite(BG, (30, 50, 100), card_alpha),
                          width=1)

        # Dollar amount — count up
        if t < 3.5:
            dollar_val = lerp(0, 19, eased((t - 2.5) / 1.0, "out"))
        else:
            dollar_val = 19

        dollar_text = f"${dollar_val:.0f}"
        draw.text((cx - 180, cy), dollar_text, font=font(72, bold=True),
                  fill=alpha_composite(BG, (200, 80, 80), card_alpha), anchor="mm")
        draw.text((cx + 80, cy - 14), "lost on every", font=font(22),
                  fill=alpha_composite(BG, GRAY, card_alpha), anchor="mm")
        draw.text((cx + 80, cy + 18), "$300 sent — monthly", font=font(22, bold=True),
                  fill=alpha_composite(BG, WHITE, card_alpha), anchor="mm")

    # ── VO cue text ── t > 5
    cue_alpha = eased((t - 5.0) / 0.6, "out") if t > 5.0 else 0
    if cue_alpha > 0:
        draw.text((W // 2, 870),
                  "For the people who send money home. Every month. For years.",
                  font=font(24), fill=alpha_composite(BG, (120, 130, 160), cue_alpha),
                  anchor="mm")

    # Fade out
    if t > 6.3:
        fade_out = eased((t - 6.3) / 0.7, "in")
        img = fade_img(img, 1.0 - fade_out)

    return img


def render_scene3_solution(t):
    """10-22s: Solution — phone UI + stats. t is 0-12s."""
    img = new_frame()
    draw = ImageDraw.Draw(img)

    fade_in = eased(t / 0.5, "out")

    # ── Phone mockup — left side ──
    ph_x, ph_y = 380, 540   # phone center
    ph_w, ph_h = 280, 520
    ph_alpha = eased(t / 0.7, "out")

    # Phone shell
    if ph_alpha > 0:
        shell_color = alpha_composite(BG, (22, 32, 60), ph_alpha)
        border_color = alpha_composite(BG, (40, 60, 100), ph_alpha)
        draw_rounded_rect(draw,
                          ph_x - ph_w // 2, ph_y - ph_h // 2,
                          ph_x + ph_w // 2, ph_y + ph_h // 2,
                          r=36, fill=shell_color, outline=border_color, width=2)

        # Screen area
        scr_pad = 14
        screen_color = alpha_composite(BG, (8, 12, 28), ph_alpha)
        draw_rounded_rect(draw,
                          ph_x - ph_w // 2 + scr_pad,
                          ph_y - ph_h // 2 + scr_pad + 30,
                          ph_x + ph_w // 2 - scr_pad,
                          ph_y + ph_h // 2 - scr_pad - 10,
                          r=24, fill=screen_color)

        # App header on phone
        hdr_y = ph_y - ph_h // 2 + 70
        draw.text((ph_x, hdr_y), "Telcoin Wallet", font=font(18, bold=True),
                  fill=alpha_composite(BG, CYAN, ph_alpha), anchor="mm")

        # Amount input
        amt_y = hdr_y + 60
        draw.text((ph_x, amt_y), "$200.00", font=font(38, bold=True),
                  fill=alpha_composite(BG, WHITE, ph_alpha), anchor="mm")
        draw.text((ph_x, amt_y + 36), "Amount to send", font=font(14),
                  fill=alpha_composite(BG, GRAY, ph_alpha), anchor="mm")

        # Divider
        draw.line([(ph_x - 100, amt_y + 58), (ph_x + 100, amt_y + 58)],
                  fill=alpha_composite(BG, (30, 45, 80), ph_alpha), width=1)

        # Fee line — the key comparison
        fee_y = amt_y + 88
        draw.text((ph_x - 85, fee_y), "Fee:", font=font(16),
                  fill=alpha_composite(BG, GRAY, ph_alpha), anchor="lm")

        # Animate fee — count down from $12.50 to $4.00 (t 2.0 to 3.5)
        if t < 2.0:
            fee_shown = 12.50
            fee_color = (200, 80, 80)
        elif t < 3.5:
            progress = eased((t - 2.0) / 1.5, "inout")
            fee_shown = lerp(12.50, 4.00, progress)
            fee_color = lerp_color((200, 80, 80), GREEN_SOFT, progress)
        else:
            fee_shown = 4.00
            fee_color = GREEN_SOFT

        draw.text((ph_x + 85, fee_y), f"${fee_shown:.2f}", font=font(18, bold=True),
                  fill=alpha_composite(BG, fee_color, ph_alpha), anchor="rm")

        # Recipient
        rec_y = fee_y + 34
        draw.text((ph_x - 85, rec_y), "To:", font=font(16),
                  fill=alpha_composite(BG, GRAY, ph_alpha), anchor="lm")
        draw.text((ph_x + 85, rec_y), "Maria — GCash", font=font(16),
                  fill=alpha_composite(BG, WHITE, ph_alpha), anchor="rm")

        # Send button — appears and animates at t=3.8
        btn_y = ph_y + ph_h // 2 - 90
        btn_alpha = eased((t - 3.6) / 0.5, "out") if t > 3.6 else 0
        if btn_alpha > 0:
            btn_color = alpha_composite(BG, BLUE, btn_alpha * ph_alpha)
            draw_rounded_rect(draw,
                              ph_x - 100, btn_y - 22,
                              ph_x + 100, btn_y + 22,
                              r=22, fill=btn_color)
            draw.text((ph_x, btn_y), "Send", font=font(18, bold=True),
                      fill=alpha_composite(BG, WHITE, btn_alpha * ph_alpha),
                      anchor="mm")

        # Confirmation — sent! appears at t=5
        confirm_alpha = eased((t - 5.0) / 0.6, "out") if t > 5.0 else 0
        if confirm_alpha > 0:
            # Green checkmark circle
            ck_y = btn_y
            img = glow_dot(img, ph_x, ck_y, 22,
                           GREEN_SOFT, intensity=confirm_alpha * ph_alpha)
            # Draw checkmark manually
            overlay_ck = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            dck = ImageDraw.Draw(overlay_ck)
            ck_size = 12
            dck.line([(ph_x - ck_size + 2, ck_y),
                       (ph_x - 4, ck_y + ck_size - 4),
                       (ph_x + ck_size, ck_y - ck_size + 4)],
                     fill=(*WHITE, int(255 * confirm_alpha)), width=3)
            img = Image.alpha_composite(img.convert("RGBA"), overlay_ck).convert("RGB")
            draw = ImageDraw.Draw(img)

            # "Sent!" text
            draw.text((ph_x, ck_y + 40), "Sent!", font=font(16, bold=True),
                      fill=alpha_composite(BG, GREEN_SOFT, confirm_alpha * ph_alpha),
                      anchor="mm")

    # ── Stat cards — right side ──
    right_x = 1100

    # Card 1: 16 countries — appears at t=1.5
    c1_alpha = eased((t - 1.5) / 0.7, "out") if t > 1.5 else 0
    if c1_alpha > 0:
        cy1 = 400
        draw_rounded_rect(draw,
                          right_x - 380, cy1 - 70,
                          right_x + 380, cy1 + 70,
                          r=16,
                          fill=alpha_composite(BG, (12, 18, 40), c1_alpha),
                          outline=alpha_composite(BG, (0, 71, 255), c1_alpha),
                          width=1)
        draw.text((right_x, cy1 - 24), "16 countries", font=font(42, bold=True),
                  fill=alpha_composite(BG, WHITE, c1_alpha), anchor="mm")
        draw.text((right_x, cy1 + 22), "23+ mobile money platforms",
                  font=font(24), fill=alpha_composite(BG, GRAY, c1_alpha),
                  anchor="mm")

    # Card 2: Fees — appears at t=3.0
    c2_alpha = eased((t - 3.0) / 0.7, "out") if t > 3.0 else 0
    if c2_alpha > 0:
        cy2 = 580
        draw_rounded_rect(draw,
                          right_x - 380, cy2 - 70,
                          right_x + 380, cy2 + 70,
                          r=16,
                          fill=alpha_composite(BG, (8, 20, 14), c2_alpha),
                          outline=alpha_composite(BG, (50, 200, 120), c2_alpha),
                          width=1)
        draw.text((right_x, cy2 - 24), "Fees: 2% or less",
                  font=font(48, bold=True),
                  fill=alpha_composite(BG, GREEN_SOFT, c2_alpha), anchor="mm")
        draw.text((right_x, cy2 + 22), "vs. 6.3% global average",
                  font=font(24), fill=alpha_composite(BG, GRAY, c2_alpha),
                  anchor="mm")

    # Card 3: Same day delivery — t=5.5
    c3_alpha = eased((t - 5.5) / 0.7, "out") if t > 5.5 else 0
    if c3_alpha > 0:
        cy3 = 760
        draw_rounded_rect(draw,
                          right_x - 380, cy3 - 60,
                          right_x + 380, cy3 + 60,
                          r=16,
                          fill=alpha_composite(BG, (14, 12, 30), c3_alpha),
                          outline=alpha_composite(BG, (0, 212, 255), c3_alpha),
                          width=1)
        draw.text((right_x, cy3 - 18), "Delivered same day",
                  font=font(32, bold=True),
                  fill=alpha_composite(BG, CYAN, c3_alpha), anchor="mm")
        draw.text((right_x, cy3 + 22), "Direct to mobile money",
                  font=font(22), fill=alpha_composite(BG, GRAY, c3_alpha),
                  anchor="mm")

    # GSMA + Bank credibility line — t=7.5
    gsma_alpha = eased((t - 7.5) / 0.7, "out") if t > 7.5 else 0
    if gsma_alpha > 0:
        draw.text((W // 2, 940),
                  "Validated by GSMA MNO members  ·  Telcoin Digital Asset Bank — Nebraska charter",
                  font=font(20), fill=alpha_composite(BG, (120, 130, 160), gsma_alpha),
                  anchor="mm")

    # Fade out
    if t > 10.8:
        fade_out = eased((t - 10.8) / 1.2, "in")
        img = fade_img(img, 1.0 - fade_out)

    return img


def render_scene4_map(t):
    """22-27s: World map with corridor animation. t is 0-5s."""
    img = new_frame()
    draw = ImageDraw.Draw(img)

    # Map bounding box
    MX, MY = 80, 140
    MW, MH = W - 160, H - 280

    fade_in = eased(t / 0.5, "out")

    # ── Draw continent fills ──
    for name, pts in CONTINENTS.items():
        px_pts = [lonlat_to_xy(lon, lat, MX, MY, MW, MH) for lon, lat in pts]
        if len(px_pts) >= 3:
            cont_color = alpha_composite(BG, (18, 26, 52), fade_in)
            draw.polygon(px_pts, fill=cont_color, outline=alpha_composite(BG, (28, 40, 72), fade_in))

    # Hub position
    hub_x, hub_y = lonlat_to_xy(HUB[1], HUB[2], MX, MY, MW, MH)

    # ── Animate city dots and corridor lines ──
    # Each city appears 0.5s apart starting at t=0.5
    for i, (name, lon, lat) in enumerate(CITIES):
        cx, cy = lonlat_to_xy(lon, lat, MX, MY, MW, MH)
        city_start = 0.5 + i * 0.5
        city_alpha = eased((t - city_start) / 0.4, "out") if t > city_start else 0

        if city_alpha <= 0:
            continue

        # Line from city to hub — animates after dot appears
        line_start = city_start + 0.3
        line_progress = eased((t - line_start) / 0.8, "out") if t > line_start else 0
        if line_progress > 0:
            # Draw line with glow
            overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            dov = ImageDraw.Draw(overlay)
            px = int(cx + (hub_x - cx) * line_progress)
            py = int(cy + (hub_y - cy) * line_progress)
            line_a = int(80 * city_alpha)
            dov.line([(cx, cy), (px, py)], fill=(*CYAN, line_a), width=1)
            img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
            draw = ImageDraw.Draw(img)

        # City dot
        img = glow_dot(img, cx, cy, 5, CYAN, intensity=city_alpha)
        draw = ImageDraw.Draw(img)

        # City label
        label_alpha = eased((t - city_start - 0.2) / 0.4, "out") if t > city_start + 0.2 else 0
        if label_alpha > 0:
            # Offset label to avoid overlap
            offsets = [(12, -8), (12, 8), (-80, -8), (12, 8), (12, -8), (-100, -8)]
            ox, oy = offsets[i]
            draw.text((cx + ox, cy + oy), name, font=font(16),
                      fill=alpha_composite(BG, GRAY, label_alpha))

    # Hub dot
    hub_alpha = eased((t - 0.2) / 0.4, "out") if t > 0.2 else 0
    if hub_alpha > 0:
        img = glow_dot(img, hub_x, hub_y, 7, BLUE, intensity=hub_alpha)
        draw = ImageDraw.Draw(img)

    # ── Title / VO support text ──
    title_alpha = eased((t - 0.8) / 0.5, "out") if t > 0.8 else 0
    if title_alpha > 0:
        draw.text((W // 2, 60),
                  "GSMA-member mobile network operators validate every transaction",
                  font=font(26), fill=alpha_composite(BG, GRAY, title_alpha),
                  anchor="mm")

    # Credibility pills at t=2.5
    pill_alpha = eased((t - 2.5) / 0.6, "out") if t > 2.5 else 0
    if pill_alpha > 0:
        pills = [
            "GSMA Mobile Network Operator validators",
            "Telcoin Digital Asset Bank — Nebraska DADI charter  ·  Nov 12, 2025",
        ]
        for pi, pill_text in enumerate(pills):
            py_ = H - 130 + pi * 50
            # Measure text
            bbox = font(20).getbbox(pill_text)
            tw = bbox[2] - bbox[0]
            px_ = W // 2
            pad = 20
            draw_rounded_rect(draw,
                              px_ - tw // 2 - pad, py_ - 16,
                              px_ + tw // 2 + pad, py_ + 16,
                              r=16,
                              fill=alpha_composite(BG, (14, 18, 40), pill_alpha),
                              outline=alpha_composite(BG, (40, 60, 100), pill_alpha),
                              width=1)
            draw.text((px_, py_), pill_text, font=font(20),
                      fill=alpha_composite(BG, WHITE, pill_alpha), anchor="mm")

    # Fade out
    if t > 4.3:
        fade_out = eased((t - 4.3) / 0.7, "in")
        img = fade_img(img, 1.0 - fade_out)

    return img


def render_scene5_cta(t):
    """27-30s: CTA — TELCOIN wordmark. t is 0-3s."""
    img = new_frame()
    draw = ImageDraw.Draw(img)

    # Fade in from black
    fade_in = eased(t / 0.5, "out")

    # Subtle horizontal rule
    rule_alpha = eased((t - 0.4) / 0.4, "out") if t > 0.4 else 0
    if rule_alpha > 0:
        rw = int(180 * rule_alpha)
        draw.line([(W // 2 - rw, H // 2 - 80), (W // 2 + rw, H // 2 - 80)],
                  fill=alpha_composite(BG, (40, 60, 100), rule_alpha), width=1)

    # Wordmark — large tracking
    word_alpha = eased((t - 0.2) / 0.6, "out") if t > 0.2 else 0
    if word_alpha > 0:
        # Draw spaced TELCOIN
        letters = "TELCOIN"
        spacing = 28
        f_wm = font(82, bold=True)
        total_w = sum(f_wm.getbbox(c)[2] - f_wm.getbbox(c)[0] for c in letters) + spacing * (len(letters) - 1)
        sx = W // 2 - total_w // 2
        for ch in letters:
            cw = f_wm.getbbox(ch)[2] - f_wm.getbbox(ch)[0]
            draw.text((sx, H // 2 - 20), ch, font=f_wm,
                      fill=alpha_composite(BG, WHITE, word_alpha), anchor="lm")
            sx += cw + spacing

    # Tagline
    tag_alpha = eased((t - 0.9) / 0.5, "out") if t > 0.9 else 0
    if tag_alpha > 0:
        draw.text((W // 2, H // 2 + 52), "Money that moves.",
                  font=font(30), fill=alpha_composite(BG, GRAY, tag_alpha),
                  anchor="mm")

    # URL
    url_alpha = eased((t - 1.4) / 0.5, "out") if t > 1.4 else 0
    if url_alpha > 0:
        draw.text((W // 2, H // 2 + 100), "telco.in",
                  font=font(24), fill=alpha_composite(BG, CYAN, url_alpha),
                  anchor="mm")

    # Fade to black at end
    if t > 2.3:
        fade_out = eased((t - 2.3) / 0.7, "in")
        img = fade_img(img, 1.0 - fade_out)

    img = fade_img(img, fade_in)
    return img


# ─── SCENE TIMELINE ──────────────────────────────────────────────────────────
# Scene boundaries in global seconds:
#   Scene 1:  0.0 –  3.0  (hook)
#   Scene 2:  3.0 – 10.0  (problem stat)
#   Scene 3: 10.0 – 22.0  (solution phone + cards)
#   Scene 4: 22.0 – 27.0  (world map)
#   Scene 5: 27.0 – 30.0  (CTA)

def render_frame(global_t):
    if global_t < 3.0:
        return render_scene1_hook(global_t)
    elif global_t < 10.0:
        return render_scene2_problem(global_t - 3.0)
    elif global_t < 22.0:
        return render_scene3_solution(global_t - 10.0)
    elif global_t < 27.0:
        return render_scene4_map(global_t - 22.0)
    else:
        return render_scene5_cta(global_t - 27.0)


# ─── RENDER ──────────────────────────────────────────────────────────────────

def main():
    print(f"Rendering {TOTAL_FRAMES} frames at {FPS}fps ({DURATION}s)")
    print(f"Output: {OUT_FILE}")

    from moviepy import VideoClip

    def make_frame(t):
        img = render_frame(t)
        return np.array(img)

    clip = VideoClip(make_frame, duration=DURATION)
    clip.write_videofile(
        OUT_FILE,
        fps=FPS,
        codec="libx264",
        audio=False,
        preset="medium",
        ffmpeg_params=["-crf", "18", "-pix_fmt", "yuv420p"],
        logger="bar",
    )
    print(f"\nDone: {OUT_FILE}")


if __name__ == "__main__":
    main()
