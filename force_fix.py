with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ใส่ CSS ท้าย head บังคับให้เฉพาะกล่อง pExpDate ไม่ล้นขอบเด็ดขาด
fix_css = """
<style id="direct-date-fix">
  /* บังคับ input วันที่และตัวครอบให้หดอยู่ในกรอบพอดี */
  #pExpDate {
    width: 100% !important;
    max-width: calc(100% - 24px) !important;
    box-sizing: border-box !important;
    display: block !important;
    margin: 0 auto !important;
  }
</style>
"""

# ลบตัวเก่าออกก่อนแล้วใส่ใหม่
import re
html = re.sub(r'<style id="direct-date-fix">.*?</style>', '', html, flags=re.DOTALL)
html = html.replace('</head>', f'{fix_css}\n</head>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# สำเนาไปที่ www ด้วยหากมีโฟลเดอร์นี้
import os
if os.path.exists('www/index.html'):
    with open('www/index.html', 'w', encoding='utf-8') as f:
        f.write(html)

print("CSS injected successfully")
