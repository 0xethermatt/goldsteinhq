from pathlib import Path

# Use square crops from the supplied six-card rank strip. This keeps the complete NFT frame visible.
p = Path('assets/rank-sprite.css')
s = p.read_text()
s = s.replace('background-size:689.474% 368.276%!important', 'background-size:693.529% 314.118%!important')
replacements = {
    'rank-intern{background-position:6.151% 6.941%': 'rank-intern{background-position:6.442% 8.242%',
    'rank-analyst{background-position:24.802% 6.941%': 'rank-analyst{background-position:24.281% 8.242%',
    'rank-associate{background-position:44.048% 6.941%': 'rank-associate{background-position:41.625% 8.242%',
    'rank-vp{background-position:62.202% 6.941%': 'rank-vp{background-position:58.870% 8.242%',
    'rank-md{background-position:80.853% 6.941%': 'rank-md{background-position:76.511% 8.242%',
    'rank-partner{background-position:99.306% 6.941%': 'rank-partner{background-position:93.756% 8.242%',
}
for old,new in replacements.items():
    s = s.replace(old,new)
p.write_text(s)

# My Seat: default a freshly claimed sample Seat to Intern / 0 stake and keep the whole NFT frame square.
p = Path('my-seat.html')
s = p.read_text()
s = s.replace('aspect-ratio:171/145', 'aspect-ratio:1/1')
s = s.replace('rankArtwork rank-associate rankSeatArt', 'rankArtwork rank-intern rankSeatArt')
s = s.replace('id="visualRank">Associate</strong>', 'id="visualRank">Intern</strong>')
s = s.replace('id="seatRankName">Associate</span>', 'id="seatRankName">Intern</span>')
s = s.replace('id="rankValue">Associate</div><div class="statSub" id="rankNextTop">2,500 $GLDSTN to VP</div>', 'id="rankValue">Intern</div><div class="statSub" id="rankNextTop">1,000 $GLDSTN to Analyst</div>')
s = s.replace('id="stakedTop">12,500</span>', 'id="stakedTop">0</span>')
s = s.replace('id="capacityValue">3 slots</div>', 'id="capacityValue">1 slot</div>')
s = s.replace('id="stakedAmount">12,500</span>', 'id="stakedAmount">0</span>')
s = s.replace('id="rankLeft">Associate</span><span id="rankProgress">12,500 / 15,000</span><span id="rankRight">VP</span>', 'id="rankLeft">Intern</span><span id="rankProgress">0 / 1,000</span><span id="rankRight">Analyst</span>')
s = s.replace('id="feeTier">Associate tier</strong>', 'id="feeTier">Intern tier</strong>')
s = s.replace('id="salaryTier">Associate tier</strong>', 'id="salaryTier">Intern tier</strong>')
s = s.replace("goldsteinSeatStake'", "goldsteinSeatStakeV2'")
s = s.replace("||12500", "||0")
s = s.replace("staked=12500;", "staked=0;")
p.write_text(s)

# Mint: make a successful sample claim initialize the same Seat at 0 stake.
p = Path('index.html')
s = p.read_text()
s = s.replace('aspect-ratio:171/145', 'aspect-ratio:1/1')
needle = "localStorage.setItem('goldsteinSeatIdentity',JSON.stringify({seat:$('seatNumber').textContent,name:$('characterName').textContent}));"
if needle in s and "goldsteinSeatStakeV2" not in s:
    s = s.replace(needle, needle + "if($('characterName').textContent==='Rabbi Schlomo Goldstein')localStorage.setItem('goldsteinSeatStakeV2','0');", 1)
p.write_text(s)

# Welcome/share shell: carry the exact sample NFT artwork through the post-claim moment.
p = Path('welcome.html')
s = p.read_text()
if '/assets/rank-sprite.css' not in s:
    s = s.replace('<meta name="viewport" content="width=device-width,initial-scale=1" />', '<meta name="viewport" content="width=device-width,initial-scale=1" />\n<link rel="stylesheet" href="/assets/rank-sprite.css" />', 1)

welcome_css = '''
/* Claimed Seat artwork handoff */
.nftRankArt{position:absolute;inset:0;display:none;border-radius:15px}
.nftInner.hasRank .nftRankArt{display:block}
.nftInner.hasRank #nftImage,.nftInner.hasRank .nftPlaceholder{display:none!important}
.nftFrame.hasRankFrame{aspect-ratio:1/1}
'''
if '/* Claimed Seat artwork handoff */' not in s:
    s = s.replace('</style>', welcome_css + '\n</style>', 1)

if 'id="nftRankArt"' not in s:
    s = s.replace('<img id="nftImage" alt="Minted Goldstein NFT">', '<img id="nftImage" alt="Minted Goldstein NFT">\n              <div id="nftRankArt" class="rankArtwork rank-intern nftRankArt" role="img" aria-label="Rabbi Schlomo Goldstein Intern rank"></div>', 1)
if 'id="nftFrame"' not in s:
    s = s.replace('<div class="nftFrame">', '<div class="nftFrame" id="nftFrame">', 1)

s = s.replace("let state={seat:'SEAT #0354',identity:'Goldstein Member',nftUrl:null};", "let state={seat:'SEAT #0354',identity:'Goldstein Member',nftUrl:null,rankKey:null};")
old_set = "function setNft(url){state.nftUrl=url||null;const inner=$('nftInner'),img=$('nftImage');if(url){img.src=url;inner.classList.add('hasImage')}else{img.removeAttribute('src');inner.classList.remove('hasImage')}}"
new_set = "function setNft(url,rankKey){state.nftUrl=url||null;state.rankKey=rankKey||null;const inner=$('nftInner'),img=$('nftImage'),frameEl=$('nftFrame'),rankArt=$('nftRankArt');inner.classList.remove('hasImage','hasRank');frameEl.classList.remove('hasRankFrame');if(rankKey){rankArt.className=`rankArtwork rank-${rankKey} nftRankArt`;inner.classList.add('hasRank');frameEl.classList.add('hasRankFrame');img.removeAttribute('src')}else if(url){img.src=url;inner.classList.add('hasImage')}else{img.removeAttribute('src')}}"
if old_set in s:
    s = s.replace(old_set,new_set,1)

old_open = "state.nftUrl=findNftUrl(doc);\n  const short=normalizeSeat(state.seat);\n  $('seatInline').textContent=short;$('nftSeat').textContent='Seat '+short;$('identityName').textContent=state.identity;$('identityInline').textContent=state.identity;$('nftIdentity').textContent=state.identity;setNft(state.nftUrl);"
new_open = "state.nftUrl=findNftUrl(doc);\n  state.rankKey=state.identity==='Rabbi Schlomo Goldstein'?'intern':null;\n  const short=normalizeSeat(state.seat);\n  $('seatInline').textContent=short;$('nftSeat').textContent='Seat '+short;$('identityName').textContent=state.identity;$('identityInline').textContent=state.identity;$('nftIdentity').textContent=state.identity;setNft(state.nftUrl,state.rankKey);"
if old_open in s:
    s = s.replace(old_open,new_open,1)

# Canvas renderer: crop the same rank art from the CSS sprite for the downloadable share card.
helper_anchor = "function rounded(ctx,x,y,w,h,r){ctx.beginPath();ctx.roundRect(x,y,w,h,r)}"
helper = """function rounded(ctx,x,y,w,h,r){ctx.beginPath();ctx.roundRect(x,y,w,h,r)}
async function drawRankArtwork(ctx,x,y,w,h,key){
  const el=$('nftRankArt'),bg=getComputedStyle(el).backgroundImage,m=bg.match(/url\\([\\\"']?(data:image\\/[^\\\"')]+)[\\\"']?\\)/);if(!m)throw new Error('Rank art unavailable');
  const sprite=await loadImage(m[1]);const xs={intern:65,analyst:245,associate:420,vp:594,md:772,partner:946};const sx=xs[key]??65,sy=30,sw=170,sh=170;ctx.drawImage(sprite,sx,sy,sw,sh,x,y,w,h);
}"""
if helper_anchor in s and 'async function drawRankArtwork' not in s:
    s = s.replace(helper_anchor,helper,1)

old_canvas = "if(state.nftUrl){try{const nft=await loadImage(state.nftUrl);ctx.save();rounded(ctx,nx+12,ny+12,nw-24,nh-24,18);ctx.clip();cover(ctx,nft,nx+12,ny+12,nw-24,nh-24);ctx.restore()}catch{drawPlaceholder(ctx,nx,ny,nw,nh)}}else{drawPlaceholder(ctx,nx,ny,nw,nh)}"
new_canvas = "if(state.rankKey){try{const size=nw-24,yy=ny+(nh-size)/2;ctx.save();rounded(ctx,nx+12,yy,size,size,18);ctx.clip();await drawRankArtwork(ctx,nx+12,yy,size,size,state.rankKey);ctx.restore()}catch{drawPlaceholder(ctx,nx,ny,nw,nh)}}else if(state.nftUrl){try{const nft=await loadImage(state.nftUrl);ctx.save();rounded(ctx,nx+12,ny+12,nw-24,nh-24,18);ctx.clip();cover(ctx,nft,nx+12,ny+12,nw-24,nh-24);ctx.restore()}catch{drawPlaceholder(ctx,nx,ny,nw,nh)}}else{drawPlaceholder(ctx,nx,ny,nw,nh)}"
if old_canvas in s:
    s = s.replace(old_canvas,new_canvas,1)

p.write_text(s)
print('Rank integration polished across Mint, claim handoff, and My Seat.')
