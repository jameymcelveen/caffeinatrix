#!/usr/bin/env python3
"""Generate the Caffeinatrix logo as a self-contained SVG.
Coffee cup as the vessel, matrix code as the rising steam and the brew.
Steam/rain are geometric dashes (no CJK font dependency) so it rasterizes
identically everywhere."""
import math, random

random.seed(7)
S = 1024
parts = []

def rect(x, y, w, h, fill, rx=3, op=1.0):
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'rx="{rx}" fill="{fill}" opacity="{op:.3f}"/>')

# ---- defs: glows, clip, cup gradient ----
parts.append('''<defs>
  <clipPath id="squircle">
    <rect x="0" y="0" width="1024" height="1024" rx="224"/>
  </clipPath>
  <radialGradient id="glow" cx="50%" cy="60%" r="62%">
    <stop offset="0%" stop-color="#00ff41" stop-opacity="0.28"/>
    <stop offset="55%" stop-color="#00ff41" stop-opacity="0.06"/>
    <stop offset="100%" stop-color="#00ff41" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="cup" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#f2f7f1"/>
    <stop offset="45%" stop-color="#cdd8cf"/>
    <stop offset="100%" stop-color="#8f9d92"/>
  </linearGradient>
  <linearGradient id="rim" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#ffffff"/>
    <stop offset="100%" stop-color="#b9c6bb"/>
  </linearGradient>
</defs>''')

# ---- background squircle + glow ----
g = ['<g clip-path="url(#squircle)">']
g.append('<rect x="0" y="0" width="1024" height="1024" fill="#050a06"/>')
g.append('<rect x="0" y="0" width="1024" height="1024" fill="url(#glow)"/>')

# ---- faint background rain ----
col_w = 6
gap_y = 16
for cx in range(40, S, 84):
    start = random.randint(-200, 200)
    op = random.uniform(0.05, 0.13)
    n = 0
    y = start
    while y < S + 40:
        h = random.choice([18, 22, 26])
        # brighter "head" every so often
        head = (n % random.choice([5, 6, 7]) == 0)
        fill = '#7dffae' if head else '#00ff41'
        o = op * (1.7 if head else 1.0)
        g.append(rect(cx, y, col_w, h, fill, rx=2, op=min(o, 0.5)))
        y += h + gap_y
        n += 1

# ---- rising steam = brighter code streams above the cup ----
def steam(cx0, y_bottom, y_top, amp, phase):
    out = []
    y = y_bottom
    i = 0
    while y > y_top:
        t = (y_bottom - y) / (y_bottom - y_top)   # 0 at bottom -> 1 at top
        x = cx0 + amp * math.sin(phase + t * 3.0)
        op = (1.0 - t) * 0.9 + 0.05
        head = (i % 4 == 0)
        fill = '#aaffc8' if head else '#00ff41'
        out.append(rect(x, y, 7, 20, fill, rx=3, op=min(op * (1.4 if head else 1.0), 0.95)))
        y -= 20 + 14
        i += 1
    return out

g += steam(430, 560, 250, 16, 0.4)
g += steam(512, 545, 215, 20, 1.7)
g += steam(596, 560, 250, 16, 2.9)

# ---- coffee cup ----
# body (rounded trapezoid, wider at top)
g.append('<path d="M 326 612 L 698 612 L 650 800 '
         'Q 644 818 622 818 L 402 818 Q 380 818 374 800 Z" '
         'fill="url(#cup)" stroke="#00ff41" stroke-opacity="0.25" stroke-width="3"/>')
# left highlight
g.append('<path d="M 350 628 L 386 792 Q 388 800 396 802" fill="none" '
         'stroke="#ffffff" stroke-opacity="0.45" stroke-width="10" stroke-linecap="round"/>')
# handle
g.append('<path d="M 694 640 C 800 632 806 770 700 778" fill="none" '
         'stroke="url(#cup)" stroke-width="30" stroke-linecap="round"/>')
g.append('<path d="M 694 640 C 800 632 806 770 700 778" fill="none" '
         'stroke="#00ff41" stroke-opacity="0.18" stroke-width="32" stroke-linecap="round"/>')
# rim opening
g.append('<ellipse cx="512" cy="612" rx="186" ry="46" fill="url(#rim)" '
         'stroke="#00ff41" stroke-opacity="0.35" stroke-width="3"/>')
# brew (dark code pool)
g.append('<ellipse cx="512" cy="614" rx="164" ry="37" fill="#04130a"/>')
# code floating in the brew
for _ in range(9):
    a = random.uniform(0, 2 * math.pi)
    rr = random.uniform(0, 0.82)
    bx = 512 + math.cos(a) * 150 * rr
    by = 614 + math.sin(a) * 30 * rr
    head = random.random() < 0.4
    g.append(rect(bx, by - 7, 6, 14, '#9dffc4' if head else '#00ff41', rx=2,
                  op=random.uniform(0.55, 0.95)))
# rim shine
g.append('<path d="M 360 600 Q 512 566 664 600" fill="none" stroke="#ffffff" '
         'stroke-opacity="0.5" stroke-width="6" stroke-linecap="round"/>')

g.append('</g>')

# subtle inner border for the icon edge
g.append('<rect x="3" y="3" width="1018" height="1018" rx="222" fill="none" '
         'stroke="#00ff41" stroke-opacity="0.18" stroke-width="3"/>')

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" '
       f'viewBox="0 0 {S} {S}">' + ''.join(parts) + ''.join(g) + '</svg>')

with open('assets/logo.svg', 'w') as f:
    f.write(svg)
print('wrote assets/logo.svg', len(svg), 'bytes')
