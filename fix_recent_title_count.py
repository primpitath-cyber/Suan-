# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. ใส่ id ให้กับหัวข้อเพื่อให้อัปเดตตัวเลขตามจริงได้
text = text.replace(
    'ประวัติการขายล่าสุด (5 รายการ)',
    'ประวัติการขายล่าสุด (<span id="recentSalesCount">0</span> รายการ)'
)

# 2. อัปเดตใน loadRecentSales ให้ใส่จำนวนบิลจริงลงใน recentSalesCount
old_snippet = "const recent5 = [...salesWithNo].reverse().slice(0, 5);"
new_snippet = """const recent5 = [...salesWithNo].reverse().slice(0, 5);
    const countEl = document.getElementById('recentSalesCount');
    if (countEl) countEl.innerText = recent5.length;"""

text = text.replace(old_snippet, new_snippet)

# กรณีร้านที่ยังไม่มีประวัติการขาย ให้เซตเป็น 0
old_empty = "tbody.innerHTML = '<tr><td colspan=\"3\" class=\"empty-text\">ยังไม่มีประวัติการขาย</td></tr>';"
new_empty = """tbody.innerHTML = '<tr><td colspan=\"3\" class=\"empty-text\">ยังไม่มีประวัติการขาย</td></tr>';
      const countEl = document.getElementById('recentSalesCount');
      if (countEl) countEl.innerText = '0';"""

text = text.replace(old_empty, new_empty)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

with open('www/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("TITLE_COUNT_UPDATED_SUCCESSFULLY")
