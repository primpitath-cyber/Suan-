# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. เปลี่ยน id="tabReports" ให้มี class="tab-content" เพื่อให้ทำงานกับ CSS หลักของระบบ
c = c.replace('id="tabReports" class="tab-pane" style="display:none; padding:16px;"', 'id="tabReports" class="tab-content" style="padding:16px;"')
c = c.replace('id="tabReports" class="tab-pane"', 'id="tabReports" class="tab-content"')

# 2. เพิ่มเงื่อนไขเปิดไฟ active ให้ปุ่ม navReports ในฟังก์ชัน switchTab
old_check = "if (tabId === 'tabSettings') document.getElementById('navSettings').classList.add('active');"
new_check = """if (tabId === 'tabSettings') document.getElementById('navSettings').classList.add('active');
    if (tabId === 'tabReports') document.getElementById('navReports').classList.add('active');"""

if 'navReports' not in c[c.find('function switchTab'):c.find('window.scrollTo')]:
    c = c.replace(old_check, new_check)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("FIX_ACTIVE_DONE")
