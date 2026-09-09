#!/usr/bin/env python3
# Builds the 1200x630 social preview card: the taper, on cream, in Helvetica.
# Emits og.png next to index.html.

import io, cairosvg

OUT = "/Users/michaelweinfeld/Documents/2026/PJ O'Rourke/Milestones1/og.png"

PAPER = "#F6F2E8"
INK = "#0C0C0C"
GREY = "#78766F"

# service colours, band 1 (the L) first
COLS = ["#A7A9AC", "#0039A6", "#FF6319", "#6CBE45",
        "#00933C", "#FCCC0A", "#996633", "#B933AD"]

W, H = 1200, 630
PITCH = 26          # spacing between bands
BANDW = 15          # band thickness
X0 = 78             # left edge of band 1
TOP = 0
BOT = H

# Each band k terminates at its own height going down, so the bundle tapers
# left to right the same way the page does: band 1 (the L) runs the full drop.
ENDS = [H, 545, 470, 395, 320, 245, 170, 95]

parts = []
parts.append('<rect width="%d" height="%d" fill="%s"/>' % (W, H, PAPER))

for k, c in enumerate(COLS):
    x = X0 + k * PITCH
    parts.append('<rect x="%d" y="0" width="%d" height="%d" fill="%s"/>'
                 % (x, BANDW, ENDS[k], c))

# station dots down the L, marking the stops
for y in [95, 170, 245, 320, 395, 470, 545]:
    parts.append('<circle cx="%d" cy="%d" r="11" fill="%s" stroke="%s" stroke-width="5"/>'
                 % (X0 + BANDW / 2, y, INK, PAPER))
# the terminal dot at the platform
parts.append('<circle cx="%d" cy="%d" r="15" fill="%s" stroke="%s" stroke-width="6"/>'
             % (X0 + BANDW / 2, 600, INK, PAPER))

TX = X0 + 8 * PITCH + 74
FAM = "Helvetica Neue, Helvetica, Arial, sans-serif"

def t(x, y, s, size, weight="700", fill=INK, spacing="0"):
    return ('<text x="%d" y="%d" font-family="%s" font-size="%d" font-weight="%s" '
            'fill="%s" letter-spacing="%s">%s</text>' % (x, y, FAM, size, weight, fill, spacing, s))

parts.append(t(TX, 132, "PLATFORM&#8217;S EDGE", 19, "700", INK, "4"))
parts.append(t(TX, 246, "THE LINE", 92, "700", INK, "-4"))
parts.append(t(TX, 330, "RUNS BOTH", 92, "700", INK, "-4"))
parts.append(t(TX, 414, "WAYS", 92, "700", INK, "-4"))
parts.append(t(TX, 476, "A map of your career, read from the last stop", 25, "400", INK))
parts.append(t(TX, 510, "backwards to the platform you are standing on.", 25, "400", INK))
parts.append('<rect x="%d" y="546" width="%d" height="3" fill="%s"/>' % (TX, W - TX - 78, INK))
parts.append(t(TX, 586, "EIGHT SERVICES AT THE TOP&#160;&#160;/&#160;&#160;ONE GREY L AT THE BOTTOM",
               18, "700", GREY, "3"))

svg = '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">%s</svg>' \
      % (W, H, W, H, "".join(parts))

cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=OUT,
                 output_width=W, output_height=H)
print("wrote", OUT)
