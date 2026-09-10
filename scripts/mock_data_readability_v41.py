from pathlib import Path
import re

ROOT=Path('.')
HTML_FILES=['index.html','landing.html','app.html','welcome.html','my-seat.html','funds.html','fund-detail.html']


def lift_floor(text,floor=12):
    def size_repl(m):
        n=float(m.group(2))
        return m.group(1)+f'{floor}px' if 0<n<floor else m.group(0)
    text=re.sub(r'(font-size\s*:\s*)(\d+(?:\.\d+)?)px',size_repl,text)
    def font_repl(m):
        prop=m.group(0)
        def one(pm):
            n=float(pm.group(1))
            return f'{floor}px' if 0<n<floor else pm.group(0)
        return re.sub(r'(\d+(?:\.\d+)?)px',one,prop,count=1)
    return re.sub(r'font\s*:[^;{}]+',font_repl,text)

# Readability floor: 12px everywhere except deliberate font-size:0 hiding rules.
for name in HTML_FILES:
    p=ROOT/name
    s=lift_floor(p.read_text(),12)
    p.write_text(s)

# Funds overview: replace the demo wallet handler with a reversible version and
# populate market data in action tickets as well.
p=ROOT/'funds.html'
s=p.read_text()
if '/* Mock data final QA v4.1 */' not in s:
    patch=r'''
<script>
/* Mock data final QA v4.1 */
(()=>{
 const mock={
  gaix:{tvl:'$6.84M',apr:'18.6%',emissions:'42.0K GLDSTN / day',holding:'114.2 gAIX',value:'$12,486',lp:'$18,750',fees:'$184.26',earned:'3,840 GLDSTN'},
  meme:{tvl:'$2.31M',apr:'32.4%',emissions:'58.5K GLDSTN / day',holding:'86.4 gMEMESTONK',value:'$3,778',lp:'$7,420',fees:'$96.84',earned:'2,960 GLDSTN'}
 };
 const wallet=document.getElementById('walletBtn'),holdings=document.getElementById('fundHoldings'),table=document.querySelector('.lpTable');
 if(wallet&&holdings&&table){
   let connected=false;
   const emptyRow=()=>'<div class="lpRow" id="lpPositions"><div class="lpPool"><strong>—</strong><small class="mono">Connect wallet</small></div><strong>—</strong><strong>—</strong><strong>—</strong><strong>—</strong><div class="lpRowActions"><button class="claimFees" disabled>Claim</button><button class="manageLp" disabled>Manage</button></div></div>';
   const row=(ticker,d,extra='')=>`<div class="lpRow ${extra}" ${extra?'':'id="lpPositions"'}><div class="lpPool"><strong>$${ticker} / GLD</strong><small class="mono">Mock connected position</small></div><strong>${d.lp}</strong><strong>${d.apr}</strong><strong>${d.fees}</strong><strong>${d.earned}</strong><div class="lpRowActions"><button class="claimFees">Claim</button><button class="manageLp">Manage</button></div></div>`;
   const label=table.querySelector('.lpLabels');
   const render=()=>{
     table.querySelectorAll('.lpRow:not(.lpLabels)').forEach(n=>n.remove());
     if(!connected){label.insertAdjacentHTML('afterend',emptyRow());holdings.textContent='Connect wallet to view holdings.';return;}
     label.insertAdjacentHTML('afterend',row('gAIX',mock.gaix)+row('gMEMESTONK',mock.meme,'mockLpExtra'));
     holdings.innerHTML=`<span class="mockTag mono">Mock wallet</span><div class="mockHoldingGrid"><div class="mockHolding"><div><b>$gAIX</b><small>${mock.gaix.holding}</small></div><strong>${mock.gaix.value}</strong></div><div class="mockHolding"><div><b>$gMEMESTONK</b><small>${mock.meme.holding}</small></div><strong>${mock.meme.value}</strong></div></div>`;
     table.querySelectorAll('.claimFees').forEach(b=>b.onclick=()=>{b.textContent='Claimed';setTimeout(()=>b.textContent='Claim',1100)});
   };
   wallet.onclick=()=>{connected=!connected;wallet.innerHTML=connected?'<i></i>0x71…9A3':'<i></i>Connect wallet';render();};
 }
 const ticketRows=[...document.querySelectorAll('#actionModal .ticketRow')];
 document.querySelectorAll('.action').forEach(btn=>btn.addEventListener('click',()=>{
   const d=String(btn.dataset.fund).toLowerCase().includes('meme')?mock.meme:mock.gaix;
   if(ticketRows[1])ticketRows[1].querySelector('b').textContent=d.tvl;
   if(ticketRows[2])ticketRows[2].querySelector('b').textContent=d.apr;
   if(ticketRows[3])ticketRows[3].querySelector('b').textContent=d.emissions;
 }));
})();
</script>
'''
    s=s.replace('</body>',patch+'\n</body>',1)
p.write_text(s)

# Detail tickets should carry the same mock market context as the page.
p=ROOT/'fund-detail.html'
s=p.read_text()
if '/* Detail ticket mock sync v4.1 */' not in s:
    patch=r'''
<script>
/* Detail ticket mock sync v4.1 */
(()=>{
 const meme=location.pathname.includes('gmemestonk');
 const d=meme?{tvl:'$2.31M',apr:'32.4%',emissions:'58.5K GLDSTN / day'}:{tvl:'$6.84M',apr:'18.6%',emissions:'42.0K GLDSTN / day'};
 const rows=[...document.querySelectorAll('#modal .ticketRow')];
 if(rows[1])rows[1].querySelector('b').textContent=d.tvl;
 if(rows[2])rows[2].querySelector('b').textContent=d.apr;
 if(rows[3])rows[3].querySelector('b').textContent=d.emissions;
})();
</script>
'''
    s=s.replace('</body>',patch+'\n</body>',1)
p.write_text(s)

# Keep duplicated public landing prototype synchronized.
(ROOT/'landing.html').write_text((ROOT/'index.html').read_text())
print('Applied v4.1 QA: 12px type floor and complete mock-data ticket sync.')
