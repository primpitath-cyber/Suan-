# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

new_load_func = '''
  async function loadMonthlyReport() {
    const mInput = document.getElementById('rep-month-input');
    if (!mInput) return;
    if (!mInput.value) {
      const now = new Date();
      mInput.value = now.getFullYear() + '-' + String(now.getMonth() + 1).padStart(2, '0');
    }
    const [y, m] = mInput.value.split('-');
    const startDate = new Date(y, m - 1, 1).toISOString();
    const endDate = new Date(y, m, 0, 23, 59, 59).toISOString();

    try {
      // ดึงข้อมูลจากตาราง sales ของร้านปัจจุบัน
      let q = sb.from('sales').select('*, sale_items(*, products(*))');
      if (typeof currentShopId !== 'undefined' && currentShopId) {
        q = q.eq('shop_id', currentShopId);
      }
      const { data: sales, error } = await q
        .gte('created_at', startDate)
        .lte('created_at', endDate)
        .order('created_at', { ascending: false });

      let inc = 0, exp = 0;
      const tbody = document.getElementById('rep-table-rows');

      if (!sales || sales.length === 0) {
        if (tbody) tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; padding:16px; color:#888;">ไม่มีรายการขายในเดือนนี้</td></tr>';
        document.getElementById('rep-inc-val').textContent = '0 บ.';
        document.getElementById('rep-exp-val').textContent = '0 บ.';
        document.getElementById('rep-net-val').textContent = '0 บ.';
        return;
      }

      let rows = '';
      sales.forEach(sale => {
        const dt = new Date(sale.created_at).toLocaleDateString('th-TH', { day: 'numeric', month: 'short' });
        const saleTotal = sale.total_amount || sale.total || sale.grand_total || 0;
        inc += saleTotal;

        if (sale.sale_items && sale.sale_items.length > 0) {
          sale.sale_items.forEach(item => {
            const qty = item.quantity || item.qty || 1;
            const itemPrice = item.price || item.total_price || 0;
            const itemCost = (item.products && item.products.cost ? item.products.cost : (item.cost || 0)) * qty;
            const itemProfit = (item.total_price || (itemPrice * qty)) - itemCost;
            exp += itemCost;
            const prodName = item.products ? item.products.name : (item.name || item.product_name || 'สินค้า');

            rows += `<tr style="border-bottom:1px solid #eee;">
              <td style="padding:8px;">${dt}</td>
              <td style="padding:8px;">${prodName}</td>
              <td style="padding:8px; text-align:center;">${qty}</td>
              <td style="padding:8px; text-align:right;">${(item.total_price || (itemPrice * qty)).toLocaleString()} บ.</td>
              <td style="padding:8px; text-align:right; color:${itemProfit >= 0 ? '#15803d' : '#b91c1c'}; font-weight:600;">${itemProfit.toLocaleString()} บ.</td>
            </tr>`;
          });
        } else {
          rows += `<tr style="border-bottom:1px solid #eee;">
            <td style="padding:8px;">${dt}</td>
            <td style="padding:8px;">รายการขาย #${sale.id ? String(sale.id).slice(0, 6) : '-'}</td>
            <td style="padding:8px; text-align:center;">-</td>
            <td style="padding:8px; text-align:right;">${saleTotal.toLocaleString()} บ.</td>
            <td style="padding:8px; text-align:right; color:#15803d; font-weight:600;">${saleTotal.toLocaleString()} บ.</td>
          </tr>`;
        }
      });

      if (tbody) tbody.innerHTML = rows;
      const net = inc - exp;
      document.getElementById('rep-inc-val').textContent = inc.toLocaleString() + ' บ.';
      document.getElementById('rep-exp-val').textContent = exp.toLocaleString() + ' บ.';
      
      const netEl = document.getElementById('rep-net-val');
      const netLbl = document.getElementById('rep-net-lbl');
      const netBox = document.getElementById('rep-net-box');
      if (netEl) {
        netEl.textContent = Math.abs(net).toLocaleString() + ' บ.';
        if (net >= 0) {
          netLbl.textContent = 'กำไรสุทธิ';
          netLbl.style.color = '#1e40af';
          netEl.style.color = '#1d4ed8';
          netBox.style.background = '#eff6ff';
        } else {
          netLbl.textContent = 'ขาดทุนสุทธิ';
          netLbl.style.color = '#991b1b';
          netEl.style.color = '#b91c1c';
          netBox.style.background = '#fef2f2';
        }
      }
    } catch (err) {
      console.error('Report error:', err);
    }
  }
'''

import re
text = re.sub(r'async function loadMonthlyReport\(\)\s*\{[\s\S]*?\n  \}', new_load_func, text, count=1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("QUERY_UPDATED_SUCCESS")
