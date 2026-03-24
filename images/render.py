#!/usr/bin/env python3
"""Render diagram images for the AI Primer.

Finds <!-- diagram:NAME ... --> comments in all markdown files under sections/
and renders the contained text as PNG images using Fira Code.

Markdown format:
    <!-- diagram:01-plain-llm-diagram1
    ```
            "The capital of France is"
                           │
                           ▼
                  ┌───────────────┐
                  │      LLM      │
                  └───────────────┘
    ```
    -->
    ![The Plain LLM](../images/01-plain-llm-diagram1.png)

Usage:
    python3 images/render.py          # render all diagrams
    python3 images/render.py --list   # list all diagrams without rendering
"""

import re
import sys
import glob
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Config
SCRIPT_DIR = Path(__file__).parent
SECTIONS_DIR = SCRIPT_DIR.parent / "sections"
OUTPUT_DIR = SCRIPT_DIR
FONT_PATH = SCRIPT_DIR / "FiraCode.ttf"
FONT_SIZE = 28
PADDING = 48
LINE_HEIGHT = 1.5
BG_COLOR = "white"
FG_COLOR = "#1a1a1a"

# Pattern: <!-- diagram:NAME\n```\n...content...\n```\n-->
DIAGRAM_PATTERN = re.compile(
    r"<!-- diagram:(\S+)\s*\n```\n(.*?)```\n-->",
    re.DOTALL,
)


def extract_all_diagrams(sections_dir):
    """Extract all <!-- diagram:NAME --> blocks from all markdown files."""
    diagrams = []
    for md_path in sorted(glob.glob(str(sections_dir / "*.md"))):
        with open(md_path) as f:
            content = f.read()
        diagrams.extend(DIAGRAM_PATTERN.findall(content))
    return diagrams


def render_text_to_image(text, font, canvas_width):
    """Render monospaced text to a fixed-width PIL Image."""
    lines = text.rstrip("\n").split("\n")
    line_h = int(FONT_SIZE * LINE_HEIGHT)

    img = Image.new("RGB", (canvas_width, line_h * len(lines) + PADDING * 2), BG_COLOR)
    draw = ImageDraw.Draw(img)

    y = PADDING
    for line in lines:
        draw.text((PADDING, y), line, fill=FG_COLOR, font=font)
        y += line_h

    return img


def compute_canvas_width(diagrams, font):
    """Find the widest diagram and use that as canvas width for all."""
    max_w = 0
    for _, text in diagrams:
        for line in text.rstrip("\n").split("\n"):
            bbox = font.getbbox(line)
            max_w = max(max_w, bbox[2] - bbox[0])
    return max_w + PADDING * 2


def main():
    list_only = "--list" in sys.argv

    if not FONT_PATH.exists():
        print(f"Error: Font not found at {FONT_PATH}")
        print("Download Fira Code TTF and place it next to this script.")
        sys.exit(1)

    font = ImageFont.truetype(str(FONT_PATH), FONT_SIZE)
    diagrams = extract_all_diagrams(SECTIONS_DIR)

    if not diagrams:
        print(f"No <!-- diagram:NAME --> blocks found in {SECTIONS_DIR}/*.md")
        sys.exit(1)

    if list_only:
        for name, _ in diagrams:
            out_file = OUTPUT_DIR / f"{name}.png"
            status = "exists" if out_file.exists() else "MISSING"
            print(f"  {name}.png [{status}]")
        print(f"\n{len(diagrams)} diagrams found")
        return

    canvas_width = compute_canvas_width(diagrams, font)

    for name, text in diagrams:
        out_file = OUTPUT_DIR / f"{name}.png"
        img = render_text_to_image(text, font, canvas_width)
        img.save(out_file)
        print(f"  {name}.png ({img.width}x{img.height})")

    print(f"\nDone: {len(diagrams)} diagrams rendered at {canvas_width}px wide")


if __name__ == "__main__":
    main()
