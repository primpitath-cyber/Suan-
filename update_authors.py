# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# สร้าง HTML โครงสร้างผู้จัดทำทั้งหมดตามข้อมูลของกลุ่ม
new_modal_content = '''<!-- Popup แสดงชื่อผู้จัดทำ -->
<div id="authorModal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(15,23,42,0.65); z-index:99999; justify-content:center; align-items:center; backdrop-filter:blur(4px); padding:16px; box-sizing:border-box;">
  <div style="background:#ffffff; border-radius:24px; width:100%; max-width:480px; max-height:90vh; overflow-y:auto; padding:28px 22px; box-shadow:0 25px 50px -12px rgba(0,0,0,0.25); text-align:center; animation:fadeInModal 0.25s ease-out; box-sizing:border-box;">
    
    <div style="width:60px; height:60px; background:#e8f5e9; border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto 12px auto; font-size:2rem;">
      🌱
    </div>

    <h3 style="font-size:1.35rem; font-weight:700; color:#0f172a; margin:0 0 4px 0;">คณะผู้จัดทำโครงงาน</h3>
    <p style="font-size:0.95rem; color:#16a34a; font-weight:600; margin:0 0 16px 0;">ระบบจัดการผลผลิตทางการเกษตร "สวนพร้อม"</p>
    
    <div style="background:#f8fafc; border-radius:14px; padding:12px 16px; margin-bottom:16px; text-align:left; border:1px solid #e2e8f0; font-size:0.9rem; color:#475569; line-height:1.5;">
      <div style="font-weight:700; color:#1e293b;">สถาบันเทคโนโลยีพระจอมเกล้าเจ้าคุณทหารลาดกระบัง</div>
      <div>คณะเทคโนโลยีการเกษตร • สาขานิเทศศาสตร์เกษตร (ชั้นปีที่ 2)</div>
    </div>

    <div style="text-align:left; border:1px solid #e2e8f0; border-radius:16px; padding:6px 14px; background:#ffffff; margin-bottom:20px;">
      
      <div style="display:flex; justify-content:space-between; align-items:center; padding:10px 0; border-bottom:1px solid #f1f5f9;">
        <div>
          <div style="font-weight:600; color:#0f172a; font-size:0.95rem;">นางสาวพริมพริตา โพธิ์ทอง</div>
        </div>
        <span style="background:#dcfce7; color:#166534; font-size:0.75rem; font-weight:700; padding:4px 8px; border-radius:20px;">Project Manager</span>
      </div>

      <div style="display:flex; justify-content:space-between; align-items:center; padding:10px 0; border-bottom:1px solid #f1f5f9;">
        <div>
          <div style="font-weight:600; color:#0f172a; font-size:0.95rem;">นายกฤตณัฐ ธีระเกตุ</div>
        </div>
        <span style="background:#e0f2fe; color:#0369a1; font-size:0.75rem; font-weight:700; padding:4px 8px; border-radius:20px;">Programmer</span>
      </div>

      <div style="display:flex; justify-content:space-between; align-items:center; padding:10px 0; border-bottom:1px solid #f1f5f9;">
        <div>
          <div style="font-weight:600; color:#0f172a; font-size:0.95rem;">นางสาวปัทมา แร่เอ็น</div>
        </div>
        <span style="background:#fef3c7; color:#92400e; font-size:0.75rem; font-weight:700; padding:4px 8px; border-radius:20px;">Report</span>
      </div>

      <div style="display:flex; justify-content:space-between; align-items:center; padding:10px 0; border-bottom:1px solid #f1f5f9;">
        <div>
          <div style="font-weight:600; color:#0f172a; font-size:0.95rem;">นางสาวกีรติกานต์ ใยคง</div>
        </div>
        <span style="background:#fef3c7; color:#92400e; font-size:0.75rem; font-weight:700; padding:4px 8px; border-radius:20px;">Report</span>
      </div>

      <div style="display:flex; justify-content:space-between; align-items:center; padding:10px 0; border-bottom:1px solid #f1f5f9;">
        <div>
          <div style="font-weight:600; color:#0f172a; font-size:0.95rem;">นายบุญรักษา วัยวุฒิ</div>
          <div style="font-size:0.8rem; color:#64748b;">รหัส 68040295</div>
        </div>
        <span style="background:#f3e8ff; color:#6b21a8; font-size:0.75rem; font-weight:700; padding:4px 8px; border-radius:20px;">Graphic + Slide</span>
      </div>

      <div style="display:flex; justify-content:space-between; align-items:center; padding:10px 0;">
        <div>
          <div style="font-weight:600; color:#0f172a; font-size:0.95rem;">นางสาวอนัญญา ใจดี</div>
          <div style="font-size:0.8rem; color:#64748b;">รหัส 68040553</div>
        </div>
        <span style="background:#fce7f3; color:#9d174d; font-size:0.75rem; font-weight:700; padding:4px 8px; border-radius:20px;">Report + Slide</span>
      </div>

    </div>

    <button onclick="hideAuthorModal()" style="width:100%; padding:14px; background:#16a34a; color:#ffffff; border:none; border-radius:14px; font-size:1.05rem; font-weight:600; cursor:pointer; box-shadow:0 4px 6px -1px rgba(22,163,74,0.3);">
      ปิดหน้าต่าง
    </button>
  </div>
</div>

<script>
  function showAuthorModal() {
    const modal = document.getElementById('authorModal');
    if (modal) modal.style.display = 'flex';
  }
  function hideAuthorModal() {
    const modal = document.getElementById('authorModal');
    if (modal) modal.style.display = 'none';
  }
</script>'''

# แทนที่ modal เดิมด้วยข้อมูลรายชื่อจริงทั้งหมด
if 'id="authorModal"' in text:
    text = re.sub(r'<!-- Popup แสดงชื่อผู้จัดทำ -->[\s\S]*?<\/script>', new_modal_content, text)
else:
    # เพิ่ม modal ใหม่หากยังไม่มี
    text = text.replace('</body>', new_modal_content + '\n</body>', 1)

# ตรวจสอบให้แน่ใจว่าคลิกที่หัวข้อสวนพร้อมแล้วเรียก showAuthorModal()
if 'showAuthorModal()' not in text:
    text = re.sub(
        r'(>[^<]*สวนพร้อม[^<]*<)',
        r' style="cursor:pointer;" onclick="showAuthorModal()"\1',
        text,
        count=1
    )

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

with open('www/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("AUTHORS_DATA_APPLIED_SUCCESSFULLY")
