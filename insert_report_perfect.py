# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. แทรกปุ่มเมนูสรุปยอด ตรงหน้า navSettings ให้ตรงกับโครงสร้างจริง
target_nav = '''    <button class="nav-item" id="navSettings" onclick="switchTab('tabSettings')">'''

report_btn = '''    <button class="nav-item" id="navReports" onclick="switchTab('tabReports')">
      <span class="icon">📊</span>
      <span>สรุปยอด</span>
    </button>
'''

if 'id="navReports"' not in c and target_nav in c:
    c = c.replace(target_nav, report_btn + target_nav)
    print("BUTTON_INSERTED_SUCCESSFULLY")
else:
    print("BUTTON_ALREADY_EXISTS_OR_TARGET_NOT_FOUND")

# 2. ตรวจสอบและแทรกแท็บแสดงผล tabReports
if 'id="tabReports"' not in c and 'id="tab-reports"' not in c:
    report_html = '''
  <!-- แท็บสรุปยอด รายรับ-รายจ่าย-กำไรขาดทุน -->
  <div id="tabReports" class="tab-pane" style="display:none; padding:16px;">
    <div style="background:#fff; border-radius:16px; padding:18px; box-shadow:0 2px 10px rgba(0,0,0,0.06);">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
        <h3 style="margin:0; font-size:1.15rem; color:#1e4620; font-weight:700;">📊 สรุปยอด รายรับ - รายจ่าย</h3>
        <input type="month" id="rep-month-input" onchange="loadMonthlyReport()" style="padding:6px 10px; border-radius:8px; border:1px solid #ccc; font-family:inherit;">
      </div>

      <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:10px; margin-bottom:16px;">
        <div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:12px; padding:12px; text-align:center;">
          <div style="font-size:0.8rem; color:#166534; font-weight:600;">รายรับ (ยอดขาย)</div>
          <div id="rep-inc-val" style="font-size:1.1rem; font-weight:700; color:#15803d; margin-top:4px;">0 บ.</div>
        </div>
        <div style="background:#fef2f2; border:1px solid #fecaca; border-radius:12px; padding:12px; text-align:center;">
          <div style="font-size:0.8rem; color:#991b1b; font-weight:600;">รายจ่าย (ต้นทุน)</div>
          <div id="rep-exp-val" style="font-size:1.1rem; font-weight:700; color:#b91c1c; margin-top:4px;">0 บ.</div>
        </div>
        <div id="rep-net-box" style="background:#eff6ff; border:1px solid #bfdbfe; border-radius:12px; padding:12px; text-align:center;">
          <div id="rep-net-lbl" style="font-size:0.8rem; color:#1e40af; font-weight:600;">กำไรสุทธิ</div>
          <div id="rep-net-val" style="font-size:1.1rem; font-weight:700; color:#1d4ed8; margin-top:4px;">0 บ.</div>
        </div>
      </div>

      <h4 style="margin:0 0 10px 0; font-size:0.95rem; color:#555;">รายละเอียดรายการขายประจำเดือน</h4>
      <div style="overflow-x:auto;">
        <table style="width:100%; border-collapse:collapse; font-size:0.85rem; text-align:left;">
          <thead>
            <tr style="border-bottom:2px solid #eee; color:#666;">
              <th style="padding:8px;">วันที่</th>
              <th style="padding:8px;">สินค้า</th>
              <th style="padding:8px; text-align:center;">จำนวน</th>
              <th style="padding:8px; text-align:right;">ยอดขาย</th>
              <th style="padding:8px; text-align:right;">กำไร</th>
            </tr>
          </thead>
          <tbody id="rep-table-rows">
            <tr><td colspan="5" style="text-align:center; padding:16px; color:#999;">กำลังโหลดข้อมูล...</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
'''
    settings_marker = 'id="tabSettings"'
    pos = c.find(settings_marker)
    if pos != -1:
        div_start = c.rfind('<div', 0, pos)
        if div_start != -1:
            c = c[:div_start] + report_html + '\n  ' + c[div_start:]

# 3. ใส่ฟังก์ชันโหลดข้อมูลเดือน
js_fetcher = '''
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
      const { data: sales, error } = await sb
        .from('orders')
        .select('*, products(name, cost, price)')
        .eq('shop_id', currentShopId)
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
      sales.forEach(s => {
        const qty = s.quantity || 1;
        const total = s.total_price || (s.price * qty) || 0;
        const cost = (s.products && s.products.cost ? s.products.cost : 0) * qty;
        const p = total - cost;
        inc += total;
        exp += cost;
        const dt = new Date(s.created_at).toLocaleDateString('th-TH', { day: 'numeric', month: 'short' });
        const name = s.products ? s.products.name : (s.item_name || 'สินค้า');
        rows += `<tr style="border-bottom:1px solid #eee;">
          <td style="padding:8px;">${dt}</td>
          <td style="padding:8px;">${name}</td>
          <td style="padding:8px; text-align:center;">${qty}</td>
          <td style="padding:8px; text-align:right;">${total.toLocaleString()} บ.</td>
          <td style="padding:8px; text-align:right; color:${p >= 0 ? '#15803d' : '#b91c1c'}; font-weight:600;">${p.toLocaleString()} บ.</td>
        </tr>`;
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
      console.error(err);
    }
  }
'''

if 'loadMonthlyReport' not in c:
    c = c.replace('function switchTab(', js_fetcher + '\n  function switchTab(')

if "if (tabId === 'tabReports') loadMonthlyReport();" not in c:
    c = c.replace("function switchTab(tabId) {", "function switchTab(tabId) {\n    if (tabId === 'tabReports') loadMonthlyReport();")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("ALL_DONE")
