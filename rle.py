"""
Load patterns in RLE (Run Length Encoded) format, the standard way the Life
community shares patterns (see conwaylife.com/wiki).

Example:
    from rle import parse_rle
    cells = parse_rle("x = 3, y = 3\nbob$2bo$3o!")   # a glider
    PATTERNS["my_glider"] = cells
"""
import re


def parse_rle(text):
    """Return a list of (row, col) live-cell offsets from an RLE string."""
    body = "".join(
        line for line in text.splitlines()
        if line.strip() and not line.startswith("#") and not line.startswith("x")
    )
    cells, row, col = [], 0, 0
    for count, tag in re.findall(r"(\d*)([bo$!])", body):
        n = int(count) if count else 1
        if tag == "b":
            col += n
        elif tag == "o":
            cells.extend((row, col + i) for i in range(n))
            col += n
        elif tag == "$":
            row += n
            col = 0
        else:  # "!"
            break
    return cells


def to_rle(cells):
    """Encode (row, col) cells back into RLE."""
    if not cells:
        return "x = 0, y = 0\n!"
    live = set(cells)
    h = max(r for r, _ in live) + 1
    w = max(c for _, c in live) + 1
    out = []
    for r in range(h):
        run, prev = 0, None
        for c in range(w):
            ch = "o" if (r, c) in live else "b"
            if ch == prev:
                run += 1
            else:
                if prev:
                    out.append((str(run) if run > 1 else "") + prev)
                prev, run = ch, 1
        if prev == "o":
            out.append((str(run) if run > 1 else "") + prev)
        out.append("$")
    return f"x = {w}, y = {h}\n" + "".join(out)[:-1] + "!"
