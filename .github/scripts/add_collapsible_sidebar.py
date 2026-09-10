from pathlib import Path

PAGES = ["app.html", "my-seat.html", "funds.html", "fund-detail.html"]

EARLY = r'''<script>
/* Restore the desktop sidebar preference before first paint. */
try {
  if (localStorage.getItem('goldsteinSidebarCollapsed') === '1' && window.matchMedia('(min-width:761px)').matches) {
    document.documentElement.classList.add('sidebarCollapsed');
  }
} catch (e) {}
</script>
'''

CSS = r'''
/* Collapsible Goldstein HQ sidebar */
:root{--sidebar-width:216px}
@media(min-width:761px) and (max-width:1050px){:root{--sidebar-width:88px}}
@media(min-width:761px){
  .sidebar{width:var(--sidebar-width)!important;transition:transform .22s cubic-bezier(.2,.75,.25,1),box-shadow .22s ease;will-change:transform}
  main{transition:margin-left .22s cubic-bezier(.2,.75,.25,1)}
  .prototype{transition:left .22s cubic-bezier(.2,.75,.25,1)}
  .sidebarToggle{position:fixed;z-index:101;top:83px;left:calc(var(--sidebar-width) - 19px);width:38px;height:38px;padding:0;display:grid;place-items:center;border:1px solid #4c4022;border-radius:10px;background:linear-gradient(180deg,#17150e,#0d0d09);color:#cfc4a7;box-shadow:0 10px 26px rgba(0,0,0,.28);transition:left .22s cubic-bezier(.2,.75,.25,1),background .16s,border-color .16s,transform .16s;color-scheme:dark}
  .sidebarToggle:hover{background:#1c180d;border-color:#745e20;color:#f0cf58;transform:translateY(-1px)}
  .sidebarToggle:focus-visible{outline:2px solid #e8c43f;outline-offset:3px}
  .sidebarToggle svg{width:18px;height:18px;transition:transform .22s cubic-bezier(.2,.75,.25,1)}
  html.sidebarCollapsed{--side:0px}
  html.sidebarCollapsed .sidebar{transform:translateX(calc(-1 * var(--sidebar-width)));box-shadow:none}
  html.sidebarCollapsed .sidebarToggle{left:12px}
  html.sidebarCollapsed .sidebarToggle svg{transform:rotate(180deg)}
}
@media(max-width:760px){.sidebarToggle{display:none!important}}
@media(prefers-reduced-motion:reduce){.sidebar,.sidebarToggle,.sidebarToggle svg,main,.prototype{transition:none!important}}
'''

BUTTON = r'''<button class="sidebarToggle" id="sidebarToggle" type="button" aria-controls="appSidebar" aria-expanded="true" aria-label="Hide sidebar" title="Hide sidebar">
  <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M14.5 5.5 8 12l6.5 6.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
</button>'''

JS = r'''<script>
/* Persisted desktop sidebar controller. Mobile keeps the existing menu behavior. */
(()=>{
  const root=document.documentElement,btn=document.getElementById('sidebarToggle');
  if(!btn)return;
  const mq=window.matchMedia('(min-width:761px)');
  const stored=()=>{try{return localStorage.getItem('goldsteinSidebarCollapsed')==='1'}catch(e){return false}};
  const save=v=>{try{localStorage.setItem('goldsteinSidebarCollapsed',v?'1':'0')}catch(e){}};
  const sync=()=>{
    const collapsed=mq.matches&&root.classList.contains('sidebarCollapsed');
    const label=collapsed?'Show sidebar':'Hide sidebar';
    btn.setAttribute('aria-expanded',String(!collapsed));
    btn.setAttribute('aria-label',label);
    btn.title=label;
  };
  btn.addEventListener('click',()=>{
    if(!mq.matches)return;
    const collapsed=root.classList.toggle('sidebarCollapsed');
    save(collapsed);sync();
  });
  const onBreakpoint=()=>{
    if(!mq.matches)root.classList.remove('sidebarCollapsed');
    else root.classList.toggle('sidebarCollapsed',stored());
    sync();
  };
  if(mq.addEventListener)mq.addEventListener('change',onBreakpoint);else mq.addListener(onBreakpoint);
  onBreakpoint();
})();
</script>
'''

for name in PAGES:
    p=Path(name)
    s=p.read_text()

    # Idempotent: update/insert each layer once.
    if "goldsteinSidebarCollapsed') === '1'" not in s:
        marker='<style>'
        if marker not in s: raise SystemExit(f'{name}: missing style marker')
        s=s.replace(marker, EARLY+marker, 1)

    if '/* Collapsible Goldstein HQ sidebar */' not in s:
        if '</style>' not in s: raise SystemExit(f'{name}: missing style close')
        s=s.replace('</style>', CSS+'\n</style>', 1)

    if 'id="appSidebar"' not in s:
        old='<aside class="sidebar">'
        if old not in s: raise SystemExit(f'{name}: sidebar markup not found')
        s=s.replace(old,'<aside class="sidebar" id="appSidebar">',1)

    if 'id="sidebarToggle"' not in s:
        close='</aside>'
        if close not in s: raise SystemExit(f'{name}: sidebar close not found')
        s=s.replace(close,close+'\n'+BUTTON,1)

    if '/* Persisted desktop sidebar controller.' not in s:
        if '</body>' not in s: raise SystemExit(f'{name}: missing body close')
        s=s.replace('</body>',JS+'\n</body>',1)

    p.write_text(s)
    print('patched', name)
