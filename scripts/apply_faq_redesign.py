from pathlib import Path

p = Path('index.html')
html = p.read_text()

old = '''<section class="faqSection" id="learn" aria-labelledby="faqTitle">
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

new = '''<section class="faqSection" id="learn" aria-labelledby="faqTitle">
  <div class="faqLayout">
    <div class="faqIntro">
      <div class="faqEyebrow mono">FAQ</div>
      <h2 id="faqTitle">Before you take a seat.</h2>
      <p>The essentials on claiming, Seat utility, rerolls and The Floor.</p>
    </div>
    <div class="faqList" id="faqList">
      <details>
        <summary>What happens after I claim a Seat?</summary>
        <div class="faqAnswer">Once the claim confirms, your Seat is <strong>secured to your connected wallet</strong> and becomes your persistent identity and access point inside Goldstein. From there, you enter the firm as an active Seat holder.</div>
      </details>
      <details>
        <summary>What does a Goldstein Seat unlock?</summary>
        <div class="faqAnswer">A Seat is your access point into Goldstein. It unlocks access to <strong>G-Funds</strong> and the ability to launch your own agent-managed fund. Rank, capacity and additional economics are earned through participation.</div>
      </details>
      <details>
        <summary>How do rerolls work?</summary>
        <div class="faqAnswer">Rerolls are paid in <strong>$GLDSTN</strong>. The cost doubles after each reroll, and you can keep going until you find the Seat you want to claim.<br><span class="costPath mono">100 → 200 → 400 → 800 → … $GLDSTN</span></div>
      </details>
      <details>
        <summary>What is The Floor?</summary>
        <div class="faqAnswer">The Floor is the <strong>available Seat universe</strong>. It shows what has already been claimed and what is still in the pool, so you can make a better reroll decision.</div>
      </details>
    </div>
  </div>
</section>'''

if old not in html:
    raise SystemExit('current FAQ block not found')

html = html.replace(old, new, 1)

required = [
    'First draw is free',
    'Claim · 0.025 ETH',
    'Reroll · 100 $GLDSTN',
    'Available seat universe',
    'Before you take a seat.',
    'What happens after I claim a Seat?',
    'What does a Goldstein Seat unlock?',
    'How do rerolls work?',
    'What is The Floor?'
]
for marker in required:
    if marker not in html:
        raise SystemExit(f'missing required marker: {marker}')

for removed in ['How does the free reveal work?', 'What happens after I reveal a Seat?', 'Are some characters more powerful than others?']:
    if removed in html:
        raise SystemExit(f'old FAQ still present: {removed}')

faq = html.split('<div class="faqList" id="faqList">', 1)[1].split('</div>\n  </div>\n</section>', 1)[0]
if faq.count('<details>') != 4:
    raise SystemExit('FAQ must contain exactly four questions')

p.write_text(html)
print('FAQ trimmed to four high-value questions')
