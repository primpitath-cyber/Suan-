with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re

# 1. แทรก CSS รีเซ็ต appearance ของ iOS Safari สำหรับ input date
safari_fix = """
<style id="safari-date-reset">
  /* ล้างสไตล์เริ่มต้นของ Safari สำหรับ input date */
  input[type="date"]#pExpDate,
  #pExpDate {
    -webkit-appearance: none !important;
    -moz-appearance: none !important;
    appearance: none !important;
    display: block !important;
    width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
    margin: 0 !important;
  }
  
  /* ตัวครอบเส้นประ */
  div[style*="dashed"] {
    box-sizing: border-box !important;
    width: 100% !important;
    overflow: hidden !important;
  }
</style>
"""

# ลบ style เก่าที่เคยใส่ไว้
html = re.sub(r'<style id="safari-date-reset">.*?</style>', '', html, flags=re.DOTALL)
html = html.replace('</head>', f'{safari_fix}\n</head>')

# 2. แก้ที่ตัวแท็ก input id="pExpDate" โดยตรงเพื่อ override ทุกกรณี
html = re.sub(
    r'<input([^>]*id=["\']pExpDate["\'][^>]*)>',
    r'<input\1 style="-webkit-appearance:none; width:100%; box-sizing:border-box; margin:0;">',
    html
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

import os
if os.path.exists('www/index.html'):
    with open('www/index.html', 'w', encoding='utf-8') as f:
        f.write(html)

print("Applied Safari date reset successfully")
