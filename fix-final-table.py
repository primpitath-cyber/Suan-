with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re

# ล้างแท็กสไตล์แปลกปลอมเดิมทิ้ง
html = re.sub(r'<style id="[^"]*">.*?</style>', '', html, flags=re.DOTALL)

# สไตล์ตารางที่ทำให้กว้างเต็มการ์ด ไม่หดเข้าซ้าย และตัดคำสวยงามเหมือนรูปมือถือ
final_css = """
<style id="perfect-suan-table">
  /* บังคับคอนเทนเนอร์และตัวตารางให้กว้าง 100% เต็มพื้นที่การ์ด */
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

  /* รักษากล่องวันหมดอายุไม่ให้ทะลุกรอบ */
  #pExpDate {
    width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
  }
</style>
"""

html = html.replace('</head>', f'{final_css}\n</head>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

if __import__('os').path.exists('www/index.html'):
    with open('www/index.html', 'w', encoding='utf-8') as f:
        f.write(html)

print("Applied 100% width fixed table layout successfully")
