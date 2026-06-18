#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, re, sys
from collections import defaultdict

# 强制UTF-8输出
sys.stdout.reconfigure(encoding="utf-8")

# 读取原始文件
content = open(
    "G:/君子诗集/2023-2025/君子诗集_下册_data.js", "r", encoding="utf-8"
).read()

# 提取poemsData
match = re.search(r"var poemsData = (\[.*?\]);", content, re.DOTALL)
if not match:
    match = re.search(r"var poemsData = (\[.*?\])\s*$", content, re.DOTALL)
if not match:
    print("未匹配到poemsData")
    exit(1)

poems = json.loads(match.group(1))

# 提取chaptersData
chapters_match = re.search(r"var chaptersData = (\[.*?\]);", content, re.DOTALL)
if not chapters_match:
    chapters_match = re.search(r"var chaptersData = (\[.*?\])\s*$", content, re.DOTALL)
if chapters_match:
    chapters = json.loads(chapters_match.group(1))
else:
    chapters = None

print(f"总诗数: {len(poems)}", flush=True)

if chapters:
    print(f"章节数: {len(chapters)}", flush=True)
    # 按卷分组
    groups = defaultdict(list)
    for p in poems:
        groups[p["volume"]].append(p)

    # 对每个chapter中的poems按日期排序
    for chapter in chapters:
        chapter_poems = chapter.get("poems", [])
        if chapter_poems:
            # 按日期排序，无日期放最后
            def sort_key(p):
                d = p.get("date", "")
                if d and d.strip():
                    return (0, d)
                return (2, "")

            chapter_poems.sort(key=sort_key)
            print(f"\n{chapter['name']} 排序后 ({len(chapter_poems)}首):", flush=True)
            for p in chapter_poems[:5]:  # 只打印前5首
                date_str = p.get("date", "无日期")
                print(f"  {date_str} - {p['title']}", flush=True)
            if len(chapter_poems) > 5:
                print(f"  ... 还有 {len(chapter_poems) - 5} 首", flush=True)

    # 重新构建poemsData，按章节顺序排列
    sorted_poems = []
    for chapter in chapters:
        sorted_poems.extend(chapter.get("poems", []))

    # 生成新文件内容
    header_lines = []
    for line in content.split("\n")[:4]:
        if line.startswith("//") or line.strip() == "":
            header_lines.append(line)

    final_content = "\n".join(header_lines) + "\n\n"
    final_content += (
        "var poemsData = "
        + json.dumps(sorted_poems, ensure_ascii=False, indent=2)
        + ";\n\n"
    )
    final_content += (
        "var chaptersData = "
        + json.dumps(chapters, ensure_ascii=False, indent=2)
        + ";\n"
    )

    open("G:/君子诗集/2023-2025/君子诗集_下册_data.js", "w", encoding="utf-8").write(
        final_content
    )
    print(
        f"\n已保存，poemsData {len(sorted_poems)} 首，chaptersData {len(chapters)} 章节",
        flush=True,
    )
else:
    # 只有poemsData，按volume分组排序
    groups = defaultdict(list)
    for p in poems:
        groups[p["volume"]].append(p)

    sorted_poems = []
    for vol in sorted(groups.keys()):
        vol_poems = groups[vol]

        def sort_key(p):
            d = p.get("date", "")
            if d and d.strip():
                return (0, d)
            return (2, "")

        vol_poems.sort(key=sort_key)
        sorted_poems.extend(vol_poems)

    header_lines = []
    for line in content.split("\n")[:4]:
        if line.startswith("//") or line.strip() == "":
            header_lines.append(line)

    final_content = (
        "\n".join(header_lines)
        + "\n\nvar poemsData = "
        + json.dumps(sorted_poems, ensure_ascii=False, indent=2)
        + ";\n"
    )

    open("G:/君子诗集/2023-2025/君子诗集_下册_data.js", "w", encoding="utf-8").write(
        final_content
    )
    print(f"\n已保存，poemsData {len(sorted_poems)} 首（无chaptersData）", flush=True)
