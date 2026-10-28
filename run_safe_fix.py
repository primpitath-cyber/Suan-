# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. เพิ่มปุ่มเมนูสรุปยอด
btn_html = '''<button class="nav-item" id="navReports" onclick="switchTab('tabReports')">
      <span class="icon">📊</span>
      <span>สรุปยอด</span>
    </button>\n    '''
target_btn = '<button class="nav-item" id="navSettings"'
if 'id="navReports"' not in text and target_btn in text:
    text = text.replace(target_btn, btn_html + target_btn, 1)

# 2. เพิ่มกล่องเนื้อหาแท็บสรุปยอด
tab_view = '''
  <div id="tabReports" class="tab-content" style="padding:16px;">
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
              <th style="padding:8px;">รายการ</th>
              <th style="padding:8px; text-align:center;">จำนวน</th>
              <th style="padding:8px; text-align:right;">ยอดขาย</th>
              <th style="padding:8px; text-align:right;">กำไร</th>
            </tr>
          </thead>
          <tbody id="rep-table-rows">
            <tr><td colspan="5" style="text-align:center; padding:16px; color:#888;">กำลังโหลด...</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
'''
if 'id="tabReports"' not in text:
    settings_idx = text.find('id="tabSettings"')
    div_start = text.rfind('<div', 0, settings_idx)
    text = text[:div_start] + tab_view + '\n' + text[div_start:]

# 3. ใส่ฟังก์ชัน loadMonthlyReport
js_load = '''
  async function loadMonthlyReport() {
    try {
      const mInput = document.getElementById('rep-month-input');
      if (mInput && !mInput.value) {
        const d = new Date();
        mInput.value = d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0');
      }
      const parts = (mInput ? mInput.value : '').split('-');
      const y = Number(parts[0]);
      const m = Number(parts[1]);
      const start = new Date(y, m - 1, 1).toISOString();
      const end = new Date(y, m, 0, 23, 59, 59).toISOString();

      let q = sb.from('sales').select('id, total, created_at');
      if (typeof activeShopId !== 'undefined' && activeShopId) {
        q = q.eq('shop_id', activeShopId);
      }
      const { data: sales, error } = await q.gte('created_at', start).lte('created_at', end).order('created_at', { ascending: false });

      const tbody = document.getElementById('rep-table-rows');
      if (error || !sales || sales.length === 0) {
        if (tbody) tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; padding:16px; color:#888;">ไม่มีรายการขายในเดือนนี้</td></tr>';
        document.getElementById('rep-inc-val').textContent = '0 บ.';
        document.getElementById('rep-exp-val').textContent = '0 บ.';
        document.getElementById('rep-net-val').textContent = '0 บ.';
        return;
      }

      let inc = 0;
      let rows = '';
      sales.forEach(s => {
        const amt = Number(s.total) || 0;
        inc += amt;
        const dt = new Date(s.created_at).toLocaleDateString('th-TH', { day: 'numeric', month: 'short' });
        rows += `<tr style="border-bottom:1px solid #eee;">
          <td style="padding:8px;">${dt}</td>
          <td style="padding:8px;">บิลขาย #${String(s.id).slice(0, 6)}</td>
          <td style="padding:8px; text-align:center;">1</td>
          <td style="padding:8px; text-align:right;">${amt.toLocaleString()} บ.</td>
          <td style="padding:8px; text-align:right; color:#15803d; font-weight:600;">${amt.toLocaleString()} บ.</td>
        </tr>`;
      });

      if (tbody) tbody.innerHTML = rows;
      document.getElementById('rep-inc-val').textContent = inc.toLocaleString() + ' บ.';
      document.getElementById('rep-exp-val').textContent = '0 บ.';
      document.getElementById('rep-net-val').textContent = inc.toLocaleString() + ' บ.';
    } catch(err) {
      console.error(err);
    }
  }
'''
if 'loadMonthlyReport' not in text:
    text = text.replace('function switchTab(', js_load + '\n  function switchTab(')

# 4. เพิ่มการสลับแท็บให้ tabReports
hook = """if (tabId === 'tabSettings') document.getElementById('navSettings').classList.add('active');
    if (tabId === 'tabReports') {
      const b = document.getElementById('navReports');
      if (b) b.classList.add('active');
      loadMonthlyReport();
    }"""
text = text.replace("if (tabId === 'tabSettings') document.getElementById('navSettings').classList.add('active');", hook)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("SCRIPT_SUCCESSFULLY_APPLIED")
