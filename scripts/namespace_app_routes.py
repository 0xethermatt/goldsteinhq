from pathlib import Path
import json

files = ['index.html','my-seat.html','funds.html','fund-detail.html']
for filename in files:
    p=Path(filename)
    s=p.read_text()
    replacements=[
        ('href="/" target="_top"','href="/app" target="_top"'),
        ('href="/my-seat" target="_top"','href="/app/my-seat" target="_top"'),
        ('href="/funds" target="_top"','href="/app/funds" target="_top"'),
        ('href="/funds/gaix"','href="/app/funds/gaix"'),
        ('href="/funds/gmemestonk"','href="/app/funds/gmemestonk"'),
        ('location.href=\'/funds/gaix\'','location.href=\'/app/funds/gaix\''),
        ('location.href=\'/funds/gmemestonk\'','location.href=\'/app/funds/gmemestonk\''),
        ('?\'/funds/gaix\':\'/funds/gmemestonk\'','?\'/app/funds/gaix\':\'/app/funds/gmemestonk\''),
        ('href="/funds">← G-Funds','href="/app/funds">← G-Funds'),
        ('.nav a[href="/"]', '.nav a[href="/app"]'),
        ('.nav a[href="/my-seat"]', '.nav a[href="/app/my-seat"]'),
        ('.nav a[href="/funds"]', '.nav a[href="/app/funds"]'),
    ]
    for a,b in replacements:
        s=s.replace(a,b)
    p.write_text(s)

p=Path('welcome.html')
s=p.read_text().replace("window.location.href='/my-seat'","window.location.href='/app/my-seat'")
p.write_text(s)

config={
  'rewrites':[
    {'source':'/','destination':'/landing.html'},
    {'source':'/app','destination':'/welcome.html'},
    {'source':'/app/my-seat','destination':'/my-seat.html'},
    {'source':'/app/funds','destination':'/funds.html'},
    {'source':'/app/funds/gaix','destination':'/fund-detail.html'},
    {'source':'/app/funds/gmemestonk','destination':'/fund-detail.html'},
    {'source':'/my-seat','destination':'/my-seat.html'},
    {'source':'/funds','destination':'/funds.html'},
    {'source':'/funds/gaix','destination':'/fund-detail.html'},
    {'source':'/funds/gmemestonk','destination':'/fund-detail.html'}
  ]
}
Path('vercel.json').write_text(json.dumps(config,separators=(',',':'))+'\n')
