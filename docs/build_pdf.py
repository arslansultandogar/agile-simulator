"""Render a Markdown doc (with Mermaid diagrams) to a styled HTML file.

Mermaid blocks are extracted before Markdown conversion so their content is not
HTML-escaped, then reinserted as ``<div class="mermaid">`` elements. The HTML is
designed to be printed to PDF with headless Chrome, which renders the Mermaid
diagrams via the bundled CDN script.
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

import markdown

HERE = Path(__file__).resolve().parent

MERMAID_BLOCK = re.compile(r"```mermaid\n(.*?)```", re.DOTALL)

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>
  mermaid.initialize({{ startOnLoad: true, theme: "neutral", securityLevel: "loose" }});
</script>
<style>
  @page {{
    size: A4 landscape;
    margin: 10mm;
  }}
  body {{
    font-family: -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #1a1a1a;
    line-height: 1.5;
    max-width: none;
    margin: 0 auto;
    padding: 0;
    font-size: 11px;
  }}
  h1 {{ font-size: 24px; border-bottom: 2px solid #333; padding-bottom: 6px; }}
  h2 {{ font-size: 19px; margin-top: 28px; border-bottom: 1px solid #ccc; padding-bottom: 4px; }}
  h3 {{ font-size: 15px; margin-top: 20px; }}
  h4 {{ font-size: 13px; margin-top: 16px; color: #333; }}
  code {{ background: #f3f3f3; padding: 1px 4px; border-radius: 3px; font-size: 10px; }}
  pre {{ background: #f6f8fa; padding: 10px; border-radius: 6px; overflow-x: auto; }}
  table {{
    border-collapse: collapse;
    width: 100%;
    margin: 12px 0;
    font-size: 9.5px;
    table-layout: fixed;
    page-break-inside: auto;
  }}
  th, td {{
    border: 1px solid #ddd;
    padding: 5px 6px;
    text-align: left;
    vertical-align: top;
    overflow-wrap: anywhere;
    word-break: normal;
  }}
  th {{ background: #f2f2f2; }}
  tr {{ page-break-inside: avoid; page-break-after: auto; }}
  blockquote {{
    border-left: 4px solid #5b8def; background: #f3f7ff; margin: 12px 0;
    padding: 8px 14px; color: #2a3b5f;
  }}
  .mermaid {{ text-align: center; margin: 16px 0; page-break-inside: avoid; }}
  h2, h3 {{ page-break-after: avoid; }}
</style>
</head>
<body>
{body}
</body>
</html>
"""


def render(md_path: Path, html_path: Path) -> None:
    text = md_path.read_text(encoding="utf-8")

    diagrams: list[str] = []

    def _stash(match: re.Match) -> str:
        diagrams.append(match.group(1).strip())
        return f"@@MERMAID_{len(diagrams) - 1}@@"

    text = MERMAID_BLOCK.sub(_stash, text)

    body = markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "sane_lists", "attr_list"],
    )

    for index, diagram in enumerate(diagrams):
        placeholder = f"@@MERMAID_{index}@@"
        # Placeholder may be wrapped in <p> tags by the markdown converter.
        block = f'<div class="mermaid">{html.escape(diagram)}</div>'
        body = body.replace(f"<p>{placeholder}</p>", block).replace(placeholder, block)

    rendered = HTML_TEMPLATE.format(title=md_path.stem, body=body)
    html_path.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    source = HERE / "UML_CI_PERFORMANCE_ANALYSIS.md"
    output = HERE / "UML_CI_PERFORMANCE_ANALYSIS.html"
    if len(sys.argv) >= 3:
        source = Path(sys.argv[1])
        output = Path(sys.argv[2])
    render(source, output)
    print(f"Wrote {output}")
