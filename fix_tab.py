with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = '<button class="nav-item" id="navSettings"'
new_btn = '''<button class="nav-item" id="navReports" onclick="switchTab('tabReports')">
      <span class="icon">📊</span>
      <span>สรุปยอด</span>
    </button>\n    '''

if 'id="navReports"' not in text and target in text:
    text = text.replace(target, new_btn + target)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("SUCCESS_INSERT_BUTTON")
else:
    print("ALREADY_EXISTS_OR_NOT_FOUND")
