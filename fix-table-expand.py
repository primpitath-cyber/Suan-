with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re

# ลบ style ทดลองก่อนหน้าทิ้งทั้งหมด
html = re.sub(r'<style id="[^"]*">.*?</style>', '', html, flags=re.DOTALL)

# สไตล์ตารางที่ทำให้กระจายเต็มพื้นที่การ์ดบนทุกหน้าจอ (ทั้ง iPad และมือถือ)
full_expand_css = """
<style id="perfect-suan-table">
  /* บังคับคอนเทนเนอร์และตัวตารางให้กว้างเต็ม 100% เสมอ ไม่หดเข้ามุมซ้าย */
  .table-container, .stock-table-wrap, div:has(> table) {
    width: 100% !important;
    max-width: 100% !important;
    display: block !important;
  }

  table {
    width: 100% !important;
    min-width: 100% !important;
    display: table !important;
    border-collapse: collapse !important;
    table-layout: fixed !important; /* กระจายทุกคอลัมน์ให้กว้างสม่ำเสมอเต็มการ์ด */
  }

  table th, table td {
    padding: 10px 4px !important;
    text-align: center !important;
    word-wrap: break-word !important;
    white-space: normal !important; /* ให้ตัดคำสองบรรทัดได้เหมือนรูปมือถือ */
    font-size: 13px !important;
  }

  /* รักษากล่องวันหมดอายุไม่ให้ล้นขอบ */
  #pExpDate {
    width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
  }
</style>
"""

html = html.replace('</head>', f'{full_expand_css}\n</head>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

if __import__('os').path.exists('www/index.html'):
    with open('www/index.html', 'w', encoding='utf-8') as f:
        f.write(html)

print("Applied full expand table style")
