# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# นำบล็อกรหัสนักศึกษาของทั้ง 2 ท่านออก
text = text.replace('<div style="font-size:0.8rem; color:#64748b;">รหัส 68040295</div>', '')
text = text.replace('<div style="font-size:0.8rem; color:#64748b;">รหัส 68040553</div>', '')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

with open('www/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("STUDENT_IDS_REMOVED_SUCCESSFULLY")
