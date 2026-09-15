"""Animated GitHub-style contribution heatmap SVG, built from real contributionCalendar data."""
import json

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]

def level(count, buckets):
    if count == 0:
        return 0
    for i, b in enumerate(buckets):
        if count <= b:
            return i + 1
    return len(buckets) + 1

def build(contrib_json_path, path_out):
    d = json.load(open(contrib_json_path, encoding="utf-8"))
    cal = d["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    weeks = cal["weeks"]
    total = cal["totalContributions"]

    counts = [day["contributionCount"] for w in weeks for day in w["contributionDays"]]
    nonzero = sorted(c for c in counts if c > 0)
    if nonzero:
        # simple quartile-ish buckets over the real distribution, never invented
        buckets = [
            nonzero[len(nonzero) // 4] if len(nonzero) >= 4 else nonzero[0],
            nonzero[len(nonzero) // 2],
            nonzero[3 * len(nonzero) // 4] if len(nonzero) >= 4 else nonzero[-1],
        ]
    else:
        buckets = [1, 2, 3]

    cell = 11
    gap = 3
    step = cell + gap
    pad_left = 28
    pad_top = 20
    n_weeks = len(weeks)
    W = pad_left + n_weeks * step + 10
    H = pad_top + 7 * step + 30

    month_labels = []
    seen_months = set()
    for wi, w in enumerate(weeks):
        first_day = w["contributionDays"][0]["date"]
        m = first_day[:7]  # YYYY-MM
        if m not in seen_months:
            seen_months.add(m)
            mon = int(m[5:7])
            names = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            month_labels.append((wi, names[mon]))

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
                f'viewBox="0 0 {W} {H}" font-family="\'JetBrains Mono\',monospace">')
    svg.append(f'<rect width="{W}" height="{H}" rx="10" fill="#0d1117"/>')
    svg.append(f'<text x="{pad_left}" y="14" font-size="11" fill="#7d8590">'
                f'{total} contributions in the last year</text>')

    for wi, name in month_labels:
        x = pad_left + wi * step
        svg.append(f'<text x="{x}" y="{pad_top-6}" font-size="9" fill="#7d8590">{name}</text>')

    day_labels = {1: "Mon", 3: "Wed", 5: "Fri"}
    for di, name in day_labels.items():
        y = pad_top + di * step + cell - 1
        svg.append(f'<text x="0" y="{y}" font-size="9" fill="#7d8590">{name}</text>')

    i = 0
    total_cells = n_weeks * 7
    for wi, w in enumerate(weeks):
        x = pad_left + wi * step
        for day in w["contributionDays"]:
            wd = day["weekday"]
            y = pad_top + wd * step
            lv = level(day["contributionCount"], buckets)
            color = PALETTE[lv]
            delay = (i / max(1, total_cells - 1)) * 1.6
            svg.append(
                f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2.5" '
                f'fill="{color}" opacity="0">'
                f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.3f}s" '
                f'dur="0.25s" fill="freeze"/>'
                f'<title>{day["date"]}: {day["contributionCount"]} contributions</title>'
                f'</rect>'
            )
            i += 1

    legend_x = W - 120
    legend_y = 12
    svg.append(f'<text x="{legend_x-24}" y="{legend_y+8}" font-size="9" fill="#7d8590">Less</text>')
    for i2, c in enumerate(PALETTE):
        svg.append(f'<rect x="{legend_x + i2*13}" y="{legend_y}" width="{cell}" height="{cell}" '
                    f'rx="2.5" fill="{c}"/>')
    svg.append(f'<text x="{legend_x + len(PALETTE)*13 + 4}" y="{legend_y+8}" font-size="9" '
                f'fill="#7d8590">More</text>')

    svg.append(f'<rect width="{W}" height="{H}" rx="10" fill="none" stroke="#30363d"/>')
    svg.append("</svg>")
    with open(path_out, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"wrote {path_out}: {W}x{H}, {total} total contributions, {n_weeks} weeks")

if __name__ == "__main__":
    build("contrib.json", "heatmap.svg")
