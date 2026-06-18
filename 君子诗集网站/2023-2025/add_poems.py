#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import re
import json
import copy

sys.stdout.reconfigure(encoding="utf-8")

# Read 诗.txt
with open(r"G:\君子诗集\2023-2025\诗.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Read existing data
with open(r"G:\君子诗集\2023-2025\君子诗集_下册_data.js", "r", encoding="utf-8") as f:
    js_content = f.read()

# Extract existing titles from 卷五
existing_titles = set()
title_matches = re.findall(r'"title":\s*"([^"]+)"', js_content)
volume_matches = re.findall(r'"volume":\s*"([^"]+)"', js_content)
for i, (title, volume) in enumerate(zip(title_matches, volume_matches)):
    if volume == "卷五 · 二零二三":
        existing_titles.add(title)

print(f"卷五现有: {len(existing_titles)} 首")

# Parse 诗.txt - extract all poems with author=君子 and date in 2023
sections = re.split(r"\n---\n", text)


def parse_section(section):
    """Parse a section and return poem data"""
    section = section.strip()
    if not section:
        return None

    # Check author
    author_match = re.search(r"\*\*作者：\*\*\s*(.+)", section)
    if not author_match:
        return None
    author = author_match.group(1).strip()
    if author != "君子":
        return None

    # Check date
    date_match = re.search(r"\*\*时间：\*\*\s*(\d{4})年(\d{1,2})月(\d{1,2})日", section)
    if not date_match:
        return None
    year = int(date_match.group(1))
    if year != 2023:
        return None
    month = int(date_match.group(2))
    day = int(date_match.group(3))
    date_str = f"{year}-{month:02d}-{day:02d}"

    # Extract title
    title_match = re.search(r"## 第\d+篇\s*·\s*(.+)", section)
    if title_match:
        title = title_match.group(1).strip()
    else:
        title_match = re.search(r"## (.+)", section)
        if title_match:
            title = title_match.group(1).strip()
        else:
            return None

    if title in existing_titles:
        return None  # Already exists

    # Extract content - everything between the metadata lines and the annotation or next section
    lines = section.split("\n")

    # Find content start: after the metadata lines (author, time, sender)
    content_start = -1
    for i, line in enumerate(lines):
        if line.strip().startswith("- **发送人：**") or line.strip().startswith(
            "- **类型：**"
        ):
            content_start = i + 1
            break

    if content_start == -1:
        # Try after the last metadata line
        for i, line in enumerate(lines):
            if line.strip().startswith("- **时间：**"):
                content_start = i + 1
                break

    if content_start == -1:
        return None

    # Skip blank lines after metadata
    while content_start < len(lines) and lines[content_start].strip() == "":
        content_start += 1

    # Find annotation start
    annotation_start = -1
    for i in range(content_start, len(lines)):
        if (
            lines[i].strip().startswith("**注释：**")
            or lines[i].strip() == "**注释：**"
        ):
            annotation_start = i
            break

    # Extract content lines
    if annotation_start > 0:
        content_lines = lines[content_start:annotation_start]
    else:
        content_lines = lines[content_start:]

    # Clean content - remove empty lines at start and end
    while content_lines and content_lines[0].strip() == "":
        content_lines.pop(0)
    while content_lines and content_lines[-1].strip() == "":
        content_lines.pop()

    # Extract annotation
    annotation = ""
    if annotation_start >= 0:
        anno_lines = lines[annotation_start:]
        anno_text = "\n".join(anno_lines)
        # Remove **注释：** prefix
        anno_text = re.sub(r"^\*\*注释：\*\*\s*", "", anno_text)
        annotation = anno_text.strip()

    # Build content array - split into lines, remove empty
    content = []
    for line in content_lines:
        stripped = line.strip()
        if stripped:
            content.append(stripped)

    return {
        "title": title,
        "date": date_str,
        "author": "君子",
        "content": content,
        "annotation": annotation,
        "volume": "卷五 · 二零二三",
    }


new_poems = []
for section in sections:
    poem = parse_section(section)
    if poem:
        new_poems.append(poem)

print(f"\n新增诗篇 ({len(new_poems)} 首):")
for p in new_poems:
    print(f"  {p['date']} - {p['title']} ({len(p['content'])} 行)")

# Now load the existing data and add new poems
# Parse existing JS file
# Find poemsData array
poems_start = js_content.index("var poemsData = [")
# Find the matching closing bracket
brace_count = 0
poems_end = -1
for i in range(poems_start, len(js_content)):
    if js_content[i] == "[":
        brace_count += 1
    elif js_content[i] == "]":
        brace_count -= 1
        if brace_count == 0:
            poems_end = i + 1
            break

poems_json_str = js_content[poems_start + len("var poemsData = ") : poems_end]
poems_data = json.loads(poems_json_str)

# Find chaptersData array
chapters_start = js_content.index("var chaptersData = [")
brace_count = 0
chapters_end = -1
for i in range(chapters_start, len(js_content)):
    if js_content[i] == "[":
        brace_count += 1
    elif js_content[i] == "]":
        brace_count -= 1
        if brace_count == 0:
            chapters_end = i + 1
            break

chapters_json_str = js_content[
    chapters_start + len("var chaptersData = ") : chapters_end
]
chapters_data = json.loads(chapters_json_str)

print(f"\n现有 poemsData: {len(poems_data)} 首")
print(f"现有 chaptersData: {len(chapters_data)} 章节")

# Add new poems to poemsData
# Assign _poemsDataIndex
max_index = max(p.get("_poemsDataIndex", 0) for p in poems_data)
for p in new_poems:
    max_index += 1
    p["_poemsDataIndex"] = max_index
    poems_data.append(p)

print(f"添加后 poemsData: {len(poems_data)} 首")

# Sort 卷五 poems by date
v5_poems = [p for p in poems_data if p.get("volume") == "卷五 · 二零二三"]
v5_poems.sort(key=lambda p: p.get("date", ""))
print(f"卷五排序后: {len(v5_poems)} 首")

# Rebuild chaptersData for 卷五
v5_chapter = None
for ch in chapters_data:
    if ch.get("name") == "卷五 · 二零二三":
        v5_chapter = ch
        break

if v5_chapter:
    v5_chapter["poems"] = v5_poems
    print(f"更新卷五章节: {len(v5_chapter['poems'])} 首")

# Reassign _poemsDataIndex for all poems
for i, p in enumerate(poems_data):
    p["_poemsDataIndex"] = i

# Write output
output = f"""// 君子诗集 · 下册数据
// 生成: 2026-06-17
// 共 {len(poems_data)} 首

var poemsData = {json.dumps(poems_data, ensure_ascii=False, indent=2)};

var chaptersData = {json.dumps(chapters_data, ensure_ascii=False, indent=2)};
"""

with open(r"G:\君子诗集\2023-2025\君子诗集_下册_data.js", "w", encoding="utf-8") as f:
    f.write(output)

print(f"\n完成! 写入 {len(poems_data)} 首诗到数据文件")

# Verify
v5_count = sum(1 for p in poems_data if p.get("volume") == "卷五 · 二零二三")
print(f"卷五 · 二零二三: {v5_count} 首")
