# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# 1. ลบ CSS แปลกๆ ที่ทำให้สเกลหดตัวออกไป
text = re.sub(r'<style id="ipad-table-fix">[\s\S]*?<\/style>', '', text)
text = re.sub(r'<style>\s*\.brand-title[\s\S]*?<\/style>', '', text)

# 2. ปรับโครงสร้าง brand-title ให้แตะได้ 100% บน iPad
# แปลงแท็ก brand-title ให้กลายเป็น element ที่มี role="button" และ inline onclick ชัดเจน
text = re.sub(
    r'<div[^>]*class=[\"\x27]brand-title[\"\x27][^>]*>[\s\S]*?<\/div>',
    '''<div class="brand-title" id="btnAppBrand" role="button" tabindex="0" onclick="openAuthorModalDirect()" style="cursor:pointer; display:inline-flex; align-items:center; gap:6px; font-weight:700; user-select:none; -webkit-tap-highlight-color:rgba(0,0,0,0.1); padding:4px 8px; border-radius:8px;">🌱 สวนพร้อม</div>''',
    text,
    count=1
)

# 3. ใส่ JavaScript เปิด/ปิด Modal แบบ Direct DOM เข้าไปที่ท้ายไฟล์
modal_script = '''
<script>
  function openAuthorModalDirect(e) {
    if (e) {
      e.preventDefault();
      e.stopPropagation();
    }
    var m = document.getElementById('authorModal');
    if (m) {
      m.style.setProperty('display', 'flex', 'important');
    }
  }

  function closeAuthorModalDirect(e) {
    if (e) {
      e.preventDefault();
      e.stopPropagation();
    }
    var m = document.getElementById('authorModal');
    if (m) {
      m.style.setProperty('display', 'none', 'important');
    }
  }

  // ดักการคลิกและแตะที่ปุ่ม brand
  document.addEventListener('DOMContentLoaded', function() {
    var btn = document.getElementById('btnAppBrand');
    if (btn) {
      btn.addEventListener('touchstart', function(e) {
        openAuthorModalDirect(e);
      }, { passive: false });
    }
  });
</script>
'''

# ปรับปุ่มปิดใน authorModal ให้เรียก closeAuthorModalDirect
text = text.replace('onclick="hideAuthorModal()"', 'onclick="closeAuthorModalDirect(event)"')

# อัปเดตสคริปต์
text = re.sub(r'<script>\s*window\.showAuthorModal[\s\S]*?<\/script>', '', text)
text = text.replace('</body>', modal_script + '\n</body>', 1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

with open('www/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("LAYOUT_AND_TOUCH_FIXED_SUCCESSFULLY")
