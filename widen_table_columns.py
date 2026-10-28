# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# 1. ปรับขนาดฟอนต์กลับมาเป็นขนาดมาตรฐานสบายตา (ไม่ใหญ่เกินไป) แต่ให้คอลัมน์กว้างยาวสะใจ
text = text.replace('font-size:1.25rem;', 'font-size:0.95rem;')
text = text.replace('font-size:1.2rem;', 'font-size:0.95rem;')
text = text.replace('font-size:1.15rem;', 'font-size:0.95rem;')

# 2. ปรับแต่งโครงสร้างตารางรายงานสรุปยอด ให้มี min-width กว้างพอ และแบ่งความกว้างแต่ละคอลัมน์ชัดเจน ไม่เบียดกัน
table_css = '''
<style id="wide-table-style">
  /* ให้กรอบการ์ดขาวขยายความกว้างเต็มพื้นที่การ์ดบน */
  #tabReports .card, #tabReports > div {
    width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
  }
  
  /* ตัวตารางรายงาน ยืดความกว้างให้แต่ละช่องมีพื้นที่ ไม่บีบตัวอักษร */
  #tabReports table {
    width: 100% !important;
    min-width: 650px !important; /* การันตีว่าช่องจะไม่ถูกบีบเบียด */
    border-collapse: separate !important;
    border-spacing: 0 !important;
  }
  
  #tabReports th, #tabReports td {
    white-space: nowrap !important; /* ป้องกันข้อความตัดบรรทัดเบียดกัน */
    padding: 14px 18px !important;   /* เพิ่มระยะห่างซ้าย-ขวาให้โปร่ง */
    font-size: 0.95rem !important;
  }

  /* กำหนดสัดส่วนคอลัมน์ให้ยืดขยายยาวพอดี */
  #tabReports th:nth-child(1), #tabReports td:nth-child(1) { width: 20%; text-align: left; }
  #tabReports th:nth-child(2), #tabReports td:nth-child(2) { width: 30%; text-align: left; }
  #tabReports th:nth-child(3), #tabReports td:nth-child(3) { width: 15%; text-align: center; }
  #tabReports th:nth-child(4), #tabReports td:nth-child(4) { width: 18%; text-align: right; }
  #tabReports th:nth-child(5), #tabReports td:nth-child(5) { width: 17%; text-align: right; }

  /* กล่องที่หุ้มตาราง ให้เลื่อน scroll แนวนอนได้หากหน้าจอแคบ */
  #tabReports .table-responsive, #tabReports .table-container {
    width: 100% !important;
    overflow-x: auto !important;
    -webkit-overflow-scrolling: touch !important;
  }
</style>
'''

if 'id="wide-table-style"' in text:
    text = re.sub(r'<style id="wide-table-style">[\s\S]*?<\/style>', table_css, text)
else:
    text = text.replace('</head>', table_css + '\n</head>', 1)

# ตรวจสอบจุดครอบตารางในแท็บ tabReports ให้ใส่คลาส table-responsive
text = re.sub(
    r'(<div[^>]*class=[\"\x27]table-container[\"\x27][^>]*>)',
    r'<div class="table-container table-responsive" style="width:100%; overflow-x:auto;">',
    text
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

with open('www/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("WIDEN_TABLE_COLUMNS_SUCCESS")
