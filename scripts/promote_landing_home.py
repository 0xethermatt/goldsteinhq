from pathlib import Path
import json

# One-time architecture migration: public site at /, product app under /app.
# Preserve the existing Mint experience as the app entry document.
current_app = Path('index.html').read_text()
if 'Free Seat Reveal' in current_app and 'id="drawBtn"' in current_app:
    Path('app.html').write_text(current_app)
elif not Path('app.html').exists():
    raise SystemExit('Could not identify current Mint page to preserve as app.html')

landing = Path('landing.html').read_text()
if 'The investment firm' not in landing or 'href="/app"' not in landing:
    raise SystemExit('Landing page validation failed')
Path('index.html').write_text(landing)

welcome = Path('welcome.html').read_text().replace('src="/index.html" title="Goldstein mint"','src="/app.html" title="Goldstein mint"')
Path('welcome.html').write_text(welcome)

config={
  'rewrites':[
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
