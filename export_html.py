"""
Export a simulation as a single self-contained HTML file you can open in any
browser and share. Pre-computes the frames in Python, plays them on a canvas.

    python3 export_html.py --pattern glider_gun --generations 200 -o gun.html
"""
import argparse
import json

from life import (ALIVE, PATTERNS, grid_from_pattern, next_generation,
                  random_grid)

TEMPLATE = """<!doctype html><meta charset="utf-8"><title>Game of Life</title>
<style>body{margin:0;background:#0b0f14;color:#9fb;font:14px monospace;text-align:center}
canvas{margin-top:16px;image-rendering:pixelated}</style>
<div id=hud></div><canvas id=c></canvas>
<script>
const F=__FRAMES__,W=__W__,H=__H__,S=__S__;
const c=document.getElementById('c'),x=c.getContext('2d'),hud=document.getElementById('hud');
c.width=W*S;c.height=H*S;let i=0;
function draw(){x.fillStyle='#0b0f14';x.fillRect(0,0,c.width,c.height);x.fillStyle='#4ff0a0';
for(const k of F[i]){x.fillRect((k%W)*S,Math.floor(k/W)*S,S-1,S-1)}
hud.textContent='Generation '+i+' | Live cells: '+F[i].length;i=(i+1)%F.length}
setInterval(draw,__DELAY__);draw();
</script>"""


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--width", type=int, default=60)
    p.add_argument("--height", type=int, default=40)
    p.add_argument("--generations", type=int, default=200)
    p.add_argument("--pattern", choices=list(PATTERNS))
    p.add_argument("--scale", type=int, default=12)
    p.add_argument("--delay", type=int, default=80, help="ms per frame")
    p.add_argument("-o", "--output", default="life.html")
    a = p.parse_args()

    g = (grid_from_pattern(a.width, a.height, a.pattern) if a.pattern
         else random_grid(a.width, a.height))
    frames = []
    for _ in range(a.generations):
        frames.append([r * a.width + c for r in range(a.height)
                       for c in range(a.width) if g[r][c] == ALIVE])
        g = next_generation(g)

    html = (TEMPLATE.replace("__FRAMES__", json.dumps(frames, separators=(",", ":")))
            .replace("__W__", str(a.width)).replace("__H__", str(a.height))
            .replace("__S__", str(a.scale)).replace("__DELAY__", str(a.delay)))
    with open(a.output, "w") as f:
        f.write(html)
    print(f"Wrote {a.output} ({len(frames)} frames)")


if __name__ == "__main__":
    main()
