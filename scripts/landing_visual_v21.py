from pathlib import Path
import re

for path in (Path('index.html'), Path('landing.html')):
    text = path.read_text()

    # Move the visual roster after the product section so the story flows:
    # product first, people second, mechanics third, network fourth.
    roster_match = re.search(r'<section class="section firmRoster" id="firm-roster">.*?</section>\n\n', text, re.S)
    if not roster_match:
        raise RuntimeError(f'Roster section not found in {path}')
    roster = roster_match.group(0).rstrip()
    text = text[:roster_match.start()] + text[roster_match.end():]
    seats_marker = '<section class="section model" id="seats">'
    if seats_marker not in text:
        raise RuntimeError(f'Seats section not found in {path}')
    text = text.replace(seats_marker, roster + '\n\n' + seats_marker, 1)

    text = text.replace(
        '<div class="eyebrow">Inside the firm</div>',
        '<div class="eyebrow">02 / People</div>',
        1,
    )
    text = text.replace(
        '<div class="eyebrow">02 / Operating model</div>',
        '<div class="eyebrow">03 / Operating model</div>',
        1,
    )
    text = text.replace(
        '<div class="eyebrow">03 / Network</div>',
        '<div class="eyebrow">04 / Network</div>',
        1,
    )

    text = text.replace(
        'G-Funds are agent-managed tokenized index products designed to turn market theses into transparent, programmable portfolios. Each fund turns a market thesis into a transparent, programmable product. Goldstein HQ is where investors and Seat holders move from the story into the market.',
        'G-Funds turn market theses into transparent, programmable portfolios. House managers operate the mandates; Goldstein HQ is where investors and Seat holders move from the story into the market.',
    )
    text = text.replace(
        'House managers connect individual Seats to live product mandates.',
        'House managers connect individual Seats to Goldstein product mandates.',
    )
    text = text.replace('House manager NFT</small>', 'House fund manager</small>')

    path.write_text(text)

print('Landing narrative polish v2.1 applied')
