with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re

# ค้นหาและเปลี่ยนโครงสร้างกล่องวันหมดอายุโดยตรง
pattern = r'<div class="form-row"[^>]*dashed[^>]*>[\s\S]*?<input[^>]*id="pExpDate"[^>]*>[\s\S]*?</div>\s*</div>'

replacement = '''<div style="background: #f7faf8; padding: 12px; border-radius: 10px; border: 1.5px dashed var(--accent); margin-bottom: 12px; box-sizing: border-box; width: 100%;">
    <label style="display: block; margin-bottom: 6px; font-weight: 500;">⏳ วันหมดอายุ / ควรย้ายปลูกก่อน (ระบุหรือไม่ก็ได้)</label>
    <div style="width: 100%; box-sizing: border-box; overflow: hidden;">
        <input type="date" id="pExpDate" style="width: 100% !important; max-width: 100% !important; box-sizing: border-box !important; display: block !important; margin: 0 !important; padding: 10px !important;">
    </div>
</div>'''

new_html = re.sub(pattern, replacement, html)

# บังคับอัปเดต Service worker timestamp เพื่อให้ iPad โหลดไฟล์ใหม่ทันที
new_html = re.sub(r'sw\.js(\?v=[0-9.]+)?', f'sw.js?v={__import__("time").time()}', new_html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

import os
if os.path.exists('www/index.html'):
    with open('www/index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)

print("Patch applied cleanly!")
