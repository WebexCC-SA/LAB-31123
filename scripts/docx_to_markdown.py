#!/usr/bin/env python3
from __future__ import annotations

import argparse
import mimetypes
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

import mammoth
from markdownify import markdownify as html_to_markdown


HEADING_RE = re.compile(r"^(#{1,2})\s+(.*\S)\s*$")
NON_WORD_RE = re.compile(r"[^a-z0-9]+")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Convert a DOCX into Markdown files under docs/, splitting each "
            "Heading 1/2 that starts with 'Lab' into its own file."
        )
    )
    parser.add_argument("input_docx", help="Path to the source .docx file")
    parser.add_argument(
        "--docs-dir",
        default="docs",
        help="Directory where markdown files should be written (default: docs)",
    )
    parser.add_argument(
        "--assets-dir",
        default=None,
        help="Directory where extracted images should be written (default: <docs-dir>/assets)",
    )
    return parser.parse_args()


def slugify(text: str) -> str:
    lowered = text.strip().lower()
    slug = NON_WORD_RE.sub("-", lowered).strip("-")
    return slug or "lab"


def unique_slug(slug: str, used: Dict[str, int]) -> str:
    if slug not in used:
        used[slug] = 1
        return slug
    used[slug] += 1
    return f"{slug}-{used[slug]}"


def build_image_converter(assets_dir: Path, assets_rel_from_docs: str):
    counter = {"value": 0}

    def convert_image(image: mammoth.images.Image):
        counter["value"] += 1
        ext = mimetypes.guess_extension(image.content_type or "") or ".bin"
        filename = f"docx-image-{counter['value']:03d}{ext}"
        output_path = assets_dir / filename
        with image.open() as image_bytes:
            output_path.write_bytes(image_bytes.read())
        src = f"{assets_rel_from_docs}/{filename}".replace("\\", "/")
        return {"src": src}

    return mammoth.images.img_element(convert_image)


def convert_docx_to_markdown(
    input_docx: Path, assets_dir: Path, assets_rel_from_docs: str
) -> Tuple[str, List[str]]:
    with input_docx.open("rb") as docx_file:
        result = mammoth.convert_to_html(
            docx_file, convert_image=build_image_converter(assets_dir, assets_rel_from_docs)
        )
    markdown = html_to_markdown(result.value, heading_style="ATX")
    markdown = markdown.replace("\r\n", "\n").replace("\r", "\n")
    return markdown, [msg.message for msg in result.messages]


def split_markdown_into_sections(markdown: str) -> Tuple[List[Tuple[str, str]], str]:
    lines = markdown.split("\n")
    headings: List[Tuple[int, str]] = []
    for idx, line in enumerate(lines):
        match = HEADING_RE.match(line)
        if match:
            headings.append((idx, match.group(2).strip()))

    labs: List[Tuple[str, str]] = []
    non_lab_chunks: List[str] = []

    if not headings:
        non_lab = "\n".join(lines).strip()
        return labs, non_lab

    preface = "\n".join(lines[: headings[0][0]]).strip()
    if preface:
        non_lab_chunks.append(preface)

    for i, (start, title) in enumerate(headings):
        end = headings[i + 1][0] if i + 1 < len(headings) else len(lines)
        chunk = "\n".join(lines[start:end]).strip()
        if not chunk:
            continue
        if title.lower().startswith("lab"):
            labs.append((title, chunk))
        else:
            non_lab_chunks.append(chunk)

    non_lab = "\n\n".join(part for part in non_lab_chunks if part).strip()
    return labs, non_lab


def write_outputs(docs_dir: Path, labs: List[Tuple[str, str]], non_lab: str) -> List[Path]:
    written_files: List[Path] = []
    used_slugs: Dict[str, int] = {}

    for title, content in labs:
        file_slug = unique_slug(slugify(title), used_slugs)
        file_path = docs_dir / f"{file_slug}.md"
        file_path.write_text(content + "\n", encoding="utf-8")
        written_files.append(file_path)

    if non_lab:
        non_lab_path = docs_dir / "non-lab.md"
        non_lab_path.write_text(non_lab + "\n", encoding="utf-8")
        written_files.append(non_lab_path)

    return written_files


def main() -> None:
    args = parse_args()
    input_docx = Path(args.input_docx).resolve()
    docs_dir = Path(args.docs_dir).resolve()
    assets_dir = Path(args.assets_dir).resolve() if args.assets_dir else (docs_dir / "assets").resolve()

    if not input_docx.exists():
        raise FileNotFoundError(f"Input DOCX not found: {input_docx}")
    if input_docx.suffix.lower() != ".docx":
        raise ValueError(f"Input file must be a .docx file: {input_docx}")

    docs_dir.mkdir(parents=True, exist_ok=True)
    assets_dir.mkdir(parents=True, exist_ok=True)

    assets_rel_str = os.path.relpath(assets_dir, docs_dir).replace("\\", "/")

    markdown, conversion_messages = convert_docx_to_markdown(input_docx, assets_dir, assets_rel_str)
    labs, non_lab = split_markdown_into_sections(markdown)
    written_files = write_outputs(docs_dir, labs, non_lab)

    if not labs:
        print("No lab headings (Heading 1/2 starting with 'Lab') were found. Wrote only non-lab content.")

    for message in conversion_messages:
        print(f"[mammoth] {message}")

    print(f"Wrote {len(written_files)} markdown file(s) to: {docs_dir}")
    print(f"Extracted images to: {assets_dir}")


if __name__ == "__main__":
    main()
