"""Convert avatar.png into a fade-in-animated ASCII-art SVG."""
from PIL import Image, ImageOps, ImageFilter, ImageEnhance

RAMP = " .`:-=+*cs#%@"  # bright -> dark
COLS = 96
ASPECT = 0.52  # char cell width/height correction for monospace

def build(path_in, path_out):
    img = Image.open(path_in).convert("L")
    # Local-contrast punch so eyes/brows/mouth survive the downsample -
    # global autocontrast alone left the face a flat mid-grey blob.
    img = ImageEnhance.Contrast(img).enhance(1.35)
    img = img.filter(ImageFilter.UnsharpMask(radius=4, percent=180, threshold=2))
    rows = round(img.width / img.height * COLS * ASPECT)
    small = img.resize((COLS, rows), Image.LANCZOS)
    small = ImageOps.autocontrast(small, cutoff=1)
    px = small.load()

    lines = []
    for y in range(rows):
        row = []
        for x in range(COLS):
            v = px[x, y]  # 0 dark .. 255 bright
            idx = int((255 - v) / 255 * (len(RAMP) - 1))
            row.append(RAMP[idx])
        lines.append("".join(row))

    cell_h = 11.6
    cell_w = 6.2
    font_size = 11
    W = COLS * cell_w + 20
    H = rows * cell_h + 20

    # GOTCHA (found live on GitHub, 15 Sep 2026): SMIL <animate> nested inside
    # a <clipPath> is a fragile combo - the width-reveal it drove never fired
    # in GitHub's render, so every row stayed clipped to width 0 forever and
    # the whole image was just the background rect. No error, just blank.
    # Fixed by never gating visibility on animation at all: every row's real
    # opacity attribute is 1 (so a renderer with zero animation support still
    # shows the full portrait immediately), and a plain top-level CSS
    # keyframe (no clipPath involved) plays a staggered fade-in as a bonus.
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" '
                f'viewBox="0 0 {W:.0f} {H:.0f}" font-family="\'JetBrains Mono\',\'Courier New\',monospace">')
    svg.append('<style>')
    svg.append('@keyframes rowIn{from{opacity:0}to{opacity:1}}')
    svg.append('.row{animation:rowIn .35s ease-out both}')
    svg.append('</style>')
    svg.append(f'<rect width="{W:.0f}" height="{H:.0f}" fill="#0d1117" rx="10"/>')
    for i, ln in enumerate(lines):
        y = 10 + i * cell_h + font_size
        esc = ln.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        svg.append(
            f'<text class="row" style="animation-delay:{i*0.045:.3f}s" '
            f'x="10" y="{y:.1f}" font-size="{font_size}" fill="#39d353" opacity="1" '
            f'xml:space="preserve">{esc}</text>'
        )
    svg.append(f'<rect width="{W:.0f}" height="{H:.0f}" fill="none" stroke="#30363d" stroke-width="1.5" rx="10"/>')
    svg.append('</svg>')

    with open(path_out, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"wrote {path_out}: {COLS}x{rows} chars, {W:.0f}x{H:.0f}px")

if __name__ == "__main__":
    build("avatar.png", "ascii_art.svg")
