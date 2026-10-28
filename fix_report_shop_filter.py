# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

new_report_code = '''async function loadMonthlyReport() {
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
      if (tbody) tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; padding:16px; color:#999;">กำลังโหลดข้อมูล...</td></tr>';

      // ดึง ID ร้านปัจจุบันจากทุกลำดับความสำคัญ
      let currentShop = localStorage.getItem('sp_user_active_shop');
      if (!currentShop && typeof activeShopId !== 'undefined' && activeShopId) {
        currentShop = activeShopId;
      }
      if (!currentShop) {
        const sel = document.getElementById('shopSelect');
        if (sel && sel.value) currentShop = sel.value;
      }

      // ดึงข้อมูลการขายจากตาราง sales
      let q = sb.from('sales').select('id, total, created_at, sale_items(*, products(name, cost))');
      if (currentShop) {
        q = q.eq('shop_id', currentShop);
      }

      let { data: sales, error } = await q
        .gte('created_at', startDate)
        .lte('created_at', endDate)
        .order('created_at', { ascending: false });

      // หาก join ตารางรองแล้วติด error ให้ดึงแบบปกติโดยกรอง shop_id
      if (error) {
        let q2 = sb.from('sales').select('id, total, created_at');
        if (currentShop) q2 = q2.eq('shop_id', currentShop);
        const res2 = await q2
          .gte('created_at', startDate)
          .lte('created_at', endDate)
          .order('created_at', { ascending: false });
        sales = res2.data;
        error = res2.error;
      }

      if (error || !sales || sales.length === 0) {
        if (tbody) tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; padding:16px; color:#888;">ไม่มีรายการขายในเดือนนี้สำหรับร้านนี้</td></tr>';
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

      sales.forEach(s => {
        const amt = Number(s.total) || 0;
        totalIncome += amt;
        const dt = new Date(s.created_at).toLocaleDateString('th-TH', { day: 'numeric', month: 'short' });

        // ตรวจสอบว่ามีรายการสินค้าย่อยในบิลหรือไม่
        if (s.sale_items && s.sale_items.length > 0) {
          s.sale_items.forEach((item, idx) => {
            const pName = item.products ? item.products.name : (item.name || 'สินค้า');
            const pCost = item.products ? (Number(item.products.cost) || 0) : 0;
            const pQty = Number(item.quantity) || 1;
            const itemPrice = Number(item.price) || 0;
            const itemTotal = itemPrice * pQty;
            const itemTotalCost = pCost * pQty;
            totalCost += itemTotalCost;
            const itemProfit = itemTotal - itemTotalCost;

            rowHtml += `<tr style="border-bottom:1px solid #f1f5f9; ${idx === 0 ? 'background:#f8fafc;' : ''}">
              <td style="padding:10px 8px; font-weight:${idx === 0 ? '600' : 'normal'};">${idx === 0 ? dt : ''}</td>
              <td style="padding:10px 8px;">
                ${idx === 0 ? '<div style="font-size:0.75rem; color:#64748b; margin-bottom:2px;">บิล #' + String(s.id).slice(0, 6) + '</div>' : ''}
                <div style="color:#0f172a;">${pName}</div>
              </td>
              <td style="padding:10px 8px; text-align:center;">${pQty}</td>
              <td style="padding:10px 8px; text-align:right;">${itemTotal.toLocaleString()} บ.</td>
              <td style="padding:10px 8px; text-align:right; color:#15803d; font-weight:600;">${itemProfit.toLocaleString()} บ.</td>
            </tr>`;
          });
        } else {
          // หากเป็นบิลเดี่ยวที่ไม่มีบันทึกตารางย่อย
          rowHtml += `<tr style="border-bottom:1px solid #f1f5f9;">
            <td style="padding:10px 8px;">${dt}</td>
            <td style="padding:10px 8px; font-weight:600; color:#0f172a;">บิลขาย #${String(s.id).slice(0, 6)}</td>
            <td style="padding:10px 8px; text-align:center;">1</td>
            <td style="padding:10px 8px; text-align:right;">${amt.toLocaleString()} บ.</td>
            <td style="padding:10px 8px; text-align:right; color:#15803d; font-weight:600;">${amt.toLocaleString()} บ.</td>
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

import re
text = re.sub(r'async function loadMonthlyReport\(\)\s*\{[\s\S]*?\n  \}', new_report_code, text, count=1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

with open('www/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("SHOP_FILTER_AND_ITEMS_APPLIED")
