"""Fresh pixel drawing kit for the 22 Nov 2026 front page.

Stdlib only: a hand-built 5x7 bitmap font, an RGB canvas with simple
shape helpers, and a minimal PNG encoder (zlib + CRC32). No network,
no clock, no randomness -- the same input always yields the same bytes.
"""

import struct
import zlib

# ---------------------------------------------------------------- font
# Each glyph is 7 rows of 5 cells; '#' is ink, '.' is empty.
_GLYPHS = {
    "A": (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "B": ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    "C": (".####", "#....", "#....", "#....", "#....", "#....", ".####"),
    "D": ("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
    "E": ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    "F": ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    "G": (".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."),
    "H": ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "I": (".###.", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "J": ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    "K": ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    "L": ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    "M": ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    "N": ("#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"),
    "O": (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "P": ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    "Q": (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    "R": ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    "S": (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    "T": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    "U": ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "V": ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    "W": ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
    "X": ("#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"),
    "Y": ("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    "Z": ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
    "0": (".###.", "#..##", "#.#.#", "##..#", "#...#", "#...#", ".###."),
    "1": ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "2": (".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"),
    "3": ("####.", "....#", "....#", ".###.", "....#", "....#", "####."),
    "4": ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
    "5": ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    "6": (".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."),
    "7": ("#####", "....#", "...#.", "...#.", "..#..", "..#..", "..#.."),
    "8": (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
    "9": (".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."),
    " ": (".....", ".....", ".....", ".....", ".....", ".....", "....."),
    ".": (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
    ",": (".....", ".....", ".....", ".....", ".##..", ".##..", ".#..."),
    ":": (".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."),
    ";": (".....", ".##..", ".##..", ".....", ".##..", ".##..", ".#..."),
    "!": ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
    "?": (".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."),
    "-": (".....", ".....", ".....", "#####", ".....", ".....", "....."),
    "'": ("..#..", "..#..", ".#...", ".....", ".....", ".....", "....."),
    '"': (".#.#.", ".#.#.", ".....", ".....", ".....", ".....", "....."),
    "(": ("...#.", "..#..", ".#...", ".#...", ".#...", "..#..", "...#."),
    ")": (".#...", "..#..", "...#.", "...#.", "...#.", "..#..", ".#..."),
    "/": ("....#", "....#", "...#.", "...#.", "..#..", ".#...", "#...."),
    "&": (".##..", "#..#.", "#.#..", ".#...", "#.#.#", "#..#.", ".##.#"),
    "%": ("#...#", "#..#.", "...#.", "..#..", ".#...", "#..#.", "#...#"),
    "+": (".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."),
    "=": (".....", ".....", "#####", ".....", "#####", ".....", "....."),
    "$": ("..#..", ".####", "#.#.#", ".#...", "..###", "#...#", ".###."),
    "*": (".....", ".#.#.", "..#..", "#####", "..#..", ".#.#.", "....."),
    "<": ("...#.", "..#..", ".#...", "#....", ".#...", "..#..", "...#."),
    ">": (".#...", "..#..", "...#.", "....#", "...#.", "..#..", ".#..."),
    "[": (".###.", ".#...", ".#...", ".#...", ".#...", ".#...", ".###."),
    "]": (".###.", "...#.", "...#.", "...#.", "...#.", "...#.", ".###."),
    "_": (".....", ".....", ".....", ".....", ".....", ".....", "#####"),
    "#": (".#.#.", ".#.#.", "#####", ".#.#.", "#####", ".#.#.", ".#.#."),
    "•": (".....", ".....", ".###.", ".###.", ".###.", ".....", "....."),
    "|": ("..#..", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
}

_GLYPH_W = 5
_GLYPH_H = 7
_ADVANCE = 6  # glyph width + 1 px tracking, in font units


def _normalise(text):
    return (
        text.replace("’", "'")
        .replace("‘", "'")
        .replace("“", '"')
        .replace("”", '"')
        .replace("–", "-")
        .replace("—", "-")
    )


def text_width(text, scale):
    return len(_normalise(text)) * _ADVANCE * scale - scale


# --------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, width, height, paper):
        self.w = width
        self.h = height
        self.px = bytearray(paper * (width * height))

    def _set(self, x, y, rgb):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i : i + 3] = rgb

    def fill(self, x, y, w, h, rgb):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.w, x + w)
        y1 = min(self.h, y + h)
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            for xx in range(x0, x1):
                self.px[base : base + 3] = rgb
                base += 3

    def border(self, x, y, w, h, rgb, t=1):
        self.fill(x, y, w, t, rgb)
        self.fill(x, y + h - t, w, t, rgb)
        self.fill(x, y, t, h, rgb)
        self.fill(x + w - t, y, t, h, rgb)

    def hline(self, x, y, length, rgb, t=1):
        self.fill(x, y, length, t, rgb)

    def vline(self, x, y, length, rgb, t=1):
        self.fill(x, y, t, length, rgb)

    def line(self, x0, y0, x1, y1, rgb):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self._set(x0, y0, rgb)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def polyline(self, points, rgb, close=False):
        pts = list(points)
        if close and len(pts) > 1:
            pts = pts + [pts[0]]
        for a, b in zip(pts, pts[1:]):
            self.line(a[0], a[1], b[0], b[1], rgb)

    def fill_poly(self, points, rgb):
        # Scanline fill of a simple polygon.
        ys = [p[1] for p in points]
        for y in range(min(ys), max(ys) + 1):
            xs = []
            n = len(points)
            for i in range(n):
                x0, y0 = points[i]
                x1, y1 = points[(i + 1) % n]
                if (y0 <= y < y1) or (y1 <= y < y0):
                    xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
            xs.sort()
            for k in range(0, len(xs) - 1, 2):
                xa = int(round(xs[k]))
                xb = int(round(xs[k + 1]))
                self.fill(xa, y, xb - xa + 1, 1, rgb)

    def circle(self, cx, cy, r, rgb):
        x = 0
        y = r
        d = 3 - 2 * r
        while y >= x:
            for px, py in (
                (cx + x, cy + y), (cx - x, cy + y), (cx + x, cy - y),
                (cx - x, cy - y), (cx + y, cy + x), (cx - y, cy + x),
                (cx + y, cy - x), (cx - y, cy - x),
            ):
                self._set(px, py, rgb)
            x += 1
            if d > 0:
                y -= 1
                d += 4 * (x - y) + 10
            else:
                d += 4 * x + 6

    def disc(self, cx, cy, r, rgb):
        for yy in range(cy - r, cy + r + 1):
            half = int((r * r - (yy - cy) ** 2) ** 0.5)
            self.fill(cx - half, yy, 2 * half + 1, 1, rgb)

    def ring(self, cx, cy, r, rgb, t=2):
        for rr in range(r - t + 1, r + 1):
            self.circle(cx, cy, rr, rgb)

    # ------------------------------------------------------------ text
    def glyph(self, x, y, ch, scale, rgb):
        rows = _GLYPHS.get(ch)
        if rows is None:
            rows = _GLYPHS["?"]
        for r, row in enumerate(rows):
            for c, cell in enumerate(row):
                if cell == "#":
                    self.fill(x + c * scale, y + r * scale, scale, scale, rgb)

    def text(self, x, y, s, scale, rgb):
        cx = x
        for ch in _normalise(s):
            self.glyph(cx, y, ch, scale, rgb)
            cx += _ADVANCE * scale
        return cx

    def text_centred(self, cx, y, s, scale, rgb):
        w = text_width(s, scale)
        return self.text(cx - w // 2, y, s, scale, rgb)

    def text_right(self, x, y, s, scale, rgb):
        w = text_width(s, scale)
        return self.text(x - w, y, s, scale, rgb)


# ------------------------------------------------------------ PNG out
def png_bytes(canvas):
    def chunk(kind, data):
        out = struct.pack(">I", len(data)) + kind + data
        out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
        return out

    header = struct.pack(">IIBBBBB", canvas.w, canvas.h, 8, 2, 0, 0, 0)
    raw = bytearray()
    for y in range(canvas.h):
        raw.append(0)
        start = y * canvas.w * 3
        raw += canvas.px[start : start + canvas.w * 3]
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", header)
        + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
        + chunk(b"IEND", b"")
    )
