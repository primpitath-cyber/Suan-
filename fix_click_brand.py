# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. ใส่ onclick และ styling ให้กับ brand-title โดยตรง
old_brand = '<div class="brand-title">🌱 สวนพร้อม</div>'
new_brand = '<div class="brand-title" onclick="showAuthorModal()" style="cursor:pointer; -webkit-tap-highlight-color:transparent; user-select:none;">🌱 สวนพร้อม</div>'

text = text.replace(old_brand, new_brand)

# 2. ปรับฟังก์ชันใน script ให้เป็น window.showAuthorModal เพื่อให้เรียกได้ 100%
script_fix = '''
<script>
  window.showAuthorModal = function() {
    var modal = document.getElementById('authorModal');
    if (modal) {
      modal.style.display = 'flex';
    }
  };
  window.hideAuthorModal = function() {
    var modal = document.getElementById('authorModal');
    if (modal) {
      modal.style.display = 'none';
    }
  };
</script>
'''

import re
if 'window.showAuthorModal' not in text:
    if 'id="authorModal"' in text:
        # แทนที่ tag script เก่าของ modal
        text = re.sub(r'<script>\s*function showAuthorModal\(\)[\s\S]*?<\/script>', script_fix, text)
    else:
        text = text.replace('</body>', script_fix + '\n</body>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

with open('www/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("BRAND_TITLE_CLICK_BOUND_SUCCESSFULLY")
