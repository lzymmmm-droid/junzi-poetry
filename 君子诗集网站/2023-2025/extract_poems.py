#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import re
import json

sys.stdout.reconfigure(encoding="utf-8")

# Read 诗.txt
with open(r"G:\君子诗集\2023-2025\诗.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Read existing data
with open(r"G:\君子诗集\2023-2025\君子诗集_下册_data.js", "r", encoding="utf-8") as f:
    js_content = f.read()

# Extract existing titles from 卷五
existing_titles = set()
# Use simple regex to find titles in 卷五
title_matches = re.findall(r'"title":\s*"([^"]+)"', js_content)
volume_matches = re.findall(r'"volume":\s*"([^"]+)"', js_content)
for i, (title, volume) in enumerate(zip(title_matches, volume_matches)):
    if volume == "卷五 · 二零二三":
        existing_titles.add(title)

print(f"卷五现有标题 ({len(existing_titles)} 首):")
for t in sorted(existing_titles):
    print(f"  - {t}")

# Parse 诗.txt - extract all poems with author=君子 and date in 2023
# Split by --- separator
sections = re.split(r"\n---\n", text)

poems_found = []

for section in sections:
    section = section.strip()
    if not section:
        continue

    # Check author
    author_match = re.search(r"\*\*作者：\*\*\s*(.+)", section)
    if not author_match:
        continue
    author = author_match.group(1).strip()
    if author != "君子":
        continue

    # Check date - must be 2023
    date_match = re.search(r"\*\*时间：\*\*\s*(\d{4})年(\d{1,2})月(\d{1,2})日", section)
    if not date_match:
        continue
    year = int(date_match.group(1))
    if year != 2023:
        continue
    month = int(date_match.group(2))
    day = int(date_match.group(3))
    date_str = f"{year}-{month:02d}-{day:02d}"

    # Extract title
    # Try "第N篇 · title" format first
    title_match = re.search(r"## 第\d+篇\s*·\s*(.+)", section)
    if title_match:
        title = title_match.group(1).strip()
    else:
        # Try "## title" format
        title_match = re.search(r"## (.+)", section)
        if title_match:
            title = title_match.group(1).strip()
        else:
            continue

    # Clean title - remove any trailing spaces
    title = title.strip()

    poems_found.append({"title": title, "date": date_str, "section": section})

print(f"\n诗.txt中2023年君子诗篇 ({len(poems_found)} 首):")
for p in poems_found:
    in_existing = "已收录" if p["title"] in existing_titles else "**未收录**"
    print(f"  {p['date']} - {p['title']} [{in_existing}]")

# Find missing ones
missing = [p for p in poems_found if p["title"] not in existing_titles]
print(f"\n未收录诗篇 ({len(missing)} 首):")
for p in missing:
    print(f"  {p['date']} - {p['title']}")
