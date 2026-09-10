from pathlib import Path

p=Path('funds.html')
s=p.read_text()
s=s.replace('Magnificent Seven AI equity index.','AI infrastructure and frontier-technology index.')
s=s.replace('<span class="holding mono">AAPL</span><span class="holding mono">MSFT</span><span class="holding mono">GOOGL</span><span class="holding mono">AMZN</span><span class="holding mono">NVDA</span><span class="holding mono">META</span><span class="holding mono">TSLA</span>','<span class="holding mono">NVDA</span><span class="holding mono">TSLA</span><span class="holding mono">MU</span><span class="holding mono">GOOGL</span><span class="holding mono">SPCX</span>')
s=s.replace('<h3>Meme Stock Fund</h3><p class="fundDesc">High-beta, attention-driven equities.</p>','<h3>Meme Index</h3><p class="fundDesc">Agent-managed internet-native and meme-market exposure.</p>')
s=s.replace('<div class="holdingsLabel mono">Strategy</div><div class="chips"><span class="holding mono">HIGH BETA</span><span class="holding mono">MEME EQUITIES</span><span class="holding mono">TACTICAL</span><span class="holding mono">AGENT MANAGED</span></div>','<div class="holdingsLabel mono">Index</div><div class="chips"><span class="holding mono">AI</span><span class="holding mono">BONER</span><span class="holding mono">MOO</span><span class="holding mono">OPTIMUS</span><span class="holding mono">MEME</span></div>')
p.write_text(s)

p=Path('fund-detail.html')
s=p.read_text()
s=s.replace("{name:'Goldstein Meme Stock Fund',ticker:'gMEMESTONK',desc:'High-beta mandate',risk:5,label:'High',basket:'Strategy',chips:['HIGH BETA','MEME EQUITIES','TACTICAL','AGENT MANAGED']}","{name:'Meme Index',ticker:'gMEMESTONK',desc:'Internet-native and meme-market index mandate',risk:5,label:'High',basket:'Constituents',chips:['AI','BONER','MOO','OPTIMUS','MEME']}")
s=s.replace("{name:'Goldstein AI Index',ticker:'gAIX',desc:'AI Index mandate',risk:3,label:'Growth',basket:'Constituents',chips:['AAPL','MSFT','GOOGL','AMZN','NVDA','META','TSLA']}","{name:'Goldstein AI Index',ticker:'gAIX',desc:'AI infrastructure and frontier-technology mandate',risk:3,label:'Growth',basket:'Constituents',chips:['NVDA','TSLA','MU','GOOGL','SPCX']}")
p.write_text(s)
