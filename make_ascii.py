"""Convert avatar.png into a typewriter-animated ASCII-art SVG."""
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

    cell_w, cell_h = 6.2, 11.6
    font_size = 11
    W = COLS * cell_w + 20
    H = rows * cell_h + 20

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" '
                f'viewBox="0 0 {W:.0f} {H:.0f}" font-family="\'JetBrains Mono\',\'Courier New\',monospace">')
    svg.append('<defs>')
    svg.append(f'<clipPath id="frame"><rect x="0" y="0" width="{W:.0f}" height="{H:.0f}" rx="10"/></clipPath>')
    for i in range(rows):
        row_w = COLS * cell_w
        svg.append(
            f'<clipPath id="rowclip{i}"><rect x="0" y="0" width="0" height="{cell_h:.1f}">'
            f'<animate attributeName="width" from="0" to="{row_w:.1f}" begin="{i*0.045:.3f}s" '
            f'dur="0.28s" fill="freeze" calcMode="spline" keySplines="0.2 0 0.2 1"/></rect></clipPath>'
        )
    svg.append('</defs>')
    svg.append(f'<rect width="{W:.0f}" height="{H:.0f}" fill="#0d1117" rx="10"/>')
    svg.append(f'<g clip-path="url(#frame)">')
    for i, line in enumerate(lines):
        y = 10 + i * cell_h + font_size
        esc = (line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                   .replace(" ", " "))
        svg.append(
            f'<g clip-path="url(#rowclip{i})">'
            f'<text x="10" y="{y:.1f}" font-size="{font_size}" fill="#39d353" '
            f'xml:space="preserve">{esc}</text></g>'
        )
    svg.append('<rect width="{:.0f}" height="{:.0f}" fill="none" stroke="#30363d" stroke-width="1.5" rx="10"/>'.format(W, H))
    svg.append('</g></svg>')

    with open(path_out, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"wrote {path_out}: {COLS}x{rows} chars, {W:.0f}x{H:.0f}px")

if __name__ == "__main__":
    build("avatar.png", "ascii_art.svg")
