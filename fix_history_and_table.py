# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. เขียนฟังก์ชัน loadRecentSales ใหม่ ให้ดึง shop_id ชัวร์ 100% และรันรหัสบิลเริ่มที่ #1
new_load_recent = '''async function loadRecentSales() {
    const tbody = document.getElementById('salesTableBody');
    if (!tbody) return;

    // หา active shop id จากทุกช่องทาง
    let currentShop = null;
    try {
      const rawSaved = localStorage.getItem('sp_user_active_shop');
      if (rawSaved) {
        if (rawSaved.startsWith('{')) {
          const parsed = JSON.parse(rawSaved);
          currentShop = parsed.id || parsed.shop_id || rawSaved;
        } else {
          currentShop = rawSaved;
        }
      }
    } catch(e) {}

    if (!currentShop && typeof activeShopId !== 'undefined' && activeShopId) {
      currentShop = activeShopId;
    }
    if (!currentShop) {
      const sel = document.getElementById('shopSelect');
      if (sel && sel.value) currentShop = sel.value;
    }

    if (!currentShop) {
      tbody.innerHTML = '<tr><td colspan="3" class="empty-text">ยังไม่มีประวัติการขาย</td></tr>';
      const statEl = document.getElementById('statTodaySales');
      if (statEl) statEl.innerText = '0 บ.';
      return;
    }

    // ดึงรายการทั้งหมดของร้านนี้เพื่อคำนวณลำดับบิลที่แท้จริง
    const { data: allSales, error } = await sb.from('sales')
      .select('id, total, created_at')
      .eq('shop_id', currentShop)
      .order('created_at', { ascending: true });

    if (error || !allSales || allSales.length === 0) {
      tbody.innerHTML = '<tr><td colspan="3" class="empty-text">ยังไม่มีประวัติการขาย</td></tr>';
      const statEl = document.getElementById('statTodaySales');
      if (statEl) statEl.innerText = '0 บ.';
      return;
    }

    let todayTotal = 0;
    const todayStr = new Date().toDateString();

    // Map ลำดับบิลเริ่มจาก #1
    const salesWithNo = allSales.map((s, idx) => ({ ...s, billNo: idx + 1 }));

    // คำนวณยอดขายวันนี้
    salesWithNo.forEach(s => {
      const saleDate = new Date(s.created_at);
      if (saleDate.toDateString() === todayStr) {
        todayTotal += Number(s.total) || 0;
      }
    });

    // นำ 5 รายการล่าสุดมาแสดงในตาราง (เรียงจากล่าสุดลงมา)
    const recent5 = [...salesWithNo].reverse().slice(0, 5);

    tbody.innerHTML = '';
    recent5.forEach(s => {
      const saleDate = new Date(s.created_at);
      const time = saleDate.toLocaleTimeString('th-TH', { hour: '2-digit', minute: '2-digit' });
      tbody.innerHTML += `
        <tr>
          <td style="padding:14px 10px; font-size:1.05rem;">${time} น.</td>
          <td style="padding:14px 10px;"><code style="background: #edf2ee; padding: 4px 8px; border-radius: 6px; font-size: 1.05rem; font-weight:600;">#${s.billNo}</code></td>
          <td style="padding:14px 10px; text-align: right; font-size: 1.05rem;"><strong style="color: var(--primary);">${(Number(s.total) || 0).toLocaleString()}</strong> บ.</td>
        </tr>
      `;
    });

    const statEl = document.getElementById('statTodaySales');
    if (statEl) statEl.innerText = todayTotal.toLocaleString() + ' บ.';
  }'''

import re
text = re.sub(r'async function loadRecentSales\(\)\s*\{[\s\S]*?\n  \}', new_load_recent, text, count=1)

# 2. ปลดล็อกขนาดความกว้างของคอนเทนเนอร์ในแท็บสรุปยอดให้ขยายเต็มหน้าจอ iPad
css_expand = '''
<style id="ipad-table-fix">
  #tabReports {
    max-width: 100% !important;
    width: 100% !important;
    padding: 20px 24px !important;
    box-sizing: border-box !important;
  }
  #tabReports > div {
    max-width: 100% !important;
    width: 100% !important;
  }
  #tabReports table {
    width: 100% !important;
    font-size: 1.25rem !important;
  }
  #tabReports th {
    padding: 18px 16px !important;
    font-size: 1.25rem !important;
    background: #f8fafc !important;
  }
  #tabReports td {
    padding: 22px 16px !important;
    font-size: 1.25rem !important;
  }
  .table-container {
    overflow-x: auto !important;
    width: 100% !important;
  }
</style>
'''
if 'id="ipad-table-fix"' not in text:
    text = text.replace('</head>', css_expand + '\n</head>', 1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

with open('www/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("SYNC_AND_FIXED_ALL_SUCCESS")
