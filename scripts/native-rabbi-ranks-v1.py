from pathlib import Path
import re

RANK_CSS = """
/* Native Rabbi Schlomo Goldstein rank artwork v1 */
.rankArtwork{
  background-repeat:no-repeat!important;
  background-position:center!important;
  background-size:cover!important;
  background-color:#0a0a07!important;
}
.rank-base{background-image:url('/18.png')!important}
.rank-intern{background-image:url('/2_intern.png')!important}
.rank-analyst{background-image:url('/3_analyst.png')!important}
.rank-associate{background-image:url('/4_associate.png')!important}
.rank-vp{background-image:url('/5_vp.png')!important}
.rank-md{background-image:url('/6_md.png')!important}
.rank-partner{background-image:url('/7_partner.png')!important}
"""


def inject_native_css(path: str) -> None:
    p = Path(path)
    s = p.read_text()
    s = s.replace('<link rel="stylesheet" href="/assets/rank-sprite.css" />\n', '')
    if '/* Native Rabbi Schlomo Goldstein rank artwork v1 */' not in s:
        s = s.replace('</style>', RANK_CSS + '\n</style>', 1)
    p.write_text(s)


def replace_once(s: str, old: str, new: str, label: str) -> str:
    if old not in s:
        raise SystemExit(f'{label} anchor not found')
    return s.replace(old, new, 1)


# ---------------- My Seat ----------------
p = Path('my-seat.html')
s = p.read_text()

old_rail = '''    <div class="rankRail" id="rankRail" aria-label="Seat rank preview">
      <button class="rankThumb" data-rank="0"><span class="rankArtwork rank-intern"></span><b>Intern</b></button>
      <button class="rankThumb" data-rank="1"><span class="rankArtwork rank-analyst"></span><b>Analyst</b></button>
      <button class="rankThumb" data-rank="2"><span class="rankArtwork rank-associate"></span><b>Associate</b></button>
      <button class="rankThumb" data-rank="3"><span class="rankArtwork rank-vp"></span><b>VP</b></button>
      <button class="rankThumb" data-rank="4"><span class="rankArtwork rank-md"></span><b>MD</b></button>
      <button class="rankThumb" data-rank="5"><span class="rankArtwork rank-partner"></span><b>Partner</b></button>
    </div>'''
new_rail = '''    <div class="rankRail" id="rankRail" aria-label="Seat evolution preview">
      <button class="rankThumb" data-rank="-1"><span class="rankArtwork rank-base"></span><b>Seat</b></button>
      <button class="rankThumb" data-rank="0"><span class="rankArtwork rank-intern"></span><b>Intern</b></button>
      <button class="rankThumb" data-rank="1"><span class="rankArtwork rank-analyst"></span><b>Analyst</b></button>
      <button class="rankThumb" data-rank="2"><span class="rankArtwork rank-associate"></span><b>Associate</b></button>
      <button class="rankThumb" data-rank="3"><span class="rankArtwork rank-vp"></span><b>VP</b></button>
      <button class="rankThumb" data-rank="4"><span class="rankArtwork rank-md"></span><b>MD</b></button>
      <button class="rankThumb" data-rank="5"><span class="rankArtwork rank-partner"></span><b>Partner</b></button>
    </div>'''
s = replace_once(s, old_rail, new_rail, 'My Seat rank rail')
s = replace_once(
    s,
    '.rankRail{grid-column:1/-1;display:grid;grid-template-columns:repeat(6,1fr);',
    '.rankRail{grid-column:1/-1;display:grid;grid-template-columns:repeat(7,1fr);',
    'My Seat rank rail columns',
)

old_ranks = """const ranks=[
  {key:'intern',label:'Intern',min:0,next:1000,capacity:1},
  {key:'analyst',label:'Analyst',min:1000,next:5000,capacity:2},
  {key:'associate',label:'Associate',min:5000,next:15000,capacity:3},
  {key:'vp',label:'VP',min:15000,next:40000,capacity:5},
  {key:'md',label:'MD',min:40000,next:100000,capacity:8},
  {key:'partner',label:'Partner',min:100000,next:null,capacity:12}
];"""
new_ranks = """const baseSeat={key:'base',label:'Seat'};
const ranks=[
  {key:'intern',label:'Intern',min:0,next:1000,capacity:1},
  {key:'analyst',label:'Analyst',min:1000,next:5000,capacity:2},
  {key:'associate',label:'Associate',min:5000,next:15000,capacity:3},
  {key:'vp',label:'VP',min:15000,next:40000,capacity:5},
  {key:'md',label:'MD',min:40000,next:100000,capacity:8},
  {key:'partner',label:'Partner',min:100000,next:null,capacity:12}
];"""
s = replace_once(s, old_ranks, new_ranks, 'My Seat ranks')

pattern = re.compile(r"function setVisualRank\(i,preview=false\)\{.*?\n\}\nfunction renderMilestones", re.S)
replacement = """function setVisualRank(i,preview=false){
  const r=i<0?baseSeat:ranks[i],art=$('rankArt');
  art.classList.add('changing');
  setTimeout(()=>{art.className=`rankArtwork rank-${r.key} rankSeatArt`;},90);
  setTimeout(()=>art.classList.remove('changing'),240);
  $('visualRank').textContent=r.label;
  $('rankCue').textContent=i<0?'Original Seat artwork':(preview?`Preview · ${r.label}`:'Rank follows staked $GLDSTN');
  document.querySelectorAll('.rankThumb').forEach(b=>b.classList.toggle('active',Number(b.dataset.rank)===i));
}
function renderMilestones"""
s, n = pattern.subn(replacement, s, count=1)
if n != 1:
    raise SystemExit('My Seat setVisualRank anchor not found')

s = replace_once(s, 'let i=0;setVisualRank(i,true);', 'let i=-1;setVisualRank(i,true);', 'My Seat autoplay start')
s = replace_once(
    s,
    "document.querySelectorAll('.rankThumb').forEach((b,i)=>b.onclick=()=>previewRank(i));",
    "document.querySelectorAll('.rankThumb').forEach(b=>b.onclick=()=>previewRank(Number(b.dataset.rank)));",
    'My Seat rank click handler',
)
p.write_text(s)
inject_native_css('my-seat.html')


# ---------------- Mint / reveal ----------------
p = Path('app.html')
s = p.read_text()
s = replace_once(
    s,
    '<div class="seatOrb rankArtwork rank-intern mintSeatArt" id="nameTag" role="img" aria-label="Rabbi Schlomo Goldstein rank artwork"></div>',
    '<div class="seatOrb rankArtwork rank-base mintSeatArt" id="nameTag" role="img" aria-label="Rabbi Schlomo Goldstein Seat evolution artwork"></div>',
    'Mint rank art',
)

old_strip = '''        <button class="mintRankChip active" data-mint-rank="0">Intern</button><button class="mintRankChip" data-mint-rank="1">Analyst</button><button class="mintRankChip" data-mint-rank="2">Associate</button><button class="mintRankChip" data-mint-rank="3">VP</button><button class="mintRankChip" data-mint-rank="4">MD</button><button class="mintRankChip" data-mint-rank="5">Partner</button>'''
new_strip = '''        <button class="mintRankChip active" data-mint-rank="0">Seat</button><button class="mintRankChip" data-mint-rank="1">Intern</button><button class="mintRankChip" data-mint-rank="2">Analyst</button><button class="mintRankChip" data-mint-rank="3">Associate</button><button class="mintRankChip" data-mint-rank="4">VP</button><button class="mintRankChip" data-mint-rank="5">MD</button><button class="mintRankChip" data-mint-rank="6">Partner</button>'''
s = replace_once(s, old_strip, new_strip, 'Mint rank strip')
s = replace_once(s, '<strong id="mintRankName">Intern</strong>', '<strong id="mintRankName">Seat</strong>', 'Mint default rank label')
s = replace_once(
    s,
    '.mintRankStrip{width:min(282px,100%);display:grid;grid-template-columns:repeat(3,1fr);',
    '.mintRankStrip{width:min(320px,100%);display:grid;grid-template-columns:repeat(4,1fr);',
    'Mint rank strip layout',
)

s = replace_once(
    s,
    "const mintRanks=[['intern','Intern'],['analyst','Analyst'],['associate','Associate'],['vp','VP'],['md','MD'],['partner','Partner']];let mintPreviewTimer=null,mintReturn=null;",
    "const mintRanks=[['base','Seat'],['intern','Intern'],['analyst','Analyst'],['associate','Associate'],['vp','VP'],['md','MD'],['partner','Partner']];let mintPreviewTimer=null,mintReturn=null;",
    'Mint ranks array',
)
s = replace_once(
    s,
    "mintReturn=setTimeout(()=>{setMintRank(0);mintReturn=null},450)",
    "mintReturn=setTimeout(()=>{setMintRank(1);mintReturn=null},520)",
    'Mint autoplay return state',
)
s = replace_once(
    s,
    "if(p[3]){art.className='seatOrb rankArtwork rank-intern mintSeatArt';art.textContent='';$('mintArtWrap').classList.remove('fallbackMode');$('mintRankStrip').style.display='grid';$('mintRankHint').style.display='block';$('mintRankName').textContent='Intern';document.querySelectorAll('.mintRankChip').forEach((b,x)=>b.classList.toggle('active',x===0));}",
    "if(p[3]){art.className='seatOrb rankArtwork rank-base mintSeatArt';art.textContent='';$('mintArtWrap').classList.remove('fallbackMode');$('mintRankStrip').style.display='grid';$('mintRankHint').style.display='block';$('mintRankName').textContent='Seat';document.querySelectorAll('.mintRankChip').forEach((b,x)=>b.classList.toggle('active',x===0));}",
    'Mint draw initial art',
)
s = replace_once(
    s,
    "document.querySelectorAll('.mintRankChip').forEach((b,i)=>b.addEventListener('click',()=>{stopMintPreview();setMintRank(i);mintReturn=setTimeout(()=>{setMintRank(0);mintReturn=null},1200)}));",
    "document.querySelectorAll('.mintRankChip').forEach((b,i)=>b.addEventListener('click',()=>{stopMintPreview();setMintRank(i);mintReturn=setTimeout(()=>{setMintRank(1);mintReturn=null},1500)}));",
    'Mint rank click handler',
)
s = replace_once(s, 'setMintRank(i)},560)', 'setMintRank(i)},760)', 'Mint autoplay pacing')
p.write_text(s)
inject_native_css('app.html')


# ---------------- Welcome / share card ----------------
p = Path('welcome.html')
s = p.read_text()
pattern = re.compile(r"async function drawRankArtwork\(ctx,x,y,w,h,key\)\{.*?\n\}", re.S)
replacement = """async function drawRankArtwork(ctx,x,y,w,h,key){
  const files={base:'/18.png',intern:'/2_intern.png',analyst:'/3_analyst.png',associate:'/4_associate.png',vp:'/5_vp.png',md:'/6_md.png',partner:'/7_partner.png'};
  const art=await loadImage(files[key]||files.intern);cover(ctx,art,x,y,w,h);
}"""
s, n = pattern.subn(replacement, s, count=1)
if n != 1:
    raise SystemExit('Welcome drawRankArtwork anchor not found')
p.write_text(s)
inject_native_css('welcome.html')


# Preload the first two states that appear immediately in the UX.
for path in ('my-seat.html', 'app.html'):
    p = Path(path)
    s = p.read_text()
    marker = '<meta name="theme-color" content="#080806" />'
    preload = '<link rel="preload" href="/18.png" as="image" />\n<link rel="preload" href="/2_intern.png" as="image" />'
    if preload not in s:
        s = s.replace(marker, marker + '\n' + preload, 1)
    p.write_text(s)

print('Native Rabbi Schlomo artwork integrated into Mint, My Seat, and Welcome.')
