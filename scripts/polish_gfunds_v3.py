from pathlib import Path
import re

ROOT = Path('.')

def require(text, needle, label):
    if needle not in text:
        raise SystemExit(f'Missing anchor: {label}')

# ---------- G-Funds overview typography / balance ----------
p = ROOT / 'funds.html'
s = p.read_text()
css = r'''

/* G-Funds visual balance v3 */
.shell{width:min(1240px,calc(100% - 64px));padding-top:36px}
.pageTop{margin-bottom:22px}.eyebrow{font-size:12px}.pageTop h1{font-size:54px}.pageTop p{font-size:16px;color:#a49b86}.wallet{height:48px;padding:0 16px;font-size:13px}
.marketLine{gap:10px;margin-bottom:30px}.marketPill{padding:8px 12px;font-size:11px}
.positionBox{padding:21px 22px}.positionHead b{font-size:15px}.positionHead span{font-size:10px}.empty{font-size:14px}
.lpPanelHead{padding:20px 22px}.lpPanelHead b{font-size:15px}.lpPanelHead span{font-size:10px}.lpRow{padding:16px 22px}.lpLabels{font-size:9px}.lpRow>strong,.lpPool strong{font-size:13px}.lpPool small{font-size:9px}
.sectionHead{margin-bottom:17px}.sectionHead h2{font-size:40px}.sectionTag{font-size:11px}
.fundsGrid{gap:16px}.fundMain{padding:26px}.fundHead{gap:16px}.managerPfp{width:58px;height:58px;border-radius:14px}.manager{gap:14px}.ticker{font-size:22px}.managerMeta small{font-size:10px}.detailsLink{font-size:12px}.fundCard h3{margin-top:24px;font-size:34px}.fundDesc{font-size:14px;line-height:1.55}.riskLine{margin-top:18px;font-size:10px}.riskDots i{width:23px;height:5px}.metrics{margin:21px 26px 0}.metric{padding:16px 14px}.metric small{font-size:9px}.metric strong{font-size:15px}.holdings{margin:19px 26px 0}.holdingsLabel{font-size:9px}.holding{padding:7px 9px;font-size:10px}.actions{padding:23px 26px 26px;gap:9px}.action{height:48px;font-size:12px}.coming{padding:22px 24px}.coming h3{font-size:23px}.coming p{font-size:13px}
@media(max-width:1050px){.shell{width:min(1020px,calc(100% - 40px))}}
@media(max-width:760px){.shell{width:calc(100% - 24px);padding-top:26px}.pageTop h1{font-size:43px}.pageTop p{font-size:14px}.sectionHead h2{font-size:34px}.fundMain{padding:21px}.managerPfp{width:52px;height:52px}.ticker{font-size:20px}.fundCard h3{font-size:30px}.fundDesc{font-size:13px}.metrics,.holdings{margin-left:21px;margin-right:21px}.actions{padding:20px 21px 22px}}
'''
if '/* G-Funds visual balance v3 */' not in s:
    s = s.replace('</style>', css + '\n</style>', 1)
# concise top-line copy
s = s.replace('<h1>G-Funds</h1><p>Seat-holder markets.</p>', '<h1>G-Funds</h1><p>Goldstein fund markets.</p>')
p.write_text(s)

# ---------- G-Fund detail rebuild ----------
p = ROOT / 'fund-detail.html'
s = p.read_text()

main_old = '<section class="mainGrid"><article class="card chartCard"><div class="cardTitle"><h2>Performance</h2><span class="mono">Launch onward</span></div><div class="chart"><svg viewBox="0 0 800 260" preserveAspectRatio="none" aria-hidden="true"><path d="M0 190 C120 170 170 182 250 160 S390 158 460 132 S610 120 800 88" fill="none" stroke="rgba(216,180,63,.48)" stroke-width="3" stroke-dasharray="6 7"/></svg><div class="chartEmpty mono">Preview · live history at launch</div></div></article><aside class="card managerCard"><div class="managerRow"><div class="pfp"></div><div><div class="eyebrow mono">Fund manager</div><strong>Goldstein House Manager</strong></div></div><h3 id="managerMandate">AI Index mandate</h3><p>NFT manager identity will populate here.</p><div class="risk mono"><span>Risk</span><div class="dots" id="riskDots"></div><span id="riskLabel">Growth</span></div></aside></section>'
main_new = '''<section class="mainGrid">
<article class="card chartCard"><div class="cardTitle"><h2>Performance</h2><span class="mono">Live after launch</span></div><div class="chart"><svg viewBox="0 0 800 260" preserveAspectRatio="none" aria-hidden="true"><path d="M0 190 C120 170 170 182 250 160 S390 158 460 132 S610 120 800 88" fill="none" stroke="rgba(216,180,63,.48)" stroke-width="3" stroke-dasharray="6 7"/></svg><div class="chartEmpty mono">Preview · performance history begins at launch</div></div></article>
<aside class="card managerCard">
  <div class="managerRow"><div class="pfp"><img id="managerImageCard" src="/b10.png" alt="Goldstein house manager NFT"></div><div><div class="eyebrow mono">Fund manager</div><strong id="managerName">Seat B10 · House Manager</strong></div></div>
  <div class="managerFacts">
    <div class="managerFact"><small class="mono">Index objective</small><p id="indexObjective">Concentrated AI infrastructure and frontier-technology exposure.</p></div>
    <div class="managerFact"><small class="mono">Agent role</small><p id="agentRole">Monitors weights, rebalances drift and enforces the fund risk policy.</p></div>
  </div>
  <div class="risk mono"><span>Risk</span><div class="dots" id="riskDots"></div><span id="riskLabel">Growth</span></div>
</aside>
</section>'''
require(s, main_old, 'detail mainGrid')
s = s.replace(main_old, main_new, 1)

bottom_old = '<section class="bottomGrid"><article class="card infoCard"><h2 id="basketTitle">Constituents</h2><div class="chips" id="chips"></div></article><article class="card infoCard"><h2>Your holdings</h2><div class="positionRow"><div class="positionItem"><small class="mono">Fund balance</small><strong>—</strong></div><div class="positionItem"><small class="mono">Value</small><strong>—</strong></div></div><div class="empty">Connect wallet to load holdings.</div></article></section>'
bottom_new = '''<section class="bottomGrid">
<article class="card infoCard compositionCard">
  <div class="cardTitle compositionTitle"><div><h2 id="basketTitle">Index composition</h2><span class="mono" id="compositionNote">Illustrative equal-weight view</span></div><span class="mono">5 assets</span></div>
  <div class="compositionLayout"><div class="donutWrap"><div class="donut" id="donut"><div class="donutCore"><strong>5</strong><span class="mono">assets</span></div></div></div><div class="legend" id="legend"></div></div>
  <div class="indexBrief"><small class="mono">What this index does</small><p id="indexBrief">Bundles the approved basket into one tokenized fund position.</p></div>
</article>
<article class="card infoCard holdingsCard"><h2>Your holdings</h2><div class="positionRow"><div class="positionItem"><small class="mono">Fund balance</small><strong>—</strong></div><div class="positionItem"><small class="mono">Value</small><strong>—</strong></div></div><div class="empty">Connect wallet to load holdings.</div></article>
</section>'''
require(s, bottom_old, 'detail bottomGrid')
s = s.replace(bottom_old, bottom_new, 1)

css2 = r'''

/* Fund detail information design v3 */
.shell{width:min(1240px,calc(100% - 64px));padding-top:34px}.back{font-size:13px}.top h1{font-size:49px}.ticker{font-size:15px}.eyebrow{font-size:11px}.btn{height:46px;font-size:12px}.summary{gap:11px;margin-bottom:30px}.stat{padding:18px 20px}.stat small{font-size:9px}.stat strong{font-size:17px}.mainGrid{grid-template-columns:minmax(0,1.55fr) minmax(330px,.55fr);gap:14px}.chartCard,.managerCard{padding:25px}.cardTitle h2{font-size:31px}.cardTitle span{font-size:9px}.chart{height:285px}
.managerCard{display:flex;flex-direction:column}.managerRow{gap:14px}.managerRow .pfp{width:68px;height:68px;border-radius:15px}.managerRow strong{font-size:16px;color:#e8dfc8}.managerFacts{display:grid;gap:0;margin-top:20px;border-top:1px solid #292419}.managerFact{padding:16px 0;border-bottom:1px solid #292419}.managerFact small,.indexBrief small{display:block;color:#c4a742;font-size:9px;font-weight:850;letter-spacing:.12em}.managerFact p,.indexBrief p{margin:7px 0 0;color:#c1b69e;font-size:14px;line-height:1.55}.risk{margin-top:auto;padding-top:18px;font-size:10px}.dots i{width:22px;height:5px}
.bottomGrid{grid-template-columns:minmax(0,1.35fr) minmax(320px,.65fr);gap:14px}.infoCard{padding:24px}.infoCard h2{font-size:29px}.compositionTitle{align-items:flex-end;margin-bottom:18px}.compositionTitle>div>span{display:block;margin-top:4px}.compositionLayout{display:grid;grid-template-columns:230px 1fr;gap:26px;align-items:center}.donutWrap{display:grid;place-items:center}.donut{width:210px;aspect-ratio:1;border-radius:50%;position:relative;background:conic-gradient(#e9c94f 0 20%,#a7b766 20% 40%,#5f9673 40% 60%,#877d4e 60% 80%,#b88f3d 80% 100%);box-shadow:inset 0 0 0 1px rgba(255,255,255,.04),0 18px 50px rgba(0,0,0,.24)}.donut:after{content:"";position:absolute;inset:36px;border-radius:50%;background:#0c0c08;border:1px solid #2f291a}.donutCore{position:absolute;z-index:2;inset:0;display:grid;place-content:center;text-align:center}.donutCore strong{font:500 34px/1 Georgia,serif;color:#eee5cf}.donutCore span{margin-top:5px;color:#756e5f;font-size:8px}.legend{display:grid;gap:8px}.legendItem{display:grid;grid-template-columns:10px minmax(0,1fr) auto;gap:9px;align-items:center;padding:9px 10px;border:1px solid #2b2719;border-radius:9px;background:#0b0b08}.legendDot{width:9px;height:9px;border-radius:50%;background:var(--swatch)}.legendItem b{font-size:12px;color:#d9cfb8}.legendItem span{font-size:10px;color:#8d846f}.indexBrief{margin-top:18px;padding-top:16px;border-top:1px solid #292419}.holdingsCard{align-self:stretch}.positionItem{padding:15px}.positionItem small{font-size:9px}.positionItem strong{font-size:15px}.empty{font-size:12px}
.top .pfp{width:70px;height:70px}.pfp img{display:block;width:100%;height:100%;object-fit:cover;object-position:center}
@media(max-width:1050px){.shell{width:min(1020px,calc(100% - 40px))}.mainGrid,.bottomGrid{grid-template-columns:1fr}.compositionLayout{grid-template-columns:210px 1fr}}
@media(max-width:760px){.shell{width:calc(100% - 24px);padding-top:24px}.top h1{font-size:40px}.top .pfp{width:60px;height:60px}.chartCard,.managerCard,.infoCard{padding:20px}.cardTitle h2,.infoCard h2{font-size:27px}.chart{height:235px}.compositionLayout{grid-template-columns:1fr}.donut{width:190px}.legend{width:100%}.managerFact p,.indexBrief p{font-size:13px}}
'''
if '/* Fund detail information design v3 */' not in s:
    s = s.replace('</style>', css2 + '\n</style>', 1)

# Replace the compact one-line data/controller with richer product data.
script_re = re.compile(r"\(\(\)=>\{const \$=id=>document\.getElementById\(id\);const meme=location\.pathname\.includes\('gmemestonk'\);const data=meme\?.*?\}\)\(\);", re.S)
new_script = r'''(()=>{
const $=id=>document.getElementById(id);
const meme=location.pathname.includes('gmemestonk');
const data=meme?{
  name:'Meme Index',ticker:'gMEMESTONK',manager:'Seat B17 · House Manager',managerImg:'/b17.png',risk:5,label:'High',
  objective:'High-beta basket of internet-native and meme-market exposure.',
  agent:'Rebalances the approved basket as signals and liquidity change, within the fund risk limits.',
  brief:'Packages five internet-native assets into one actively supervised onchain index.',
  chips:['AI','BONER','MOO','OPTIMUS','MEME'],
  colors:['#e58a4a','#d06842','#aa4f3e','#8e633c','#d9a149']
}:{
  name:'Goldstein AI Index',ticker:'gAIX',manager:'Seat B10 · House Manager',managerImg:'/b10.png',risk:3,label:'Growth',
  objective:'Concentrated AI infrastructure and frontier-technology exposure.',
  agent:'Monitors basket weights, rebalances drift and enforces the fund risk policy.',
  brief:'Bundles the approved AI-infrastructure basket into one tokenized fund position.',
  chips:['NVDA','TSLA','MU','GOOGL','SPCX'],
  colors:['#e9c94f','#a7b766','#5f9673','#877d4e','#b88f3d']
};
if(meme)$('top').classList.add('volatile');
$('managerImage').src=data.managerImg;$('managerImage').alt=data.manager+', manager of $'+data.ticker;
$('managerImageCard').src=data.managerImg;$('managerImageCard').alt=data.manager+', manager of $'+data.ticker;
$('managerName').textContent=data.manager;
document.title='Goldstein HQ — '+data.name;
$('name').textContent=data.name;$('ticker').textContent='$'+data.ticker;$('modalTicker').textContent='$'+data.ticker;$('pair').textContent='$'+data.ticker+' / GLD';$('lpPair').textContent='$'+data.ticker+' / GLD';
$('indexObjective').textContent=data.objective;$('agentRole').textContent=data.agent;$('indexBrief').textContent=data.brief;$('riskLabel').textContent=data.label;
$('basketTitle').textContent='Index composition';
$('riskDots').innerHTML=[1,2,3,4,5].map(x=>`<i class="${x<=data.risk?'on':''}"></i>`).join('');
$('legend').innerHTML=data.chips.map((x,i)=>`<div class="legendItem"><i class="legendDot" style="--swatch:${data.colors[i]}"></i><b class="mono">${x}</b><span class="mono">20%*</span></div>`).join('');
$('donut').style.background=`conic-gradient(${data.colors.map((c,i)=>`${c} ${i*20}% ${(i+1)*20}%`).join(',')})`;
$('compositionNote').textContent='Illustrative equal-weight view · final weights follow manager policy';
const toast=t=>{$('toast').textContent=t;$('toast').classList.add('show');clearTimeout(window.__t);window.__t=setTimeout(()=>$('toast').classList.remove('show'),1600)};
$('mobileMenu').onclick=()=>$('mobileNav').classList.toggle('show');document.querySelectorAll('#mobileNav a').forEach(a=>a.onclick=()=>$('mobileNav').classList.remove('show'));
document.querySelectorAll('[data-action]').forEach(b=>b.onclick=()=>{$('actionLabel').textContent=b.dataset.action;$('amount').value='';$('modal').classList.add('show')});
$('close').onclick=()=>$('modal').classList.remove('show');$('modal').onclick=e=>{if(e.target===$('modal'))$('modal').classList.remove('show')};
$('preview').onclick=()=>{const v=Number($('amount').value);if(!Number.isFinite(v)||v<=0)return toast('Enter an amount.');$('modal').classList.remove('show');toast('Preview only · simulated.')};
})();'''
if not script_re.search(s):
    raise SystemExit('Could not find fund-detail controller')
s = script_re.sub(new_script, s, count=1)

# small disclosure under the composition visualization; concise and explicit
s = s.replace('</article>\n<article class="card infoCard holdingsCard">', '<div class="compositionFoot mono">* Prototype visualization, not final live weights.</div></article>\n<article class="card infoCard holdingsCard">', 1)
s = s.replace('.indexBrief{margin-top:18px;padding-top:16px;border-top:1px solid #292419}', '.indexBrief{margin-top:18px;padding-top:16px;border-top:1px solid #292419}.compositionFoot{margin-top:11px;color:#655f52;font-size:8px;letter-spacing:.08em;text-transform:uppercase}', 1)
p.write_text(s)

print('polished funds.html and fund-detail.html')
