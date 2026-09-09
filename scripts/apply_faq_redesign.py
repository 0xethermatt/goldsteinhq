from pathlib import Path

p = Path('index.html')
html = p.read_text()

old_nav = '<a href="#learn"><span>How it works</span></a>'
new_nav = '<a href="#learn"><span>FAQ</span></a>'
if old_nav not in html:
    raise SystemExit('nav marker not found')
html = html.replace(old_nav, new_nav, 1)

old_floor_explain = '<details class="floorExplain"><summary>What is The Floor?</summary><p>Every reveal and reroll draws from the remaining collection. The Floor shows what has already been claimed and what is still available, so you can decide whether another reroll is worth it.</p></details>'
if old_floor_explain not in html:
    raise SystemExit('floor explainer marker not found')
html = html.replace(old_floor_explain, '', 1)

old_css = '.explainers{display:grid;gap:9px}.explainers details{border:1px solid #292519;border-radius:12px;background:#0d0d09}.explainers summary{cursor:pointer;list-style:none;padding:17px 18px;font-size:14px;font-weight:850}.explainers summary::-webkit-details-marker{display:none}.explainers summary:after{content:"+";float:right;color:#c6aa4a}.explainers details[open] summary:after{content:"−"}.explainers .content{padding:0 18px 18px;color:#968d78;font-size:13px;line-height:1.6}.unlockGrid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:10px}.unlock{padding:12px;border:1px solid #272318;border-radius:9px;background:#0b0b08}.unlock b{display:block;color:#ded5bd;font-size:12px}.unlock span{display:block;margin-top:2px;color:#7f7868;font-size:11px}'
new_css = '.faqSection{position:relative;margin-top:72px;padding-top:52px;border-top:1px solid #3a321e}.faqSection:before{content:"";position:absolute;top:-1px;left:0;width:180px;height:1px;background:linear-gradient(90deg,var(--gold),transparent);box-shadow:0 0 24px rgba(216,180,63,.18)}.faqLayout{display:grid;grid-template-columns:minmax(240px,.72fr) minmax(0,1.28fr);gap:54px;align-items:start}.faqIntro{padding:4px 0}.faqEyebrow{margin-bottom:10px;color:var(--gold);font-size:11px;font-weight:850;letter-spacing:.16em;text-transform:uppercase}.faqIntro h2{margin:0 0 12px;font-size:40px;line-height:1.04;font-weight:500;letter-spacing:-.03em}.faqIntro p{margin:0;max-width:340px;color:#938a76;font-size:14px;line-height:1.65}.faqList{display:grid;gap:9px}.faqList details{border:1px solid #2a2619;border-radius:12px;background:linear-gradient(180deg,#0f0f0a,#0c0c08);transition:border-color .16s,background .16s}.faqList details:hover{border-color:#40371f}.faqList details[open]{border-color:#493d20;background:linear-gradient(180deg,#121008,#0d0c08)}.faqList summary{cursor:pointer;list-style:none;display:flex;align-items:center;justify-content:space-between;gap:18px;padding:18px 19px;color:#e4dcc7;font-size:14px;font-weight:850}.faqList summary::-webkit-details-marker{display:none}.faqList summary:after{content:"+";flex:0 0 auto;width:28px;height:28px;display:grid;place-items:center;border:1px solid #40351b;border-radius:50%;color:#d8b43f;background:#151208;font-size:16px;font-weight:600}.faqList details[open] summary:after{content:"−"}.faqAnswer{padding:0 56px 18px 19px;color:#9b927d;font-size:13px;line-height:1.65}.faqAnswer strong{color:#d9cfb4}.faqAnswer .costPath{display:inline-block;margin-top:9px;padding:7px 10px;border:1px solid #352e1b;border-radius:8px;background:#0a0a07;color:#cfb75d;font-size:11px;font-weight:800;letter-spacing:.03em}'
if old_css not in html:
    raise SystemExit('old FAQ CSS marker not found')
html = html.replace(old_css, new_css, 1)

old_mobile = '@media(max-width:760px){:root{--side:0px}.sidebar{display:none}.prototype{left:0;font-size:9px;padding-inline:10px}main{margin-left:0}.shell{width:calc(100% - 24px);padding-top:12px}.hero{height:230px}.focus{padding:22px}.focus h1{font-size:40px}.focus p{font-size:15px}.flow{grid-template-columns:1fr}.revealCard{grid-template-columns:1fr}.seatVisual{border-right:0;border-bottom:1px solid var(--line);min-height:300px}.sectionHead,.floorTop{align-items:flex-start}.floorGrid{grid-template-columns:repeat(2,1fr)}.floorHint{width:100%;margin-left:0}.unlockGrid{grid-template-columns:1fr}}'
new_mobile = '@media(max-width:760px){:root{--side:0px}.sidebar{display:none}.prototype{left:0;font-size:9px;padding-inline:10px}main{margin-left:0}.shell{width:calc(100% - 24px);padding-top:12px}.hero{height:230px}.focus{padding:22px}.focus h1{font-size:40px}.focus p{font-size:15px}.flow{grid-template-columns:1fr}.revealCard{grid-template-columns:1fr}.seatVisual{border-right:0;border-bottom:1px solid var(--line);min-height:300px}.sectionHead,.floorTop{align-items:flex-start}.floorGrid{grid-template-columns:repeat(2,1fr)}.floorHint{width:100%;margin-left:0}.faqSection{margin-top:52px;padding-top:38px}.faqLayout{grid-template-columns:1fr;gap:24px}.faqIntro h2{font-size:34px}.faqIntro p{max-width:520px}}'
if old_mobile not in html:
    raise SystemExit('mobile CSS marker not found')
html = html.replace(old_mobile, new_mobile, 1)

old_small = '@media(max-width:480px){.hero{height:190px}.focus{padding:19px 17px}.focus h1{font-size:35px}.sectionHead{display:grid}.detail{padding:24px 20px}.detail h3{font-size:36px}.decision{grid-template-columns:1fr}.decisionNote{display:grid}.floorGrid{grid-template-columns:repeat(2,1fr)}.floorTools{display:grid}.tabs{width:100%}.tabs button{flex:1}.floorHint{font-size:11px}}'
new_small = '@media(max-width:480px){.hero{height:190px}.focus{padding:19px 17px}.focus h1{font-size:35px}.sectionHead{display:grid}.detail{padding:24px 20px}.detail h3{font-size:36px}.decision{grid-template-columns:1fr}.decisionNote{display:grid}.floorGrid{grid-template-columns:repeat(2,1fr)}.floorTools{display:grid}.tabs{width:100%}.tabs button{flex:1}.floorHint{font-size:11px}.faqIntro h2{font-size:31px}.faqList summary{padding:16px;font-size:13px}.faqAnswer{padding:0 44px 16px 16px}}'
if old_small not in html:
    raise SystemExit('small CSS marker not found')
html = html.replace(old_small, new_small, 1)

old_faq = '''<section class="explainers" id="learn">
  <details><summary>What does a Goldstein Seat unlock?</summary><div class="content">The character is the identity; the seat is the product.<div class="unlockGrid"><div class="unlock"><b>Access G-Funds</b><span>Interact with Goldstein's agent-managed products.</span></div><div class="unlock"><b>Launch your own fund</b><span>Create a custom fund managed by an agent.</span></div><div class="unlock"><b>Build rank</b><span>Earn capacity and fee share through participation.</span></div></div></div></details>
  <details><summary>How does the mint game work?</summary><div class="content">Your first reveal is free. If you don't want the draw, reroll with $GLDSTN; each reroll doubles in cost. When you find the seat you want, claim it for 0.025 ETH. One seat can be claimed per transaction.</div></details>
</section>'''
new_faq = '''<section class="faqSection" id="learn" aria-labelledby="faqTitle">
  <div class="faqLayout">
    <div class="faqIntro">
      <div class="faqEyebrow mono">FAQ</div>
      <h2 id="faqTitle">Before you take a seat.</h2>
      <p>Everything you need to know about revealing, rerolling and claiming — without getting in the way of the game.</p>
    </div>
    <div class="faqList" id="faqList">
      <details>
        <summary>How does the free reveal work?</summary>
        <div class="faqAnswer">Connect your wallet and sign one free transaction to see your first Seat. <strong>No ETH is charged for the reveal.</strong> You only pay if you choose to reroll or claim.</div>
      </details>
      <details>
        <summary>What happens after I reveal a Seat?</summary>
        <div class="faqAnswer">Your draw is temporarily held for you. You can either <strong>claim it for 0.025 ETH</strong> or reroll for another Seat from the remaining collection.</div>
      </details>
      <details>
        <summary>How do rerolls work?</summary>
        <div class="faqAnswer">Rerolls are paid in <strong>$GLDSTN</strong>. The cost doubles after each reroll, and you can keep going until you find the Seat you want to claim.<br><span class="costPath mono">100 → 200 → 400 → 800 → … $GLDSTN</span></div>
      </details>
      <details>
        <summary>What is The Floor?</summary>
        <div class="faqAnswer">The Floor is the <strong>available Seat universe</strong>. It shows what has already been claimed and what is still in the pool, so you can make a better reroll decision.</div>
      </details>
      <details>
        <summary>What does a Goldstein Seat unlock?</summary>
        <div class="faqAnswer">A Seat is your access point into Goldstein. It unlocks access to <strong>G-Funds</strong> and the ability to launch your own agent-managed fund. Rank, capacity and additional economics are earned through participation.</div>
      </details>
      <details>
        <summary>Are some characters more powerful than others?</summary>
        <div class="faqAnswer"><strong>No.</strong> The character is your identity; the Seat is the product. Core Seat utility does not depend on which character you draw.</div>
      </details>
    </div>
  </div>
</section>'''
if old_faq not in html:
    raise SystemExit('FAQ HTML marker not found')
html = html.replace(old_faq, new_faq, 1)

old_js = "applyFloorFilter('available');\ndocument.querySelectorAll('.nav a').forEach(a=>a.addEventListener('click',()=>{document.querySelectorAll('.nav a').forEach(x=>x.classList.remove('active'));a.classList.add('active')}));"
new_js = "applyFloorFilter('available');\ndocument.querySelectorAll('#faqList details').forEach(item=>item.addEventListener('toggle',()=>{if(item.open){document.querySelectorAll('#faqList details').forEach(other=>{if(other!==item)other.open=false;});}}));\ndocument.querySelectorAll('.nav a').forEach(a=>a.addEventListener('click',()=>{document.querySelectorAll('.nav a').forEach(x=>x.classList.remove('active'));a.classList.add('active')}));"
if old_js not in html:
    raise SystemExit('FAQ JS insertion marker not found')
html = html.replace(old_js, new_js, 1)

required = [
    'First draw is free',
    'Claim · 0.025 ETH',
    'Reroll · 100 $GLDSTN',
    'Available seat universe',
    'Before you take a seat.',
    'How does the free reveal work?',
    'Are some characters more powerful than others?'
]
for marker in required:
    if marker not in html:
        raise SystemExit(f'missing required marker: {marker}')

if html.count('<details>') < 6:
    raise SystemExit('FAQ count regression')

p.write_text(html)
print('FAQ redesign applied')