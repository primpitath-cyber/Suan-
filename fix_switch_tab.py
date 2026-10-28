# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# โค้ดฟังก์ชัน switchTab ที่รองรับทุกแท็บเดิมและแท็บสรุปยอดอย่างปลอดภัย
switch_func = '''
  function switchTab(tabId) {
    if (tabId === 'tabReports' || tabId === 'reports') {
      tabId = 'tabReports';
      if (typeof loadMonthlyReport === 'function') loadMonthlyReport();
    }

    document.querySelectorAll('.tab-content').forEach(el => {
      el.classList.remove('active');
    });
    document.querySelectorAll('.nav-item').forEach(el => {
      el.classList.remove('active');
    });

    const targetTab = document.getElementById(tabId);
    if (targetTab) {
      targetTab.classList.add('active');
    }

    if (tabId === 'tabPos') { const b = document.getElementById('navPos'); if (b) b.classList.add('active'); }
    if (tabId === 'tabStock') { const b = document.getElementById('navStock'); if (b) b.classList.add('active'); }
    if (tabId === 'tabCalc') { const b = document.getElementById('navCalc'); if (b) b.classList.add('active'); }
    if (tabId === 'tabReports') { const b = document.getElementById('navReports'); if (b) b.classList.add('active'); }
    if (tabId === 'tabSettings') { const b = document.getElementById('navSettings'); if (b) b.classList.add('active'); }
    window.scrollTo(0, 0);
  }
'''

# วางไว้เหนือ switchAuthMode
if 'function switchTab' not in text:
    text = text.replace('function switchAuthMode(mode) {', switch_func + '\n  function switchAuthMode(mode) {', 1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

with open('www/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("SWITCH_TAB_RESTORED_SUCCESSFULLY")
