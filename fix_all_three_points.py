# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. ปรับปรุง loadMonthlyReport ให้คิดต้นทุนจริง แสดง 1 แถวต่อ 1 บิล และตารางใหญ่
perfect_monthly_code = '''async function loadMonthlyReport() {
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
      if (tbody) tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; padding:30px; color:#64748b; font-size:1.2rem;">กำลังโหลดข้อมูล...</td></tr>';

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

      // ดึงบิลพร้อมรายการสินค้าเพื่อนำต้นทุนมาคิด
      let q = sb.from('sales').select('id, total, created_at, sale_items(*, products(*))');
      if (currentShop) {
        q = q.eq('shop_id', currentShop);
      }

      let { data: sales, error } = await q
        .gte('created_at', startDate)
        .lte('created_at', endDate)
        .order('created_at', { ascending: true });

      if (error || !sales || sales.length === 0) {
        if (tbody) tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; padding:32px; color:#888; font-size:1.2rem;">ไม่มีรายการขายในเดือนนี้</td></tr>';
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
        const billNo = idx + 1; // เริ่มนับ 1
        const amt = Number(s.total) || 0;
        totalIncome += amt;
        const dt = new Date(s.created_at).toLocaleDateString('th-TH', { day: 'numeric', month: 'short' });

        // คำนวณต้นทุนรวมของบิลนี้
        let billCost = 0;
        let mainProductName = 'ขายหน้าร้าน';
        if (s.sale_items && s.sale_items.length > 0) {
          mainProductName = s.sale_items.map(it => (it.products ? it.products.name : (it.name || 'สินค้า'))).join(', ');
          s.sale_items.forEach(it => {
            const costUnit = it.products ? (Number(it.products.cost) || 0) : 0;
            const qVal = Number(it.quantity) || 1;
            billCost += (costUnit * qVal);
          });
        }
        totalCost += billCost;
        const billProfit = amt - billCost;

        rowHtml += `<tr style="border-bottom:1px solid #e2e8f0; font-size:1.25rem;">
          <td style="padding:22px 16px; font-weight:500; color:#475569; vertical-align:middle;">${dt}</td>
          <td style="padding:22px 16px; font-weight:600; color:#0f172a; vertical-align:middle;">บิลที่ ${billNo}</td>
          <td style="padding:22px 16px; text-align:center; font-weight:600; color:#334155; vertical-align:middle;">1</td>
          <td style="padding:22px 16px; text-align:right; font-weight:600; color:#0f172a; vertical-align:middle;">${amt.toLocaleString()} บ.</td>
          <td style="padding:22px 16px; text-align:right; font-weight:700; color:#16a34a; vertical-align:middle;">${billProfit.toLocaleString()} บ.</td>
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
text = re.sub(r'async function loadMonthlyReport\(\)\s*\{[\s\S]*?\n  \}', perfect_monthly_code, text, count=1)

# 2. ปรับปรุงตารางประวัติการขายหน้าร้าน (Recent Sales) ให้แสดงเลขบิลเรียงตามลำดับเริ่มที่ #1
# ค้นหาจุดที่แสดง '#'+s.id หรือ #${s.id} หรือ類似กันในส่วนประวัติการขาย
text = re.sub(r'#[\'\"\`]?\s*\+\s*s\.id', r"'#' + (sales.length - idx)", text)
text = re.sub(r'#\{\s*s\.id\s*\}', r"#${sales.length - idx}", text)
text = re.sub(r'#[\'\"\`]?\s*\+\s*sale\.id', r"'#' + (sales.length - idx)", text)
text = re.sub(r'#\{\s*sale\.id\s*\}', r"#${sales.length - idx}", text)

# 3. ขยายขนาดตารางทั้งหน้ารายงานและหน้าขาย
text = text.replace('th style="padding:8px;"', 'th style="padding:18px 16px; font-size:1.25rem;"')
text = text.replace('th style="padding:8px; text-align:center;"', 'th style="padding:18px 16px; font-size:1.25rem; text-align:center;"')
text = text.replace('th style="padding:8px; text-align:right;"', 'th style="padding:18px 16px; font-size:1.25rem; text-align:right;"')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

with open('www/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("ALL_THREE_POINTS_APPLIED")
