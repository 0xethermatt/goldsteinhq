from pathlib import Path

LOGO = '/goldstein-logo-2.png.png'

# index.html
p = Path('index.html')
html = p.read_text()
old_brand = '<div class="brand"><img src="/assets/goldstein-keystone.png" alt="Goldstein"><span>Goldstein</span></div>'
new_brand = f'<div class="brand"><div class="brandViewport"><img class="brandLogo" src="{LOGO}" alt="Goldstein Group"></div></div>'
if old_brand not in html:
    raise SystemExit('index brand marker not found')
html = html.replace(old_brand, new_brand, 1)
index_css = '''
/* Goldstein monolith logo lockup */
.brand{height:78px;justify-content:center;gap:0;padding:8px 14px;overflow:hidden}
.brandViewport{width:176px;height:58px;display:grid;place-items:center;overflow:hidden;position:relative}
.brandLogo{display:block;width:176px;max-width:100%;height:auto;max-height:58px;object-fit:contain;filter:drop-shadow(0 5px 15px rgba(216,180,63,.12))}
@media(max-width:1050px) and (min-width:761px){.brand{padding:0}.brandViewport{width:36px;height:52px}.brandLogo{position:absolute;width:250px;max-width:none;height:auto;max-height:none;left:-10px;top:50%;transform:translateY(-50%)}}
'''
if '/* Goldstein monolith logo lockup */' not in html:
    html = html.replace('</style>', index_css + '</style>', 1)
p.write_text(html)

# welcome.html
p = Path('welcome.html')
html = p.read_text()
old_lock = '<div class="brandLock"><img src="/assets/goldstein-keystone.png" alt=""><div><b>Goldstein Group</b><span>Onchain investment products</span></div></div>'
new_lock = f'<div class="brandLock"><img src="{LOGO}" alt="Goldstein Group"></div>'
if old_lock not in html:
    raise SystemExit('welcome brand lock marker not found')
html = html.replace(old_lock, new_lock, 1)
html = html.replace('<img src="/assets/goldstein-keystone.png" alt="">\n                <small>Minted NFT</small>', f'<img src="{LOGO}" alt="Goldstein Group">\n                <small>Minted NFT</small>', 1)
old_canvas = "try{const logo=await loadImage('/assets/goldstein-keystone.png');ctx.drawImage(logo,74,66,70,70)}catch{}\n  ctx.fillStyle='#f4f1e8';ctx.font='700 34px Arial';ctx.fillText('GOLDSTEIN GROUP',162,98);ctx.fillStyle='#c8b981';ctx.font='700 17px monospace';ctx.fillText('ONCHAIN INVESTMENT PRODUCTS',162,127);"
new_canvas = f"try{{const logo=await loadImage('{LOGO}');ctx.drawImage(logo,72,54,330,110)}}catch{{}}"
if old_canvas not in html:
    raise SystemExit('welcome canvas logo marker not found')
html = html.replace(old_canvas, new_canvas, 1)
welcome_css = '''
/* Goldstein monolith logo lockup */
.brandLock{left:34px;top:24px;gap:0}
.brandLock img{width:220px;height:auto;max-height:74px;object-fit:contain;filter:drop-shadow(0 5px 18px rgba(0,0,0,.34))}
.nftPlaceholder img{width:170px;height:auto;max-height:72px;margin:0 auto 18px;object-fit:contain;opacity:1}
@media(max-width:520px){.brandLock{left:20px;top:18px}.brandLock img{width:168px;height:auto;max-height:58px}.nftPlaceholder img{width:145px;height:auto;max-height:62px}}
'''
if '/* Goldstein monolith logo lockup */' not in html:
    html = html.replace('</style>', welcome_css + '</style>', 1)
p.write_text(html)

# Regression guards
idx = Path('index.html').read_text()
wel = Path('welcome.html').read_text()
assert LOGO in idx and LOGO in wel
assert 'goldstein-keystone.png" alt="Goldstein"><span>Goldstein' not in idx
assert 'class="brandViewport"' in idx
assert '<span>FAQ</span>' in idx
assert 'What happens after I claim a Seat?' in idx
assert 'secureBtn' in idx and 'seatNumber' in idx and 'characterName' in idx
assert "loadImage('/goldstein-logo-2.png.png')" in wel
print('Logo update applied and regression guards passed')
