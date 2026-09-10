const fs = require('fs');

const pages = ['app.html', 'my-seat.html', 'funds.html', 'fund-detail.html'];

const items = `
  <span class="marketGroupLabel mono"><i></i>Crypto <small>spot</small></span>
  <span class="marketItem"><b>BTC</b><span class="marketPrice">$78,136</span><span class="marketChange up">▲ 0.4%</span><small>24H</small></span>
  <span class="marketItem"><b>ETH</b><span class="marketPrice">$2,468</span><span class="marketChange up">▲ 0.9%</span><small>24H</small></span>
  <span class="marketGroupLabel mono"><i></i>Equities <small>Sep 10 close</small></span>
  <span class="marketItem"><b>NVDA</b><span class="marketPrice">$218.36</span><span class="marketChange down">▼ 2.26%</span><small>1D</small></span>
  <span class="marketItem"><b>TSLA</b><span class="marketPrice">$363.56</span><span class="marketChange down">▼ 1.16%</span><small>1D</small></span>
  <span class="marketItem"><b>GOOGL</b><span class="marketPrice">$332.60</span><span class="marketChange up">▲ 0.59%</span><small>1D</small></span>
  <span class="marketItem"><b>AAPL</b><span class="marketPrice">$326.57</span><span class="marketChange up">▲ 3.56%</span><small>1D</small></span>
  <span class="marketItem"><b>MSFT</b><span class="marketPrice">$492.44</span><span class="marketChange up">▲ 0.16%</span><small>1D</small></span>
  <span class="marketItem"><b>AMZN</b><span class="marketPrice">$251.89</span><span class="marketChange down">▼ 0.20%</span><small>1D</small></span>
  <span class="marketGroupLabel goldstein mono"><i></i>Goldstein <small>mock</small></span>
  <a class="marketItem house" href="/app/funds/gaix" target="_top"><b>gAIX</b><span class="marketPrice">NAV $109.34</span><span class="marketChange up">▲ 13.4%</span><small>90D</small></a>
  <a class="marketItem house" href="/app/funds/gmemestonk" target="_top"><b>gMEMESTONK</b><span class="marketPrice">NAV $43.73</span><span class="marketChange up">▲ 27.9%</span><small>90D</small></a>
`;

const tape = `<div class="marketTape" role="region" aria-label="Market snapshot. Crypto spot prices, September 10 equity close, and mock Goldstein fund data.">
  <div class="marketViewport">
    <div class="marketTrack">
      <div class="marketGroup">${items}</div>
      <div class="marketGroup" aria-hidden="true">${items}</div>
    </div>
  </div>
</div>`;

const css = `
/* Goldstein market tape v1 */
.marketTape{
  position:fixed;z-index:80;left:var(--side);right:0;top:0;height:36px;overflow:hidden;
  border-bottom:1px solid #30291a;background:linear-gradient(180deg,#0b0a07,#080806);
  box-shadow:0 8px 24px rgba(0,0,0,.16);transition:left .22s cubic-bezier(.2,.75,.25,1)
}
.marketTape:before,.marketTape:after{content:"";position:absolute;z-index:3;top:0;bottom:0;width:34px;pointer-events:none}
.marketTape:before{left:0;background:linear-gradient(90deg,#080806,rgba(8,8,6,0))}
.marketTape:after{right:0;background:linear-gradient(270deg,#080806,rgba(8,8,6,0))}
.marketViewport{height:100%;overflow:hidden}
.marketTrack{display:flex;width:max-content;height:100%;transform:translateX(-50%);animation:goldsteinMarketRight 64s linear infinite;will-change:transform}
.marketGroup{display:flex;align-items:center;height:100%;flex:0 0 auto}
.marketGroupLabel{height:100%;display:flex;align-items:center;gap:7px;padding:0 15px;color:#8f8057;font-size:12px;font-weight:850;letter-spacing:.12em;text-transform:uppercase;border-right:1px solid #2b2618;white-space:nowrap}
.marketGroupLabel i{width:5px;height:5px;border-radius:50%;background:#b9972f;box-shadow:0 0 10px rgba(216,180,63,.28)}
.marketGroupLabel small{color:#5f594d;font:800 12px/1 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.04em;text-transform:uppercase}
.marketGroupLabel.goldstein{color:#d2b84c;background:linear-gradient(90deg,rgba(216,180,63,.035),transparent)}
.marketItem{height:100%;display:flex;align-items:center;gap:8px;padding:0 15px;border-right:1px solid #242016;color:#bdb49f;text-decoration:none;white-space:nowrap;font:800 12px/1 ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace;letter-spacing:.02em;transition:background .15s,color .15s}
.marketItem b{color:#e9e1cf;font-weight:900;letter-spacing:.045em}
.marketPrice{color:#bdb39d;font-variant-numeric:tabular-nums}
.marketChange{font-weight:900;font-variant-numeric:tabular-nums}.marketChange.up{color:#82d89d}.marketChange.down{color:#d88a87}
.marketItem small{color:#665f51;font-size:12px;font-weight:850;letter-spacing:.06em}
.marketItem.house{background:rgba(216,180,63,.025)}.marketItem.house b{color:#edca52}.marketItem.house:hover,.marketItem.house:focus-visible{background:rgba(216,180,63,.075);color:#f3e7c1;outline:none}
.marketTape:hover .marketTrack,.marketTape:focus-within .marketTrack{animation-play-state:paused}
@keyframes goldsteinMarketRight{from{transform:translateX(-50%)}to{transform:translateX(0)}}
main{padding-top:36px}
@media(max-width:760px){
  .marketTape{position:relative;left:0;right:auto;top:auto;width:100%;height:38px;box-shadow:none;transition:none}
  .marketTape:before,.marketTape:after{width:20px}
  .marketTrack{animation-duration:54s}
  .marketGroupLabel,.marketItem{padding-left:12px;padding-right:12px}
  main{padding-top:0}
}
@media(prefers-reduced-motion:reduce){
  .marketViewport{overflow-x:auto;scrollbar-width:none}.marketViewport::-webkit-scrollbar{display:none}
  .marketTrack{transform:none;animation:none}.marketGroup[aria-hidden="true"]{display:none}
}
`;

for (const file of pages) {
  let s = fs.readFileSync(file, 'utf8');
  if (s.includes('Goldstein market tape v1')) {
    console.log(`${file}: already patched`);
    continue;
  }

  const proto = /<div class="prototype mono">[\s\S]*?<\/div>/;
  if (!proto.test(s)) throw new Error(`${file}: prototype bar not found`);
  s = s.replace(proto, tape);

  s = s.replace(/<div class="sideMeta mono">[\s\S]*?<\/div>/, '<div class="sideMeta mono">Prototype · simulated data</div>');
  s = s.replace('</style>', `${css}\n</style>`);

  fs.writeFileSync(file, s);
  console.log(`${file}: patched`);
}

// Basic QA so a broken ticker never gets committed.
for (const file of pages) {
  const s = fs.readFileSync(file, 'utf8');
  for (const required of ['marketTape','goldsteinMarketRight','BTC','$218.36','gAIX','NAV $109.34','gMEMESTONK','NAV $43.73']) {
    if (!s.includes(required)) throw new Error(`${file}: missing ${required}`);
  }
  if (s.includes('<div class="prototype mono">')) throw new Error(`${file}: legacy prototype bar remains`);
}
