# Sources

All numbers in `data/cs-enrollment-verified.csv` are traceable to the documents below.
Each row in the CSV has a `source_id` column that references a source ID here.

## CRA Taulbee Survey (annual, US CS PhD-granting departments)

The Taulbee Survey reports two periods per annual report:
- **Enrollment and degrees awarded** are for the *previous* academic year
- **New students** are for the *current* academic year

So the 2020 Taulbee Survey report (released ~May 2021) covers AY 2019-20 enrollment/degrees
and AY 2020-21 new students. This is why each year of data can usually be cross-checked
against two consecutive Taulbee reports.

### [S1] 2020 CRA Taulbee Survey — 50th annual
- URL: https://cra.org/wp-content/uploads/2021/05/2020-CRA-Taulbee-Survey.pdf
- Released: May 2021
- Authors: Stuart Zweben, Betsy Bizot
- Covers: AY 2019-20 enrollment/degrees, AY 2020-21 new students
- Used for: Bachelor's & PhD totals, new students, and degrees for 2019-20

### [S2] 2021 CRA Taulbee Survey — 51st annual
- URL: https://cra.org/wp-content/uploads/2022/05/2021-Taulbee-Survey.pdf
- Released: May 2022
- Covers: AY 2020-21 enrollment/degrees, AY 2021-22 new students

### [S3] 2022 CRA Taulbee Survey — 52nd annual
- URL: https://cra.org/crn/wp-content/uploads/sites/7/2023/05/2022-Taulbee-Survey-Final.pdf
- Released: May 2023
- Covers: AY 2021-22 enrollment/degrees, AY 2022-23 new students
- Also used for: Table D4 PhD specialty data (AI/ML count for 2021-22)

### [S4] 2023 CRA Taulbee Survey — 53rd annual
- URL: https://cra.org/wp-content/uploads/2024/05/2023-CRA-Taulbee-Survey-Report.pdf
- Released: May 2024
- Covers: AY 2022-23 enrollment/degrees, AY 2023-24 new students
- Also used for: Table D4 PhD specialty data (AI/ML count for 2022-23)

### [S5] 2024 CRA Taulbee Survey — 54th annual
- URL: https://datavisualization.cra.org/TaulbeeSurvey/CRA_Taulbee_Survey_Report_2024.html
- Released: June 2025 (HTML format, redesigned)
- Covers: AY 2023-24 enrollment/degrees, AY 2024-25 new students
- Authors: Katie Siek (Indiana University), Jasmine Batten (CRA)
- **Limitation:** Numbers from this HTML report were only partially extractable in the
  session that produced this dataset. The all-departments PhD degree count of 2,352
  was verified from the Sneak Peek companion article. Bachelor's and total PhD
  enrollment for AY 2023-24 were not extracted; those cells are left blank in the CSV.
- Companion: https://cra.org/crn/2025/05/a-sneak-peek-at-doctoral-and-bachelors-enrollment-and-degree-trends-from-2024-cra-taulbee-survey/

## NCES IPEDS (national, all US degree-granting institutions)

### [S6] NCES Digest of Education Statistics 2023, Table 325.35
- URL: https://nces.ed.gov/programs/digest/d23/tables/dt23_325.35.asp
- Title: "Degrees in computer and information sciences conferred by postsecondary
  institutions, by level of degree and sex of student: Academic years 1964-65
  through 2021-22"
- Scope: All U.S. degree-granting institutions, CIP series 11 ("Computer and
  Information Sciences"). This is broader than CS specifically.
- Used for: Master's degrees conferred, AY 2018-19 through AY 2021-22
- Limitation: 2022-23 data not in this Digest edition.

### [S7] Encoura/Eduventures, "How International Students Are Saving Master's Enrollment"
- URL: https://www.encoura.org/resources/wake-up-call/how-international-students-are-saving-masters-enrollment/
- Author: Clint Raine
- Published: October 15, 2024
- Source of approximate CIP 11.0701 (CS specifically) conferral counts of
  ~12,000 (2022) and ~22,000 (2023). These are not from a primary NCES table
  in this dataset; they are commentary based on IPEDS provisional data.

## Scope mismatches

Two important caveats when comparing across degree levels:

1. **Bachelor's and PhD** numbers come from CRA Taulbee, which surveys ~144 US CS
   PhD-granting departments. This is "Computer Science" specifically.

2. **Master's** numbers from NCES IPEDS (Table 325.35) cover ALL US degree-granting
   institutions, in CIP 11 = "Computer and Information Sciences" — which includes
   Computer Science, Information Sciences, IT, etc.

The two have different denominators. Year-over-year changes within each series
remain meaningful, but the absolute level shifts between master's and the others
on the same indexed axis are not directly comparable.

## Reproduction

To reproduce or update:

1. Each Taulbee PDF link above has a "Table 1" that contains BS Enrollment,
   PhD Enrollment, New PhD Enroll, BS Awarded, PhD Awarded, and New BS Majors
   for two consecutive years (current and prior).

2. NCES Table 325.35 has columns 6 (Total master's), 7 (Male), 8 (Female).

3. For PhD specialty data, see Table D4 ("Employment of New PhD Recipients By
   Specialty") in [S3] and [S4].

When CRA publishes the next Taulbee report (typically May), append rows to the CSV
with the new academic year's numbers. NCES typically publishes its updated Digest
table in late summer/fall of the year following the academic year covered.

## Per-university sources (enrollment only)

These power the per-university chart and table at the bottom of `index.html`.
Every row in `data/university-cs-enrollment.csv` carries its own `source_url`.
`scripts/fetch_university_data.py` downloads each source and writes the CSV +
`data/university-cs-enrollment.js`. Run with `--verify` to print every value
with its source URL for spot-checking.

**Scope:** total Fall enrollment headcount (a stock — students currently in
the program), not degrees conferred (a flow — graduates per year). Schools
whose institutional-research offices do not publish multi-year per-CS
enrollment in a stable parseable form are excluded; the dead-ends are
documented below so they're not re-explored.

### [U1] Georgia Tech — Institutional Research & Planning Fact Book
**OMSCS-excluded master's series — checked and unavailable as a clean primary series.**
The IRP fact book reports College-of-Computing MS as a single combined number (residential + OMSCS, with no breakout). To construct a residential-only series we would need an authoritative year-by-year OMSCS Fall headcount. Sources surveyed:
- OMSCS Annual Reports (`omscs.gatech.edu/{2024,2025}-omscs-annual-report`) publish current-Fall stats as **infographics/images** with no extractable text totals for prior Falls.
- The "Stats (as of Fall 2021)" PDF (`omscs.gatech.edu/sites/default/files/documents/2023/The Numbers-Enrollment and Demographic Stats 2021.pdf`) gives only a single year (Fall 2021 = 11,537).
- Press articles quote isolated single-year figures (e.g. cc.gatech.edu — Fall 2022 = 11,487; iblnews.org — early 2019 ≈ 8,672) but no two snapshots come from the same source under the same definition.
- The "Ten Years, Ten Trends" L@S 2024 paper by Joyner & Duncan reportedly contains a year-by-year series but is paywalled (DOI 10.1145/3657604.3662038 returns 403 unauthenticated).

Constructing residential-only MS = Total MS − OMSCS by stitching these scattered snapshots would mix definitions and violate the project's "every cell traces to one primary source; never estimate or impute" rule. Dashboard handles this by (1) tagging the GT master's line in-figure with `(incl. OMSCS)` and (2) keeping the loud OMSCS warning in the per-school SCOPE meta box. To unlock a residential-only line, find a single authoritative source that publishes a multi-year residential-MS-only or OMSCS-only Fall headcount table.


- Office: Georgia Tech IRP
- Annual fact book PDF: https://irp.gatech.edu/files/FactBook/2025_FactBook_Final.pdf
- Tables used:
  - "Undergraduate Enrollment by College, Fall Term History" (College of Computing row, 10 columns)
  - "Graduate Enrollment by College and Degree, Fall Term History" (College of Computing × {MS, PhD})
- Scope: **College of Computing — all schools/programs combined**, including CS, Cybersecurity & Privacy, Interactive Computing, and Computational Science & Engineering. The master's series **includes the Online MS in CS (OMSCS)**, launched 2014, which scaled past 10,000 students; master's growth is dominated by OMSCS and is not directly comparable to residential master's elsewhere.
- Coverage: Fall 2016 → Fall 2025 (10 years of UG, MS, PhD).
- Year mapping: column headers are calendar years naming the Fall term, e.g. "2023" = Fall 2023 = AY 2023-24.

### [U2] Michigan State University — College of Engineering, CSE Department
- Office: MSU College of Engineering, Computer Science and Engineering Department
- Page: https://engineering.msu.edu/academics/undergraduate/enrollment-data
- Scope: **Computer Science (B.S.) major** specifically — Fall 4th-week census headcount as reported to ASEE.
- Coverage: Fall 2021 → Fall 2025 (5 years, undergraduate only).

### [U4] University of Wisconsin–Madison — DAPIR public Tableau viz
- Office: UW–Madison Data, Academic Planning & Institutional Research (DAPIR)
- Workbook: "Trends in Student Enrollments" → "Degree-Major Enrollment Comparison" sheet.
- URL: https://viz.wisc.edu/#/views/TrendsinStudentEnrollments/Degree-MajorEnrollmentComparison
- Scope: **Computer Sciences major** specifically — housed in UW–Madison's College of Letters & Science (NOT the College of Engineering). Excludes the separate "Computer Engineering" and "Electrical and Computer Engineering" majors. Each value is the Fall 10th-day-of-class headcount of degree-seeking students enrolled in the Computer Sciences major.
- Coverage: Fall 2016 → Fall 2025 (10 years, **UG / MS / PhD all populated**).
- Collection method: Tableau Crosstab download via Chrome (no `urllib` path because the viz is rendered, not static). **Five** crosstab downloads were taken and saved under `data/raw/uw-madison-cs-*.csv`:
  1. Academic Level=Undergraduate                      → bachelors series
  2. Academic Level=Graduate                           → grad-combined (cross-check)
  3. Academic Level=(All)                              → all-levels total (cross-check)
  4. Academic Level=Graduate × Degree Level=Master's   → masters series
  5. Academic Level=Graduate × Degree Level=Research Doctorate → phd series
- Cross-checks (run by `collect_uw_madison()` at build time):
  - **Primary (exact):** UG + Grad-combined = Total, every year. Holds.
  - **Secondary (bounded):** 0 ≤ (MS + PhD) − Grad-combined ≤ 25. Observed range: 6–21. The MS and PhD slices come from the Degree-Level-of-Major filter and slightly overlap because UW–Madison classifies some PhD students as concurrently Master's-degree-seeking ("MS en route to PhD"). The bounded check catches future re-exports where the overlap blows up (which would signal a filter-state error).
- Caveat: the PhD series excludes "Clinical Doctorate" — none expected for CS but worth noting. Master's includes both research and capstone-track Master's students (UW–Madison does not separate them in this dashboard).

### [U3] Carnegie Mellon — Institutional Research & Analysis (IRA)
- Office: CMU Office of Institutional Research & Analysis
- Index: https://www.cmu.edu/ira/Enrollment/index.html (lists current term only)
- Annual Fall PDFs (each contains current Fall + prior Fall side-by-side):
  - Fall 2021: https://www.cmu.edu/ira/Enrollment/pdf/fall-2021-pdfs/scs-enrollment-10.28.2021.pdf
  - Fall 2022: https://www.cmu.edu/ira/Enrollment/pdf/fall-2022-pdfs/scs-enrollment_f22_2.9.2023.pdf
  - Fall 2023: https://www.cmu.edu/ira/Enrollment/pdf/fall-2023-pdfs/scs-enrollment-f23-06oct2023.pdf
  - Fall 2024: https://www.cmu.edu/ira/Enrollment/pdf/fall-2024-pdfs/scs-f24-enrollmet-08nov2024.pdf
- Title (each PDF): "School of Computer Science Enrollment by Degree Level, Sex, and Race/Citizenship"
- Scope: **Whole School of Computer Science** (CS, AI, ML, HCI, Robotics, Computational Biology, Software Research, Language Technologies). Broader than just the CS major — comparable in spirit to Georgia Tech's College of Computing total. Unlike Georgia Tech, CMU SCS does NOT operate a mass-online MS program, so master's growth is residential.
- Coverage: Fall 2020 → Fall 2024 (5 years, UG/MS/PhD). Each year's number appears in two consecutive PDFs and was cross-checked for agreement (see `parse_cmu_scs_pdf` in `scripts/fetch_university_data.py`).
- Year mapping: Fall 2024 = AY 2024-25.
- Older PDFs (Fall 2021–2023) discovered via Wayback Machine snapshots of the IRA index page; the live index links only the latest term.
- Note: a small "Other" (non-degree-seeking) column appears Fall 2023+. We do not include it in any of the bachelors/masters/phd series.

### [U5] UMass Amherst — UAIR Annual Factbook, "Students by Major"
- Office: UMass Amherst University Analytics and Institutional Research (UAIR)
- Index: https://www.umass.edu/uair/data/factsheets-data-tables
- Three PDFs (one per degree level), each a 10-year Fall history table:
  - Undergraduate: https://www.umass.edu/uair/media/973/download
  - Master's:      https://www.umass.edu/uair/media/970/download
  - Doctoral:      https://www.umass.edu/uair/media/967/download
- Title (each PDF): "Factbook 2025-2026 — Enrollment, [UG | Master's | Doctoral] Students by Major, Fall 2016 to Fall 2025"
- Scope: **Computer Science major** in the Manning College of Information & Computer Sciences (CICS), residential. **Excludes** the Informatics major (a separate CICS degree), the Exploratory Track (CICS-undeclared UG), and the small "Computer Science (UWW)" online professional master's program (~10% of CICS MS in Fall 2025) — so the MS series here is residential-only and apples-to-apples with UW–Madison and CMU.
- Coverage: Fall 2016 → Fall 2025 (10 years, **UG / MS / PhD all populated**).
- Year mapping: column headers are calendar years naming the Fall term, e.g. "Fall 2024" = AY 2024-25.
- URL stability: UAIR overwrites each PDF at the same `media/<id>/download` URL annually; the current download is the 2025-2026 factbook. Older factbook editions exist as separate `media/<id>` slugs (visible in directory listings — e.g. media/707, media/527, media/283) but the per-major PDFs are not separately archived under stable URLs in those older bundles.
- Note: a separate `Computer Science (UWW)` row appears in the master's factbook starting Fall 2021 (10 students; growing to 60 by Fall 2025). The parser deliberately skips it via a regex lookahead — to include it, change `parse_umass_factbook` to capture both rows and sum.

### [U6] Stony Brook University — IRPE Annual Factbook XLSX
- Office: Stony Brook University Office of Institutional Research, Planning & Effectiveness (IRPE)
- Index: https://www.stonybrook.edu/commcms/irpe/factbook/data-and-reports.html
- File: https://stonybrook.edu/irpe/_media/Enrollment/FallbyLevelCollegeSchoolMajorF25.xlsx
- Title: "Stony Brook University Fall Headcount Enrollment by Level, College/School (Academic Group) and Major (Plan)"
- Scope: **Computer Science major** in the College of Engineering & Applied Sciences (CEAS). Distinct from CEAS's separate **Computer Engineering** major (excluded) and the "Area of Interest - Computer Science" UG admission status (excluded — tracks intent-to-major freshman applicants, not declared majors). Values are Fall headcount of students with primary plan = Computer Science; double-majors are counted in each plan but only once in totals.
- Coverage: Fall 2014 → Fall 2025 (12 years, **UG / MS / PhD all populated**).
- Year mapping: column headers are "Fall YYYY" naming the Fall term, e.g. "Fall 2024" = AY 2024-25.
- Layout note: graduate programs that span multiple degree levels use a "merged-cell continuation" pattern — the first row carries program name + one degree (e.g. "Computer Science" / Doctoral, row 271), and the next row has an empty label cell (visually merged) with the next degree (e.g. row 272 = Master's = 396 in Fall 2022). The parser carries forward the most-recent non-empty label so the unlabeled rows inherit it.
- Parser: stdlib `zipfile` + `xml.etree` (no `openpyxl` dependency, matching the rest of this project's collectors). `pdftotext` would not work because the merged-cell pattern is not preserved in text rendering.
- Caveat: the file's header explicitly says **"2025 data are preliminary until reported to IPEDS in spring 2026"** — Fall 2025 values are kept but flagged in the per-row `notes` field. The CSV's Fall 2025 row will need re-fetching after IRPE finalises the file (likely mid-2026).
- URL stability: IRPE replaces the XLSX at the same `/irpe/_media/Enrollment/` path annually; the file name encodes the latest Fall term ("F25"), and prior editions are not separately archived under stable URLs in this pass.

## Schools checked and excluded

Documented here so they're not re-attempted from the same dead-end source. To
add any of these, find a different primary source.

- **University of Illinois Urbana-Champaign (UIUC)** — DMI Statistical Abstract `statsfa{YY}.pdf` only contains "Degrees granted by 2-digit CIP code" — no enrollment-by-CIP table in those abstracts. The separate enrollment HTML (`enrfa{YY}.htm`) lists by *curriculum* (many "Computer Science & X" combined-major rows); aggregating to a CS-major series across years requires a stable HTML structure that has not held across years.
- **University of Maryland (UMD)** — The cited departmental article (cs.umd.edu/article/2025/10/...) only quotes degrees-conferred endpoints (FY2018, FY2023). UMD's diversity/reports pages publish PNG charts that are not extractable as text.
- **UC Berkeley** — EECS "By the Numbers" (https://eecs.berkeley.edu/about/by-the-numbers/) reports a single Fall snapshot (currently Fall 2023). No multi-year history. Older Wayback snapshots use a different format and don't carry these specific numbers.
- **Stanford** — IRDS publishes enrollment-by-major data only via interactive Tableau dashboards at `irds.stanford.edu/data-findings/enrollment` (returns 403 to programmatic clients, no downloadable CSV/PDF).
- **University of Michigan (Ann Arbor)** — CSE Department has dedicated pages (`cse.engin.umich.edu/.../cs-eng-enrollment-and-graduation-data` and `cs-lsa-enrollment-and-graduation-data`) that would be ideal scope-wise (CS-Eng vs CS-LSA majors broken out), but the site is gated by Cloudflare's JS challenge and not fetchable without a browser.
- **University of Washington (Paul G. Allen School)** — `cs.washington.edu/about/factsheet` and the public undergraduate-demographics page show only the most recent term. Multi-year series exists in the school's annual Proviso Reports filed with the WA Legislature, but the report-search UI is dynamically rendered and a stable per-year PDF URL pattern was not identified in this pass.
- **UC Irvine (Bren School ICS)** — IR data is published only via Tableau Public (`public.tableau.com/.../EnrollmentDashboard_17/...`) and the iframe URL is sandboxed from JS access, blocking automated extraction in this codebase. The "New Students" view is the default; an Enrollment-by-major view exists but values are not exposed via the rendered DOM.
- **Penn State** — `datadigest.psu.edu/student-enrollment` embeds a Microsoft PowerBI dashboard (no static crosstab export equivalent to Tableau's was found), no direct CSV/PDF for major-level series.
- **Purdue CS, UCSD CSE, USC Viterbi, Ohio State CSE, Texas A&M CSE, Princeton, Cornell Bowers, Penn IRA, NC State CS (post-2020)** — public dept/IR pages show only single-snapshot or aggregate-college figures, or multi-year data is gated behind Tableau dashboards. NC State CS specifically: the legacy `report.isa.ncsu.edu/IR/Students/EnrollmentData/fYYenrol/enrd141901.htm` URL pattern (CS dept code 141901) covers Fall 2009–2020 in stable HTML, but post-2020 reports moved to a non-scrapeable Tableau factbook on `uda.ncsu.edu`.
- **Virginia Tech** — the University DataCommons (`udc.vt.edu/irdata/data/students/enrollment/index`) renders enrollment-by-major in a Tableau dashboard with no static export discovered in this pass. The College of Engineering's "Student Facts & Figures" page (`eng.vt.edu/about/student-facts-and-figures.html`) shows only the most recent Fall (Fall 2025), no historical series.
- **University of Minnesota–Twin Cities** — IDR's "Enrollments" report (`idr.umn.edu/reports-by-topic-enrollment/enrollments`) is a Tableau dashboard with no per-major static breakdown. The Twin Cities Common Data Set PDFs (`idr.umn.edu/sites/idr.umn.edu/files/cds_YYYY_YYYY_tc.pdf`) follow the standard CDS layout, which reports degrees-conferred and aggregate enrollment but not enrollment by CIP / major.
- **UNC Chapel Hill** — OIRA's analytic reports (`oira.unc.edu/reports/`) include "Headcount and FTE Enrollment by School, Education Level and Residency" (Excel + PDF), but the smallest unit is *school* not *department*; CS-specific enrollment is not separately reported in the public series.
- **University of Pittsburgh (SCI / CS Dept)** — SCI's "At A Glance" page reports a single recent term ("over 900 pre-CS/CS majors" prose-style, not tabular), and Pitt IR's `ir.pitt.edu` factbooks publish only school-level enrollment, not departmental.
- **University of Notre Dame** — `ir.nd.edu` was DNS/connection-unreachable to programmatic clients during this pass (HTTP 000 from `curl`). May be region-restricted or temporarily down; would need re-checking from a different network before deciding it's a permanent dead-end.
- **Rice University** — Rice OIR returns 403 Forbidden to programmatic User-Agents on its public factbook URLs; Cloudflare-style protection without a public crosstab/PDF alternative discovered in this pass.
- **Indiana University Bloomington** — IU's enrollment-by-major data is published only via `tableau.bi.iu.edu` Tableau dashboards (no Crosstab download equivalent to UW–Madison's public viz exposed in this pass). The Luddy School's public factsheet shows only the most recent Fall.
- **Iowa State University** — IR factbook XLSX files are well-organised and stably hosted, but the smallest unit broken out is College × Level (e.g. "Liberal Arts & Sciences, Undergraduate"), not by major. CS-specific enrollment is not separately reported in the public series.
- **Tufts University** — Provost IR (`provost.tufts.edu/institutionalresearch/fact-book/`) publishes annual "Fact Book" PDFs with a clean by-major CS breakdown (Liberal Arts CS + Engineering CS itemised separately), but the most recent edition is the 2023-24 Fact Book whose latest column is AY 2022-23 (= Fall 2022). No 2024-25 or 2025-26 Fact Book has been published; Fall 2023 and Fall 2024 data are not yet available.
- **Oregon State University** — `institutionalresearch.oregonstate.edu/enrollment-and-demographic-reports` publishes per-Fall enrollment PDFs (`enroll-fall-YYYY.pdf`, dating back to 2009) and a "Degree Program Profile" series with major-level CS data. CS enrollment, however, is dominated by the **Ecampus Postbacc Computer Science** online program (analogous to Georgia Tech's OMSCS situation but at the bachelor's level), and the published numbers do not separate residential CS from online Postbacc CS. Including OSU without that breakdown would obscure the post-ChatGPT residential-demand signal we care about. Beyond the data issue, OSU's CSRankings AI-areas position is closer to rank 30-40 than 50-60, so it would not fill the rank-50-60 sub-band that is the current target.
- **University of Houston** — UH IR's "Facts At A Glance" series (`uh.edu/ir/reports/facts-at-a-glance/facts-at-a-glance-faYYYY.pdf`, going back to Fall 2006) is a stable, parseable per-Fall PDF, but the smallest unit broken out is by-college, not by-major. CS is bundled inside the College of Engineering total.
- **Utah, CU Boulder, Brown, Northeastern (Khoury), ASU, Rutgers, Vanderbilt, Boston University, George Mason, Dartmouth, U-Buffalo, U-Rochester, Wake Forest, William & Mary, U-Albany SUNY, Lehigh, WPI, GWU, Drexel, Stevens, NJIT** — these were investigated as candidates for the **rank 50-60 sub-band** in this pass and all share the same blocker: their IR offices either (a) publish only via Tableau/PowerBI dashboards with no Crosstab export, (b) return 403 / DNS-fail to programmatic clients, (c) do not break enrollment out by major, or (d) the dept page shows only single-snapshot figures. This is a structural pattern: rank 5-30 schools (research powerhouses with mature IR functions) tend to publish multi-year by-major static reports; rank 50-60 schools have largely migrated to interactive dashboards in the past 5 years. **Boston College** does have a clean by-major CS PDF Fact Book (UG CS = 484, 486, 555, 556, 533 for Fall 2020–2024), but BC's CSRankings AI-areas rank is closer to 100, well outside the rank-50-60 sub-band, so it was not added in this pass.

## CSRankings tier coverage

The user-facing pill selector groups schools by approximate CSRankings AI-areas
rank (ai + vision + mlmining + nlp + inforet, 2014-2024 window from CSRankings).
Tier labels in the UI: ≈ RANK 5, ≈ RANK 10, ≈ RANK 30, ≈ RANK 50.

Current coverage:

- ≈ rank 5: Carnegie Mellon (≈ 1-5)
- ≈ rank 10: Georgia Tech (≈ 7-10)
- ≈ rank 30: University of Wisconsin–Madison (≈ 20-25), UMass Amherst (≈ 25-30)
- ≈ rank 50: Michigan State University (≈ 40-60), Stony Brook University (≈ 40-60)

UMass Amherst was added as a second school in the rank-30 tier because the
true rank-30-to-50 candidates (Virginia Tech, University of Minnesota–Twin
Cities, UNC Chapel Hill, University of Pittsburgh) all gate per-major
enrollment behind Tableau/PowerBI dashboards or only report at the
school-not-department grain in static form. UAIR's annual factbook PDFs
publish a clean, parseable 10-year-by-major Fall history for all three
degree levels, making UMass the only viable static-source candidate found
in this rank band during this pass.

Stony Brook was added as a second school in the rank-50 tier alongside MSU.
Both are CS majors housed within a College of Engineering, but the data
shapes complement each other: MSU is UG-only and short (5 years), while
Stony Brook spans 12 years across UG/MS/PhD, giving the rank-50 tier the
same UG/MS/PhD richness as rank 5/10/30. The IRPE XLSX was the only
viable rank-40-to-60 static source found in this pass after Notre Dame
(unreachable), Rice (403), IU Bloomington (Tableau-only), and Iowa State
(no by-major breakdown) were ruled out — see "Schools checked and excluded".

UW–Madison was added by extracting values from DAPIR's public Tableau viz
via Chrome — the first non-`urllib` collector in the project. The pattern
generalizes to any school whose IR office publishes data via Tableau's
public-viz Crosstab download (UCI, UMinnesota, etc. would be candidates if
their workbooks expose the same Download menu).
