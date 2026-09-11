from pathlib import Path
import re

FILES = [Path("index.html"), Path("landing.html")]

CSS = r'''

/* Landing visual narrative v2 — institutional imagery + Seat roster */
.firmVisual{position:relative;min-height:560px;isolation:isolate}
.firmVisual:before{content:"";position:absolute;left:9%;right:3%;top:10%;bottom:6%;border:1px solid rgba(216,180,63,.09);border-radius:50%;filter:blur(.1px);pointer-events:none}
.firmScene{position:absolute;z-index:1;left:34px;right:50px;top:54px;bottom:50px;overflow:hidden;border:1px solid #4b4024;border-radius:22px;background:#0a0906;box-shadow:0 34px 90px rgba(0,0,0,.42),inset 0 0 0 1px rgba(255,230,145,.035)}
.firmScene:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(5,5,3,.08),rgba(5,5,3,.08) 48%,rgba(5,5,3,.76)),linear-gradient(90deg,rgba(6,6,4,.18),transparent 56%);pointer-events:none}
.firmSceneArt{display:block;width:100%;height:100%;object-fit:cover;object-position:center;filter:saturate(.88) contrast(1.03)}
.firmSceneTop{position:absolute;z-index:2;left:17px;right:17px;top:16px;display:flex;justify-content:space-between;gap:14px;align-items:center}
.firmSceneTag,.firmSceneStatus{display:inline-flex;align-items:center;min-height:30px;padding:0 9px;border:1px solid rgba(228,190,60,.28);border-radius:999px;background:rgba(8,8,5,.72);backdrop-filter:blur(9px);color:#d9c886;font:850 12px/1 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.095em;text-transform:uppercase}
.firmSceneStatus{color:#a9a087;border-color:rgba(255,255,255,.09)}.firmSceneStatus i{width:6px;height:6px;margin-right:7px;border-radius:50%;background:var(--green);box-shadow:0 0 10px rgba(143,227,170,.45)}
.firmSceneBottom{position:absolute;z-index:2;left:18px;right:18px;bottom:17px;display:flex;align-items:end;justify-content:space-between;gap:18px}
.firmSceneBottom strong{display:block;color:#f1e8d2;font:500 24px/1.05 Georgia,"Times New Roman",serif}.firmSceneBottom span{display:block;margin-top:5px;color:#a79d86;font-size:12px}.firmSceneMark{color:#d3b84f!important;font:850 12px/1 ui-monospace,SFMono-Regular,Menlo,monospace!important;letter-spacing:.12em;text-transform:uppercase;white-space:nowrap}
.heroIdentity{position:absolute;z-index:4;overflow:hidden;border:1px solid #554721;border-radius:13px;background:#0d0c08;box-shadow:0 22px 55px rgba(0,0,0,.42);transition:transform .22s ease,border-color .22s ease}
.heroIdentity:hover{transform:translateY(-3px);border-color:#856c24}.heroIdentity img{display:block;width:100%;aspect-ratio:1/1;object-fit:cover;background:#090906}.heroIdentityMeta{padding:9px 10px 10px;border-top:1px solid #2f2919;background:linear-gradient(180deg,#11100b,#0b0b08)}.heroIdentityMeta b{display:block;color:#e7dcc2;font-size:12px}.heroIdentityMeta span{display:block;margin-top:3px;color:#817866;font:800 12px/1.2 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.055em;text-transform:uppercase}.heroIdentity.main{left:-2px;bottom:20px;width:154px;transform:rotate(-2.2deg)}.heroIdentity.main:hover{transform:rotate(-2.2deg) translateY(-3px)}.heroIdentity.aix{right:-3px;top:17px;width:137px;transform:rotate(2deg)}.heroIdentity.aix:hover{transform:rotate(2deg) translateY(-3px)}.heroIdentity.meme{right:16px;bottom:9px;width:129px;transform:rotate(-1.2deg)}.heroIdentity.meme:hover{transform:rotate(-1.2deg) translateY(-3px)}
.firmFundRail{position:absolute;z-index:5;left:184px;right:175px;bottom:21px;display:flex;gap:7px;justify-content:center}.firmFundChip{min-width:0;display:flex;align-items:center;gap:7px;padding:6px 9px 6px 7px;border:1px solid #41371e;border-radius:9px;background:rgba(10,9,6,.88);backdrop-filter:blur(10px);color:#cfc3a6;font:850 12px/1 ui-monospace,SFMono-Regular,Menlo,monospace;white-space:nowrap}.firmFundChip img{width:24px;height:24px;border-radius:6px;object-fit:cover}.firmFundChip b{color:#e3c653}
.firmRoster{position:relative;overflow:hidden;background:radial-gradient(circle at 78% 32%,rgba(216,180,63,.05),transparent 34%),#080806}.rosterGrid{display:grid;grid-template-columns:minmax(280px,.64fr) minmax(0,1.36fr);gap:56px;align-items:center}.rosterCopy h2{max-width:560px;margin:10px 0 17px;font-size:clamp(44px,4.8vw,70px);line-height:.98;letter-spacing:-.045em}.rosterCopy>p{max-width:520px;margin:0;color:#9f9682;font-size:15px;line-height:1.72}.rosterFacts{display:grid;gap:1px;margin:28px 0 27px;border:1px solid #292419;border-radius:12px;overflow:hidden;background:#292419}.rosterFact{display:grid;grid-template-columns:84px 1fr;gap:15px;align-items:center;padding:13px 14px;background:#0d0d09}.rosterFact b{color:#e5d9ba;font:500 19px/1 Georgia,"Times New Roman",serif}.rosterFact span{color:#827967;font-size:12px;line-height:1.45}.rosterLink{display:inline-flex;align-items:center;gap:8px;color:#d9c167;text-decoration:none;font-size:13px;font-weight:850}.rosterLink:after{content:"→";transition:transform .15s}.rosterLink:hover:after{transform:translateX(3px)}
.seatMosaicWrap{position:relative;padding:18px;border:1px solid #302a1b;border-radius:20px;background:linear-gradient(180deg,#0e0e09,#0a0a07);box-shadow:0 28px 85px rgba(0,0,0,.22)}.seatMosaicWrap:before{content:"SELECTED FIRM SEATS";position:absolute;z-index:3;left:27px;top:28px;padding:6px 8px;border:1px solid rgba(216,180,63,.25);border-radius:7px;background:rgba(8,8,5,.78);backdrop-filter:blur(8px);color:#c5ab4e;font:850 12px/1 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.12em}
.seatMosaic{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}.rosterSeat{position:relative;overflow:hidden;aspect-ratio:1/1;border:1px solid #2f2a1c;border-radius:11px;background:#090906}.rosterSeat img{display:block;width:100%;height:100%;object-fit:cover;transition:transform .32s ease,filter .32s ease}.rosterSeat:after{content:"";position:absolute;inset:36% 0 0;background:linear-gradient(transparent,rgba(5,5,3,.89));pointer-events:none}.rosterSeat:hover img{transform:scale(1.035);filter:saturate(1.04)}.rosterSeat.manager{border-color:#5b4b20}.rosterSeatMeta{position:absolute;z-index:2;left:10px;right:10px;bottom:9px}.rosterSeatMeta b{display:block;color:#eee4ca;font-size:12px}.rosterSeatMeta span{display:block;margin-top:3px;color:#938970;font:800 12px/1.15 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.055em;text-transform:uppercase}.rosterSeat.manager .rosterSeatMeta span{color:#d2b84f}.rosterCaption{display:flex;justify-content:space-between;gap:16px;align-items:center;margin-top:12px;padding:0 2px;color:#6e6758;font-size:12px}.rosterCaption b{color:#9c927b;font-weight:800}
@media(max-width:1050px){.firmVisual{min-height:530px;max-width:760px;margin:0 auto}.rosterGrid{grid-template-columns:1fr;gap:34px}.rosterCopy{max-width:760px}.seatMosaicWrap{max-width:820px}}
@media(max-width:760px){.firmVisual{min-height:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;padding-top:4px}.firmVisual:before{display:none}.firmScene{position:relative;grid-column:1/-1;left:auto;right:auto;top:auto;bottom:auto;height:330px;border-radius:16px}.firmSceneTop{left:12px;right:12px;top:12px}.firmSceneBottom{left:14px;right:14px;bottom:14px}.firmSceneBottom strong{font-size:20px}.heroIdentity,.heroIdentity.main,.heroIdentity.aix,.heroIdentity.meme{position:relative;left:auto;right:auto;top:auto;bottom:auto;width:auto;transform:none;border-radius:10px}.heroIdentity:hover,.heroIdentity.main:hover,.heroIdentity.aix:hover,.heroIdentity.meme:hover{transform:translateY(-2px)}.heroIdentityMeta{padding:8px}.heroIdentityMeta span{white-space:normal}.firmFundRail{position:relative;grid-column:1/-1;left:auto;right:auto;bottom:auto;justify-content:flex-start;overflow-x:auto;padding:2px 0;scrollbar-width:none}.firmFundRail::-webkit-scrollbar{display:none}.rosterGrid{gap:26px}.seatMosaicWrap{padding:12px}.seatMosaicWrap:before{left:20px;top:20px}.rosterCaption{display:grid}.firmSceneMark{display:none}}
@media(max-width:520px){.firmScene{height:280px}.firmSceneStatus{display:none}.firmSceneBottom span{display:none}.heroIdentityMeta b{font-size:12px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.heroIdentityMeta span{font-size:12px}.seatMosaic{grid-template-columns:repeat(2,1fr)}.rosterFact{grid-template-columns:72px 1fr}.rosterCopy h2{font-size:44px}}
@media(prefers-reduced-motion:reduce){.heroIdentity,.rosterSeat img,.rosterLink:after{transition:none!important}}
'''

HERO = r'''<div class="firmVisual revealOnScroll" aria-label="Goldstein Group visual overview">
      <div class="firmScene">
        <img class="firmSceneArt" src="/assets/goldstein-hero.webp" alt="Goldstein Group office scene" fetchpriority="high">
        <div class="firmSceneTop"><span class="firmSceneTag">Goldstein Group</span><span class="firmSceneStatus"><i></i> Onchain firm</span></div>
        <div class="firmSceneBottom"><div><strong>Take a seat at the firm.</strong><span>Products, operators and incentives in one system.</span></div><span class="firmSceneMark">Capital · People · Progress</span></div>
      </div>
      <article class="heroIdentity main" aria-label="Goldstein Seat 18"><img src="/18.png" alt="Goldstein Seat #18 NFT"><div class="heroIdentityMeta"><b>Seat #0018</b><span>Member identity</span></div></article>
      <article class="heroIdentity aix" aria-label="Seat B10, gAIX manager"><img src="/b10.png" alt="Seat B10 NFT, manager of gAIX"><div class="heroIdentityMeta"><b>Seat B10</b><span>gAIX manager</span></div></article>
      <article class="heroIdentity meme" aria-label="Seat B17, gMEMESTONK manager"><img src="/b17.png" alt="Seat B17 NFT, manager of gMEMESTONK"><div class="heroIdentityMeta"><b>Seat B17</b><span>gMEMESTONK manager</span></div></article>
      <div class="firmFundRail" aria-label="Goldstein house funds"><span class="firmFundChip"><img src="/gAIX.png" alt=""><b>gAIX</b> House Fund</span><span class="firmFundChip"><img src="/gMEMESTOCK.png" alt=""><b>gMEMESTONK</b> House Fund</span></div>
    </div>'''

ROSTER = r'''<section class="section firmRoster" id="firm-roster"><div class="wrap rosterGrid">
  <div class="rosterCopy revealOnScroll">
    <div class="eyebrow">Inside the firm</div>
    <h2>A network with faces, roles and products.</h2>
    <p>Goldstein Seats turn participation into a visible operating identity. Some Seats manage house funds; every Seat can build rank, unlock capacity and become part of the distribution layer behind the firm's products.</p>
    <div class="rosterFacts">
      <div class="rosterFact"><b>1,500</b><span>Fixed Seat identities form the operating network.</span></div>
      <div class="rosterFact"><b>Rank</b><span>Stake $GLDSTN to progress from Intern toward Partner.</span></div>
      <div class="rosterFact"><b>Funds</b><span>House managers connect individual Seats to live product mandates.</span></div>
    </div>
    <a class="rosterLink" href="/app">Enter Goldstein HQ</a>
  </div>
  <div class="seatMosaicWrap revealOnScroll">
    <div class="seatMosaic">
      <article class="rosterSeat"><img src="/01.png" alt="Goldstein Seat #01 NFT" loading="lazy" decoding="async"><div class="rosterSeatMeta"><b>Seat #01</b><span>Seat identity</span></div></article>
      <article class="rosterSeat"><img src="/03.png" alt="Goldstein Seat #03 NFT" loading="lazy" decoding="async"><div class="rosterSeatMeta"><b>Seat #03</b><span>Seat identity</span></div></article>
      <article class="rosterSeat manager"><img src="/b10.png" alt="Goldstein Seat B10 NFT" loading="lazy" decoding="async"><div class="rosterSeatMeta"><b>Seat B10</b><span>gAIX house manager</span></div></article>
      <article class="rosterSeat"><img src="/10.png" alt="Goldstein Seat #10 NFT" loading="lazy" decoding="async"><div class="rosterSeatMeta"><b>Seat #10</b><span>Seat identity</span></div></article>
      <article class="rosterSeat"><img src="/18.png" alt="Goldstein Seat #18 NFT" loading="lazy" decoding="async"><div class="rosterSeatMeta"><b>Seat #18</b><span>Seat identity</span></div></article>
      <article class="rosterSeat manager"><img src="/b17.png" alt="Goldstein Seat B17 NFT" loading="lazy" decoding="async"><div class="rosterSeatMeta"><b>Seat B17</b><span>gMEMESTONK manager</span></div></article>
    </div>
    <div class="rosterCaption mono"><span><b>Selected Seat identities</b> · artwork from the current firm roster</span><span>Managers highlighted in gold</span></div>
  </div>
</div></section>'''

COPY_REPLACEMENTS = {
    "The landing page explains the system; Goldstein HQ is where users interact with it.": "Each fund turns a market thesis into a transparent, programmable product. Goldstein HQ is where investors and Seat holders move from the story into the market.",
    "Goldstein separates the public-facing firm from the operating app. The website explains what the firm is. Inside Goldstein HQ, a Seat becomes the user's persistent identity and the gateway to primary G-Fund activity.": "A Seat is a scarce operating identity inside Goldstein. It carries rank, capacity and economics with it, turning a wallet into a visible role inside the firm's distribution network.",
    "The UI keeps the mechanism legible: reveal → claim → stake → rank → mint. Complexity stays behind the interface instead of dominating the first interaction.": "Identity → alignment → distribution. One progression connects a Seat to rank, primary-market capacity and participation in the firm's economics.",
    "The interface should feel credible enough for capital, but native enough for crypto. The result is a visible operating system: products, participants and incentives connected in one place rather than buried behind corporate copy.": "Goldstein connects products, participants and incentives as one visible operating system. House funds create the product layer; Seats create distribution; $GLDSTN aligns rank and economics around the network.",
}

for path in FILES:
    text = path.read_text()

    if "/* Landing visual narrative v2" not in text:
        text = text.replace("\n</style>", CSS + "\n</style>", 1)

    hero_pattern = re.compile(
        r'<div class="terminal revealOnScroll" aria-label="Goldstein product preview">.*?(?=\n  </div>\n</section>\n<div class="signalStrip")',
        re.S,
    )
    if "class=\"firmVisual revealOnScroll\"" not in text:
        text, count = hero_pattern.subn(HERO, text, count=1)
        if count != 1:
            raise RuntimeError(f"Could not replace hero visual in {path}")

    if 'id="firm-roster"' not in text:
        marker = '<section class="section" id="funds">'
        if marker not in text:
            raise RuntimeError(f"Could not locate funds section in {path}")
        text = text.replace(marker, ROSTER + "\n\n" + marker, 1)

    for old, new in COPY_REPLACEMENTS.items():
        text = text.replace(old, new)

    # Load below-the-fold product artwork without blocking first paint.
    text = text.replace('src="/b10.png" alt="Seat B10, manager of gAIX"', 'src="/b10.png" alt="Seat B10, manager of gAIX" loading="lazy" decoding="async"')
    text = text.replace('src="/b17.png" alt="Seat B17, manager of gMEMESTONK"', 'src="/b17.png" alt="Seat B17, manager of gMEMESTONK" loading="lazy" decoding="async"')

    path.write_text(text)

print("Landing visual narrative v2 applied to index.html and landing.html")
