from pathlib import Path
import re

NFTS = [
    ('01.png', 'Seat #01', 'available', 'Available'),
    ('02.png', 'Seat #02', 'claimed', 'Claimed'),
    ('03.png', 'Seat #03', 'available', 'Available'),
    ('10.png', 'Seat #10', 'available', 'Available'),
    ('11.png', 'Seat #11', 'claimed', 'Claimed'),
    ('12.png', 'Seat #12', 'claimed', 'Claimed'),
    ('18.png', 'Seat #18', 'claimed', 'Claimed'),
    ('b10.png', 'Seat B10', 'claimed', 'House manager'),
    ('b17.png', 'Seat B17', 'claimed', 'House manager'),
]


def add_css(path, css, marker):
    p = Path(path)
    s = p.read_text()
    if marker not in s:
        s = s.replace('</style>', f'\n{css}\n</style>', 1)
        p.write_text(s)
    return s


def patch_mint_floor():
    p = Path('app.html')
    s = p.read_text()
    css = r'''
/* Real legendary Seat artwork */
.miniArt{overflow:hidden;background:#0b0b08!important}
.miniArt img{display:block;width:100%;height:100%;object-fit:cover;object-position:center;transition:transform .28s ease,filter .28s ease}
.mini:hover .miniArt img{transform:scale(1.035)}
.mini.claimed .miniArt:after{z-index:2}
.mini.houseManager{opacity:.86;border-color:#4b3f22}
.mini.houseManager .miniArt:after{content:"HOUSE MANAGER";position:absolute;inset:auto 8px 8px 8px;display:block;padding:7px 8px;border:1px solid rgba(224,185,54,.34);border-radius:7px;background:rgba(7,7,5,.82);color:#edcb57;text-align:center;font:850 8px/1 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.1em}
.mini.houseManager small{color:#d4b74f!important}
'''
    if '/* Real legendary Seat artwork */' not in s:
        s = s.replace('</style>', '\n' + css + '\n</style>', 1)

    cards = []
    for filename, label, status, status_label in NFTS:
        extra = ' houseManager' if status_label == 'House manager' else ''
        cards.append(
            f'    <div class="mini {status}{extra}" data-status="{status}">'
            f'<div class="miniArt"><img src="/{filename}" alt="Goldstein {label} NFT"></div>'
            f'<div class="miniBody"><b>{label}</b><small class="mono">{status_label}</small></div></div>'
        )
    grid = '<div class="floorGrid" id="floorGrid">\n' + '\n'.join(cards) + '\n  </div>'
    pattern = re.compile(r'<div class="floorGrid" id="floorGrid">.*?</div>\s*\n\s*</section>', re.S)
    if not pattern.search(s):
        raise SystemExit('Could not locate mint Floor grid')
    s = pattern.sub(grid + '\n  \n</section>', s, count=1)
    p.write_text(s)


def patch_funds():
    p = Path('funds.html')
    s = p.read_text()
    css = r'''
/* House manager NFT portraits */
.managerPfp{overflow:hidden;background:#0b0b08!important}
.managerPfp img{display:block;width:100%;height:100%;object-fit:cover;object-position:center}
'''
    if '/* House manager NFT portraits */' not in s:
        s = s.replace('</style>', '\n' + css + '\n</style>', 1)

    # The two fund cards occur in gAIX then gMEMESTONK order.
    old = '<div class="managerPfp" aria-label="Fund manager NFT placeholder"></div>'
    replacements = [
        '<div class="managerPfp" aria-label="gAIX manager NFT — Seat B10"><img src="/b10.png" alt="Seat B10, manager of gAIX"></div>',
        '<div class="managerPfp" aria-label="gMEMESTONK manager NFT — Seat B17"><img src="/b17.png" alt="Seat B17, manager of gMEMESTONK"></div>',
    ]
    if old in s:
        for repl in replacements:
            s = s.replace(old, repl, 1)
    elif '/b10.png' not in s or '/b17.png' not in s:
        raise SystemExit('Could not locate G-Fund manager placeholders')

    s = s.replace('House manager · NFT</small>', 'Seat B10 · House manager</small>', 1)
    s = s.replace('House manager · NFT</small>', 'Seat B17 · House manager</small>', 1)
    p.write_text(s)


def patch_fund_detail():
    p = Path('fund-detail.html')
    s = p.read_text()
    css = r'''
/* House manager NFT portrait */
.pfp{overflow:hidden;background:#0b0b08!important}
.pfp img{display:block;width:100%;height:100%;object-fit:cover;object-position:center}
'''
    if '/* House manager NFT portrait */' not in s:
        s = s.replace('</style>', '\n' + css + '\n</style>', 1)

    if 'id="managerImage"' not in s:
        s = s.replace('<div class="pfp"></div>', '<div class="pfp"><img id="managerImage" src="/b10.png" alt="Goldstein house manager NFT"></div>', 1)
    needle = "const data=meme?"
    if needle not in s:
        raise SystemExit('Could not locate fund-detail data bootstrap')
    if "$('managerImage').src=meme?'/b17.png':'/b10.png';" not in s:
        s = s.replace("if(meme)$('top').classList.add('volatile');", "if(meme)$('top').classList.add('volatile');$('managerImage').src=meme?'/b17.png':'/b10.png';$('managerImage').alt=meme?'Seat B17, manager of gMEMESTONK':'Seat B10, manager of gAIX';")
    p.write_text(s)


def patch_public_landing(path):
    p = Path(path)
    if not p.exists():
        return
    s = p.read_text()
    css = r'''
/* House manager identity on G-Fund cards */
.productManager{display:flex;align-items:center;gap:9px;margin-top:19px;color:#756e5d}
.productManager img{width:40px;height:40px;border:1px solid #4a4026;border-radius:9px;object-fit:cover;background:#0a0a07}
.productManager b{display:block;color:#d8cba8;font-size:10px}.productManager small{display:block;margin-top:2px;font-size:8px;letter-spacing:.09em;text-transform:uppercase}
.product .productManager+h3{margin-top:26px}
'''
    if '/* House manager identity on G-Fund cards */' not in s:
        s = s.replace('</style>', '\n' + css + '\n</style>', 1)

    if 'Seat B10</b><small>House manager NFT' not in s:
        s = s.replace('</div><h3>Goldstein AI Index</h3>', '</div><div class="productManager"><img src="/b10.png" alt="Seat B10, manager of gAIX"><span><b>Seat B10</b><small>House manager NFT</small></span></div><h3>Goldstein AI Index</h3>', 1)
    if 'Seat B17</b><small>House manager NFT' not in s:
        s = s.replace('</div><h3>Meme Index</h3>', '</div><div class="productManager"><img src="/b17.png" alt="Seat B17, manager of gMEMESTONK"><span><b>Seat B17</b><small>House manager NFT</small></span></div><h3>Meme Index</h3>', 1)
    p.write_text(s)


patch_mint_floor()
patch_funds()
patch_fund_detail()
patch_public_landing('index.html')
patch_public_landing('landing.html')
print('Integrated NFT artwork into Mint Floor, G-Funds and public landing.')
