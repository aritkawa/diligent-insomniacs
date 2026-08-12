# Evidence 3: Before → After — AI-involved spots, before and after

> Every row has a primary record in `_progress.md` (the daily working log). Dates are the record dates.

| # | Target | Before | After | Primary record |
|---|---|---|---|---|
| 1 | Theme selection | 3 candidates (income × happiness / marriage × fertility / sleep × work) | 2 killed by data validation; concentrated on the single outlier — Japan's "twist" (Evidence 1, Figures 1–4) | 07-08–09 |
| 2 | Core fact | First draft: "women sleep less than men in 5 of 33 countries" | Re-validated and **corrected to 7 of 33**. At the same time, discovered "Japanese men's 40 min of unpaid work = lowest in the world" and promoted it to the core framing of Act 3 | 07-09 |
| 3 | Curbing exaggeration | "Japan also has the worst gender sleep gap in the world" (catchy but wrong) | Found the largest gap is India at −14 min → corrected to "men too sleep the least, and women sleep 12 min less even than those men" | 07-09 |
| 4 | UX | 6 scroll screens, 2 ranking charts | Human feedback "too long" → compressed to 4 screens, merged into one chart with a toggle + FLIP animation | 07-09 |
| 5 | ILO data | Manually shaped CSV, 26 countries (**UK missing**, undetected) | Scripted the extraction (`extract_ilo_49h.py`): 591 rows / 27 countries, missing data structurally prevented; synced down to the country-count wording | 07-16 |
| 6 | Rejecting an expansion | Happiness × unpaid-work gap r=−0.74 (promising) | A stricter re-spike with exact survey-year matching **decayed it to r=−0.55** → not adopted (Evidence 1, Figure 3) | 07-16 |
| 7 | Security | LLM answer inserted directly via `innerHTML` (a self-XSS seedling) | Escaped with `esc()` + confirmed neutralized by a malicious-payload injection test × 4 files | 07-12 |
| 8 | Bug fix | The note timeline shook the screen on hover (a reflow loop) | Root-caused (caption swap → height change → scroll anchoring) → moved into fixed-size text inside the SVG, zeroing out the layout shift itself | 07-12 |
| 9 | Citations | LLM-sourced academic citations (fabrication risk) | Cross-checked DOI, volume, and PMID against PubMed itself. For "light," which could not be verified, no specific paper is cited in the body | 07-16 |
| 10 | Accessibility (a11y) | SVG charts were hover-only (no keyboard / screen reader) | Implemented tabindex + role + aria-label + focus/keydown in 8 places; headless 30 checks PASS | 07-16 |
| 11 | Maintainability | Double-managing 4 files, including standalone versions | Consolidated to a single source (index_ja / index + data.js) + inline expansion at delivery time | 07-16 |
