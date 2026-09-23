# Lab 1 · AI and contribution record

Members: Sebastián Ramorino, Álvaro Torres.

## AI used / not used

USED. Two tools were used across the lab, by different members for different sections:

- **Sebastián Ramorino** used Claude Sonnet 5 (Anthropic), via chat, for Sections 1–3: framing the target/audit definition (prediction moment, unit, population, target, classification-vs-completion distinction), proposing and helping select EDA questions, and drafting/debugging the pandas/matplotlib code for the data-quality checks and the first two EDA questions (grid-slot top-10 rate; qualifying position vs. grid position).
- **Álvaro Torres** used an AI assistant for Sections 4–7, to help inspect the supplied notebook structure, draft reproducible pandas/matplotlib analysis cells, and improve the wording of the audit and interpretation sections. Meaningful assistance accepted: suggestion of three train-only EDA questions; drafted code for qualifying-position bands, seasonal stability, and the missing-qualifying selection check; drafted neutral explanations of the confusion-matrix metrics and prediction-moment constraints. (Tool: ChatGPT 5.6 — see Prompts, entry 4.)

## Own decision

- **Sebastián:** Selected which 2 of the 6 proposed EDA questions to pursue first (grid-slot top10 rate; qualifying vs. grid), based on which gave the clearest interpretable chart with the least additional feature engineering. Verified the target definition (`target_top10` from numeric `position`, not `position_text` or `status`) against the actual column contents before accepting it.
- **Álvaro:** Decided to use the missing-qualifying records as an explicit selection-trap EDA question rather than dropping them, because the brief defines the population from race results and requires a left join with a fixed majority fallback.

## Verification, observed result and limitation

**Sebastián (Sections 1–3):** Ran every AI-suggested cell against the actual `train`/`qualifying`/`results` DataFrames rather than trusting the code by inspection — confirmed the duplicate-key check returned 0 unexpected duplicates, confirmed the anti-join counts matched the missing-qualifying counts shown in the notebook (2/0/1 rows by season), and confirmed the `is_numeric_text` check flagged the expected letter codes (`R`, `W`, `D`, etc.) with no unexpected numeric-nulls. Cleaned up the AI-generated code for redundant intermediate variables before merging with Álvaro's sections (shared `grid_bucket` labeling, consistent target column naming). Limitation: the AI-drafted checks and questions rely on the 2019–2021 dataset as given, so conclusions inherit the source limitations documented in Section 1 (missing qualifying rows, pre-2022 regulation era, no weather/reliability data) — the AI did not independently verify these against the source, they were reasoned from the data itself.

**Álvaro (Sections 4–7):** The generated calculations were checked directly against the supplied CSV snapshots and the provided `lab01_support_v1.py` functions. Observed training counts were independently checked: 1,200 result rows, 1,197 qualifying rows, 3 unmatched result keys, and a 50.0% target rate. Calibration metrics were independently executed before the test set was opened. The missing-qualifying analysis was retained because the data showed an inner join would remove 3 result rows, including one top-ten outcome. AI output was not treated as evidence for data claims; the notebook's observed values are the evidence. Result: the training audit found 3/1,200 (0.25%) result rows without a qualifying match, with target values 1, 0 and 0 — so an inner join would change the evaluated population, and the fixed fallback was retained. Limitation: the missing subgroup is very small, so its observed target rate is not stable evidence by itself.

## Contributions

| Member | Contribution and evidence reference |
|---|---|
| Sebastián Ramorino | Sections 1–3: target/audit definition, initial data-quality checks (duplicate keys, qualifying-only/results-only anti-joins, missing values, coverage), EDA question proposal (6 candidates), and first 2 EDA questions coded and debugged (grid-slot top10 rate; qualifying position vs. grid position, including the categorical dtype bugfix). Prompts referenced below (entries 1–3). |
| Álvaro Torres | Sections 4–7: EDA Question 3 (constructor effect / qualifying-position bands and seasonal stability), missing-qualifying / selection-trap analysis, temporal-split and test-period discipline, baseline evaluation, interpretation, AI-use documentation, and reproducibility documentation. Prompt referenced below (entry 4). |

## Prompts used

**Sebastián Ramorino**

### 1.
- Tool: Claude Sonnet 5 Medium
- Purpose: Initial exploration of the database along with proposal of possible EDA questions given the context.
- Meaningful assistance: Cleared up the prediction moment and unit of observation. The rest is mostly stuff already known from reading the problem and looking at the data. The EDA ideas were helpful; ended up going with the first three EDA prompts.

### 2.
- Tool: Claude Sonnet 5 Medium
- Purpose: Programming the necessary checks for question number 1.
- Meaningful assistance: Provided code that had to be cleaned up to create the relevant checks without much extra clutter.

### 3.
- Tool: Claude Sonnet 5 Medium
- Purpose: Programming EDA.
- Meaningful assistance: Provided data exploration and graphs.

**Álvaro Torres**

### 4.
- Tool: ChatGPT 5.6
- Purpose: Programming remaining EDA, baselines, freeze and final conclusion.
- Meaningful assistance: Suggested three train-only EDA questions; drafted code for qualifying-position bands, seasonal stability, and the missing-qualifying selection check; drafted neutral explanations of the confusion-matrix metrics and prediction-moment constraints. All outputs were reinterpreted and verified by the group (see Verification above) to make sense in context — observed values from the notebook, not AI output, were treated as evidence for data claims.