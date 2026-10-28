# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

simple_report_code = '''async function loadMonthlyReport() {
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
      if (tbody) tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; padding:24px; color:#64748b; font-size:1.1rem;">กำลังโหลดข้อมูล...</td></tr>';

      // หารหัสร้านปัจจุบัน
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

      // ดึงข้อมูลบิลขายเรียงจากบิลแรกไปล่าสุดเพื่อเริ่มบิลที่ 1
      let q = sb.from('sales').select('id, total, created_at');
      if (currentShop) {
        q = q.eq('shop_id', currentShop);
      }

      let { data: sales, error } = await q
        .gte('created_at', startDate)
        .lte('created_at', endDate)
        .order('created_at', { ascending: true });

      if (error || !sales || sales.length === 0) {
        if (tbody) tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; padding:28px; color:#888; font-size:1.1rem;">ไม่มีรายการขายในเดือนนี้</td></tr>';
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

      // แสดงเป็นรายบิล เริ่มจากบิลที่ 1
      sales.forEach((s, idx) => {
        const billNo = idx + 1;
        const amt = Number(s.total) || 0;
        totalIncome += amt;
        const dt = new Date(s.created_at).toLocaleDateString('th-TH', { day: 'numeric', month: 'short' });

        rowHtml += `<tr style="border-bottom:1px solid #e2e8f0; font-size:1.15rem;">
          <td style="padding:18px 12px; font-weight:500; color:#475569; vertical-align:middle;">${dt}</td>
          <td style="padding:18px 12px; font-weight:600; color:#0f172a; vertical-align:middle;">บิลที่ ${billNo}</td>
          <td style="padding:18px 12px; text-align:center; font-weight:600; color:#334155; vertical-align:middle;">1</td>
          <td style="padding:18px 12px; text-align:right; font-weight:600; color:#0f172a; vertical-align:middle;">${amt.toLocaleString()} บ.</td>
          <td style="padding:18px 12px; text-align:right; font-weight:700; color:#16a34a; vertical-align:middle;">${amt.toLocaleString()} บ.</td>
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

import re
text = re.sub(r'async function loadMonthlyReport\(\)\s*\{[\s\S]*?\n  \}', simple_report_code, text, count=1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

with open('www/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("RESTORED_SIMPLE_BILLS_SUCCESS")
