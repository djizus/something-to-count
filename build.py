#!/usr/bin/env python3
"""Build the reading copy from manuscript/NN.md.

Writes book/<slug>.md, book/<slug>.html and, if LibreOffice is installed,
book/<slug>.pdf. Usage: python3 build.py "Title" ["Author"]
"""
import html
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "manuscript"
OUT = ROOT / "book"


def chapters():
    for path in sorted(SRC.glob("[0-9][0-9].md")):
        lines = path.read_text(encoding="utf-8").strip().split("\n")
        heading = lines[0].lstrip("# ").strip() if lines[0].startswith("#") else str(int(path.stem))
        number = heading  # "1", "2", ... or the title of an unnumbered opening
        body = "\n".join(lines[1:]).strip() if lines[0].startswith("#") else "\n".join(lines)
        blocks = [b.strip() for b in re.split(r"\n\s*\n", body) if b.strip()]
        yield number, blocks


def is_break(block):
    return block.replace(" ", "") == "***"


OPENS_AFTER = set(" \t\n([—–-*\"'")


def curl(text):
    """Turn straight quotation marks into typographic ones.

    A mark opens when it follows a space, a dash or another opening mark and
    is followed by a character; every other single mark closes or is an
    apostrophe. The manuscript has no word that begins with an apostrophe.
    """
    out = []
    for i, ch in enumerate(text):
        if ch in "'\"":
            before = text[i - 1] if i else " "
            after = text[i + 1] if i + 1 < len(text) else " "
            opens = before in OPENS_AFTER and not after.isspace()
            out.append({"'": "‘’", '"': "“”"}[ch][0 if opens else 1])
        else:
            out.append(ch)
    return "".join(out)


def inline(text, italic, escape):
    parts = re.split(r"\*([^*]+)\*", text)
    return "".join(italic(escape(p)) if i % 2 else escape(p) for i, p in enumerate(parts))


def build(title, author):
    OUT.mkdir(exist_ok=True)
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    book = list(chapters())
    words = sum(len(b.split()) for _, blocks in book for b in blocks if not is_break(b))

    md = [f"# {title}", ""]
    page = [f"<h1 class='title'>{html.escape(title)}</h1>"]
    if author:
        md += [author, ""]
        page.append(f"<p class='author'>{html.escape(author)}</p>")
    for number, blocks in book:
        md += [f"## {number}", ""]
        page.append(f"<h2>{html.escape(number)}</h2>")
        first = True
        for block in blocks:
            if is_break(block):
                md += ["* * *", ""]
                page.append("<p class='break'>* * *</p>")
                first = True
                continue
            text = curl(" ".join(block.split("\n")))
            md += [text, ""]
            cls = " class='first'" if first else ""
            page.append(f"<p{cls}>" + inline(text, lambda s: f"<em>{s}</em>", html.escape) + "</p>")
            first = False

    (OUT / f"{slug}.md").write_text("\n".join(md), encoding="utf-8")
    css = ("body{max-width:34em;margin:3em auto;padding:0 1.2em;font:1.15em/1.6 Georgia,'Noto Serif',serif;"
           "color:#1b1b1b;background:#fbfaf7}h1.title{text-align:center;margin:4em 0 .5em;font-weight:normal}"
           "p.author{text-align:center;margin-bottom:6em}h2{text-align:center;font-weight:normal;margin:4em 0 2em}"
           "p{margin:0;text-indent:1.4em;text-align:justify;hyphens:auto}p.first{text-indent:0}"
           "p.break{text-align:center;text-indent:0;margin:1.4em 0}"
           "@media(prefers-color-scheme:dark){body{background:#161616;color:#e6e3dc}}")
    (OUT / f"{slug}.html").write_text(
        "<!doctype html><html lang='en-GB'><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        f"<title>{html.escape(title)}</title><style>{css}</style></head><body>"
        + "\n".join(page) + "</body></html>", encoding="utf-8")

    made = [f"{slug}.md", f"{slug}.html"]
    office = shutil.which("soffice") or shutil.which("libreoffice")
    if office:
        print_css = ("@page{size:A5;margin:2cm 1.8cm}body{font:11pt/1.45 'Liberation Serif','Noto Serif',serif}"
                     "h1.title{text-align:center;margin-top:6cm;font-weight:normal;font-family:'Liberation Serif','Noto Serif',serif}"
                     "p.author{text-align:center;text-indent:0;margin-top:1cm}h2{text-align:center;font-weight:normal;margin:2cm 0 1cm;"
                     "page-break-before:always}p{margin:0;text-indent:1.2em;text-align:justify}"
                     "p.first{text-indent:0}p.break{text-align:center;text-indent:0;margin:.8em 0}")
        work = OUT / "_print"
        work.mkdir(exist_ok=True)
        (work / f"{slug}.html").write_text(
            "<!doctype html><html lang='en-GB'><head><meta charset='utf-8'>"
            f"<title>{html.escape(title)}</title><style>{print_css}</style></head><body>"
            + "\n".join(page) + "</body></html>", encoding="utf-8")
        run = subprocess.run([office, "--headless", "--convert-to", "pdf:writer_web_pdf_Export",
                              "--outdir", str(OUT), str(work / f"{slug}.html")],
                             capture_output=True, text=True)
        if (OUT / f"{slug}.pdf").exists():
            made.append(f"{slug}.pdf")
        else:
            print("PDF not built:", (run.stderr or run.stdout)[-400:])
    print(f"{len(book)} chapters, {words} words ->", ", ".join(made))


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else "Untitled", sys.argv[2] if len(sys.argv) > 2 else "")
