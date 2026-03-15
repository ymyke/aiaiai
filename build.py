#!/usr/bin/env python3
"""
Builds the AI Primer as a multi-page website.

Usage:  ./build.sh   (or:  python3 build.py)
Output: site/  folder with self-contained HTML files
Needs:  pandoc
"""

import re
import subprocess
import sys
import shutil
from pathlib import Path

DIR = Path(__file__).parent.resolve()
SITE = DIR / "site"

if not shutil.which("pandoc"):
    sys.exit("Error: pandoc required  (brew install pandoc / apt install pandoc)")

# ── Read sources ─────────────────────────────────────────

def read_file(name):
    return (DIR / name).read_text().replace("\r\n", "\n").replace("\r", "\n")

primer_md = read_file("primer.md")
uth_md = read_file("uth.md")

PARTS = [
    ("Part I: The Evolution", "part1-the-evolution.md"),
    ("Part II: What the Model Sees", "part2-what-the-model-sees.md"),
    ("Part III: In Practice", "part3-in-practice.md"),
]

# ── Helpers ──────────────────────────────────────────────

def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def md_to_html(md):
    md = md.replace("uth.md#", "under-the-hood.html#")
    r = subprocess.run(
        ["pandoc", "-f", "markdown", "-t", "html5", "--wrap=none",
         "--syntax-highlighting=kate"],
        input=md, capture_output=True, text=True, check=True,
    )
    return r.stdout


def promote_headings(md):
    """Promote ## → # and ### → ## for standalone section pages."""
    lines = md.split("\n")
    out = []
    first_h2 = True
    in_fence = False
    for line in lines:
        if line.startswith("```"):
            in_fence = not in_fence
        if in_fence:
            out.append(line)
            continue
        if first_h2 and line.startswith("## "):
            out.append(line[1:])  # ## → # (drop one #)
            first_h2 = False
        elif line.startswith("### "):
            out.append(line[1:])  # ### → ##
        else:
            out.append(line)
    return "\n".join(out)


# ── Parse sections ───────────────────────────────────────

def parse_part(md, part_title):
    sections = []
    for chunk in re.split(r"(?=^## )", md, flags=re.MULTILINE):
        chunk = chunk.strip()
        if not chunk.startswith("## "):
            continue
        heading = chunk.split("\n", 1)[0].lstrip("# ").strip()
        m = re.match(r"(\d+)\.\s+(.+?)(?:\s*—\s*(.+))?$", heading)
        if m:
            num = int(m.group(1))
            title = m.group(2).strip()
            subtitle = (m.group(3) or "").strip()
            slug = f"{num:02d}-{slugify(title)}"
        else:
            num, title, subtitle = None, heading, ""
            slug = slugify(heading)

        sections.append(dict(
            num=num, title=title, subtitle=subtitle, heading=heading,
            slug=slug, filename=f"{slug}.html", part=part_title, md=chunk,
        ))
    return sections


# ── Build page list ──────────────────────────────────────

pages = []
for part_title, filename in PARTS:
    pages += parse_part(read_file(filename), part_title)

pages.append(dict(
    num=None, title="Under the Hood", subtitle="", heading="Under the Hood",
    slug="under-the-hood", filename="under-the-hood.html", part="Appendix",
    md=uth_md,
))

glossary_match = re.search(r"(## Glossary.*)", primer_md, re.DOTALL)
pages.append(dict(
    num=None, title="Glossary", subtitle="", heading="Glossary",
    slug="glossary", filename="glossary.html", part="Appendix",
    md=glossary_match.group(1) if glossary_match else "## Glossary",
))

# Section descriptions from primer.md (for index page)
descriptions = {}
for m in re.finditer(r"(\d+)\.\s+\*\*(.+?)\*\*\s*—\s*(.+)", primer_md):
    descriptions[int(m.group(1))] = m.group(3).strip()

# Part subtitles from blockquotes
part_subtitles = {}
for pt, fn in PARTS:
    m = re.search(r"^>\s*(.+?)$", read_file(fn), re.MULTILINE)
    if m:
        part_subtitles[pt] = m.group(1).strip()


# ── CSS ──────────────────────────────────────────────────

CSS = """\
:root {
  --bg: #ffffff;
  --text: #0f172a;
  --muted: #64748b;
  --accent: #2563eb;
  --accent-hover: #1d4ed8;
  --accent-light: #eff6ff;
  --border: #e2e8f0;
  --code-bg: #f8fafc;
}

*, *::before, *::after { box-sizing: border-box; }

html { font-size: 17px; scroll-behavior: smooth; }

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
               "Helvetica Neue", Arial, sans-serif;
  color: var(--text);
  background: var(--bg);
  line-height: 1.75;
  margin: 0 auto;
  padding: 2rem 1.5rem 3rem;
  max-width: 720px;
}

/* ── Breadcrumb ── */
.breadcrumb {
  font-size: 0.85rem;
  color: var(--muted);
  margin-bottom: 1.5rem;
}
.breadcrumb a { color: var(--accent); text-decoration: none; }
.breadcrumb a:hover { text-decoration: underline; }
.breadcrumb .sep { margin: 0 0.35rem; color: var(--border); }

/* ── Headings ── */
h1 {
  font-size: 1.9rem;
  font-weight: 700;
  margin: 0 0 1.25rem;
  line-height: 1.3;
  padding-bottom: 0.4rem;
  border-bottom: 2px solid var(--border);
}
h2 {
  font-size: 1.4rem;
  font-weight: 600;
  color: var(--accent);
  margin: 2.5rem 0 0.75rem;
  line-height: 1.35;
}
h3 {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 1.5rem 0 0.5rem;
}

/* ── Prose ── */
p { margin: 0.65rem 0; }
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; color: var(--accent-hover); }
strong { font-weight: 600; }

blockquote {
  border-left: 4px solid var(--accent);
  background: var(--accent-light);
  margin: 1.25rem 0;
  padding: 0.6rem 1rem;
  color: var(--muted);
  font-style: italic;
}
blockquote p { margin: 0.25rem 0; }

hr { border: none; border-top: 1px solid var(--border); margin: 2.5rem 0; }

/* ── Lists ── */
ul, ol { margin: 0.65rem 0; padding-left: 1.5rem; }
li { margin: 0.2rem 0; }
li > ul, li > ol { margin: 0.15rem 0; }

/* ── Code ── */
code {
  font-family: "SF Mono", "Fira Code", "Cascadia Code", "JetBrains Mono",
               Consolas, "Liberation Mono", Menlo, monospace;
  font-size: 0.88em;
  background: var(--code-bg);
  padding: 0.15em 0.35em;
  border-radius: 4px;
  border: 1px solid var(--border);
}
pre {
  background: var(--code-bg);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 1rem 1.25rem;
  overflow-x: auto;
  margin: 1.25rem 0;
  line-height: 1.5;
}
pre code { background: none; border: none; padding: 0; font-size: 0.82rem; }

/* ── Tables ── */
table { width: 100%; border-collapse: collapse; margin: 1.25rem 0; font-size: 0.93rem; }
th, td { padding: 0.5rem 0.75rem; text-align: left; border-bottom: 1px solid var(--border); }
th { background: var(--code-bg); font-weight: 600; white-space: nowrap; }

/* ── Page navigation ── */
.page-nav {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-top: 3rem;
  padding-top: 1.5rem;
  border-top: 2px solid var(--border);
  gap: 1rem;
}
.page-nav a {
  text-decoration: none;
  max-width: 48%;
  line-height: 1.4;
}
.page-nav a:hover { text-decoration: none; }
.page-nav a:hover .nav-title { text-decoration: underline; }
.page-nav .nav-label {
  display: block;
  font-size: 0.75rem;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.2rem;
}
.page-nav .nav-title {
  display: block;
  color: var(--accent);
  font-weight: 600;
  font-size: 0.95rem;
}
.page-nav .next { text-align: right; margin-left: auto; }

/* ── Version ── */
.version {
  margin-top: 2.5rem;
  color: var(--muted);
  font-size: 0.78rem;
  text-align: center;
}

@media print {
  .breadcrumb, .page-nav { display: none; }
  body { max-width: none; padding: 1cm; font-size: 11pt; }
  pre { white-space: pre-wrap; }
}
"""

INDEX_EXTRA_CSS = """\
.hero {
  text-align: center;
  margin-bottom: 3rem;
  padding-bottom: 2rem;
  border-bottom: 2px solid var(--accent);
}
.hero h1 { font-size: 2.4rem; margin-bottom: 0.25rem; border: none; padding: 0; }
.hero .subtitle { color: var(--muted); font-size: 1.05rem; margin: 0.4rem 0; }
.hero .note { font-style: italic; color: var(--muted); font-size: 0.88rem; margin-top: 1rem; }

.part-section { margin-bottom: 2.5rem; }
.part-section h2 { font-size: 1.3rem; margin-bottom: 0.2rem; border: none; padding: 0; }
.part-desc { color: var(--muted); font-size: 0.9rem; margin: 0 0 0.5rem; }

.toc-list { list-style: none; padding: 0; }
.toc-list li {
  margin: 0;
  border-radius: 6px;
  transition: background 0.15s;
}
.toc-list li:hover { background: var(--accent-light); }
.toc-list a {
  display: block;
  padding: 0.55rem 0.85rem;
  text-decoration: none;
  color: var(--text);
}
.toc-list a:hover { text-decoration: none; }
.toc-list .num { color: var(--accent); font-weight: 700; min-width: 1.8em; display: inline-block; }
.toc-list .section-title { font-weight: 600; }
.toc-list .section-desc { display: block; color: var(--muted); font-size: 0.86rem; margin-top: 0.1rem; padding-left: 1.8em; }

.appendix-list { list-style: none; padding: 0; }
.appendix-list li { margin: 0; }
.appendix-list a {
  display: block;
  padding: 0.55rem 0.85rem;
  border-radius: 6px;
  color: var(--accent);
  font-weight: 600;
  transition: background 0.15s;
}
.appendix-list a:hover { background: var(--accent-light); text-decoration: none; }
"""


# ── Render pages ─────────────────────────────────────────

def html_escape(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render_page(page, prev_page, next_page):
    md = promote_headings(page["md"]) if page["num"] is not None else page["md"]
    body = md_to_html(md)

    bc = (
        '<nav class="breadcrumb">'
        '<a href="index.html">AI Primer</a>'
        '<span class="sep">&rsaquo;</span>'
        f'<span>{html_escape(page["part"])}</span>'
        '</nav>'
    )

    nav_items = []
    if prev_page:
        nav_items.append(
            f'<a class="prev" href="{prev_page["filename"]}">'
            f'<span class="nav-label">&larr; Previous</span>'
            f'<span class="nav-title">{html_escape(prev_page["title"])}</span></a>'
        )
    else:
        nav_items.append('<a class="prev" href="index.html">'
                         '<span class="nav-label">&larr; Back</span>'
                         '<span class="nav-title">Overview</span></a>')
    if next_page:
        nav_items.append(
            f'<a class="next" href="{next_page["filename"]}">'
            f'<span class="nav-label">Next &rarr;</span>'
            f'<span class="nav-title">{html_escape(next_page["title"])}</span></a>'
        )
    else:
        nav_items.append(
            '<a class="next" href="index.html">'
            '<span class="nav-label">Back to</span>'
            '<span class="nav-title">Overview</span></a>'
        )

    nav = f'<nav class="page-nav">{"".join(nav_items)}</nav>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html_escape(page["heading"])} &mdash; AI Primer</title>
<style>{CSS}</style>
</head>
<body>
{bc}
<main>
{body}
</main>
{nav}
<p class="version">AI Primer &middot; v.3-en &middot; March 2026</p>
</body>
</html>"""


def render_index():
    # Group pages by part
    groups = {}
    for p in pages:
        groups.setdefault(p["part"], []).append(p)

    toc = ""
    for pt, _ in PARTS:
        subtitle = part_subtitles.get(pt, "")
        items = groups.get(pt, [])
        lis = ""
        for item in items:
            desc = descriptions.get(item["num"], item["subtitle"])
            desc_html = f'<span class="section-desc">{html_escape(desc)}</span>' if desc else ""
            lis += (
                f'<li><a href="{item["filename"]}">'
                f'<span class="num">{item["num"]}.</span>'
                f'<span class="section-title">{html_escape(item["title"])}</span>'
                f'{desc_html}</a></li>\n'
            )
        toc += (
            f'<section class="part-section">'
            f'<h2>{html_escape(pt)}</h2>'
            f'<p class="part-desc">{html_escape(subtitle)}</p>'
            f'<ul class="toc-list">{lis}</ul>'
            f'</section>\n'
        )

    appendix = groups.get("Appendix", [])
    app_lis = "".join(
        f'<li><a href="{p["filename"]}">{html_escape(p["title"])}</a></li>\n'
        for p in appendix
    )
    toc += (
        f'<section class="part-section">'
        f'<h2>Appendix</h2>'
        f'<ul class="appendix-list">{app_lis}</ul>'
        f'</section>\n'
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI Primer: The Evolution of AI Systems</title>
<style>{CSS}
{INDEX_EXTRA_CSS}</style>
</head>
<body>
<div class="hero">
  <h1>AI Primer</h1>
  <p class="subtitle">The Evolution of AI Systems</p>
  <p class="subtitle">A non-technical guide to how AI systems actually work.<br>
  From fundamentals to agents &mdash; step by step.</p>
  <p class="note">This guide deliberately simplifies. Some details are omitted,
  some analogies are imperfect. The goal is a useful mental model, not a textbook.</p>
</div>
{toc}
<p class="version">v.3-en &mdash; March 2026</p>
</body>
</html>"""


# ── Generate ─────────────────────────────────────────────

SITE.mkdir(exist_ok=True)

for f in SITE.glob("*.html"):
    f.unlink()

for i, page in enumerate(pages):
    prev_p = pages[i - 1] if i > 0 else None
    next_p = pages[i + 1] if i < len(pages) - 1 else None
    (SITE / page["filename"]).write_text(render_page(page, prev_p, next_p))

(SITE / "index.html").write_text(render_index())

print(f"✓ Built {len(pages) + 1} pages in site/")
