# RUBRIC — SMS classification (`ham` / `spam` / `unclear`)

## Definitions
- **ham**: Personal, conversational, or informational message with no solicitation. Includes short acknowledgements like “k” or “ok thanks”.
- **spam**: Unsolicited promotions, prizes/lotteries, premium-rate numbers/shortcodes, aggressive CTAs (“CALL NOW”, “Text XYZ to 8xxxx”), claim codes, pricing/validity windows, or generic sender copy.
- **unclear**: Too elliptical/truncated or uses non-standard/unknown language such that intent isn’t identifiable with confidence.

## Decision rules (apply in order)
1) **Promo/Prize/CTA signals ⇒ _spam_**  
   If the message pushes offers/upgrades or instructs to call/text a code/shortcode—especially with **pricing**, **claim codes**, **validity windows**, **URLs**, **opt-out** language—label **spam**.  
   _Indicators:_ “WINNER!!… claim code… valid 12 hours”, “Text CSH11 to 87575”, “Call 0800…”, “Cost 150p/day”, “STOP to opt out”.

2) **Personal conversational content ⇒ _ham_**  
   Everyday chat, plans, thanks, emotions, or direct replies with non-promotional intent → **ham**.  
   _Includes:_ very short acknowledgements like **“k”**, **“ok thanks”**.

3) **Insufficient/unknown content ⇒ _unclear_**  
   If the message appears truncated (e.g., multiple “…” mid-sentence) or uses slang/phrasing we cannot confidently interpret → **unclear** (unless Rule 1 clearly applies).

### Tie-breakers
- “Free” meaning **available** (“are you free now?”) → **ham**.  
- Personal “call me” with normal number & context → **ham**.  
- Messages with URLs: if obviously promotional/generic → **spam**; if clearly part of a personal convo (“here’s the doc we discussed”) → **ham**.

## Edge cases (dataset-driven)
- Ellipses **“…”** mid-text can indicate truncation; if intent unclear → **unclear**.  
- Convincing advertising can read like normal info → double-check for **CTA/shortcodes/pricing/claim codes**; if present → **spam**.
- Non-standard English / older slang (meaning uncertain) → **unclear**.

## Label set
`{ham, spam, unclear}`
