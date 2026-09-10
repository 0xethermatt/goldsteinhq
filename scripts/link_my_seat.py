from pathlib import Path

p = Path('welcome.html')
html = p.read_text()
old = "$('enterBtn').onclick=()=>{const doc=frame.contentDocument;closeModal();doc?.getElementById('firm')?.scrollIntoView({behavior:'smooth',block:'start'})};"
new = "$('enterBtn').onclick=()=>{closeModal();window.location.href='/my-seat'};"
if old not in html:
    if new in html:
        print('My Seat handoff already applied')
    else:
        raise SystemExit('welcome handoff marker not found')
else:
    html = html.replace(old, new, 1)
    p.write_text(html)
    print('Welcome handoff now routes to /my-seat')
