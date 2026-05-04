# ai-on-cs-edu

Tracking how the post-ChatGPT period (Nov 2022 onward) has shown up in U.S. computer science education enrollment, using verified primary sources.

## What's here

```
.
├── README.md                     # this file
├── SOURCES.md                    # all source URLs and what was extracted from each
├── index.html                    # two-panel stocks-vs-flows dashboard (self-contained)
├── .nojekyll                     # disables Jekyll on GitHub Pages
└── data/
    └── cs-enrollment-verified.csv  # primary dataset, every cell traceable to a source
```

Open `index.html` in a browser — it is self-contained, no build step. The repo is also deployable as-is to GitHub Pages (settings → Pages → deploy from `main` branch, root).

## What the data shows

Across U.S. CS programs covered by the CRA Taulbee Survey, AY 2019-20 through AY 2023-24:

- **Bachelor's enrollment** grew steadily from 150,331 to 182,973 (+22% over four years). The 16th consecutive year of growth.
- **New PhD enrollment** dipped during COVID, then jumped from 3,041 to 3,438 in AY 2023-24 — the first full academic year that began after ChatGPT. That's a +13.1% one-year rise, the steepest in this five-year window.
- **AI/ML's share of new PhD specialties** rose from 25.2% (2021-22) to 28.4% (2022-23), per Taulbee Table D4.
- **CS master's degrees conferred** (broader NCES IPEDS scope) were essentially flat 2019-22, then per the Encoura/Eduventures analysis nearly doubled in 2023 driven by international students returning post-COVID.

The chart series are indexed to AY 2019-20 = 100 because absolute scales differ by an order of magnitude (bachelor's ~150K, master's ~50K, PhD ~16K).

## Important caveats

1. **Scope mismatch on master's data.** Bachelor's and PhD numbers come from the CRA Taulbee Survey (~144 U.S. CS-PhD-granting departments). Master's numbers come from NCES IPEDS, covering all U.S. institutions in the broader "Computer and Information Sciences" category. Year-over-year changes within each series are meaningful; the level differences between master's and the others on the same axis are not directly comparable.

2. **Stocks vs flows.** Total enrollment is a stock; new enrollment and degrees conferred are flows. They respond on different timescales. The dashboard splits them into two panels for this reason.

3. **AY 2023-24 master's data is missing** from the published NCES Digest as of the data collection date for this repo. The Encoura analysis [S7] reports approximate CIP 11.0701 (CS specifically) conferrals of ~22,000 in 2023, roughly double 2022, but this is commentary on provisional IPEDS data and uses a narrower CIP code than the main IPEDS series.

4. **AY 2024-25 data does not yet exist.** The CRA Taulbee Survey covering it is expected ~May 2026.

## Methodology — one source, two metrics (national panels)

All values in the national panels come from the **CRA Taulbee Survey, Table 1**. Scope: U.S. CS-PhD-granting departments only (~144 reporting institutions). The Survey distinguishes _total Fall enrollment_ (a stock — who is currently in the program) from _new students that year_ (a flow — who entered). The two are kept on separate panels and never combined.

## Per-university view

A second view in the dashboard shows a single school at a time. Same indexing idea as the national figures, but at school level.

- **Metric.** Total Fall enrollment headcount only — _not_ degrees conferred and _not_ first-time enrollment. Mixing metrics on a shared indexed y-axis would be misleading (degrees lag enrollment by 2–6 years).
- **Indexing.** Each school's earliest available year is set to 100; later years are scaled relative to that. The y-axis auto-fits per school so high-growth lines (e.g. Georgia Tech master's, dominated by OMSCS scaling) don't clip.
- **Source rule.** Every value comes from the university's _own_ institutional-research / college / department page — no third-party aggregators (no CollegeFactual, US News, Petersons). NCES IPEDS is acceptable only as a documented fallback because it's the institution's own federally-mandated reporting.
- **Pipeline.** `data/university-cs-enrollment.csv` is the source of truth; `scripts/fetch_university_data.py` rebuilds it from the official sources and re-emits the JS payload (`data/university-cs-enrollment.js`) that the dashboard loads. Run with `--verify` to print every value with its source URL.

### Schools currently included

| School | Source | Scope |
| --- | --- | --- |
| Carnegie Mellon | IRA School-of-Computer-Science PDFs | Whole SCS (CS, AI, ML, HCI, Robotics, Computational Biology, Software Research, Language Technologies) |
| Georgia Tech | College of Computing fact book | **Whole College of Computing**, including OMSCS — master's growth is dominated by OMSCS scaling, not residential demand |
| Michigan State | CSE Department enrollment page | CS B.S. major in the College of Engineering — Fall 4th-week census headcount |
| Stony Brook | IRPE annual factbook XLSX | CS major in the College of Engineering & Applied Sciences — Fall headcount of declared CS plan; excludes the separate Computer Engineering major and "Area of Interest - CS" UG admit status |
| UMass Amherst | UAIR factbook "Students by Major" PDFs | CS major headcount |
| UW–Madison | DAPIR "Trends in Student Enrollments" Tableau viz | Computer Sciences major in the College of Letters & Science; MS + PhD slightly overlap (6–21 students/year) due to MS-en-route-to-PhD students |

Different universities report at different scopes — **do not assume cross-university comparability**. The dashboard surfaces each school's scope text in a red-bordered metadata box below the chart.

### Schools checked and excluded

These schools were checked but **excluded** because their public sources do not publish per-CS-major enrollment in a stable, parseable form (most institutional-research offices publish degrees conferred — federally required for IPEDS — but not enrollment):

> Stanford, U Washington, U Michigan, UIUC, UMD, UC Berkeley, Purdue, UCSD, UC Irvine, Penn State, Princeton, Cornell, Penn, NC State (post-2020), USC, Ohio State, Texas A&M, Virginia Tech, U Minnesota–Twin Cities, UNC Chapel Hill, U Pittsburgh, Notre Dame, Rice, Indiana University Bloomington, Iowa State

Adding any of them requires finding a different primary source. See `SOURCES.md` for the dead-ends already explored. Better an honest gap than a metric substitution.

## Updating the data

When new source documents are published, add rows to `data/cs-enrollment-verified.csv` and a citation line to `SOURCES.md`. The dashboard has hardcoded numbers — update the SVG `points` attributes and table cells in `index.html` accordingly.

See `SOURCES.md` for which specific tables in each Taulbee report and NCES Digest page contain which numbers.

## Conversation log

This dataset and the dashboard were built collaboratively in a Claude conversation. The methodology emphasis was on traceability over completeness: every number must trace to a primary source, and missing data is marked "not extracted" rather than estimated.

## License

Source data is from CRA (Taulbee Survey, public publications) and U.S. Department of Education NCES (IPEDS, public domain). The dashboard and CSV in this repo are released under the MIT License.
