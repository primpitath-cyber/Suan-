with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = "const { data, error } = await sb.from('shops').select('id, name').order('created_at', { ascending: false });"
replacement = "const { data, error } = await sb.from('shops').select('id, name').eq('owner_id', currentUser.id).order('created_at', { ascending: false });"

if target in text:
    text = text.replace(target, replacement)
    print("Direct string replacement successful!")
else:
    # เผื่อช่องว่างไม่ตรงกัน
    lines = text.split('\n')
    new_lines = []
    for line in lines:
        if "from('shops').select(" in line and "loadShops" not in line:
            line = line.replace("select('id, name')", "select('id, name').eq('owner_id', currentUser.id)")
        new_lines.append(line)
    text = '\n'.join(new_lines)
    print("Line-by-line replacement applied!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

import os
if os.path.exists('www/index.html'):
    with open('www/index.html', 'w', encoding='utf-8') as f:
        f.write(text)

