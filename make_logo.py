"""Draw the Personal Data Client logo as a PNG.

A single confident pulse on a deep-green rounded tile. One idea, few vertices:
at 120px a logo has room for exactly one thing, and stacking a second motif
next to this one only muddied it.

Rendered at 6x and downsampled with LANCZOS so the corners and joints stay
clean at Google's 120x120 consent-screen size.

    python make_logo.py
"""

from PIL import Image, ImageDraw

SS = 6                      # supersample factor
GREEN = (43, 92, 79)        # #2b5c4f -- matches the site accent
INK = (255, 255, 255)
SIZES = [120, 512]

# Design space is 120x120. Few vertices on purpose: Pillow stamps a round
# joint at each one, so a dense path reads as a lumpy worm at this weight.
PATH = [
    (20, 60),
    (48, 60),
    (56, 33),
    (64, 87),
    (72, 60),
    (100, 60),
]


def draw(size):
    S = size * SS
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    d.rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * 0.225), fill=GREEN)

    pts = [(x / 120 * S, y / 120 * S) for x, y in PATH]
    w = max(2, round(S * 0.056))

    d.line(pts, fill=INK, width=w, joint="curve")

    # Round the two free ends so the stroke doesn't look chopped.
    r = w / 2
    for x, y in (pts[0], pts[-1]):
        d.ellipse([x - r, y - r, x + r, y + r], fill=INK)

    return img.resize((size, size), Image.LANCZOS)


if __name__ == "__main__":
    for s in SIZES:
        out = f"logo-{s}.png"
        draw(s).save(out)
        print(f"wrote {out}")
