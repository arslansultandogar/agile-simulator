#!/usr/bin/env python3
"""Convert internship Markdown reports to PDF via HTML and headless Chrome."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import markdown

HERE = Path(__file__).resolve().parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
  @page {{
    size: A4;
    margin: 20mm 18mm 22mm 18mm;
  }}
  body {{
    font-family: "Times New Roman", Times, serif;
    font-size: 12pt;
    line-height: 1.5;
    color: #000;
    max-width: none;
    margin: 0;
    padding: 0;
  }}
  h1 {{
    font-size: 16pt;
    page-break-after: avoid;
    border-bottom: 1px solid #333;
    padding-bottom: 4px;
  }}
  h2 {{
    font-size: 14pt;
    margin-top: 18pt;
    page-break-after: avoid;
  }}
  h3 {{
    font-size: 12pt;
    margin-top: 14pt;
    page-break-after: avoid;
  }}
  p, li {{
    text-align: justify;
  }}
  code {{
    font-family: "Courier New", monospace;
    font-size: 10pt;
    background: #f5f5f5;
    padding: 1px 3px;
  }}
  pre {{
    font-size: 10pt;
    background: #f5f5f5;
    padding: 10px;
    white-space: pre-wrap;
    word-wrap: break-word;
  }}
  table {{
    border-collapse: collapse;
    width: 100%;
    margin: 10pt 0;
    font-size: 11pt;
    page-break-inside: avoid;
  }}
  th, td {{
    border: 1px solid #333;
    padding: 4pt 6pt;
    vertical-align: top;
  }}
  th {{
    background: #eee;
  }}
  hr {{
    border: none;
    border-top: 1px solid #999;
    margin: 16pt 0;
  }}
  .cover {{
    text-align: center;
    margin-top: 60pt;
    page-break-after: always;
  }}
  .cover h1 {{
    font-size: 18pt;
    border: none;
    margin-bottom: 24pt;
  }}
  .cover p {{
    text-align: center;
    margin: 8pt 0;
  }}
</style>
</head>
<body>
{body}
</body>
</html>
"""


def md_to_html(md_path: Path, html_path: Path) -> None:
    text = md_path.read_text(encoding="utf-8")
    body = markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "sane_lists", "nl2br"],
    )
    rendered = HTML_TEMPLATE.format(title=md_path.stem.replace("_", " "), body=body)
    html_path.write_text(rendered, encoding="utf-8")


def html_to_pdf(html_path: Path, pdf_path: Path) -> None:
    cmd = [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        html_path.resolve().as_uri(),
    ]
    subprocess.run(cmd, check=True, capture_output=True)


def process(md_path: Path, pdf_dir: Path) -> Path:
    html_dir = pdf_dir / "html"
    html_dir.mkdir(parents=True, exist_ok=True)
    pdf_dir.mkdir(parents=True, exist_ok=True)
    html_path = html_dir / f"{md_path.stem}.html"
    pdf_path = pdf_dir / f"{md_path.stem}.pdf"
    md_to_html(md_path, html_path)
    html_to_pdf(html_path.resolve(), pdf_path)
    return pdf_path


def main() -> None:
    pdf_dir = HERE / "pdf"
    sources = [HERE / "INTERNSHIP_PLAN.md", HERE / "FINAL_INTERNSHIP_REPORT.md", HERE / "DELIVERABLES_SUPPLEMENT.md"]
    sources += sorted((HERE / "progress-reports").glob("PROGRESS_REPORT_*.md"))
    sources.append(HERE / "REPORT_INDEX.md")

    if not Path(CHROME).exists():
        print(f"Chrome not found at {CHROME}", file=sys.stderr)
        sys.exit(1)

    for md in sources:
        if not md.exists():
            print(f"Skip missing: {md}")
            continue
        pdf = process(md, pdf_dir)
        print(f"Created {pdf}")


if __name__ == "__main__":
    main()
