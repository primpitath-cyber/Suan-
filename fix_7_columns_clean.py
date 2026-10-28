# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# 1. ปรับ thead เป็น 7 คอลัมน์: วันที่ | สินค้า | รหัสบิล | จำนวน | ต้นทุน | ยอดขาย | กำไร
thead_target = '''<table style="width:100%; min-width:720px; border-collapse:collapse;">
          <thead>
            <tr style="border-bottom:2px solid #e2e8f0; background:#f8fafc;">
              <th style="padding:12px 14px; text-align:left; font-size:0.95rem; font-weight:600; color:#475569;">วันที่</th>
              <th style="padding:12px 14px; text-align:left; font-size:0.95rem; font-weight:600; color:#475569;">สินค้า</th>
              <th style="padding:12px 14px; text-align:center; font-size:0.95rem; font-weight:600; color:#475569;">รหัสบิล</th>
              <th style="padding:12px 14px; text-align:center; font-size:0.95rem; font-weight:600; color:#475569;">จำนวน</th>
              <th style="padding:12px 14px; text-align:right; font-size:0.95rem; font-weight:600; color:#475569;">ต้นทุน</th>
              <th style="padding:12px 14px; text-align:right; font-size:0.95rem; font-weight:600; color:#475569;">ยอดขาย</th>
              <th style="padding:12px 14px; text-align:right; font-size:0.95rem; font-weight:600; color:#475569;">กำไร</th>
            </tr>
          </thead>'''

pos_tab = text.find('id="tabReports"')
if pos_tab != -1:
    pos_tbl = text.find('<table', pos_tab)
    pos_th_end = text.find('</thead>', pos_tbl)
    if pos_tbl != -1 and pos_th_end != -1:
        text = text[:pos_tbl] + thead_target + text[pos_th_end+8:]

# 2. ปรับปรุงฟังก์ชัน loadMonthlyReport ดึงต้นทุนและแสดงครบทั้ง 7 ช่อง
report_code = '''async function loadMonthlyReport() {
    try {
      const monthInput = document.getElementById('rep-month-input');
      if (!monthInput) return;
      if (!monthInput.value) {
        const now = new Date();
        monthInput.value = now.getFullYear() + '-' + String(now.getMonth() + 1).padStart(2, '0');
      }
      const [y, m] = monthInput.value.split('-');
      const startDate = new Date(Number(y), Number(m) - 1, 1).toISOString();
      const endDate = new Date(Number(y), Number(m), 0, 23, 59, 59).toISOString();

      const tbody = document.getElementById('rep-table-rows');
      if (tbody) tbody.innerHTML = '<tr><td colspan="7" style="text-align:center; padding:24px; color:#64748b;">กำลังโหลดข้อมูล...</td></tr>';

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
      } catch (e) {}

      if (!currentShop && typeof activeShopId !== 'undefined' && activeShopId) currentShop = activeShopId;
      if (!currentShop) {
        const sel = document.getElementById('shopSelect');
        if (sel && sel.value) currentShop = sel.value;
      }

      let q = sb.from('sales').select('id, total, created_at, sale_items(*, products(*))');
      if (currentShop) q = q.eq('shop_id', currentShop);

      let { data: sales, error } = await q
        .gte('created_at', startDate)
        .lte('created_at', endDate)
        .order('created_at', { ascending: true });

      if (error || !sales || sales.length === 0) {
        if (tbody) tbody.innerHTML = '<tr><td colspan="7" style="text-align:center; padding:24px; color:#888;">ไม่มีรายการขายในเดือนนี้</td></tr>';
        const inc = document.getElementById('rep-inc-val');
        const exp = document.getElementById('rep-exp-val');
        const net = document.getElementById('rep-net-val');
        if (inc) inc.textContent = '0 บ.';
        if (exp) exp.textContent = '0 บ.';
        if (net) net.textContent = '0 บ.';
        return;
      }

      let totalIncome = 0;
      let totalCost = 0;
      let rowHtml = '';

      sales.forEach((s, idx) => {
        const billNo = idx + 1;
        const amt = Number(s.total) || 0;
        totalIncome += amt;
        const dt = new Date(s.created_at).toLocaleDateString('th-TH', { day: 'numeric', month: 'short' });

        let billCost = 0;
        let productNames = [];
        let totalQty = 0;

        if (s.sale_items && s.sale_items.length > 0) {
          s.sale_items.forEach(it => {
            const pName = it.products ? it.products.name : (it.name || 'สินค้าทั่วไป');
            productNames.push(pName);
            const qVal = Number(it.quantity) || 1;
            totalQty += qVal;
            const costUnit = it.products ? (Number(it.products.cost) || 0) : 0;
            billCost += (costUnit * qVal);
          });
        } else {
          productNames.push('ขายหน้าร้าน');
          totalQty = 1;
        }

        totalCost += billCost;
        const billProfit = amt - billCost;
        const displayProductName = productNames.join(', ');

        rowHtml += `<tr style="border-bottom:1px solid #f1f5f9;">
          <td style="padding:14px 14px; color:#334155; font-size:0.95rem; white-space:nowrap;">${dt}</td>
          <td style="padding:14px 14px; font-weight:600; color:#0f172a; font-size:0.95rem; white-space:nowrap;">${displayProductName}</td>
          <td style="padding:14px 14px; text-align:center; white-space:nowrap;"><code style="background:#edf2ee; color:#166534; padding:3px 7px; border-radius:5px; font-size:0.85rem; font-weight:700;">#${billNo}</code></td>
          <td style="padding:14px 14px; text-align:center; font-weight:600; color:#475569; font-size:0.95rem; white-space:nowrap;">${totalQty}</td>
          <td style="padding:14px 14px; text-align:right; font-weight:600; color:#dc2626; font-size:0.95rem; white-space:nowrap;">${billCost.toLocaleString()} บ.</td>
          <td style="padding:14px 14px; text-align:right; font-weight:600; color:#0f172a; font-size:0.95rem; white-space:nowrap;">${amt.toLocaleString()} บ.</td>
          <td style="padding:14px 14px; text-align:right; font-weight:700; color:#16a34a; font-size:0.95rem; white-space:nowrap;">${billProfit.toLocaleString()} บ.</td>
        </tr>`;
      });

      if (tbody) tbody.innerHTML = rowHtml;

      const incEl = document.getElementById('rep-inc-val');
      const expEl = document.getElementById('rep-exp-val');
      const netEl = document.getElementById('rep-net-val');
      const netLbl = document.getElementById('rep-net-lbl');
      const netBox = document.getElementById('rep-net-box');

      if (incEl) incEl.textContent = totalIncome.toLocaleString() + ' บ.';
      if (expEl) expEl.textContent = totalCost.toLocaleString() + ' บ.';
      
      const netProfit = totalIncome - totalCost;
      if (netEl) {
        netEl.textContent = Math.abs(netProfit).toLocaleString() + ' บ.';
        if (netProfit >= 0) {
          if (netLbl) { netLbl.textContent = 'กำไรสุทธิ'; netLbl.style.color = '#1e40af'; }
          netEl.style.color = '#1d4ed8';
          if (netBox) netBox.style.background = '#eff6ff';
        } else {
          if (netLbl) { netLbl.textContent = 'ขาดทุนสุทธิ'; netLbl.style.color = '#991b1b'; }
          netEl.style.color = '#b91c1c';
          if (netBox) netBox.style.background = '#fef2f2';
        }
      }
    } catch (err) {
      console.error('Report error:', err);
    }
  }'''

text = re.sub(r'async function loadMonthlyReport\(\)\s*\{[\s\S]*?\n  \}', report_code, text, count=1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

with open('www/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("SUCCESS_APPLIED_ALL_7_COLUMNS")
