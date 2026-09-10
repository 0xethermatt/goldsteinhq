from pathlib import Path

ROOT = Path('.')


def require(text, needle, label):
    if needle not in text:
        raise SystemExit(f'Missing anchor: {label}')


def replace_once(text, old, new, label):
    require(text, old, label)
    return text.replace(old, new, 1)


def append_css(text, css, marker):
    if marker not in text:
        require(text, '</style>', f'{marker} style close')
        text = text.replace('</style>', css + '\n</style>', 1)
    return text


# Ensure the three user-supplied fund logos are present.
for asset in ['gAIX.png', 'gMEMESTOCK.png', 'gDefensive.png']:
    if not (ROOT / asset).exists():
        raise SystemExit(f'Missing fund logo: {asset}')


# ------------------------------------------------------------------
# G-Funds overview: use fund marks as the primary fund identity.
# ------------------------------------------------------------------
p = ROOT / 'funds.html'
s = p.read_text()

s = replace_once(
    s,
    '<div class="managerPfp" aria-label="gAIX manager NFT — Seat B10"><img src="/b10.png" alt="Seat B10, manager of gAIX"></div><div class="managerMeta"><div class="ticker mono">$gAIX</div><small class="mono">Seat B10 · House manager</small></div>',
    '<div class="managerPfp fundLogo" aria-label="gAIX fund logo"><img src="/gAIX.png" alt="gAIX fund logo"></div><div class="managerMeta"><div class="ticker mono">$gAIX</div><small class="mono">House fund · managed by Seat B10</small></div>',
    'funds gAIX identity',
)
s = replace_once(
    s,
    '<div class="managerPfp" aria-label="gMEMESTONK manager NFT — Seat B17"><img src="/b17.png" alt="Seat B17, manager of gMEMESTONK"></div><div class="managerMeta"><div class="ticker mono">$gMEMESTONK</div><small class="mono">Seat B17 · House manager</small></div>',
    '<div class="managerPfp fundLogo" aria-label="gMEMESTONK fund logo"><img src="/gMEMESTOCK.png" alt="gMEMESTONK fund logo"></div><div class="managerMeta"><div class="ticker mono">$gMEMESTONK</div><small class="mono">House fund · managed by Seat B17</small></div>',
    'funds meme identity',
)
s = replace_once(
    s,
    '<div class="comingIcon"></div><div><h3>Goldstein Preserve</h3>',
    '<div class="comingIcon fundLogo"><img src="/gDefensive.png" alt="Goldstein Preserve fund logo"></div><div><h3>Goldstein Preserve</h3>',
    'funds defensive identity',
)

s = append_css(s, r'''

/* House-fund logos v1 */
.managerPfp.fundLogo,.comingIcon.fundLogo{position:relative;overflow:hidden;background:#020202!important;border-color:#44391d;box-shadow:0 8px 26px rgba(0,0,0,.24)}
.managerPfp.fundLogo img,.comingIcon.fundLogo img{position:absolute;left:50%;top:50%;width:132%;height:132%;max-width:none;transform:translate(-50%,-50%);object-fit:cover;object-position:center}
.comingIcon.fundLogo{width:52px;height:52px;flex:0 0 52px}
''', '/* House-fund logos v1 */')
p.write_text(s)


# ------------------------------------------------------------------
# Fund detail: fund logo at the top; manager NFT remains in manager card.
# ------------------------------------------------------------------
p = ROOT / 'fund-detail.html'
s = p.read_text()

s = replace_once(
    s,
    '<div class="pfp"><img id="managerImage" src="/b10.png" alt="Goldstein house manager NFT"></div>',
    '<div class="pfp fundIdentityLogo"><img id="fundLogoImage" src="/gAIX.png" alt="gAIX fund logo"></div>',
    'detail top identity',
)
s = s.replace("managerImg:'/b17.png',risk:5", "managerImg:'/b17.png',logoImg:'/gMEMESTOCK.png',risk:5")
s = s.replace("managerImg:'/b10.png',risk:3", "managerImg:'/b10.png',logoImg:'/gAIX.png',risk:3")
s = replace_once(
    s,
    "$('managerImage').src=data.managerImg;$('managerImage').alt=data.manager+', manager of $'+data.ticker;\n$('managerImageCard').src=data.managerImg;$('managerImageCard').alt=data.manager+', manager of $'+data.ticker;",
    "$('fundLogoImage').src=data.logoImg;$('fundLogoImage').alt='$'+data.ticker+' fund logo';\n$('managerImageCard').src=data.managerImg;$('managerImageCard').alt=data.manager+', manager of $'+data.ticker;",
    'detail identity script',
)
s = append_css(s, r'''

/* House-fund logo identity v1 */
.fundIdentityLogo{position:relative;overflow:hidden;background:#020202!important;border-color:#51441f!important;box-shadow:0 10px 28px rgba(0,0,0,.28)!important}
.fundIdentityLogo img{position:absolute!important;left:50%;top:50%;width:132%!important;height:132%!important;max-width:none;transform:translate(-50%,-50%);object-fit:cover!important;object-position:center}
''', '/* House-fund logo identity v1 */')
p.write_text(s)


# ------------------------------------------------------------------
# My Seat: show each house-fund logo next to its ticker.
# ------------------------------------------------------------------
p = ROOT / 'my-seat.html'
s = p.read_text()
for ticker, img, label in [
    ('gAIX', '/gAIX.png', 'gAIX fund logo'),
    ('gMEMESTONK', '/gMEMESTOCK.png', 'gMEMESTONK fund logo'),
    ('gPRESERVE', '/gDefensive.png', 'Goldstein Preserve fund logo'),
]:
    old = f'<div class="fundTag"><span class="fundTicker mono">{ticker}</span>'
    if ticker == 'gPRESERVE':
        old = '<div class="fundTag"><span class="fundTicker mono">gPRESERVE</span>'
    new = f'<div class="fundTag"><span class="seatFundIdentity"><span class="fundLogoMini"><img src="{img}" alt="{label}"></span><span class="fundTicker mono">{ticker}</span></span>'
    s = replace_once(s, old, new, f'my-seat {ticker} identity')
s = append_css(s, r'''

/* House-fund logos in Seat dashboard v1 */
.seatFundIdentity{display:flex;align-items:center;gap:10px;min-width:0}
.fundLogoMini{position:relative;width:48px;height:48px;flex:0 0 48px;overflow:hidden;border:1px solid #44391d;border-radius:11px;background:#020202;box-shadow:0 8px 24px rgba(0,0,0,.24)}
.fundLogoMini img{position:absolute;left:50%;top:50%;width:132%;height:132%;max-width:none;transform:translate(-50%,-50%);object-fit:cover;object-position:center}
@media(max-width:500px){.fundLogoMini{width:42px;height:42px;flex-basis:42px}.fundTicker{font-size:16px}}
''', '/* House-fund logos in Seat dashboard v1 */')
p.write_text(s)


# ------------------------------------------------------------------
# Public landing (both routes): logo is the product identity; manager NFT
# remains separately visible underneath for the agent/operator identity.
# ------------------------------------------------------------------
for name in ['index.html', 'landing.html']:
    p = ROOT / name
    s = p.read_text()
    replacements = [
        (
            '<div class="productHead"><span class="productTicker mono">gAIX</span><span class="productState mono">Launch fund</span></div>',
            '<div class="productHead"><span class="productIdentity"><span class="productFundLogo"><img src="/gAIX.png" alt="gAIX fund logo"></span><span class="productTicker mono">gAIX</span></span><span class="productState mono">Launch fund</span></div>',
            'landing gAIX',
        ),
        (
            '<div class="productHead"><span class="productTicker mono">gMEMESTONK</span><span class="productState mono">Launch fund</span></div>',
            '<div class="productHead"><span class="productIdentity"><span class="productFundLogo"><img src="/gMEMESTOCK.png" alt="gMEMESTONK fund logo"></span><span class="productTicker mono">gMEMESTONK</span></span><span class="productState mono">Launch fund</span></div>',
            'landing meme',
        ),
        (
            '<div class="productHead"><span class="productTicker mono" style="color:#d0b967">gPRESERVE</span><span class="productState mono">Coming soon</span></div>',
            '<div class="productHead"><span class="productIdentity"><span class="productFundLogo"><img src="/gDefensive.png" alt="Goldstein Preserve fund logo"></span><span class="productTicker mono" style="color:#d0b967">gPRESERVE</span></span><span class="productState mono">Coming soon</span></div>',
            'landing defensive',
        ),
    ]
    for old, new, label in replacements:
        s = replace_once(s, old, new, f'{name} {label}')
    s = append_css(s, r'''

/* House-fund product logos v1 */
.productIdentity{display:flex;align-items:center;gap:12px;min-width:0}
.productFundLogo{position:relative;width:54px;height:54px;flex:0 0 54px;overflow:hidden;border:1px solid #44391d;border-radius:12px;background:#020202;box-shadow:0 10px 28px rgba(0,0,0,.25)}
.productFundLogo img{position:absolute;left:50%;top:50%;width:132%;height:132%;max-width:none;transform:translate(-50%,-50%);object-fit:cover;object-position:center}
@media(max-width:760px){.productFundLogo{width:48px;height:48px;flex-basis:48px}.productHead{align-items:center}}
''', '/* House-fund product logos v1 */')
    p.write_text(s)

print('Applied house-fund logos across overview, detail, Seat dashboard and public product cards.')
