"""Build the 22 November 2026 front page and write it as a PNG.

One-page newspaper "THE WORLD TODAY -- SUNDAY, 22 NOVEMBER 2026".
Drawn entirely with the fresh pixel kit in frontpage.py: stdlib only,
no network, no clock, no randomness, so repeated runs are byte-identical.

Usage: python3 main.py [output-path]
If no path is given, writes $MAKEFUN_OUTPUT_DIR/entry.png, else entry.png.
"""

import os
import sys

from frontpage import Canvas, png_bytes

W, H = 1024, 1024

PAPER = bytes((247, 241, 222))
CARD = bytes((255, 252, 240))
INK = bytes((20, 20, 20))
WHITE = bytes((255, 255, 255))
NAVY = bytes((14, 42, 78))
NAVY2 = bytes((22, 64, 110))
NAVY3 = bytes((10, 32, 60))
GOLD = bytes((232, 185, 60))
RED = bytes((176, 32, 32))
DARKRED = bytes((122, 31, 31))
TEAL = bytes((15, 107, 92))
STEEL = bytes((46, 110, 158))
HULL = bytes((30, 60, 90))
FLAME = bytes((220, 110, 30))
FLAME2 = bytes((240, 180, 60))
BRICK = bytes((140, 47, 27))
DARK = bytes((16, 20, 24))


def card(cv, x, y, w, h, accent):
    cv.fill(x, y, w, h, CARD)
    cv.fill(x, y, w, 9, accent)
    cv.border(x, y, w, h, INK, 2)


def masthead(cv):
    cv.text_centred(512, 12, "THE WORLD TODAY", 6, INK)
    cv.hline(24, 60, 976, INK, 2)
    cv.text_centred(512, 70, "SUNDAY, 22 NOVEMBER 2026", 3, INK)
    cv.text_centred(512, 94, "WARSAW • BALTIC • ANTALYA • WASHINGTON • LIMA", 2, INK)
    cv.hline(24, 110, 976, INK, 2)


def shield_and_map(cv):
    # NATO shield with a four-point compass star, right of the hero.
    shield = [(748, 140), (908, 140), (908, 250), (880, 300),
              (828, 335), (776, 300), (748, 250)]
    cv.fill_poly(shield, NAVY2)
    cv.polyline(shield, GOLD, close=True)
    star = [(828, 160), (840, 203), (883, 215), (840, 227),
            (828, 270), (816, 227), (773, 215), (816, 203)]
    cv.fill_poly(star, GOLD)
    cv.text_centred(828, 276, "NATO", 4, WHITE)
    # Simplified Poland outline with the three impact dots.
    poland = [(690, 360), (740, 345), (800, 350), (860, 340), (920, 355),
              (950, 375), (940, 405), (900, 415), (840, 420), (780, 415),
              (720, 405), (685, 385)]
    cv.fill_poly(poland, NAVY2)
    cv.polyline(poland, WHITE, close=True)
    for dx, dy in ((770, 378), (835, 398), (895, 372)):
        cv.disc(dx, dy, 6, RED)
        cv.circle(dx, dy, 6, WHITE)


def hero(cv):
    cv.fill(0, 112, 1024, 384, NAVY)
    cv.text(24, 130, "NATO • WARSAW", 2, GOLD)
    cv.text(24, 168, "NATO WILL DEFEND", 5, WHITE)
    cv.text(24, 223, "EVERY INCH OF POLAND", 5, GOLD)
    cv.text(24, 292, "RUTTE: 'I CAN GUARANTEE NATO WILL", 2, WHITE)
    cv.text(24, 314, "DEFEND EVERY INCH OF POLAND'", 2, WHITE)
    cv.text(24, 336, "POLAND INVOKES ARTICLE 4", 2, WHITE)
    cv.text(24, 358, "NATO COUNCIL MEETS MONDAY", 2, WHITE)
    shield_and_map(cv)
    cv.fill(0, 420, 1024, 56, NAVY3)
    cv.text_centred(
        512, 440,
        "IMPACT SITES: NOWY LIPOWIEC • RUDNIK NAD SANEM • MOLODYCZ",
        2, GOLD,
    )
    cv.hline(0, 494, 1024, GOLD, 2)


def row_a(cv):
    # Baltic ship card.
    card(cv, 24, 496, 476, 172, STEEL)
    cv.text(40, 514, "BALTIC SEA • GULF OF FINLAND", 2, STEEL)
    cv.text(40, 538, "DRONES HIT SHIP", 4, INK)
    cv.text(40, 572, "IN THE BALTIC", 4, INK)
    cv.text(40, 612, "SPARTA II ABLAZE, CREW SAFE", 2, INK)
    cv.text(40, 632, "FINLAND: LIKELY UKRAINE", 2, INK)
    # Ship, flames, drones and waves at the card's right edge.
    cv.fill_poly([(372, 628), (486, 628), (472, 652), (386, 652)], HULL)
    cv.vline(430, 600, 28, INK, 3)
    cv.fill_poly([(405, 628), (420, 600), (435, 628)], FLAME)
    cv.fill_poly([(412, 628), (420, 610), (428, 628)], FLAME2)
    cv.disc(395, 590, 4, INK)
    cv.disc(455, 584, 4, INK)
    cv.line(395, 594, 405, 612, INK)
    cv.line(455, 588, 448, 610, INK)
    cv.hline(372, 656, 114, STEEL, 2)
    cv.hline(382, 661, 94, STEEL, 2)

    # COP31 card.
    card(cv, 524, 496, 476, 172, TEAL)
    cv.text(540, 514, "CLIMATE • ANTALYA", 2, TEAL)
    cv.text(540, 538, "COP31: GOOD DEAL", 4, INK)
    cv.text(540, 572, "OR NO DEAL", 4, INK)
    cv.text(540, 612, "TALKS IN OVERTIME", 2, INK)
    cv.text(540, 632, "$120BN AID CUT FROM DRAFT", 2, INK)
    # Globe with the summit number inside.
    cv.circle(925, 605, 40, TEAL)
    cv.ring(925, 605, 40, TEAL, 2)
    cv.hline(892, 592, 66, TEAL, 2)
    cv.hline(890, 618, 70, TEAL, 2)
    cv.text_centred(925, 594, "31", 3, TEAL)


def row_b(cv):
    # Trump data-centres card.
    card(cv, 24, 668, 314, 172, RED)
    cv.text(40, 686, "WASHINGTON", 2, RED)
    cv.text(40, 708, "TRUMP: NO DATA", 3, INK)
    cv.text(40, 735, "CENTRES ABROAD", 3, INK)
    cv.text(40, 772, "TREMENDOUS TAX", 2, INK)
    cv.text(40, 790, "ON FIRMS THAT BUILD", 2, INK)
    cv.text(40, 808, "OVERSEAS", 2, INK)
    for by in (684, 692, 700):
        cv.fill(290, by, 36, 6, INK)

    # Zelenskyy card.
    card(cv, 354, 668, 314, 172, NAVY)
    cv.text(370, 686, "KYIV • CNN", 2, NAVY)
    cv.text(370, 708, "ZELENSKYY:", 3, INK)
    cv.text(370, 735, "PUTIN IS", 3, INK)
    cv.text(370, 762, "A KILLER", 3, INK)
    cv.text(370, 796, "AFTER TRUMP CALLS", 2, INK)
    cv.text(370, 814, "HIM 'MY FRIEND'", 2, INK)

    # Peru quake card.
    card(cv, 684, 668, 316, 172, BRICK)
    cv.text(700, 686, "LIMA • JUNIN", 2, BRICK)
    cv.text(700, 708, "6.9 QUAKE", 3, INK)
    cv.text(700, 735, "SHAKES PERU'S", 3, INK)
    cv.text(700, 762, "ANDES", 3, INK)
    cv.text(700, 796, "FELT IN LIMA", 2, INK)
    cv.text(700, 814, "NO DAMAGE REPORTED", 2, INK)


def band_and_ticker(cv):
    # Wall Street band.
    cv.fill(0, 840, 1024, 96, DARKRED)
    cv.polyline([(48, 868), (80, 880), (112, 872), (144, 892), (176, 908)], GOLD)
    for bx, bh in ((850, 40), (880, 30), (910, 20), (940, 12)):
        cv.fill(bx, 912 - bh, 22, bh, GOLD)
    cv.text_centred(512, 858, "WALL ST: S&P DOWN 9% SINCE NOV 4", 3, WHITE)
    cv.text_centred(512, 894, "AI SELL-OFF DEEPENS • NASDAQ 100 AT 7-MONTH LOW", 2, GOLD)

    # Ticker.
    cv.fill(0, 936, 1024, 88, DARK)
    cv.text_centred(
        512, 950,
        "NATO COUNCIL MEETS MONDAY • ANTHROPIC SHARES FALL AFTER RECORD IPO",
        2, WHITE,
    )
    cv.text_centred(
        512, 978,
        "MAMDANI: CLOSE RIKERS ISLAND • TRUMP: PUTIN WOULD LOVE TO END WAR",
        2, GOLD,
    )


def build():
    cv = Canvas(W, H, PAPER)
    masthead(cv)
    hero(cv)
    row_a(cv)
    row_b(cv)
    band_and_ticker(cv)
    cv.border(0, 0, W, H, INK, 4)
    return cv


def main():
    if len(sys.argv) > 1:
        out = sys.argv[1]
    else:
        out = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "."), "entry.png")
    data = png_bytes(build())
    with open(out, "wb") as fh:
        fh.write(data)
    print("wrote %s (%d bytes)" % (out, len(data)))


if __name__ == "__main__":
    main()
