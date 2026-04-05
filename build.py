#!/usr/bin/env python3
"""Build the AI Primer as a static HTML site into docs/.

Reads toc.md for page order, converts each .md to HTML,
wraps in a template with sidebar navigation. Uses Fira Code
for code blocks (ASCII diagrams render correctly).

Usage:
    python3 build.py
"""

import re
import os
import shutil
from pathlib import Path

try:
    import mistune
except ImportError:
    print("Error: mistune not installed. Run: pip install mistune")
    exit(1)

ROOT = Path(__file__).parent
DOCS_DIR = ROOT / "docs"


def parse_summary():
    """Returns list of (title, filepath) from toc.md."""
    pages = []
    with open(ROOT / "toc.md") as f:
        for line in f:
            m = re.match(r'\* \[(.+?)\]\((.+?)\)', line)
            if m:
                pages.append((m.group(1), m.group(2)))
    return pages



def fix_internal_links(html, pages):
    """Convert .md links to .html links."""
    for _, path in pages:
        md_name = os.path.basename(path)
        html_name = md_name.replace('.md', '.html')
        href = '/' if html_name == 'index.html' else html_name
        # Match both markdown-style (name) and HTML href="name"
        html = html.replace(f'({md_name})', f'({href})')
        html = html.replace(f'({path})', f'({href})')
        html = html.replace(f'"{md_name}"', f'"{href}"')
        html = html.replace(f'"{path}"', f'"{href}"')
    return html


def render_page(md_text):
    """Convert markdown to HTML."""
    renderer = mistune.create_markdown(escape=False, plugins=['table'])
    return renderer(md_text)


def html_name_for(path):
    return os.path.basename(path).replace('.md', '.html')


def href_for(path):
    name = html_name_for(path)
    return '/' if name == 'index.html' else name


def build_sidebar(pages, current_idx):
    """Build sidebar navigation HTML with chapter numbers."""
    items = []
    for i, (title, path) in enumerate(pages):
        # Skip index — the sidebar logo already links home
        if os.path.basename(path) == 'index.md':
            continue
        href = href_for(path)
        cls = ' class="active"' if i == current_idx else ''
        basename = os.path.basename(path)
        num_match = re.match(r'(\d+)-', basename)
        if num_match:
            num = int(num_match.group(1))
            # Strip leading "N. " from title since we show the number separately
            short_title = re.sub(r'^\d+\.\s*', '', title)
            items.append(
                f'<a href="{href}"{cls}>'
                f'<span class="ch-num">{num}.</span>{short_title}</a>'
            )
        else:
            items.append(f'<a href="{href}"{cls}>{title}</a>')
    items.append('<a href="/" class="sidebar-about">About</a>')
    return '\n'.join(items)


def build_prev_next(pages, current_idx):
    """Build previous/next navigation."""
    prev_html = ''
    next_html = ''
    if current_idx > 0:
        t, p = pages[current_idx - 1]
        prev_html = f'<a href="{href_for(p)}">← {t}</a>'
    if current_idx < len(pages) - 1:
        t, p = pages[current_idx + 1]
        next_html = f'<a href="{href_for(p)}">{t} →</a>'
    return prev_html, next_html


def build_brand_lockup(extra_class=''):
    classes = "logo-mark"
    if extra_class:
        classes += f" {extra_class}"
    return f'aiaiai<span class="{classes}">·&gt;</span>'


def strip_first_h1(html):
    """Remove the first H1 from rendered HTML."""
    return re.sub(r'<h1>.*?</h1>\s*', '', html, count=1, flags=re.DOTALL)


TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — AI Primer</title>
  <link rel="icon" type="image/svg+xml" href="favicon.svg">
  <script>(function(){{var t=localStorage.getItem('theme')||(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light');document.documentElement.setAttribute('data-theme',t)}})();</script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700;800&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&family=Fira+Code:wght@400&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="style.css?v=2">
</head>
<body>
  <div class="mobile-overlay"></div>
  <button class="mobile-menu-btn" aria-label="Toggle navigation">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
  </button>
  <nav class="sidebar">
    <div class="sidebar-header">
      <a href="/" class="sidebar-logo">{brand}</a>
    </div>
    <div class="sidebar-links">
      {sidebar}
    </div>
    <div class="sidebar-footer">
      <button class="theme-toggle" aria-label="Toggle theme">
        <svg class="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
        <svg class="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>
      </button>
    </div>
  </nav>
  <main class="content">
    <article>{hero_title}{content}</article>
    <div class="prev-next">
      <div>{prev}</div>
      <div>{next}</div>
    </div>
    <footer class="license">
      Licensed under <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>
    </footer>
  </main>
  <script>
    (function() {{
      document.querySelectorAll('pre code').forEach(function(el) {{
        el.innerHTML = el.innerHTML.replace(/([┌┐└┘│─├┤┬┴┼▼▶◀═╔╗╚╝║╠╣╦╩╬→←↓↑▲►◄●·]+)/g, '<span class="dc">$1</span>');
      }});
      var btn = document.querySelector('.mobile-menu-btn');
      var sidebar = document.querySelector('.sidebar');
      var overlay = document.querySelector('.mobile-overlay');
      btn.addEventListener('click', function() {{
        sidebar.classList.toggle('open');
        overlay.classList.toggle('open');
      }});
      overlay.addEventListener('click', function() {{
        sidebar.classList.remove('open');
        overlay.classList.remove('open');
      }});
      document.querySelector('.theme-toggle').addEventListener('click', function() {{
        var d = document.documentElement;
        var next = d.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
        d.setAttribute('data-theme', next);
        localStorage.setItem('theme', next);
      }});
    }})();
  </script>
</body>
</html>
"""


def main():
    pages = parse_summary()

    # Clean and create docs/
    if DOCS_DIR.exists():
        shutil.rmtree(DOCS_DIR, ignore_errors=True)
    DOCS_DIR.mkdir(exist_ok=True)

    # Copy static files
    for name in ["favicon.svg", "CNAME", "style.css"]:
        with open(ROOT / "static" / name) as src, open(DOCS_DIR / name, "w") as dst:
            dst.write(src.read())

    # Build each page from toc
    for i, (title, path) in enumerate(pages):
        # Index page is built separately below
        if os.path.basename(path) == 'index.md':
            continue
        md_path = ROOT / path
        if not md_path.exists():
            print(f"  SKIP {path} (not found)")
            continue

        with open(md_path) as f:
            md_text = f.read()

        content = render_page(md_text)
        content = fix_internal_links(content, pages)
        sidebar = build_sidebar(pages, i)
        prev, next_ = build_prev_next(pages, i)

        html = TEMPLATE.format(
            title=title,
            brand=build_brand_lockup(),
            hero_title='',
            sidebar=sidebar,
            content=content,
            prev=prev,
            next=next_,
        )

        out_path = DOCS_DIR / html_name_for(path)
        with open(out_path, 'w') as f:
            f.write(html)
        print(f"  {out_path.name}")

    # Build index from sections/index.md
    index_src = ROOT / "sections" / "index.md"
    if index_src.exists():
        with open(index_src) as f:
            md_text = f.read()
        content = render_page(md_text)
        content = fix_internal_links(content, pages)
        content = strip_first_h1(content)
        sidebar = build_sidebar(pages, -1)

        html = TEMPLATE.format(
            title="aiaiai",
            brand=build_brand_lockup(),
            hero_title=f"<h1>{build_brand_lockup('title-logo-mark')}AI Primer</h1>",
            sidebar=sidebar,
            content=content,
            prev='',
            next=f'<a href="{href_for(pages[1][1])}">{pages[1][0]} →</a>',
        )
        with open(DOCS_DIR / "index.html", 'w') as f:
            f.write(html)
        print("  index.html")

    print(f"\nDone: {len(list(DOCS_DIR.glob('*.html')))} pages in docs/")


if __name__ == "__main__":
    main()
