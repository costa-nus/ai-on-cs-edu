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

## Schools checked and excluded

Documented here so they're not re-attempted from the same dead-end source. To
add any of these, find a different primary source.

- **Carnegie Mellon (CMU)** — IRA publishes per-school *degrees-granted* PDFs (https://www.cmu.edu/ira/degrees-granted/) but the IRA index does not link any per-CS-Department or per-SCS-school *enrollment* PDFs. CDS would be university-level only.
- **University of Illinois Urbana-Champaign (UIUC)** — DMI Statistical Abstract `statsfa{YY}.pdf` only contains "Degrees granted by 2-digit CIP code" — no enrollment-by-CIP table in those abstracts. The separate enrollment HTML (`enrfa{YY}.htm`) lists by *curriculum* (many "Computer Science & X" combined-major rows); aggregating to a CS-major series across years requires a stable HTML structure that has not held across years.
- **University of Maryland (UMD)** — The cited departmental article (cs.umd.edu/article/2025/10/...) only quotes degrees-conferred endpoints (FY2018, FY2023). UMD's diversity/reports pages publish PNG charts that are not extractable as text.
- **UC Berkeley** — EECS "By the Numbers" (https://eecs.berkeley.edu/about/by-the-numbers/) reports a single Fall snapshot (currently Fall 2023). No multi-year history. Older Wayback snapshots use a different format and don't carry these specific numbers.

## CSRankings tier coverage

The user-facing pill selector groups schools by approximate CSRankings AI-areas
rank (ai + vision + mlmining + nlp + inforet, 2014-2024 window from CSRankings).
Tier labels in the UI: ≈ RANK 5, ≈ RANK 10, ≈ RANK 30, ≈ RANK 50.

Current coverage:

- ≈ rank 10: Georgia Tech (≈ 7-10)
- ≈ rank 50: Michigan State University (≈ 40-60)

Tiers ≈ rank 5 and ≈ rank 30 currently have no schools because the candidates
explored (CMU, UIUC, UMD, UC Berkeley) don't publish per-CS enrollment in a
parseable form. Filling these tiers requires finding a different primary
source — Stanford IRDS, U Washington OPB, UCSD, or Penn IRA would be the next
candidates if their pages publish CS-program enrollment headcount.
