#!/usr/bin/env python3
"""Render a plain-text terminal transcript (docs/demo.txt) as an SVG window.

The text is copied verbatim; the only thing added is colour, chosen from the
same line prefixes the tool itself colours in a real terminal:
"$ " prompt, "[+]" ok, "[-]" error, "[!]" warning, "[*]" info, the
"WARNING" box, and JSON keys/strings.

Usage: python3 docs/render_svg.py docs/demo.txt docs/demo.svg
"""
import html
import re
import sys

FONT_SIZE = 14
LINE_H = 19
CHAR_W = 8.43  # advance width of a 14px monospace glyph
PAD_X = 18
PAD_TOP = 46
PAD_BOTTOM = 18

BG = "#0d1117"
BAR = "#161b22"
FG = "#c9d1d9"
COLORS = {
    "prompt": "#7ee787",
    "ok": "#3fb950",
    "err": "#f85149",
    "warn": "#d29922",
    "info": "#58a6ff",
    "dim": "#8b949e",
    "key": "#79c0ff",
    "str": "#a5d6ff",
}


def classify(line):
    if line.startswith("$ "):
        return "prompt"
    if line.startswith("[+]"):
        return "ok"
    if line.startswith("[-]"):
        return "err"
    if line.startswith("[!]"):
        return "warn"
    if line.startswith("[*]"):
        return "info"
    if line[:1] in "╔║╚":
        return "err"
    if line.startswith(("---", "rtt ", "Starting Nmap", "Nmap done")):
        return "dim"
    return None


JSON_KV = re.compile(r'^(\s*)("[^"]+")(: )(.*)$')


def render_line(line):
    esc = html.escape
    kind = classify(line)
    if kind == "prompt":
        return (f'<tspan fill="{COLORS["prompt"]}">$ </tspan>'
                f'<tspan fill="{FG}" font-weight="bold">{esc(line[2:])}</tspan>')
    if kind:
        return f'<tspan fill="{COLORS[kind]}">{esc(line)}</tspan>'
    m = JSON_KV.match(line)
    if m:
        indent, key, sep, value = m.groups()
        vcol = COLORS["str"] if value.startswith('"') else COLORS["ok"]
        return (f'{esc(indent)}<tspan fill="{COLORS["key"]}">{esc(key)}</tspan>'
                f'{esc(sep)}<tspan fill="{vcol}">{esc(value)}</tspan>')
    return esc(line)


def main(src, dst):
    with open(src, encoding="utf-8") as fh:
        lines = fh.read().rstrip("\n").split("\n")
    cols = max(len(line) for line in lines)
    width = int(PAD_X * 2 + cols * CHAR_W) + 1
    height = PAD_TOP + len(lines) * LINE_H + PAD_BOTTOM

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" '
        f'aria-label="Terminal session running the log analyzer and the IAM policy analyzer">',
        f'<rect width="{width}" height="{height}" rx="8" fill="{BG}"/>',
        f'<rect width="{width}" height="30" rx="8" fill="{BAR}"/>',
        f'<rect y="22" width="{width}" height="8" fill="{BAR}"/>',
        '<circle cx="18" cy="15" r="6" fill="#ff5f56"/>',
        '<circle cx="38" cy="15" r="6" fill="#ffbd2e"/>',
        '<circle cx="58" cy="15" r="6" fill="#27c93f"/>',
        f'<text x="{width / 2}" y="20" fill="{COLORS["dim"]}" font-size="12" '
        'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
        'text-anchor="middle">icc-03 tools</text>',
        f'<text font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, \'DejaVu Sans Mono\', monospace" '
        f'font-size="{FONT_SIZE}" fill="{FG}" xml:space="preserve">',
    ]
    # Box-drawing frames (the WARNING box) are drawn as SVG rectangles, not
    # glyphs: many fonts give box characters a different width than letters,
    # which made the right-hand border look ragged in some browsers.
    frames = []
    box_top = None
    for i, line in enumerate(lines):
        y = PAD_TOP + i * LINE_H + FONT_SIZE
        if line.startswith("╔"):
            box_top = (i, len(line))
            continue
        if line.startswith("╚") and box_top is not None:
            top, ncols = box_top
            box_top = None
            x0 = PAD_X + CHAR_W / 2
            y0 = PAD_TOP + top * LINE_H + LINE_H / 2
            w = (ncols - 1) * CHAR_W
            h = (i - top) * LINE_H
            for inset in (0, 3):
                frames.append(
                    f'<rect x="{x0 + inset:.2f}" y="{y0 + inset:.2f}" '
                    f'width="{w - 2 * inset:.2f}" height="{h - 2 * inset:.2f}" '
                    f'fill="none" stroke="{COLORS["err"]}" stroke-width="1.2"/>')
            continue
        if line.startswith("║") and box_top is not None:
            inner = html.escape(line[1:].rstrip("║").rstrip())
            out.append(f'<tspan x="{PAD_X + CHAR_W}" y="{y}" '
                       f'fill="{COLORS["err"]}">{inner}</tspan>')
            continue
        out.append(f'<tspan x="{PAD_X}" y="{y}">{render_line(line)}</tspan>')
    out.append("</text>")
    out.extend(frames)
    out.append("</svg>")
    with open(dst, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
