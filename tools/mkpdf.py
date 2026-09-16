#!/usr/bin/env python3
"""mkpdf.py  <input.md> <output.pdf> "Running title"
Renders a Court of the Dragon markdown doc to a print-ready PDF."""
import sys, re, markdown
from weasyprint import HTML, CSS

src, out = sys.argv[1], sys.argv[2]
title = sys.argv[3] if len(sys.argv) > 3 else "Court of the Dragon"

text = open(src, encoding="utf-8").read()

html_body = markdown.markdown(
    text, extensions=["tables", "sane_lists", "attr_list"]
)

CSS_TEXT = """
@page {
  size: Letter; margin: 16mm 15mm 18mm 15mm;
  @bottom-center {
    content: "TITLE  ·  " counter(page);
    font-family: "DejaVu Serif", serif; font-size: 7.5pt;
    color: #8a7f74; letter-spacing: .08em;
  }
}
body { font-family: "DejaVu Serif", serif; font-size: 9pt; line-height: 1.42;
       color: #1b1714; }
h1 { font-size: 24pt; text-align: center; letter-spacing: .16em;
     text-transform: uppercase; margin: 0 0 2mm 0; color: #14100e; }
h1 + h3 { text-align: center; font-size: 9pt; letter-spacing: .14em;
          text-transform: uppercase; color: #6d3128; font-weight: normal;
          border: none; margin: 0 0 6mm 0; }
h2 { font-size: 13pt; text-transform: uppercase; letter-spacing: .14em;
     color: #6d3128; margin: 7mm 0 2mm 0; padding-bottom: 1mm;
     border-bottom: .6pt solid #6d3128; break-after: avoid; }
h3 { font-size: 10.5pt; text-transform: uppercase; letter-spacing: .08em;
     color: #14100e; margin: 4.5mm 0 1.5mm 0; break-after: avoid; }
h4 { font-size: 9.5pt; margin: 3mm 0 1mm 0; break-after: avoid; }
p, li { margin: 0 0 1.6mm 0; orphans: 2; widows: 2; }
ul { margin: 0 0 2mm 0; padding-left: 4.5mm; }
ol { margin: 0 0 2mm 0; padding-left: 5.5mm; }
ol li { padding-left: 0; }
em { color: #4a3f38; }
strong { color: #14100e; }
hr { border: none; border-top: .5pt solid #cfc4b8; margin: 5mm 0; }
table { width: 100%; border-collapse: collapse; margin: 1.5mm 0 3mm 0;
        font-size: 8.5pt; break-inside: avoid; }
th { text-transform: uppercase; letter-spacing: .07em; font-size: 7.5pt;
     text-align: left; color: #6d3128; border-bottom: .6pt solid #6d3128;
     padding: 1mm 2mm; }
td { padding: .9mm 2mm; border-bottom: .3pt solid #ddd3c7; vertical-align: top; }
tr:last-child td { border-bottom: none; }
"""

HTML(string=f"<html><body>{html_body}</body></html>").write_pdf(
    out, stylesheets=[CSS(string=CSS_TEXT.replace("TITLE", title))]
)
print("wrote", out)
