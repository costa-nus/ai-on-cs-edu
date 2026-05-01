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

## CSRankings tier coverage

The user-facing pill selector groups schools by approximate CSRankings AI-areas
rank (ai + vision + mlmining + nlp + inforet, 2014-2024 window from CSRankings).
Tier labels in the UI: ≈ RANK 5, ≈ RANK 10, ≈ RANK 30, ≈ RANK 50.

Current coverage:

- ≈ rank 5: Carnegie Mellon (≈ 1-5)
- ≈ rank 10: Georgia Tech (≈ 7-10)
- ≈ rank 30: University of Wisconsin–Madison (≈ 20-25)
- ≈ rank 50: Michigan State University (≈ 40-60)

UW–Madison was added by extracting values from DAPIR's public Tableau viz
via Chrome — the first non-`urllib` collector in the project. The pattern
generalizes to any school whose IR office publishes data via Tableau's
public-viz Crosstab download (UCI, UMinnesota, etc. would be candidates if
their workbooks expose the same Download menu).
