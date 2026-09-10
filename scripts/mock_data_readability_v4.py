from pathlib import Path
import re

ROOT = Path('.')
HTML_FILES = ['index.html','landing.html','app.html','welcome.html','my-seat.html','funds.html','fund-detail.html']


def require(text, needle, label):
    if needle not in text:
        raise SystemExit(f'Missing anchor: {label}')


def append_css(text, css, marker):
    if marker not in text:
        require(text, '</style>', f'{marker} style close')
        text = text.replace('</style>', css + '\n</style>', 1)
    return text


def append_script(text, script, marker):
    if marker not in text:
        require(text, '</body>', f'{marker} body close')
        text = text.replace('</body>', script + '\n</body>', 1)
    return text


def lift_font_floor(text, floor=11):
    # Raise only CSS font sizes / font shorthand sizes, never layout dimensions.
    def size_repl(m):
        prefix, raw = m.group(1), m.group(2)
        n = float(raw)
        if 0 < n < floor:
            return prefix + f'{floor}px'
        return m.group(0)

    text = re.sub(r'(font-size\s*:\s*)(\d+(?:\.\d+)?)px', size_repl, text)

    def font_prop_repl(m):
        prop = m.group(0)
        def px_repl(pm):
            n = float(pm.group(1))
            return f'{floor}px' if 0 < n < floor else pm.group(0)
        return re.sub(r'(\d+(?:\.\d+)?)px', px_repl, prop, count=1)

    text = re.sub(r'font\s*:[^;{}]+', font_prop_repl, text)
    return text


# -----------------------------------------------------------------------------
# G-Funds overview: visible mock market data + wallet-populated portfolio demo.
# -----------------------------------------------------------------------------
p = ROOT / 'funds.html'
s = p.read_text()
s = s.replace(
    'Prototype only — simulated fund data. No real assets or transactions.',
    'Prototype only — mock market & portfolio data. No real assets or transactions.'
)

overview_css = r'''

/* Mock market data + readable overview v4 */
.metric strong{font-size:16px}.metric small,.holdingsLabel,.managerMeta small,.riskLine{font-size:11px}
.lpLabels{font-size:10px}.lpPool small,.lpPanelHead span{font-size:11px}.lpRow>strong,.lpPool strong{font-size:14px}
.mockHoldingGrid{display:grid;grid-template-columns:1fr 1fr;gap:9px;margin-top:14px;padding-top:14px;border-top:1px solid #2a2619}
.mockHolding{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:10px;align-items:center;padding:12px 13px;border:1px solid #2d291c;border-radius:10px;background:#0b0b08}
.mockHolding b{display:block;color:#ddd4bd;font-size:14px}.mockHolding small{display:block;margin-top:3px;color:#817968;font-size:11px}.mockHolding strong{color:#d7c67d;font-size:13px;white-space:nowrap}
.mockTag{display:inline-flex;align-items:center;padding:5px 7px;border:1px solid #4a4024;border-radius:999px;color:#bba65b;font-size:11px;font-weight:850;letter-spacing:.06em;text-transform:uppercase}
@media(max-width:650px){.mockHoldingGrid{grid-template-columns:1fr}.lpPanelHead{min-width:760px}.lpTable{min-width:760px}}
'''
s = append_css(s, overview_css, '/* Mock market data + readable overview v4 */')

overview_script = r'''
<script>
/* Mock data controller v4 — layout/demo values only. */
(()=>{
  const mock={
    gaix:{tvl:'$6.84M',apr:'18.6%',emissions:'42.0K GLDSTN / day',holding:'114.2 gAIX',value:'$12,486',lp:'$18,750',fees:'$184.26',earned:'3,840 GLDSTN'},
    meme:{tvl:'$2.31M',apr:'32.4%',emissions:'58.5K GLDSTN / day',holding:'86.4 gMEMESTONK',value:'$3,778',lp:'$7,420',fees:'$96.84',earned:'2,960 GLDSTN'}
  };
  const cards=[...document.querySelectorAll('.fundCard')];
  cards.forEach(card=>{
    const d=card.dataset.href.includes('gmemestonk')?mock.meme:mock.gaix;
    const vals=card.querySelectorAll('.metric strong');
    if(vals.length>=3){vals[0].textContent=d.tvl;vals[1].textContent=d.apr;vals[2].textContent=d.emissions;}
  });

  const wallet=document.getElementById('walletBtn');
  const holdings=document.getElementById('fundHoldings');
  const lpTable=document.querySelector('.lpTable');
  const firstLp=document.getElementById('lpPositions');
  if(!wallet||!holdings||!lpTable||!firstLp)return;
  let on=false;
  const lpRow=(ticker,d,extra='')=>`<div class="lpRow ${extra}"><div class="lpPool"><strong>$${ticker} / GLD</strong><small class="mono">Mock connected position</small></div><strong>${d.lp}</strong><strong>${d.apr}</strong><strong>${d.fees}</strong><strong>${d.earned}</strong><div class="lpRowActions"><button class="claimFees">Claim</button><button class="manageLp">Manage</button></div></div>`;
  const disconnected=()=>{
    holdings.textContent='Connect wallet to view holdings.';
    firstLp.innerHTML='<div class="lpPool"><strong>—</strong><small class="mono">Connect wallet</small></div><strong>—</strong><strong>—</strong><strong>—</strong><strong>—</strong><div class="lpRowActions"><button class="claimFees" disabled>Claim</button><button class="manageLp" disabled>Manage</button></div>';
    lpTable.querySelectorAll('.mockLpExtra').forEach(n=>n.remove());
  };
  const connected=()=>{
    holdings.innerHTML=`<span class="mockTag mono">Mock wallet</span><div class="mockHoldingGrid"><div class="mockHolding"><div><b>$gAIX</b><small>${mock.gaix.holding}</small></div><strong>${mock.gaix.value}</strong></div><div class="mockHolding"><div><b>$gMEMESTONK</b><small>${mock.meme.holding}</small></div><strong>${mock.meme.value}</strong></div></div>`;
    firstLp.outerHTML=lpRow('gAIX',mock.gaix,'') .replace('class="lpRow "','class="lpRow"').replace('<div class="lpRow"','<div class="lpRow" id="lpPositions"');
    document.getElementById('lpPositions').insertAdjacentHTML('afterend',lpRow('gMEMESTONK',mock.meme,'mockLpExtra'));
    document.querySelectorAll('.claimFees:not([disabled])').forEach(b=>b.onclick=()=>{b.textContent='Claimed';setTimeout(()=>b.textContent='Claim',1200)});
  };
  wallet.onclick=()=>{
    on=!on;
    wallet.innerHTML=on?'<i></i>0x71…9A3':'<i></i>Connect wallet';
    on?connected():disconnected();
  };
})();
</script>
'''
s = append_script(s, overview_script, '/* Mock data controller v4')
p.write_text(s)


# -----------------------------------------------------------------------------
# Fund detail: realistic mock data, performance, interactive index composition.
# -----------------------------------------------------------------------------
p = ROOT / 'fund-detail.html'
s = p.read_text()
s = s.replace(
    'Prototype only — no live market data or transactions.',
    'Prototype only — mock market & portfolio data. No real assets or transactions.'
)

# Add one useful manager dimension without adding prose elsewhere.
agent_anchor = '<div class="managerFact"><small class="mono">Agent role</small><p id="agentRole">Monitors weights, rebalances drift and enforces the fund risk policy.</p></div>'
if 'id="managerStyle"' not in s:
    require(s, agent_anchor, 'manager agent fact')
    s = s.replace(agent_anchor, agent_anchor + '\n    <div class="managerFact"><small class="mono">Manager style</small><p id="managerStyle">Systematic · risk-aware · rules-based.</p></div>', 1)

s = re.sub(
    r'<div class="donut" id="donut"><div class="donutCore"><strong>5</strong><span class="mono">assets</span></div></div>',
    '<div class="donut" id="donut"><svg id="compositionSvg" class="compositionSvg" viewBox="0 0 220 220" role="img" aria-label="Mock index composition"></svg><div class="donutCore"><strong id="donutValue">100%</strong><span class="mono" id="donutLabel">modeled</span></div></div>',
    s,
    count=1
)
# Make disclaimer unambiguous even if prior wording changed.
s = re.sub(r'<div class="compositionFoot mono">.*?</div>', '<div class="compositionFoot mono">* Mock model weights for prototype UI — not live portfolio weights.</div>', s, count=1)

detail_css = r'''

/* Interactive composition + mock market detail v4 */
.compositionNote,.cardTitle span,.stat small,.managerFact small,.indexBrief small,.positionItem small,.lpPositionRow small,.lpPositionHead>span{font-size:11px}
.chartEmpty,.risk,.compositionFoot{font-size:11px}.managerFact p,.indexBrief p{font-size:14px}.empty{font-size:13px}
.donut{background:none!important;overflow:visible}.compositionSvg{position:absolute;inset:0;width:100%;height:100%;overflow:visible;transform:rotate(0deg)}
.compositionSlice{stroke:#0c0c08;stroke-width:2;cursor:pointer;transition:opacity .16s ease,filter .16s ease,transform .16s ease;transform-origin:110px 110px;outline:none}
.compositionSlice:hover,.compositionSlice:focus,.compositionSlice.active{filter:brightness(1.22) drop-shadow(0 3px 8px rgba(0,0,0,.35));opacity:1;transform:scale(1.025)}
.compositionSvg.hasActive .compositionSlice:not(.active){opacity:.38}
.legendItem{width:100%;font:inherit;color:inherit;text-align:left;cursor:pointer;transition:border-color .15s,background .15s,transform .15s;outline:none}
.legendItem:hover,.legendItem:focus,.legendItem.active{border-color:#655522;background:#151208;transform:translateX(2px)}
.legendItem.active b{color:#f0d56f}.donutCore{pointer-events:none}.donutCore strong{transition:color .15s}.donut.inspecting .donutCore strong{color:#f1d05d}
.mockBadge{display:inline-flex;align-items:center;margin-left:8px;padding:4px 7px;border:1px solid #4e4327;border-radius:999px;color:#c4aa50;font-size:11px;font-weight:850;letter-spacing:.07em;text-transform:uppercase}
.mockPositive{color:#8fe3aa!important}.mockHot{color:#e6ad6f!important}
'''
s = append_css(s, detail_css, '/* Interactive composition + mock market detail v4 */')

detail_script = r'''
<script>
/* Interactive mock fund model v4 — all values are prototype data. */
(()=>{
  const $=id=>document.getElementById(id);
  const meme=location.pathname.includes('gmemestonk');
  const d=meme?{
    ticker:'gMEMESTONK',tvl:'$2.31M',apr:'32.4%',emissions:'58.5K GLDSTN / day',perf:'+27.9%',
    holding:'86.4 gMEMESTONK',value:'$3,778',lp:'$7,420',fees:'$96.84',earned:'2,960 GLDSTN',
    objective:'High-beta index for internet-native, meme and attention-driven markets.',
    agent:'Scores momentum, liquidity and volatility; rebalances the approved basket while enforcing exposure and drawdown limits.',
    style:'Fast-reacting · momentum-aware · volatility constrained.',
    brief:'One tokenized position for a five-asset meme-market basket, continuously supervised by the fund agent.',
    assets:[['AI',26,'#e58a4a'],['BONER',18,'#d06842'],['MOO',16,'#aa4f3e'],['OPTIMUS',22,'#8e633c'],['MEME',18,'#d9a149']],
    path:'M0 204 C70 177 118 202 165 158 S260 174 315 123 S410 152 465 96 S570 134 630 68 S716 94 800 42'
  }:{
    ticker:'gAIX',tvl:'$6.84M',apr:'18.6%',emissions:'42.0K GLDSTN / day',perf:'+13.4%',
    holding:'114.2 gAIX',value:'$12,486',lp:'$18,750',fees:'$184.26',earned:'3,840 GLDSTN',
    objective:'Concentrated index for the AI compute, platforms and frontier-technology stack.',
    agent:'Monitors concentration, momentum and drift; rebalances weights and enforces the fund risk policy as conditions change.',
    style:'Systematic · conviction-weighted · risk-aware.',
    brief:'One tokenized position for the approved AI basket, with weights maintained by an autonomous portfolio agent.',
    assets:[['NVDA',30,'#e9c94f'],['GOOGL',25,'#a7b766'],['TSLA',18,'#5f9673'],['MU',15,'#877d4e'],['SPCX',12,'#b88f3d']],
    path:'M0 196 C72 180 124 187 170 166 S258 175 320 137 S410 148 470 115 S566 126 630 82 S720 92 800 60'
  };

  const stats=document.querySelectorAll('.summary .stat strong');
  if(stats.length>=4){stats[0].textContent=d.tvl;stats[1].textContent=d.apr;stats[2].textContent=d.emissions;stats[3].textContent='GLD';}
  if($('indexObjective'))$('indexObjective').textContent=d.objective;
  if($('agentRole'))$('agentRole').textContent=d.agent;
  if($('managerStyle'))$('managerStyle').textContent=d.style;
  if($('indexBrief'))$('indexBrief').textContent=d.brief;
  if($('compositionNote'))$('compositionNote').textContent='Mock model weights · hover or tap to inspect';

  const path=document.querySelector('.chart svg path');
  if(path){path.setAttribute('d',d.path);path.setAttribute('stroke',meme?'rgba(230,173,111,.78)':'rgba(216,180,63,.78)');path.setAttribute('stroke-dasharray','0');path.setAttribute('stroke-width','4');}
  const chartNote=document.querySelector('.chartEmpty');
  if(chartNote){chartNote.innerHTML=`Mock 90D performance · <strong class="${meme?'mockHot':'mockPositive'}">${d.perf}</strong>`;}

  const pos=document.querySelectorAll('.holdingsCard .positionItem strong');
  if(pos.length>=2){pos[0].textContent=d.holding;pos[1].textContent=d.value;}
  const empty=document.querySelector('.holdingsCard .empty');
  if(empty)empty.innerHTML='<span class="mockBadge mono">Mock wallet</span> Layout preview only.';

  const lpVals=document.querySelectorAll('.lpPositionRow strong');
  if(lpVals.length>=5){lpVals[0].textContent='$'+d.ticker+' / GLD';lpVals[1].textContent=d.lp;lpVals[2].textContent=d.apr;lpVals[3].textContent=d.fees;lpVals[4].textContent=d.earned;}
  const claim=document.querySelector('.claimLp');
  if(claim){claim.disabled=false;claim.onclick=()=>{const old=claim.textContent;claim.textContent='Claimed';setTimeout(()=>claim.textContent=old,1200);};}

  const donut=$('donut'), svg=$('compositionSvg'), legend=$('legend');
  if(!donut||!svg||!legend)return;
  donut.style.background='none';
  legend.innerHTML='';svg.innerHTML='';
  const NS='http://www.w3.org/2000/svg', cx=110,cy=110,ro=96,ri=59;
  const point=(r,a)=>{const rad=(a-90)*Math.PI/180;return [cx+r*Math.cos(rad),cy+r*Math.sin(rad)]};
  const ring=(start,end)=>{const p1=point(ro,start),p2=point(ro,end),p3=point(ri,end),p4=point(ri,start),large=end-start>180?1:0;return `M ${p1[0]} ${p1[1]} A ${ro} ${ro} 0 ${large} 1 ${p2[0]} ${p2[1]} L ${p3[0]} ${p3[1]} A ${ri} ${ri} 0 ${large} 0 ${p4[0]} ${p4[1]} Z`;};
  let angle=0, locked=null;
  const slices=[];
  const activate=i=>{slices.forEach((s,x)=>s.classList.toggle('active',x===i));[...legend.children].forEach((n,x)=>n.classList.toggle('active',x===i));svg.classList.add('hasActive');donut.classList.add('inspecting');$('donutValue').textContent=d.assets[i][1]+'%';$('donutLabel').textContent=d.assets[i][0];};
  const reset=()=>{slices.forEach(s=>s.classList.remove('active'));[...legend.children].forEach(n=>n.classList.remove('active'));svg.classList.remove('hasActive');donut.classList.remove('inspecting');$('donutValue').textContent='100%';$('donutLabel').textContent='modeled';};
  d.assets.forEach(([name,w,color],i)=>{
    const start=angle,end=angle+w*3.6;angle=end;
    const path=document.createElementNS(NS,'path');path.setAttribute('d',ring(start,end));path.setAttribute('fill',color);path.setAttribute('class','compositionSlice');path.setAttribute('tabindex','0');path.setAttribute('role','button');path.setAttribute('aria-label',`${name}, ${w}% mock weight`);svg.appendChild(path);slices.push(path);
    const row=document.createElement('button');row.type='button';row.className='legendItem';row.innerHTML=`<i class="legendDot" style="--swatch:${color}"></i><b class="mono">${name}</b><span class="mono">${w}%</span>`;legend.appendChild(row);
    const enter=()=>activate(i),leave=()=>{if(locked===null)reset()};
    path.addEventListener('mouseenter',enter);path.addEventListener('mouseleave',leave);path.addEventListener('focus',enter);path.addEventListener('blur',leave);
    row.addEventListener('mouseenter',enter);row.addEventListener('mouseleave',leave);row.addEventListener('focus',enter);row.addEventListener('blur',leave);
    const toggle=()=>{locked=locked===i?null:i;locked===null?reset():activate(i)};path.addEventListener('click',toggle);row.addEventListener('click',toggle);
  });
  donut.addEventListener('mouseleave',()=>{if(locked===null)reset()});
})();
</script>
'''
s = append_script(s, detail_script, '/* Interactive mock fund model v4')
p.write_text(s)


# -----------------------------------------------------------------------------
# Readability scan: raise the actual CSS type floor across every rendered page.
# Deliberate font-size:0 values used to hide tablet labels remain untouched.
# -----------------------------------------------------------------------------
for name in HTML_FILES:
    p = ROOT / name
    text = p.read_text()
    text = lift_font_floor(text, floor=11)
    if '/* Site-wide type floor v4 */' not in text:
        text = append_css(text, '\n/* Site-wide type floor v4 */\nhtml{-webkit-text-size-adjust:100%;text-size-adjust:100%}\n', '/* Site-wide type floor v4 */')
    p.write_text(text)

# index.html and landing.html intentionally remain identical public landing surfaces.
landing = (ROOT/'landing.html').read_text()
index = (ROOT/'index.html').read_text()
if landing != index:
    # They are aliases in this prototype; keep typography fixes synchronized.
    (ROOT/'landing.html').write_text(index)

print('Applied mock data, interactive composition, and site-wide readability floor.')
