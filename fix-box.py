with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# CSS เจาะจงแก้กล่องวันหมดอายุ และ container ทุกตัวไม่ให้ล้น
strict_css = """
/* Fix dashed container and inner inputs */
div[style*="border"], div[class*="border"], fieldset, form div {
  max-width: 100% !important;
  box-sizing: border-box !important;
}

input[type="text"], input[type="date"], input[type="number"], select {
  width: 100% !important;
  max-width: 100% !important;
  box-sizing: border-box !important;
  margin-left: 0 !important;
  margin-right: 0 !important;
}
"""

if "/* Fix dashed container" not in html:
    html = html.replace('</head>', f'<style>{strict_css}</style>\n</head>')
else:
    html = html.replace('/* Fix dashed container and inner inputs */', strict_css)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Applied strict box fix")
