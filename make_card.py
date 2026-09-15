"""Neofetch-style info card SVG with a staggered line-by-line fade-in."""

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
            f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" '
            f'begin="{delay:.2f}s" dur="0.4s" fill="freeze"/>'
            f'<text x="{pad_x}" y="{y}" font-size="13" fill="{ACCENT}">&gt;</text>'
            f'<text x="{pad_x+16}" y="{y}" font-size="13" fill="{LABEL_COLOR}">{label}:</text>'
            f'<text x="{pad_x+16+len(label)*7.6+14}" y="{y}" font-size="13" '
            f'fill="{VALUE_COLOR}">{value}</text></g>'
        )

    # blinking cursor after the last line
    last_y = y0 + len(lines) * row_h
    cursor_x = pad_x + 8
    svg.append(
        f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" '
        f'begin="{0.15*len(lines):.2f}s" dur="0.2s" fill="freeze"/>'
        f'<rect x="{cursor_x}" y="{last_y-11}" width="8" height="14" fill="{ACCENT}">'
        f'<animate attributeName="opacity" values="1;1;0;0;1" keyTimes="0;0.49;0.5;0.99;1" '
        f'dur="1s" begin="{0.15*len(lines):.2f}s" repeatCount="indefinite"/></rect></g>'
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
