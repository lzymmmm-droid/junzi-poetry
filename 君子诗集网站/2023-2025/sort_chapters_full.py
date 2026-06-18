#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, sys
from collections import defaultdict

# 强制UTF-8输出
sys.stdout.reconfigure(encoding="utf-8")

# 读取原始文件
content = open(
    "G:/君子诗集/2023-2025/君子诗集_下册_data.js", "r", encoding="utf-8"
).read()

# 提取poemsData
import re

match = re.search(r"var poemsData = (\[.*?\]);", content, re.DOTALL)
if not match:
    match = re.search(r"var poemsData = (\[.*?\])\s*$", content, re.DOTALL)
if not match:
    print("未匹配到poemsData")
    exit(1)

poems = json.loads(match.group(1))

print(f"总诗数: {len(poems)}", flush=True)

# 按volume分组
groups = defaultdict(list)
for p in poems:
    v = p.get("volume", "附录")
    groups[v].append(p)

# 按日期排序，无日期放最后
for vol, vol_poems in groups.items():

    def sort_key(p):
        d = p.get("date", "")
        if d and d.strip():
            return (0, d)
        return (2, "")

    vol_poems.sort(key=sort_key)

# 定义章节顺序
order = ["序", "卷五 · 二零二三", "卷六 · 二零二四", "卷七 · 二零二五", "附录", "后记"]

# 构建chaptersData
chaptersData = []
for vol in order:
    if vol in groups and groups[vol]:
        chaptersData.append({"name": vol, "poems": groups[vol]})

# 重新构建poemsData，按章节顺序
sorted_poems = []
for chapter in chaptersData:
    sorted_poems.extend(chapter["poems"])

print(f"\n章节数: {len(chaptersData)}", flush=True)
for ch in chaptersData:
    print(f"\n{ch['name']} ({len(ch['poems'])}首):", flush=True)
    for p in ch["poems"][:5]:
        date_str = p.get("date", "无日期")
        print(f"  {date_str} - {p['title']}", flush=True)
    if len(ch["poems"]) > 5:
        print(f"  ... 还有 {len(ch['poems']) - 5} 首", flush=True)

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
    + json.dumps(chaptersData, ensure_ascii=False, indent=2)
    + ";\n"
)

open("G:/君子诗集/2023-2025/君子诗集_下册_data.js", "w", encoding="utf-8").write(
    final_content
)
print(
    f"\n已保存，poemsData {len(sorted_poems)} 首，chaptersData {len(chaptersData)} 章节",
    flush=True,
)
