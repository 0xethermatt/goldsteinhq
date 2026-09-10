from pathlib import Path

p = Path('index.html')
html = p.read_text()

old = '<div class="brand"><div class="brandViewport"><img class="brandLogo" src="/goldstein-logo-2.png.png" alt="Goldstein Group"></div></div>'
new = '<div class="brand"><span class="brandText">Goldstein HQ</span></div>'

if old not in html:
    raise SystemExit('Current sidebar logo marker not found')
html = html.replace(old, new, 1)

css = '''
/* Goldstein HQ sidebar wordmark */
.brand{height:72px;justify-content:flex-start;gap:0;padding:0 18px;overflow:visible}
.brandText{display:block;color:#f4f1e8;font-size:18px;font-weight:850;letter-spacing:-.025em;line-height:1;white-space:nowrap}
@media(max-width:1050px) and (min-width:761px){
  .brand{height:72px;justify-content:center;padding:0}
  .brandText{font-size:0}
  .brandText:after{content:"HQ";font-size:16px;font-weight:900;letter-spacing:.02em;color:#f0df9d}
}
'''
html = html.replace('</style>', css + '</style>', 1)

# Guards: only change the main sidebar brand; keep the full monolith logo elsewhere.
assert '<span class="brandText">Goldstein HQ</span>' in html
assert '<div class="brand"><div class="brandViewport">' not in html
assert 'Reveal</span>' in html and 'The Floor</span>' in html and 'FAQ</span>' in html
assert 'secureBtn' in html and 'seatNumber' in html and 'characterName' in html

p.write_text(html)
print('Sidebar updated to Goldstein HQ')
