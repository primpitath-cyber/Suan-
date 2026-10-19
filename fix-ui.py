import re

# 1. ตกแต่ง CSS แก้ปัญหากล่อง input ล้น และตารางเลื่อนได้บนมือถือ
css_fix = """
/* Fix input overflow & table responsiveness */
*, *::before, *::after {
  box-sizing: border-box !important;
}

input, select, textarea {
  max-width: 100% !important;
}

.table-responsive, table {
  width: 100% !important;
  display: block !important;
  overflow-x: auto !important;
  -webkit-overflow-scrolling: touch !important;
  white-space: nowrap !important;
}

th, td {
  padding: 8px 10px !important;
  font-size: 13px !important;
}
"""

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# แทรก CSS fix เข้าไปก่อน </head>
if "/* Fix input overflow" not in content:
    content = content.replace('</head>', f'<style>{css_fix}</style>\n</head>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated index.html successfully")
