# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# 1. ปลดล็อกความกว้างของกรอบแท็บสรุปยอด ให้กว้างเต็มจอ iPad (ไม่แคบตรงกลาง)
# คืนค่าสไตล์ของแท็บรายงานและขยายการ์ดให้เต็มพื้นที่
text = re.sub(
    r'<div id=[\"\x27]tabReports[\"\x27][^>]*>',
    '<div id="tabReports" class="tab-content" style="width:100%; max-width:960px; margin:0 auto; padding:16px 12px; box-sizing:border-box;">',
    text
)

# 2. ปรับการ์ดสีขาวของสรุปยอดให้กว้างเต็มกรอบและมีระยะพอดีตา
text = text.replace(
    'style="background:#fff; border-radius:16px; padding:18px;',
    'style="background:#fff; border-radius:20px; padding:24px 20px; width:100%; box-sizing:border-box;'
)
text = text.replace(
    'style="background:#fff; border-radius:20px; padding:24px 20px; width:100%; box-sizing:border-box;',
    'style="background:#fff; border-radius:20px; padding:28px 22px; width:100%; box-sizing:border-box; box-shadow:0 4px 12px rgba(0,0,0,0.03);'
)

# 3. ขยายขนาดฟอนต์ของตารางรายงานรายบิล (วันที่ สินค้า จำนวน ยอดขาย กำไร) ให้ใหญ่ ชัดเจน
text = text.replace('font-size:0.85rem;', 'font-size:1.15rem;')
text = text.replace('font-size:1.05rem;', 'font-size:1.2rem;')
text = text.replace('padding:8px;', 'padding:16px 12px;')
text = text.replace('padding:10px 8px;', 'padding:18px 14px;')

# 4. นำรหัสนักศึกษาของทั้ง 2 ท่านออกอย่างถาวร
text = text.replace('<div style="font-size:0.8rem; color:#64748b;">รหัส 68040295</div>', '')
text = text.replace('<div style="font-size:0.8rem; color:#64748b;">รหัส 68040553</div>', '')

# 5. แก้ไขปุ่ม 🌱 สวนพร้อม ให้รองรับการกดบน iPad ทุกกรณี (ทั้ง onclick และ ontouchend)
old_brand_pattern = r'<div[^>]*class=[\"\x27]brand-title[\"\x27][^>]*>[\s\S]*?สวนพร้อม[\s\S]*?<\/div>'
new_brand_html = '<div class="brand-title" id="btnAppBrand" onclick="window.showAuthorModal()" ontouchend="window.showAuthorModal()" style="cursor:pointer; display:inline-flex; align-items:center; gap:6px; font-weight:700; -webkit-tap-highlight-color:rgba(0,0,0,0.1); user-select:none; z-index:9999; position:relative;">🌱 สวนพร้อม</div>'

text = re.sub(old_brand_pattern, new_brand_html, text, count=1)

# ตรวจสอบฟังก์ชัน showAuthorModal ใน window
script_modal = '''
<script>
  window.showAuthorModal = function(e) {
    if (e && e.preventDefault) e.preventDefault();
    var m = document.getElementById('authorModal');
    if (m) m.style.display = 'flex';
  };
  window.hideAuthorModal = function(e) {
    if (e && e.preventDefault) e.preventDefault();
    var m = document.getElementById('authorModal');
    if (m) m.style.display = 'none';
  };
</script>
'''
if 'window.showAuthorModal = function' not in text:
    text = text.replace('</body>', script_modal + '\n</body>', 1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

with open('www/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("BOX_EXPANDED_AND_AUTHORS_FIXED")
