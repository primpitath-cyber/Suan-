with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
# ล้าง style fix เดิมเฉพาะส่วนที่เกี่ยวกับ table ออก
html = re.sub(r'<style id="table-full-fix">.*?</style>', '', html, flags=re.DOTALL)

# สไตล์ตารางที่ยืดเต็ม 100% สม่ำเสมอตามดีไซน์เดิม
table_style = """
<style id="table-full-fix">
  /* บังคับตารางสินค้าให้กว้างเต็มการ์ด ไม่หดเข้าซ้าย */
  table {
    display: table !important;
    width: 100% !important;
    min-width: 100% !important;
    border-collapse: collapse !important;
    margin-top: 10px !important;
  }

  table th, table td {
    padding: 10px 6px !important;
    font-size: 13px !important;
    text-align: center !important;
    vertical-align: middle !important;
  }

  /* ตัวครอบตารางป้องกันหลุดจอ แต่รักษาความกว้างเต็มพื้นที่ */
  .table-responsive, div:has(> table) {
    width: 100% !important;
    overflow-x: auto !important;
    -webkit-overflow-scrolling: touch !important;
  }
</style>
"""

html = html.replace('</head>', f'{table_style}\n</head>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

if __import__('os').path.exists('www/index.html'):
    with open('www/index.html', 'w', encoding='utf-8') as f:
        f.write(html)

print("Applied full-width table layout")
