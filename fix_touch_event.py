# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# เพิ่ม CSS ให้ brand-title แตะได้ชัดเจน และใส่ script ดักทั้ง click + touchend
touch_fix = '''
<style>
  .brand-title {
    cursor: pointer !important;
    pointer-events: auto !important;
    position: relative !important;
    z-index: 100 !important;
    -webkit-tap-highlight-color: rgba(0,0,0,0.1) !important;
  }
  #authorModal {
    z-index: 999999 !important;
  }
</style>
<script>
  window.showAuthorModal = function(e) {
    if (e) {
      e.preventDefault();
      e.stopPropagation();
    }
    var modal = document.getElementById('authorModal');
    if (modal) {
      modal.style.display = 'flex';
    }
  };
  
  window.hideAuthorModal = function(e) {
    if (e) {
      e.preventDefault();
      e.stopPropagation();
    }
    var modal = document.getElementById('authorModal');
    if (modal) {
      modal.style.display = 'none';
    }
  };

  // ผูก touch และ click เข้ากับทุกที่ที่เป็น brand-title ทันทีที่โหลดหน้า
  function bindBrandClick() {
    var brandEls = document.querySelectorAll('.brand-title');
    brandEls.forEach(function(el) {
      el.onclick = window.showAuthorModal;
      el.addEventListener('touchend', function(ev) {
        window.showAuthorModal(ev);
      }, { passive: false });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bindBrandClick);
  } else {
    bindBrandClick();
  }
</script>
'''

text = text.replace('</body>', touch_fix + '\n</body>', 1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

with open('www/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("TOUCH_AND_CLICK_FORCE_BOUND")
