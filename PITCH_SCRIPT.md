# Chargeback Shield — 5-Minute Pitch Script

**Track:** Razorpay AI Buildathon 2026 — Track 02, AI Risk Manager
**Total runtime target:** 5:00
**Format:** Screen recording (dashboard walkthrough) with voiceover. Cues in *[brackets]* are on-screen direction, not spoken.

---

## 0:00–0:30 — Cold open: the problem

*[Screen: title card "Chargeback Shield" fades in over a static graphic — a card swipe, then a red "DISPUTED" stamp]*

"A merchant doesn't lose a sale to fraud at checkout. Most of the time, they lose it two weeks later — when a customer disputes the charge, and the merchant has ten days to prove it was legitimate or eat the loss. That's a chargeback. And most merchants either fight blind, or don't fight at all.

Track 02 asks for a fraud detection or automated-response system for one class of loss. We picked that one — the chargeback and dispute lifecycle — on purpose."

## 0:30–1:10 — Why this loss class, not generic fraud

*[Screen: ARCHITECTURE.md diagram — the two-stage Predict → Respond flow]*

"Pre-authorization transaction fraud scoring is already a crowded lane in this buildathon — we checked the public repos before committing. So instead of scoring 'is this transaction fraudulent right now,' Chargeback Shield does two things nobody else in this track was doing together: it predicts which transactions are at elevated risk of a *future* dispute, before one is even filed — so a merchant can send a confirmation email or hold settlement for a few days, cheaply. And when a dispute *is* filed, it automatically assembles exactly the evidence that transaction's reason code requires, and recommends fight, concede, or review — under a fixed, auditable policy."

## 1:10–2:40 — Live demo

*[Screen: dashboard at localhost, walk through top to bottom]*

"Here's the live dashboard. [Point to hero/KPI tiles] These are the model's held-out test metrics, regenerated fresh every run — not hand-picked. At our chosen operating threshold, the model catches 31.8% of disputes at 40% precision. [Point to baseline row] We report that next to the naive one-line rule — 'flag digital goods with no delivery confirmation' — which only gets 27.6% recall at 29.7% precision. So the model is a real improvement over the obvious guess, not just a black box we're asking you to trust.

[Point to tradeoff table] And here's the full precision/recall curve, not one cherry-picked number — because a 40% precision floor was a *business* choice: the action on a flagged transaction is a cheap email, not a decline, so it's worth trading precision for recall. A stricter threshold is one line away if the action ever gets more expensive.

[Score a sample transaction] Let's score a transaction live. [Click 'Score'] It comes back with a risk band, and — this is new this week — the top three factors that actually moved *this* prediction, in plain English, computed by swapping each feature for its typical value and measuring the shift. No black box.

[Switch to evidence packet demo] Now say this transaction gets disputed. [Click 'Generate packet'] The evidence engine pulls exactly what that reason code needs, scores how complete the packet is, and recommends fight, concede, or review. Notice there's no LLM anywhere in that decision — it's a fixed policy over real evidence completeness. The only place we *optionally* use an LLM is drafting the human-readable narrative paragraph at the bottom — never the decision itself, and if that call fails for any reason, the packet still works with every field filled, just without the paragraph.

[Click an audit ID] Every one of those decisions — score or packet — is written to an append-only audit log the moment it happens. You can pull any past decision back up by ID."

## 2:40–3:20 — Why we trust our own numbers

*[Screen: model_card.md scrolling]*

"Everything you just saw is trained on 100% synthetic data — we say that everywhere, starting with the README, because we're not going to pretend a few hours of buildathon time produced real cardholder patterns. What we can stand behind is the *methodology*: a held-out test set that never touched hyperparameter tuning, a documented reason for every correlate we built into the synthetic data, and — when we improved recall this week — a model card section that's honest about *why* it improved: mostly a business threshold decision and a bigger dataset, not a smarter model dressed up as one. We'd rather show you the real breakdown than round up."

## 3:20–4:10 — Engineering rigor

*[Screen: GitHub repo — Actions tab with green checks, then test file list]*

"Under the hood: 19 tests covering the evidence engine, the audit log, the model, the API, and the optional narrative layer, running in CI on every push. The evidence engine never fabricates evidence — if a document isn't in the store, the packet says so and the completeness score reflects it. The audit trail is append-only JSONL, so nothing about a past decision can be quietly edited. And the whole thing is one FastAPI service with a dependency-free dashboard — no build step, no external UI framework, so it runs the same way in a live demo as it does in your terminal."

## 4:10–4:45 — What's next

*[Screen: README "known limitations" section]*

"We're upfront about the gaps too: synthetic data can't capture real adversarial adaptation, and the model only sees pre-dispute signal — it doesn't yet know how a merchant's past dispute *rate* compares to their peers, which is the natural next feature. That's the first thing we'd build with real data."

## 4:45–5:00 — Close

*[Screen: title card again, GitHub URL on screen]*

"Chargeback Shield: predict the dispute before it happens, and respond to it honestly when it does — with a policy you can audit, not a model you have to trust. Thanks."

---

**Word count (spoken lines only): ~830 words → ~5:00 at a measured pace (~165 wpm), before demo-click pauses.**

**Recording checklist:**
- [ ] Start the local server (`uvicorn src.api:app --reload`) and pre-load one sample dispute before recording, so the packet demo doesn't stall on a slow synthetic lookup.
- [ ] Rerun `python -m scripts.train` right before recording so the numbers on screen match the numbers spoken.
- [ ] Zoom the browser to ~110% so dashboard text is legible in a screen recording.
- [ ] Practice the 1:10–2:40 demo block separately — it's the longest and most click-dependent segment.
- [ ] Have a fallback: if a live dispute-packet lookup is ever slow, cut to a pre-generated one rather than let dead air run.
