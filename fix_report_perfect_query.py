# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

new_code = '''
  async function loadMonthlyReport() {
    const tbody = document.getElementById('rep-table-rows');
    const incEl = document.getElementById('rep-inc-val');
    const expEl = document.getElementById('rep-exp-val');
    const netEl = document.getElementById('rep-net-val');
    const netLbl = document.getElementById('rep-net-lbl');
    const netBox = document.getElementById('rep-net-box');

    const mInput = document.getElementById('rep-month-input');
    if (!mInput) return;
    if (!mInput.value) {
      const now = new Date();
      mInput.value = now.getFullYear() + '-' + String(now.getMonth() + 1).padStart(2, '0');
    }
    const [y, m] = mInput.value.split('-');
    const startDate = new Date(Number(y), Number(m) - 1, 1).toISOString();
    const endDate = new Date(Number(y), Number(m), 0, 23, 59, 59).toISOString();

    if (tbody) tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; padding:16px; color:#888;">กำลังโหลดข้อมูล...</td></tr>';

    try {
      const targetShop = (typeof activeShopId !== 'undefined' && activeShopId) 
        ? activeShopId 
        : ((typeof currentShopId !== 'undefined' && currentShopId) ? currentShopId : null);

      let q = sb.from('sales').select('id, total, created_at');
      if (targetShop) {
        q = q.eq('shop_id', targetShop);
      }
      const { data: sales, error: sErr } = await q
        .gte('created_at', startDate)
        .lte('created_at', endDate)
        .order('created_at', { ascending: false });

      if (sErr || !sales || sales.length === 0) {
        if (tbody) tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; padding:16px; color:#888;">ไม่มีรายการขายในเดือนนี้</td></tr>';
        if (incEl) incEl.textContent = '0 บ.';
        if (expEl) expEl.textContent = '0 บ.';
        if (netEl) netEl.textContent = '0 บ.';
        return;
      }

      let totalIncome = 0;
      let totalCost = 0;
      const saleIds = sales.map(s => s.id);

      // ดึงรายละเอียดสินค้าจาก sale_items
      let itemsMap = {};
      try {
        const { data: items } = await sb.from('sale_items').select('*').in('sale_id', saleIds);
        if (items && items.length > 0) {
          items.forEach(it => {
            if (!itemsMap[it.sale_id]) itemsMap[it.sale_id] = [];
            itemsMap[it.sale_id].push(it);
          });
        }
      } catch (e) {
        console.warn('Item load error:', e);
      }

      let rowsHtml = '';
      sales.forEach(sale => {
        const dt = new Date(sale.created_at).toLocaleDateString('th-TH', { day: 'numeric', month: 'short' });
        const sTotal = Number(sale.total) || 0;
        totalIncome += sTotal;

        const saleItems = itemsMap[sale.id];
        if (saleItems && saleItems.length > 0) {
          saleItems.forEach(it => {
            const qty = Number(it.quantity || it.qty || 1);
            const lineTotal = Number(it.total_price || (it.price * qty) || sTotal);
            const lineCost = Number(it.cost ? it.cost * qty : 0);
            const lineProfit = lineTotal - lineCost;
            totalCost += lineCost;

            rowsHtml += `<tr style="border-bottom:1px solid #eee;">
              <td style="padding:8px;">${dt}</td>
              <td style="padding:8px;">${it.name || it.product_name || 'สินค้า'}</td>
              <td style="padding:8px; text-align:center;">${qty}</td>
              <td style="padding:8px; text-align:right;">${lineTotal.toLocaleString()} บ.</td>
              <td style="padding:8px; text-align:right; color:${lineProfit >= 0 ? '#15803d' : '#b91c1c'}; font-weight:600;">${lineProfit.toLocaleString()} บ.</td>
            </tr>`;
          });
        } else {
          rowsHtml += `<tr style="border-bottom:1px solid #eee;">
            <td style="padding:8px;">${dt}</td>
            <td style="padding:8px;">บิลขาย #${String(sale.id).slice(0, 6)}</td>
            <td style="padding:8px; text-align:center;">1</td>
            <td style="padding:8px; text-align:right;">${sTotal.toLocaleString()} บ.</td>
            <td style="padding:8px; text-align:right; color:#15803d; font-weight:600;">${sTotal.toLocaleString()} บ.</td>
          </tr>`;
        }
      });

      if (tbody) tbody.innerHTML = rowsHtml;
      if (incEl) incEl.textContent = totalIncome.toLocaleString() + ' บ.';
      if (expEl) expEl.textContent = totalCost.toLocaleString() + ' บ.';

      const net = totalIncome - totalCost;
      if (netEl) {
        netEl.textContent = Math.abs(net).toLocaleString() + ' บ.';
        if (net >= 0) {
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
      if (tbody) tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; padding:16px; color:#e11d48;">เกิดข้อผิดพลาดในการโหลดข้อมูล</td></tr>';
    }
  }
'''

import re
text = re.sub(r'async function loadMonthlyReport\(\)\s*\{[\s\S]*?\n  \}', new_code, text, count=1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("FIX_REPORT_QUERY_SUCCESS")
