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
