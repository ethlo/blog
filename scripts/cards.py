"""Thumbnails, share cards and descriptions for the posts.

For every post in docs/posts/ this
  - writes a share card to docs/assets/social/<name>.png (the picture link previews show),
  - writes a thumbnail to docs/assets/thumbs/<name>.jpg for posts with an image,
  - fills in `description`, `share` and `image` in the front matter.

A `description` or `image` already in the front matter is kept, so they can be written by hand.
`thumb: assets/...` picks a different image than the post's first one for the thumbnail.

Run it after writing or changing a post:  python3 scripts/cards.py   (needs Pillow)
"""
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
POSTS = DOCS / "posts"
FONTS = Path(__file__).resolve().parent / "fonts"

INK, SURFACE, LINE = (14, 16, 19), (22, 25, 29), (42, 45, 51)
TEXT, MUTED, ACCENT = (255, 255, 255), (169, 173, 181), (255, 90, 31)
W, H, PAD = 1200, 630, 72


def font(name, size, weight):
    f = ImageFont.truetype(str(FONTS / name), size)
    f.set_variation_by_axes([weight])
    return f


def front_matter(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    return (m.group(1), text[m.end():]) if m else ("", text)


def categories(fm):
    m = re.search(r"^categories:\n((?:\s+-\s.*\n?)+)", fm, re.M)
    return [c.strip() for c in re.findall(r"-\s*(.+)", m.group(1))] if m else []


def plain(md):
    md = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", md)
    md = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", md)
    md = re.sub(r"[*_`]", "", md)
    return " ".join(md.split())


def describe(body):
    head = body.split("<!-- more -->")[0]
    paras = [p for p in re.split(r"\n\s*\n", head) if p.strip() and not p.lstrip().startswith(("#", "!", "<", "|"))]
    text = plain(" ".join(paras))
    if len(text) <= 200:
        return text
    cut = text[:197].rsplit(" ", 1)[0].rstrip(",;:")
    return cut + "…"


def set_key(fm, key, value):
    line = f'{key}: "{value}"' if key == "description" else f"{key}: {value}"
    if re.search(rf"^{key}:", fm, re.M):
        return re.sub(rf"^{key}:.*$", lambda _: line, fm, count=1, flags=re.M)
    return fm + "\n" + line


def wrap(draw, text, f, width):
    lines, line = [], ""
    for word in text.split():
        trial = (line + " " + word).strip()
        if draw.textlength(trial, font=f) <= width or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    return lines + [line] if line else lines


def share_card(title, label, picture, out):
    card = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(card)
    text_w = W - 2 * PAD
    if picture:
        panel = 456
        img = ImageOps.fit(Image.open(picture).convert("RGB"), (panel, H), Image.LANCZOS)
        card.paste(img, (W - panel, 0))
        d.line([(W - panel - 1, 0), (W - panel - 1, H)], fill=LINE, width=2)
        text_w = W - panel - 2 * PAD
    mono = font("JetBrainsMono.ttf", 22, 500)
    d.text((PAD, PAD), "ETHLO NOTES", font=mono, fill=MUTED)
    x = PAD + d.textlength("ETHLO NOTES", font=mono)
    if label:
        d.text((x, PAD), "  ·  " + label.upper(), font=mono, fill=ACCENT)
    d.rectangle([PAD, PAD + 46, PAD + 56, PAD + 51], fill=ACCENT)
    for size in ((76, 68, 60, 54, 48, 42) if picture else (96, 88, 80, 72, 64, 56, 48)):
        tf = font("InterTight.ttf", size, 800)
        lines = wrap(d, title, tf, text_w)
        if len(lines) * size * 1.06 <= H - 2 * PAD - 150:
            break
    y = PAD + 96
    for ln in lines:
        d.text((PAD, y), ln, font=tf, fill=TEXT)
        y += int(size * 1.06)
    d.text((PAD, H - PAD - 22), "blog.ethlo.com", font=mono, fill=MUTED)
    card.save(out, optimize=True)


def make_thumb(picture, out):
    """A 4:3 thumbnail. Large screenshots are cropped to their top-left corner, so the
    thumbnail shows readable detail instead of the whole screen shrunk to noise."""
    img = Image.open(picture).convert("RGB")
    if picture.suffix.lower() in (".png", ".webp") and img.width >= 1200:
        w = int(img.width * 0.6)
        img = img.crop((0, 0, w, min(img.height, int(w * 3 / 4))))
    ImageOps.fit(img, (720, 540), Image.LANCZOS).save(out, quality=82, optimize=True, progressive=True)


def main():
    (DOCS / "assets/social").mkdir(parents=True, exist_ok=True)
    (DOCS / "assets/thumbs").mkdir(parents=True, exist_ok=True)
    share_card("Write-ups of things I have built: software, hardware, and where the two meet.",
               "", None, DOCS / "assets/social/default.png")
    for path in sorted(POSTS.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        fm, body = front_matter(text)
        if not fm:
            continue
        name = path.stem
        title = plain(re.search(r"^# (.+)$", body, re.M).group(1))
        cats = categories(fm)
        label = "From the archive" if "Archive" in cats else (next((c for c in cats if c != "Archive"), "") )
        chosen = re.search(r"^thumb:\s*(\S+)", fm, re.M)
        first = re.search(r"!\[[^\]]*\]\(\.\./(assets/[^)\s]+)\)", body)
        src = chosen.group(1) if chosen else (first.group(1) if first else None)
        picture = DOCS / src if src and not src.endswith(".gif") else None

        share_card(title, label, picture, DOCS / f"assets/social/{name}.png")
        fm = set_key(fm, "share", f"assets/social/{name}.png")
        if picture:
            thumb = DOCS / f"assets/thumbs/{name}.jpg"
            make_thumb(picture, thumb)
            if not re.search(r"^image:", fm, re.M):
                fm = set_key(fm, "image", f"assets/thumbs/{name}.jpg")
        if not re.search(r"^description:", fm, re.M):
            fm = set_key(fm, "description", describe(body).replace('"', "'"))
        path.write_text(f"---\n{fm}\n---\n{body}", encoding="utf-8")
        print(f"{name}: share{' + thumb' if picture else ''}")


if __name__ == "__main__":
    main()
