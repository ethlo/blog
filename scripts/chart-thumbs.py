#!/usr/bin/env python3
"""List pictures for posts whose only picture is a chart or diagram (inline SVG) or a GIF.

cards.py makes the thumbnail from a post's first Markdown image, so posts with just an inline
<svg> chart, or only a GIF, had none in the list. This renders the post's first SVG on the
site's dark surface (or takes the GIF's first frame) into docs/assets/thumbs/<post>.jpg, 4:3
like the rest, and sets `image:` in the front matter. Posts that already have an `image:` are
left alone; delete the line to make it again.

    python3 scripts/chart-thumbs.py        # needs Pillow, and Playwright with Chromium for SVG
"""
import re
from pathlib import Path

from PIL import Image, ImageChops, ImageOps

DOCS = Path(__file__).resolve().parent.parent / "docs"
POSTS = DOCS / "posts"
W, H = 720, 540            # the list thumbnail, as cards.py makes it
SCALE = 3                  # rendered large, then cropped to the chart and scaled to fill
SURFACE, INK = "#16191D", "#E4E6EA"   # --kw-surface and --md-default-fg-color (extra.css)

PAGE = """<!doctype html><html><head><meta charset="utf-8"><style>
html, body {{ margin: 0; width: {w}px; height: {h}px; background: {bg}; color: {fg};
  font-family: Inter, "Helvetica Neue", Arial, sans-serif; }}
body {{ display: flex; align-items: center; justify-content: center; }}
.chart {{ width: {cw}px; max-height: {ch}px; display: flex; justify-content: center; }}
.chart svg {{ width: 100% !important; max-width: none !important; height: auto !important;
  max-height: {ch}px; }}
</style></head><body><div class="chart">{svg}</div></body></html>"""


def front_matter(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    return (m.group(1), text[m.end():]) if m else (None, text)


def render_svg(page, svg, out):
    """Render on the site's surface, crop to what was drawn, and scale that to fill the
    thumbnail with a margin: a short, wide bar chart gets as big as a square diagram."""
    page.set_content(PAGE.format(w=W, h=H, bg=SURFACE, fg=INK, cw=W - 72, ch=H - 72, svg=svg))
    tmp = out.with_suffix(".png")
    page.screenshot(path=str(tmp))
    img = Image.open(tmp).convert("RGB")
    tmp.unlink()
    box = ImageChops.difference(img, Image.new("RGB", img.size, SURFACE)).getbbox() or (0, 0, *img.size)
    chart = img.crop(box)
    fit = min(W * 0.9 / chart.width, H * 0.8 / chart.height)
    chart = chart.resize((max(1, round(chart.width * fit)), max(1, round(chart.height * fit))), Image.LANCZOS)
    canvas = Image.new("RGB", (W, H), SURFACE)
    canvas.paste(chart, ((W - chart.width) // 2, (H - chart.height) // 2))
    canvas.save(out, quality=86, optimize=True, progressive=True)


def gif_frame(gif, out):
    img = Image.open(gif).convert("RGB")       # the first frame
    ImageOps.fit(img, (W, H), Image.LANCZOS).save(out, quality=82, optimize=True, progressive=True)


def main():
    todo = []
    for path in sorted(POSTS.glob("*.md")):
        fm, body = front_matter(path.read_text(encoding="utf-8"))
        if fm is None or re.search(r"^image:", fm, re.M):
            continue
        svg = re.search(r"<svg\b.*?</svg>", body, re.S)
        gif = re.search(r"!\[[^\]]*\]\(\.\./(assets/[^)\s]+\.gif)\)", body)
        if svg or gif:
            todo.append((path, fm, body, svg.group(0) if svg else None, gif.group(1) if gif else None))
    if not todo:
        print("nothing to do")
        return

    browser = page = None
    try:
        for path, fm, body, svg, gif in todo:
            out = DOCS / f"assets/thumbs/{path.stem}.jpg"
            if svg:
                if page is None:
                    from playwright.sync_api import sync_playwright
                    pw = sync_playwright().start()
                    browser = pw.chromium.launch()
                    page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=SCALE)
                render_svg(page, svg, out)
            else:
                gif_frame(DOCS / gif, out)
            fm = fm.rstrip("\n") + f"\nimage: assets/thumbs/{path.stem}.jpg"
            path.write_text(f"---\n{fm}\n---\n{body}", encoding="utf-8")
            print(f"{path.stem}: {'chart' if svg else 'gif'}")
    finally:
        if browser:
            browser.close()


if __name__ == "__main__":
    main()
