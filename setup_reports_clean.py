# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. เพิ่มปุ่มเมนู สรุปยอด ที่แถบนำทางด้านล่าง
old_nav = '''      <button class="nav-item" onclick="switchTab('settings')">
        <span class="nav-icon">⚙️</span>
        <span class="nav-label">จัดการสวน</span>
      </button>'''

new_nav = '''      <button class="nav-item" id="nav-reports" onclick="switchTab('reports')">
        <span class="nav-icon">📊</span>
        <span class="nav-label">สรุปยอด</span>
      </button>
      <button class="nav-item" onclick="switchTab('settings')">
        <span class="nav-icon">⚙️</span>
        <span class="nav-label">จัดการสวน</span>
      </button>'''

if 'switchTab(\'reports\')' not in html and old_nav in html:
    html = html.replace(old_nav, new_nav)

# 2. เพิ่มกล่องเนื้อหาหน้าต่าง สรุปยอด
report_section = '''
    <!-- แท็บสรุปยอด รายรับ-รายจ่าย-กำไรขาดทุน -->
    <section id="tab-reports" class="tab-content" style="display:none;">
      <div class="card">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
          <h2 style="font-size:1.15rem; font-weight:700; color:var(--text-main); margin:0;">📊 สรุปยอด รายรับ - รายจ่าย</h2>
          <input type="month" id="report-month-select" onchange="loadMonthlyReport()" style="padding:6px 10px; border-radius:8px; border:1px solid var(--border-subtle); font-family:inherit; font-size:0.9rem;">
        </div>

        <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:10px; margin-bottom:16px;">
          <div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:12px; padding:12px; text-align:center;">
            <div style="font-size:0.8rem; color:#166534; font-weight:600;">รายรับ (ยอดขาย)</div>
            <div id="rep-income" style="font-size:1.15rem; font-weight:700; color:#15803d; margin-top:4px;">0 บ.</div>
          </div>
          <div style="background:#fef2f2; border:1px solid #fecaca; border-radius:12px; padding:12px; text-align:center;">
            <div style="font-size:0.8rem; color:#991b1b; font-weight:600;">รายจ่าย (ต้นทุน)</div>
            <div id="rep-expense" style="font-size:1.15rem; font-weight:700; color:#b91c1c; margin-top:4px;">0 บ.</div>
          </div>
          <div id="rep-profit-box" style="background:#eff6ff; border:1px solid #bfdbfe; border-radius:12px; padding:12px; text-align:center;">
            <div id="rep-profit-label" style="font-size:0.8rem; color:#1e40af; font-weight:600;">กำไรสุทธิ</div>
            <div id="rep-profit" style="font-size:1.15rem; font-weight:700; color:#1d4ed8; margin-top:4px;">0 บ.</div>
          </div>
        </div>

        <h3 style="font-size:0.95rem; font-weight:600; margin-bottom:8px; color:var(--text-muted);">รายละเอียดรายการขายประจำเดือน</h3>
        <div style="overflow-x:auto;">
          <table style="width:100%; border-collapse:collapse; font-size:0.85rem; text-align:left;">
            <thead>
              <tr style="border-bottom:2px solid var(--border-subtle); color:var(--text-muted);">
                <th style="padding:8px;">วันที่</th>
                <th style="padding:8px;">สินค้า</th>
                <th style="padding:8px; text-align:center;">จำนวน</th>
                <th style="padding:8px; text-align:right;">ยอดขาย</th>
                <th style="padding:8px; text-align:right;">กำไร</th>
              </tr>
            </thead>
            <tbody id="report-table-body">
              <tr><td colspan="5" style="text-align:center; padding:16px; color:var(--text-muted);">ไม่มีข้อมูลในเดือนนี้</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>
'''

if 'id="tab-reports"' not in html:
    marker = '<!-- แท็บจัดการสวน / สิทธิ์ -->'
    if marker in html:
        html = html.replace(marker, report_section + '\n    ' + marker)
    else:
        html = html.replace('<section id="tab-settings"', report_section + '\n    <section id="tab-settings"')

# 3. ใส่ JavaScript สำหรับคำนวณและโหลดข้อมูล
js_code = '''
    async function loadMonthlyReport() {
      const monthInput = document.getElementById('report-month-select');
      if (!monthInput) return;
      if (!monthInput.value) {
        const now = new Date();
        monthInput.value = now.getFullYear() + '-' + String(now.getMonth() + 1).padStart(2, '0');
      }
      const selectedMonth = monthInput.value;
      const [y, m] = selectedMonth.split('-');
      const startDate = new Date(y, m - 1, 1).toISOString();
      const endDate = new Date(y, m, 0, 23, 59, 59).toISOString();

      try {
        const { data: sales, error } = await sb
          .from('orders')
          .select('*, products(name, cost, price)')
          .eq('shop_id', currentShopId)
          .gte('created_at', startDate)
          .lte('created_at', endDate)
          .order('created_at', { ascending: false });

        let totalIncome = 0;
        let totalCost = 0;
        const tbody = document.getElementById('report-table-body');

        if (!sales || sales.length === 0) {
          if (tbody) tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; padding:16px; color:var(--text-muted);">ไม่มีรายการขายในเดือนนี้</td></tr>';
          document.getElementById('rep-income').textContent = '0 บ.';
          document.getElementById('rep-expense').textContent = '0 บ.';
          document.getElementById('rep-profit').textContent = '0 บ.';
          return;
        }

        let rowHtml = '';
        sales.forEach(s => {
          const qty = s.quantity || 1;
          const income = s.total_price || (s.price * qty) || 0;
          const prodCost = s.products ? (s.products.cost || 0) : 0;
          const cost = prodCost * qty;
          const profit = income - cost;

          totalIncome += income;
          totalCost += cost;

          const dateStr = new Date(s.created_at).toLocaleDateString('th-TH', { day: 'numeric', month: 'short' });
          const prodName = s.products ? s.products.name : (s.item_name || 'สินค้า');

          rowHtml += `<tr style="border-bottom:1px solid var(--border-subtle);">
            <td style="padding:8px;">${dateStr}</td>
            <td style="padding:8px;">${prodName}</td>
            <td style="padding:8px; text-align:center;">${qty}</td>
            <td style="padding:8px; text-align:right;">${income.toLocaleString()} บ.</td>
            <td style="padding:8px; text-align:right; color:${profit >= 0 ? '#15803d' : '#b91c1c'}">${profit.toLocaleString()} บ.</td>
          </tr>`;
        });

        if (tbody) tbody.innerHTML = rowHtml;
        const netProfit = totalIncome - totalCost;

        document.getElementById('rep-income').textContent = totalIncome.toLocaleString() + ' บ.';
        document.getElementById('rep-expense').textContent = totalCost.toLocaleString() + ' บ.';
        
        const profitEl = document.getElementById('rep-profit');
        const profitBox = document.getElementById('rep-profit-box');
        const profitLabel = document.getElementById('rep-profit-label');

        if (profitEl) {
          profitEl.textContent = Math.abs(netProfit).toLocaleString() + ' บ.';
          if (netProfit >= 0) {
            profitLabel.textContent = 'กำไรสุทธิ';
            profitLabel.style.color = '#1e40af';
            profitEl.style.color = '#1d4ed8';
            profitBox.style.background = '#eff6ff';
          } else {
            profitLabel.textContent = 'ขาดทุนสุทธิ';
            profitLabel.style.color = '#991b1b';
            profitEl.style.color = '#b91c1c';
            profitBox.style.background = '#fef2f2';
          }
        }
      } catch (err) {
        console.error('Report error:', err);
      }
    }
'''

if 'loadMonthlyReport' not in html:
    html = html.replace('function switchTab(tabId) {', js_code + '\n    function switchTab(tabId) {')

# เรียกฟังก์ชันเมื่อกดเปลี่ยนแท็บมาที่ reports
hook = "if (tabId === 'reports') loadMonthlyReport();"
if hook not in html:
    html = html.replace('function switchTab(tabId) {', 'function switchTab(tabId) {\n      ' + hook)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('INSTALLATION_SUCCESSFUL')
