# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# 1. เปลี่ยนคำว่า "หมดอายุ" ในส่วนแสดงผลการ์ดสินค้าหน้าร้านและคลังสินค้า
text = text.replace('หมดอายุ', 'พร้อมย้ายปลูก')

# 2. ปรับสไตล์ป้ายสถานะจากสีแดง/ส้มเตือนของเสีย ให้เป็นสีเขียวสดใสสื่อถึงต้นกล้าที่สมบูรณ์พร้อมลงแปลง
text = text.replace('color: #dc2626; background: #fee2e2;', 'color: #166534; background: #dcfce7;')
text = text.replace('color:#dc2626;background:#fee2e2;', 'color:#166534;background:#dcfce7;')
text = text.replace('background: #fef2f2; color: #ef4444;', 'background: #f0fdf4; color: #16a34a;')

# 3. ตรวจสอบในฟังก์ชัน render สินค้าหน้าร้านหรือคลังสินค้า
text = re.sub(r'badge-danger[^>]*>.*?พร้อมย้ายปลูก.*?</span>', '<span class="badge" style="background:#dcfce7; color:#166534; font-size:0.75rem; padding:2px 8px; border-radius:12px; font-weight:600;">พร้อมย้ายปลูก</span>', text)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

with open('www/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("PLANT_READY_STATUS_UPDATED_SUCCESSFULLY")
