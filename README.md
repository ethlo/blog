# blog.ethlo.com

Notes from the bench: write-ups of things I have built, what I measured and what broke.

A post is a Markdown file in `docs/posts/` with a date and categories in its front matter:

```markdown
---
date: 2026-11-17
categories:
  - 3D printing
---

# The title states the finding

The first paragraph is shown in the list.

<!-- more -->

The rest of the post.
```

`draft: true` in the front matter keeps a post out of the published site.

## Pictures and link previews

After writing or changing a post, run:

```bash
python3 scripts/cards.py   # needs Pillow
```

For every post it makes a share card (`docs/assets/social/`, the picture LinkedIn, Slack and others
show for a link) and, for posts with an image, a thumbnail for the list (`docs/assets/thumbs/`).
It also fills in `description`, `share` and `image` in the front matter. A `description` written by
hand is kept; `thumb: assets/...` picks another image for the thumbnail than the post's first one.

The list templates are in `overrides/`: `partials/post.html` is one post in the list,
`main.html` adds the link-preview tags. The three "Start here" posts are in `docs/index.md`.

## Build

```bash
uv venv && uv pip install -r .github/requirements.txt
.venv/bin/zensical serve
```

A push to `main` builds and publishes the site with GitHub Pages (`.github/workflows/pages.yml`).
The look follows ethlo.com and lives in `docs/stylesheets/extra.css`.
