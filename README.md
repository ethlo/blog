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

## Build

```bash
uv venv && uv pip install -r .github/requirements.txt
.venv/bin/zensical serve
```

A push to `main` builds and publishes the site with GitHub Pages (`.github/workflows/pages.yml`).
The look follows ethlo.com and lives in `docs/stylesheets/extra.css`.
