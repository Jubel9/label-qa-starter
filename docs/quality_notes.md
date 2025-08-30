# Quality notes
- κ on 800 items (two independent passes): 0.967 — most disagreements ham↔unclear.
- Spam stayed clean due to strong prize/CTA/shortcode/pricing cues.
- To reduce ham↔unclear, add explicit guidance for short replies beyond “ok/thanks” and define signs of truncation (“…”) vs. stylistic ellipses.

# Edge-cases
    1. Some messages have “…” in the middle, which causes confusion; this might be due to truncation or because the original message actually contains ellipses.
    2. Some advertising messages are convincing enough to be overlooked as `ham`; if not read carefully, they may be mistakenly labeled as `ham`.
    3. Some messages are not identifiable as correct English, probably because they were sent long ago and use slang, causing misunderstanding of the meaning of the words.
    4. Some messages contains phone numbers or website link, if not read carefully might be mistaken as `spam`.
    5. Some personal texts using full uppercase letter, a typical `spam` advertising message and might be mistaken as one if not read carefully.
    6. Some numbers might be censored as `&lt;DECIMAL&gt` or `&lt;#&gt` which are confusing if not really understand the context.