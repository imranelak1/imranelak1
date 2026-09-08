"""Build the self-contained SVG banner. Requires fonttools (pip install fonttools)."""

from pathlib import Path
import math
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

ROOT = Path(__file__).resolve().parents[1]
FONT = instantiateVariableFont(TTFont(ROOT / "assets/fonts/SpaceGrotesk.ttf"), {"wght": 600})
GLYPHS = FONT.getGlyphSet()
CMAP = FONT.getBestCmap()
UNITS = FONT["head"].unitsPerEm


def lettering(text, x, y, size, color, extra=""):
    pen = SVGPathPen(GLYPHS)
    cursor = x
    scale = size / UNITS
    for char in text:
        name = CMAP[ord(char)]
        GLYPHS[name].draw(TransformPen(pen, (scale, 0, 0, -scale, cursor, y)))
        cursor += GLYPHS[name].width * scale
    return f'<path fill="{color}" d="{pen.getCommands()}" {extra}/>'


def point(t, angle):
    # A trefoil tube, projected into the right side of the banner.
    radius = 2 + .72 * math.cos(3 * t)
    x = (radius + .23 * math.cos(angle)) * math.cos(2 * t)
    y = (radius + .23 * math.cos(angle)) * math.sin(2 * t)
    z = .85 * math.sin(3 * t) + .23 * math.sin(angle)
    tilt = .78
    yy = y * math.cos(tilt) - z * math.sin(tilt)
    zz = y * math.sin(tilt) + z * math.cos(tilt)
    xx = x * math.cos(.24) + zz * math.sin(.24)
    return 735 + xx * 66, 186 + yy * 66


curves = []
for index in range(24):
    points = [point(i * 2 * math.pi / 300, index * 2 * math.pi / 24) for i in range(301)]
    path = "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in points) + " Z"
    curves.append(f'<path d="{path}" fill="none" stroke="#bb86fc" stroke-width=".75" opacity=".28"/>')
    if index % 4 == 0:
        curves.append(f'<path class="thread" pathLength="1000" d="{path}" fill="none" stroke="#d7b8ff" stroke-width="1" stroke-dasharray="90 910" style="animation-delay:-{index / 2}s"/>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="380" viewBox="0 0 960 380" role="img" aria-labelledby="title desc">
<title id="title">Imrane Lakniti — full-stack developer</title>
<desc id="desc">Charcoal banner with violet lettering and an animated trefoil wireframe. Java, Spring Boot, TypeScript and React.</desc>
<style>
.thread {{ animation: travel 14s linear infinite; }}
.knot {{ transform-origin: 735px 186px; animation: turn 18s ease-in-out infinite; }}
.phrase {{ animation: phrase 12s infinite; opacity: 0; }}
.first {{ opacity: 1; }}
@keyframes travel {{ to {{ stroke-dashoffset: -1000; }} }}
@keyframes turn {{ 0%, 100% {{ transform: rotate(-6deg); }} 50% {{ transform: rotate(6deg); }} }}
@keyframes phrase {{ 0%, 27% {{ opacity: 1; }} 31%, 96% {{ opacity: 0; }} 100% {{ opacity: 1; }} }}
@media (prefers-reduced-motion: reduce) {{ .thread, .knot, .phrase {{ animation: none; }} .phrase {{ opacity: 0; }} .first {{ opacity: 1; }} }}
@media (max-width: 500px) {{ .knot {{ opacity: .65; }} }}
</style>
<rect width="960" height="380" fill="#121212"/>
<g class="knot">{''.join(curves)}</g>
{lettering('Imrane', 48, 112, 72, '#e1e1e1')}
{lettering('Lakniti.', 42, 212, 112, '#bb86fc')}
{lettering('Full-stack developer', 48, 264, 25, '#e1e1e1')}
<path d="M48 292 H490" stroke="#363139"/>
{lettering('Java / Spring Boot', 48, 328, 19, '#bcb6c4', 'class="phrase first"')}
{lettering('TypeScript / React / Next.js', 48, 328, 19, '#bcb6c4', 'class="phrase" style="animation-delay:-8s"')}
{lettering('From the API to the interface.', 48, 328, 19, '#bcb6c4', 'class="phrase" style="animation-delay:-4s"')}
</svg>
'''
(ROOT / "assets/banner.svg").write_text(svg, encoding="utf-8")
print(f"Built assets/banner.svg ({len(svg):,} bytes)")
