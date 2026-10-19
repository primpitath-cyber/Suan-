with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. บังคับ CSS ขั้นเด็ดขาดสำหรับ input วันหมดอายุ และ container
custom_style = """
<style id="permanent-box-fix">
  /* บังคับให้ container เส้นประ และ input ภายใน อยู่ในกรอบ 100% เสมอ */
  div:has(> input[type="date"]), 
  div:has(> input),
  .expiry-container,
  div[style*="border: 2px dashed"],
  div[style*="dashed"] {
    display: block !important;
    width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
    overflow: hidden !important;
  }

  /* บังคับ input ทุกตัวให้อยู่ในกรอบ ไม่ทะลุออกข้าง */
  input, select, textarea {
    display: block !important;
    width: 100% !important;
    max-width: 100% !important;
    min-width: 0 !important;
    box-sizing: border-box !important;
    margin: 0 !important;
  }

  /* ดักจับตารางข้อมูล */
  table {
    display: block !important;
    width: 100% !important;
    overflow-x: auto !important;
    white-space: nowrap !important;
  }
</style>
"""

# แทรกไว้ท้ายสุดก่อนปิด </body> เพื่อให้ override ทุกลำดับของ CSS เดิม
if "id=\"permanent-box-fix\"" not in html:
    html = html.replace('</body>', f'{custom_style}\n</body>')

# อัปเดตเวอร์ชัน Service Worker ให้เลิกแคชไฟล์เก่า
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html with body-level override")
