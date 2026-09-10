from pathlib import Path

for filename in ['index.html','landing.html']:
    p=Path(filename)
    s=p.read_text()

    if '<meta name="color-scheme"' not in s:
        s=s.replace('<meta name="theme-color" content="#080806" />', '<meta name="theme-color" content="#080806" />\n<meta name="color-scheme" content="dark" />', 1)

    if '<meta property="og:site_name"' not in s:
        s=s.replace('<meta property="og:type" content="website" />', '<meta property="og:type" content="website" />\n<meta property="og:site_name" content="Goldstein Group" />', 1)

    if '<meta name="twitter:card"' not in s:
        s=s.replace('<meta property="og:image" content="/assets/goldstein-hero.webp" />', '<meta property="og:image" content="/assets/goldstein-hero.webp" />\n<meta name="twitter:card" content="summary_large_image" />\n<meta name="twitter:title" content="Goldstein Group — The Investment Firm, Rebuilt Onchain" />\n<meta name="twitter:description" content="Agent-managed tokenized funds. Onchain distribution. One firm built for internet capital markets." />\n<meta name="twitter:image" content="/assets/goldstein-hero.webp" />', 1)

    if '.skipLink{' not in s:
        s=s.replace('</style>', '''\n/* Public-site accessibility and interaction polish */
.skipLink{position:fixed;z-index:1000;left:16px;top:12px;transform:translateY(-80px);padding:10px 13px;border:1px solid #e8c43f;border-radius:8px;background:#0e0d09;color:#f1d15a;text-decoration:none;font-size:12px;font-weight:850;transition:.16s}.skipLink:focus{transform:none}a:focus-visible,button:focus-visible{outline:2px solid #f0ca45;outline-offset:3px}.launch:focus-visible,.primaryCta:focus-visible{outline-color:#fff}.mobileMenu[aria-hidden="true"]{display:none}@media(max-width:760px){.mobileMenu[aria-hidden="false"]{display:grid}}\n</style>''', 1)

    if '<a class="skipLink"' not in s:
        s=s.replace('<body>', '<body>\n<a class="skipLink" href="#main">Skip to content</a>', 1)

    s=s.replace('<button class="menuBtn" id="menuBtn" aria-label="Open menu">☰</button>', '<button class="menuBtn" id="menuBtn" aria-label="Open menu" aria-controls="mobileMenu" aria-expanded="false">☰</button>')
    s=s.replace('<nav class="mobileMenu" id="mobileMenu" aria-label="Mobile navigation">', '<nav class="mobileMenu" id="mobileMenu" aria-label="Mobile navigation" aria-hidden="true">')
    s=s.replace('<main>', '<main id="main">', 1)

    old="menuBtn.addEventListener('click',()=>menu.classList.toggle('show'));menu.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>menu.classList.remove('show')));"
    new="const setMenu=open=>{menu.classList.toggle('show',open);menu.setAttribute('aria-hidden',String(!open));menuBtn.setAttribute('aria-expanded',String(open));menuBtn.setAttribute('aria-label',open?'Close menu':'Open menu')};menuBtn.addEventListener('click',()=>setMenu(!menu.classList.contains('show')));menu.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>setMenu(false)));document.addEventListener('keydown',e=>{if(e.key==='Escape')setMenu(false)});"
    s=s.replace(old,new)

    p.write_text(s)
