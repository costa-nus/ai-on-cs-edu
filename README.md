# ai-on-cs-edu

Tracking how the post-ChatGPT period (Nov 2022 onward) has shown up in U.S. computer science education enrollment, using verified primary sources.

## What's here

```
.
├── README.md                     # this file
├── SOURCES.md                    # all source URLs and what was extracted from each
├── data/
│   └── cs-enrollment-verified.csv  # primary dataset, every cell traceable to a source
└── dashboards/
    ├── cs-enrollment-stocks-vs-flows-v4.html   # latest two-panel dashboard (recommended)
    ├── cs-enrollment-stocks-vs-flows.html      # earlier two-panel version
    └── cs-enrollment-gpt-moment-v2.html        # combined dashboard with GPT marker
```

Open any `.html` file in a browser — they are self-contained, no build step.

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

## Updating the data

When new source documents are published, add rows to `data/cs-enrollment-verified.csv` and a citation line to `SOURCES.md`. The dashboards have hardcoded numbers — update the SVG `points` attributes and table cells accordingly.

See `SOURCES.md` for which specific tables in each Taulbee report and NCES Digest page contain which numbers.

## Conversation log

This dataset and the dashboards were built collaboratively in a Claude conversation. The methodology emphasis was on traceability over completeness: every number must trace to a primary source, and missing data is marked "not extracted" rather than estimated.

## License

Source data is from CRA (Taulbee Survey, public publications) and U.S. Department of Education NCES (IPEDS, public domain). The dashboards and CSV in this repo are released under the MIT License.
