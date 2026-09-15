"""Neofetch-style info card SVG with a staggered line-by-line fade-in.

Visibility never depends on the animation running (see make_ascii.py's note):
every line's real opacity attribute is 1, and a plain CSS keyframe (no SMIL,
no clipPath) plays the staggered fade-in as a bonus on top of that.
"""

LABEL_COLOR = "#7d8590"
VALUE_COLOR = "#e6edf3"
ACCENT = "#39d353"
BG = "#0d1117"
BORDER = "#30363d"

def line(label, value):
    return (label, value)

def build(path_out, lines, title="aditya@github"):
    W, H = 460, 46 + len(lines) * 26 + 20
    pad_x = 22
    font = "'JetBrains Mono','Courier New',monospace"

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
                f'viewBox="0 0 {W} {H}" font-family="{font}">')
    svg.append('<style>')
    svg.append('@keyframes lineIn{from{opacity:0}to{opacity:1}}')
    svg.append('.ln{animation:lineIn .4s ease-out both}')
    svg.append('@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}')
    svg.append('.cursor{animation:blink 1s step-end infinite}')
    svg.append('</style>')
    svg.append(f'<rect width="{W}" height="{H}" rx="10" fill="{BG}" stroke="{BORDER}"/>')

    # terminal titlebar
    svg.append(f'<rect width="{W}" height="34" rx="10" fill="#161b22"/>')
    svg.append(f'<rect y="24" width="{W}" height="10" fill="#161b22"/>')
    for i, c in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        svg.append(f'<circle cx="{20 + i*18}" cy="17" r="6" fill="{c}"/>')
    svg.append(f'<text x="{W/2}" y="22" font-size="12" fill="{LABEL_COLOR}" '
                f'text-anchor="middle">{title}</text>')

    y0 = 60
    row_h = 26
    for i, (label, value) in enumerate(lines):
        y = y0 + i * row_h
        delay = 0.15 * i
        svg.append(
            f'<g class="ln" opacity="1" style="animation-delay:{delay:.2f}s">'
            f'<text x="{pad_x}" y="{y}" font-size="13" fill="{ACCENT}">&gt;</text>'
            f'<text x="{pad_x+16}" y="{y}" font-size="13" fill="{LABEL_COLOR}">{label}:</text>'
            f'<text x="{pad_x+16+len(label)*7.6+14}" y="{y}" font-size="13" '
            f'fill="{VALUE_COLOR}">{value}</text></g>'
        )

    # blinking cursor after the last line - visible immediately, blink is decorative
    last_y = y0 + len(lines) * row_h
    cursor_x = pad_x + 8
    svg.append(
        f'<rect class="cursor" x="{cursor_x}" y="{last_y-11}" width="8" height="14" '
        f'fill="{ACCENT}" opacity="1"/>'
    )

    svg.append("</svg>")
    with open(path_out, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"wrote {path_out}: {W}x{H}")

if __name__ == "__main__":
    lines = [
        line("role", "B.Tech AI/ML, Jain University"),
        line("building", "Cafecino, AUTIVA"),
        line("stack", "TypeScript / Python / SQL"),
        line("repos", "3 public"),
        line("joined", "Jul 2026"),
        line("site", "aditya-portfolio-dusky-seven.vercel.app"),
    ]
    build("card.svg", lines)
