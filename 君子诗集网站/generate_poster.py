import qrcode
from PIL import Image, ImageDraw, ImageFont
import os

# 网站URL
url = "https://lzymmmm-droid.github.io/junzi-poetry/"

# 生成二维码
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)
qr.add_data(url)
qr.make(fit=True)

# 生成二维码图片（黑色）
qr_img = qr.make_image(fill_color="black", back_color="white")
qr_img = qr_img.convert('RGBA')

# 创建海报（竖版）
width, height = 1080, 1920
poster = Image.new('RGB', (width, height), '#f8f4ed')
draw = ImageDraw.Draw(poster)

# 尝试加载字体
try:
    font_title = ImageFont.truetype("C:/Windows/Fonts/simhei.ttf", 90)
    font_sub = ImageFont.truetype("C:/Windows/Fonts/simhei.ttf", 44)
    font_desc = ImageFont.truetype("C:/Windows/Fonts/simhei.ttf", 40)
    font_small = ImageFont.truetype("C:/Windows/Fonts/simhei.ttf", 30)
    font_url = ImageFont.truetype("C:/Windows/Fonts/simhei.ttf", 26)
except:
    font_title = ImageFont.load_default()
    font_sub = font_title
    font_desc = font_title
    font_small = font_title
    font_url = font_title

# 顶部装饰区域
draw.line([(80, 150), (1000, 150)], fill='#8b4513', width=4)
draw.line([(80, 170), (1000, 170)], fill='#8b4513', width=2)

# 标题区域（上部）
title_y = 280
title = "君子诗集"
draw.text((width//2, title_y), title, fill='#8b4513', font=font_title, anchor="mm")

# 副标题
subtitle_y = title_y + 110
subtitle = "2018-2025 诗词合集"
draw.text((width//2, subtitle_y), subtitle, fill='#666666', font=font_sub, anchor="mm")

# 分隔线
sep_y = subtitle_y + 80
draw.line([(200, sep_y), (880, sep_y)], fill='#d4c5b5', width=2)

# 二维码区域（中部）
qr_size = 480
qr_img = qr_img.resize((qr_size, qr_size), Image.LANCZOS)

# 给二维码添加白色边框和装饰阴影
border = 30
qr_with_border = Image.new('RGBA', (qr_size + border*2, qr_size + border*2), 'white')
qr_with_border.paste(qr_img, (border, border), qr_img)

# 粘贴到海报
qr_x = (width - qr_size - border*2) // 2
qr_y = sep_y + 100
poster.paste(qr_with_border, (qr_x, qr_y))

# 二维码下方文字
scan_y = qr_y + qr_size + border*2 + 60
scan_text = "扫码进入网站"
draw.text((width//2, scan_y), scan_text, fill='#8b4513', font=font_desc, anchor="mm")

# 网站URL
url_y = scan_y + 60
url_text = "lzymmmm-droid.github.io/junzi-poetry"
draw.text((width//2, url_y), url_text, fill='#999999', font=font_url, anchor="mm")

# 底部信息区域（下部）
footer_sep_y = height - 340
draw.line([(200, footer_sep_y), (880, footer_sep_y)], fill='#d4c5b5', width=2)

footer_lines = [
    "686篇诗词 · 647首纯诗 · 126个典故",
    "2018-2025年创作整理",
    "支持手机/电脑浏览，支持音乐播放"
]

y = footer_sep_y + 60
for line in footer_lines:
    draw.text((width//2, y), line, fill='#666666', font=font_small, anchor="mm")
    y += 55

# 底部装饰线
draw.line([(80, height - 120), (1000, height - 120)], fill='#8b4513', width=2)
draw.line([(80, height - 105), (1000, height - 105)], fill='#8b4513', width=1)

# 保存海报
output_path = "C:/work/junzi-poetry/poster.png"
poster.save(output_path, "PNG", quality=95)
print(f"海报已生成: {output_path}")
