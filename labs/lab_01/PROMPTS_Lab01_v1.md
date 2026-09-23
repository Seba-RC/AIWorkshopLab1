# Lab 1 · AI and contribution record

Members: Sebastian Ramorino, Alvaro Torres.

AI used / not used: USED. If used, identify tool, purpose, meaningful assistance, what you accepted/changed and why. Reference relevant prompts or exchanges; no quota is required.

Own decision: TO COMPLETE.
Verification, observed result and limitation (notebook reference allowed): TO COMPLETE.

| Member | Contribution and evidence reference |
|---|---|
| TO COMPLETE | TO COMPLETE |
| TO COMPLETE | TO COMPLETE |

Prompts used:
Sebastian Ramorino
# 1. 
- Tool:Claude Sonnet 5 Medium
- Purpose: Initial exploration of the database along with proposal of possible EDA questions given the context.
- Meaningful assistance: Cleared up the prediction moment and unit of observation. The rest is mostly stuff I already knew from reading the problem and looking at the data.
Apart from this, the ideas for EDA were helpful. I ended up going with the first three EDA prompts.

## PROMPT:
"This is a small database of F1 races along with a lot of relevant data about them going from 2019 to 2021. 
After qualifying and before the Grand Prix, can we anticipate whether a driver will be classified in the final top ten? Use one driver in one race as the observation. For this lab, target = 1 when the source's numeric final race position is 1–10, and 0 otherwise. This is final classification, not necessarily completing the race, receiving points or winning a constructor contest.

For this purpose, state the prediction moment, the unit, the population and the target. Distinguish final classification from completing a race. Explain the source limitations. 

After this, propose a couple (6) EDA questions. Do not code anything yet; however, keep in mind that these questions must present the possibility to add an INTERPRETABLE table/graph."

Claude:
## 1. Prediction moment, unit, population, target

**Prediction moment:** Right after qualifying is finalized and the starting grid is set — i.e., after Q1/Q2/Q3 results are known but before lights out. At this point you have access to grid slot, qualifying position/time, driver, constructor, circuit, season/round — but nothing that happens *during* the race (laps completed, status, points).

**Unit of observation:** One driver in one Grand Prix (a driver–race pair). Each row in the `train` table is one such observation.

**Population:** All driver–race pairs across the 2019–2021 seasons for which a qualifying record exists (i.e., the driver actually took part in qualifying and got a grid slot). Rows with missing qualifying data are technically part of the population of races but can't be used as pre-race-informed observations unless you impute.

**Target:** Binary. `target_top10 = 1` if the driver's final numeric classified position is between 1 and 10 inclusive; `0` otherwise (includes retirements, DNFs, DSQs, and anyone classified 11th or lower). This must be read from the **numeric position field**, not from `position_text` or `status`, since those contain non-numeric codes (`R`, `W`, `D`, etc.) that need to be mapped to 0.

**Classification vs. completing the race — important distinction:**
- *Completing the race* (status = "Finished") means the driver crossed the line under power having run the full race distance/laps.
- *Final classification* is an FIA determination: a driver can be **classified without finishing** (e.g., retires with mechanical failure late in the race but has completed ≥90% of the winner's race distance — common statuses like "Gearbox," "Brakes," "Accident" can still carry a numeric position), and conversely a driver who **does finish** all laps can still be classified outside the top 10, or even unclassified if they fell too far behind.
- So "top 10 finish" ≠ "top 10 classification." The target here is strictly about the numeric classified position, independent of whether `status` says "Finished" or something else.

**Source limitations:**
- Missing qualifying data: 2 rows in 2019, 0 in 2020, 1 in 2021 — these drivers have no pre-race grid/quali features, so they either need to be dropped or carefully imputed (and dropping isn't fully "missing at random," since a missing quali time often means a crash, mechanical issue in Q, or a driver who didn't set a time and started from the back/pit lane — this could bias the label distribution if excluded).
- `grid` vs `qualifying_position` can diverge (grid penalties for gearbox changes, causing yellow flags, impeding, etc.), so grid is the more faithful "pre-race" feature — qualifying position tells you raw pace, grid tells you where they actually start.
- Only 3 seasons (2019–2021) covered, and all under the pre-2022 aerodynamic regulations — any model trained here won't generalize to the current car generation or new tracks.
- No weather, tire allocation, penalty, or reliability/track-status data — all known drivers of race-day variance that aren't captured, which caps how predictable the outcome can be from quali alone.
- `position_text` mixes numeric strings with letter codes, so type coercion needs to be handled carefully before deriving the target (silent NaNs from a naive `.astype(int)` are an easy bug here).
- Small season-level sample sizes (~340–440 rows/season) limit how finely you can slice by circuit or constructor without running into sparse cells.

## 2. Proposed EDA questions (pre-race features only, each interpretable as a table or chart)

1. **Grid position → top-10 rate.** What is the empirical probability of a top-10 classification for each starting grid slot (or grid buckets like 1–3 / 4–6 / 7–10 / 11+)? → bar chart or table of top10 rate by grid bucket.
2. **Qualifying position vs. grid position.** Do the two diverge often enough to matter (grid penalties), and does using one vs. the other change how strongly it predicts top10? → table comparing top10 rate curves for `qualifying_position` vs `grid`.
3. **Constructor strength.** Do certain constructors show a consistently higher top10 rate even after controlling for grid position (i.e., is there a "car effect" beyond starting slot)? → grouped bar/table of top10 rate by constructor, optionally split by grid bucket.
4. **Circuit effect on overtaking.** Does the grid→top10 relationship vary by circuit (e.g., Monaco vs. a high-overtake track like Bahrain)? → heatmap or small-multiple table of top10 rate by circuit × grid bucket.
5. **Season trend.** Did the predictive strength of grid/quali position on top10 shift from 2019 to 2021 (possible rule or competitive-balance changes)? → line/table of top10 rate by grid bucket, one line per season.
6. **Upsets / position swings.** Among the drivers who did achieve a top-10 classification, how far did they move from their grid slot to their final position (front-runners holding station vs. midfield drivers gaining places)? → histogram or summary table of (grid − final position) for the top10 = 1 subset.

# 2. 
- Tool: Claude Sonnet 5 Medium
- Purpose: Programming the necessary checks for question number 1
- Meaningful assistance: Provided code that I had to clean up to create the relevant checks without much extra clutter.
## PROMPT

"Could you code checks for duplicate keys, qualifying-only records, missing values and coverage?"

(Code in the runbook.)