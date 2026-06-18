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

# 提取JSON数据
match = re.search(r"var poemsData = (\[.*?\]);", content, re.DOTALL)
if not match:
    match = re.search(r"var poemsData = (\[.*?\])\s*$", content, re.DOTALL)
if not match:
    print("未匹配到数据")
    exit(1)

poems = json.loads(match.group(1))
print(f"总诗数: {len(poems)}", flush=True)

# 统计各卷
volumes = {}
for p in poems:
    v = p["volume"]
    volumes[v] = volumes.get(v, 0) + 1

for v, c in sorted(volumes.items()):
    print(f"{v}: {c}首", flush=True)

# 按卷分组并排序
groups = defaultdict(list)
for p in poems:
    groups[p["volume"]].append(p)

sorted_poems = []
for vol in sorted(groups.keys()):
    vol_poems = groups[vol]

    # 按日期排序，无日期放最后
    def sort_key(p):
        d = p.get("date", "")
        if d and d.strip():
            return (0, d)
        return (2, "")

    vol_poems.sort(key=sort_key)
    sorted_poems.extend(vol_poems)
    print(f"\n{vol} 排序后:", flush=True)
    for p in vol_poems:
        date_str = p.get("date", "无日期")
        print(f"  {date_str} - {p['title']}", flush=True)

# 保留头部注释
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
print(f"\n已保存，总计 {len(sorted_poems)} 首诗", flush=True)
