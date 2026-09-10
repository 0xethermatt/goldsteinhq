from pathlib import Path

p=Path('welcome.html')
s=p.read_text()
branch="if(state.rankKey){try{const size=nw-24,yy=ny+(nh-size)/2;ctx.save();rounded(ctx,nx+12,yy,size,size,18);ctx.clip();await drawRankArtwork(ctx,nx+12,yy,size,size,state.rankKey);ctx.restore()}catch{drawPlaceholder(ctx,nx,ny,nw,nh)}}"
while branch+'else '+branch in s:
    s=s.replace(branch+'else '+branch,branch,1)
p.write_text(s)
print('Welcome rank renderer deduplicated.')
