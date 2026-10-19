with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re

# ลบ style ทดลองอันก่อนหน้าออก
html = re.sub(r'<style id="perfect-suan-table">.*?</style>', '', html, flags=re.DOTALL)

# สไตล์รวม: ตารางเต็มการ์ดเท่าเดิม + กล่องวันหมดอายุอยู่ในกรอบ 100% ไม่ล้น
complete_css = """
<style id="perfect-suan-table">
  /* 1. คุมตารางให้ขยายเต็ม 100% และกระจายคอลัมน์สม่ำเสมอ */
  .table-container {
    width: 100% !important;
    display: block !important;
    overflow-x: auto !important;
    -webkit-overflow-scrolling: touch !important;
    margin-top: 10px !important;
  }

  .table-container table {
    width: 100% !important;
    min-width: 100% !important;
    display: table !important;
    border-collapse: collapse !important;
    table-layout: fixed !important;
  }

  .table-container th, 
  .table-container td {
    padding: 12px 6px !important;
    text-align: center !important;
    font-size: 13px !important;
    line-height: 1.4 !important;
    word-break: break-word !important;
    white-space: normal !important;
  }

  /* 2. บังคับกล่องเส้นประและ input วันหมดอายุให้อยู่ในกรอบ ไม่ล้นขอบขวา */
  div[style*="dashed"] {
    width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
    overflow: hidden !important;
    display: block !important;
  }

  div[style*="dashed"] .form-group {
    width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
    margin: 0 !important;
    padding: 0 !important;
  }

  #pExpDate,
  div[style*="dashed"] input {
    width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
    display: block !important;
    margin: 0 !important;
  }
</style>
"""

html = html.replace('</head>', f'{complete_css}\n</head>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

if __import__('os').path.exists('www/index.html'):
    with open('www/index.html', 'w', encoding='utf-8') as f:
        f.write(html)

print("Updated: Full width table + contained date box")
