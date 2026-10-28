# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

perfect_report_code = '''async function loadMonthlyReport() {
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
      if (tbody) tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; padding:24px; color:#64748b; font-size:1rem;">กำลังโหลดข้อมูล...</td></tr>';

      // ค้นหารหัสร้านค้าปัจจุบัน (Active Shop ID) ให้ตรง 100%
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

      if (!currentShop && typeof activeShopId !== 'undefined' && activeShopId) {
        currentShop = activeShopId;
      }
      if (!currentShop) {
        const sel = document.getElementById('shopSelect');
        if (sel && sel.value) currentShop = sel.value;
      }

      // ดึงบิลเฉพาะร้านปัจจุบัน
      let q = sb.from('sales').select('*, sale_items(*, products(*))');
      if (currentShop) {
        q = q.eq('shop_id', currentShop);
      }

      let { data: sales, error } = await q
        .gte('created_at', startDate)
        .lte('created_at', endDate)
        .order('created_at', { ascending: true }); // เรียงจากเก่าไปใหม่ เพื่อเริ่มบิลที่ 1

      if (error || !sales || sales.length === 0) {
        if (tbody) tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; padding:28px; color:#888; font-size:1.05rem;">ไม่มีรายการขายในเดือนนี้</td></tr>';
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

      // วนลูปสร้างตาราง โดยเริ่มลำดับ "บิลที่ 1", "บิลที่ 2", ...
      sales.forEach((s, billIndex) => {
        const billNo = billIndex + 1; // เริ่มต้นที่ 1
        const billTotal = Number(s.total) || 0;
        totalIncome += billTotal;
        const dt = new Date(s.created_at).toLocaleDateString('th-TH', { day: 'numeric', month: 'short' });

        let billItems = s.sale_items || [];
        if (billItems.length > 0) {
          billItems.forEach((item, itemIdx) => {
            const pName = item.products ? item.products.name : (item.name || 'สินค้าทั่วไป');
            const pQty = Number(item.quantity) || 1;
            const pCostUnit = item.products ? (Number(item.products.cost) || 0) : 0;
            const itemCost = pCostUnit * pQty;
            totalCost += itemCost;

            // ถ้ารายการย่อยไม่มีราคา ให้แบ่งจาก total ของบิล
            let itemPrice = Number(item.price) || 0;
            if (itemPrice === 0 && billItems.length === 1) {
              itemPrice = billTotal;
            }
            const itemTotal = itemPrice > 0 ? (itemPrice * pQty) : billTotal;
            const itemProfit = itemTotal - itemCost;

            rowHtml += `<tr style="border-bottom:1px solid #e2e8f0; font-size:1.05rem;">
              <td style="padding:16px 12px; font-weight:600; color:#334155; vertical-align:middle;">
                ${itemIdx === 0 ? `<div>บิลที่ ${billNo}</div><div style="font-size:0.85rem; color:#64748b; font-weight:normal;">${dt}</div>` : ''}
              </td>
              <td style="padding:16px 12px; color:#0f172a; vertical-align:middle; font-weight:500;">${pName}</td>
              <td style="padding:16px 12px; text-align:center; vertical-align:middle; font-weight:600;">${pQty}</td>
              <td style="padding:16px 12px; text-align:right; vertical-align:middle; font-weight:600; color:#0f172a;">${itemTotal.toLocaleString()} บ.</td>
              <td style="padding:16px 12px; text-align:right; vertical-align:middle; font-weight:700; color:#16a34a;">${itemProfit.toLocaleString()} บ.</td>
            </tr>`;
          });
        } else {
          // กรณีไม่มีรายการสินค้าย่อยในตาราง sale_items
          rowHtml += `<tr style="border-bottom:1px solid #e2e8f0; font-size:1.05rem;">
            <td style="padding:16px 12px; font-weight:600; color:#334155; vertical-align:middle;">
              <div>บิลที่ ${billNo}</div>
              <div style="font-size:0.85rem; color:#64748b; font-weight:normal;">${dt}</div>
            </td>
            <td style="padding:16px 12px; color:#0f172a; vertical-align:middle; font-weight:500;">ขายหน้าร้าน</td>
            <td style="padding:16px 12px; text-align:center; vertical-align:middle; font-weight:600;">1</td>
            <td style="padding:16px 12px; text-align:right; vertical-align:middle; font-weight:600; color:#0f172a;">${billTotal.toLocaleString()} บ.</td>
            <td style="padding:16px 12px; text-align:right; vertical-align:middle; font-weight:700; color:#16a34a;">${billTotal.toLocaleString()} บ.</td>
          </tr>`;
        }
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

# ขยายขนาดตารางใน HTML ให้เต็มจอและดูง่าย
text = text.replace('font-size:0.85rem; text-align:left;', 'font-size:1.05rem; text-align:left; width:100%; border-collapse:separate; border-spacing:0;')
text = text.replace('padding:8px;', 'padding:14px 12px;')

import re
text = re.sub(r'async function loadMonthlyReport\(\)\s*\{[\s\S]*?\n  \}', perfect_report_code, text, count=1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

with open('www/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("PERFECT_REPORT_UPDATED")
