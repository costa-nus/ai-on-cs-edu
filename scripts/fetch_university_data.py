#!/usr/bin/env python3
"""
fetch_university_data.py — download per-university CS enrollment data
from each university's own official institutional-research source and write
data/university-cs-enrollment.csv with a source_url on every row.

Scope: ENROLLMENT ONLY (i.e. number of students currently in the program at a
Fall snapshot). Degrees-conferred (graduates per year) is excluded — it lags
the population we care about by 2-6 years and would mix metrics on a single
chart.

Hard rule: every value committed to the CSV must come from the URL recorded
in that row's source_url column. No third-party aggregators. No interpolation.
If a value is not extractable from the named source, leave it blank with a
notes explanation. If a school's institutional-research office does not
publish per-CS enrollment in a stable, parseable form, the school is
EXCLUDED — better to be honest about coverage gaps than to substitute a
different metric.

Schools currently included (limited by what enrollment data is publicly
available):
    - Georgia Tech (College of Computing — UG/MS/PhD, 10 years)
    - Michigan State University (CS B.S. — Fall 2021-2025)
    - Carnegie Mellon (School of Computer Science — UG/MS/PhD, Fall 2020-2024)
    - University of Wisconsin–Madison (CS major in L&S, B.S. only — Fall 2016-2025;
      values extracted manually from DAPIR's public Tableau viz)
    - UMass Amherst (CS major in CICS — UG/MS/PhD, Fall 2016-2025; UAIR factbook
      "Students by Major" PDFs, one per degree level)
    - Stony Brook University (CS major in CEAS — UG/MS/PhD, Fall 2014-2025;
      IRPE annual factbook XLSX parsed via stdlib zipfile + xml.etree)

Schools intentionally excluded:
    - UIUC: DMI Statistical Abstract PDFs only contain degrees-by-CIP, not
      enrollment-by-CIP. The separate enrollment HTML is by-curriculum and
      multi-year coverage is not stable.
    - UMD: The cited department article only quotes degrees, not enrollment.
    - UC Berkeley: EECS "By the Numbers" page reports a single Fall snapshot
      with no multi-year history.

Notes on previously-excluded schools that were re-evaluated:
    - CMU was originally excluded because the IRA degrees-granted PDFs are
      the only ones indexed from cmu.edu/ira/degrees-granted/. The IRA
      *Enrollment* series (cmu.edu/ira/Enrollment/) is a separate page tree
      that DOES publish per-SCS Fall enrollment headcount tables.
    - UW–Madison was originally listed as Tableau-only (which is true for the
      Department Planning Profiles, gated behind WiscVPN). But DAPIR's PUBLIC
      "Trends in Student Enrollments" Tableau viz exposes a Crosstab
      download — values for the Computer Sciences major were extracted that
      way; see collect_uw_madison() below.

Run:
    python3 scripts/fetch_university_data.py

Outputs:
    data/raw/<university-slug>-<...>.{pdf,html}  — local copies of sources
    data/university-cs-enrollment.csv            — one row per (uni, year, level)
    data/university-cs-enrollment.js             — same data as JS object literal
"""
from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
import urllib.request
import zipfile
from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
CSV_OUT = ROOT / "data" / "university-cs-enrollment.csv"
JS_OUT = ROOT / "data" / "university-cs-enrollment.js"
RAW.mkdir(parents=True, exist_ok=True)


# ──────────────────────────────────────────────────────────────────────────────
# helpers

def fetch(url: str, dest: Path, *, force: bool = False) -> Path:
    if dest.exists() and not force and dest.stat().st_size > 0:
        return dest
    req = urllib.request.Request(url, headers={"User-Agent": "ai-on-cs-edu/1.0 (educational research)"})
    with urllib.request.urlopen(req, timeout=30) as r, open(dest, "wb") as f:
        f.write(r.read())
    return dest


def pdftotext(path: Path) -> str:
    out = subprocess.run(
        ["pdftotext", "-layout", str(path), "-"],
        capture_output=True, check=True, text=True,
    )
    return out.stdout


@dataclass
class Row:
    university: str
    csrankings_tier: str            # "top5" | "top10" | "top30" | "top50"
    academic_year: str              # "2022-23"
    degree_level: str               # "bachelors" | "masters" | "phd"
    metric: str                     # always "total_enrollment" in this collector
    value: int | None
    scope: str                      # what unit the count covers
    source_url: str
    source_label: str
    notes: str = ""


rows: list[Row] = []


# ──────────────────────────────────────────────────────────────────────────────
# Michigan State University — CS B.S. Fall enrollment headcount
# Source: MSU College of Engineering, CSE Department enrollment-data page.
# Publishes Fall headcount for the most recent ~5 Fall terms.

def parse_msu_cse_page(html_text: str) -> dict[int, int]:
    norm = re.sub(r"</?(tr|table)[^>]*>", "\n", html_text, flags=re.I)
    norm = re.sub(r"</?t[hd][^>]*>", " ", norm, flags=re.I)
    norm = re.sub(r"<[^>]+>", "", norm)
    norm = re.sub(r"[ \t]+", " ", norm)
    out: dict[int, int] = {}
    in_cs = False
    for line in norm.split("\n"):
        line = line.strip()
        if not line:
            continue
        if "Computer Science (B.S.)" in line:
            in_cs = True
            continue
        if in_cs:
            if "Undergraduate Enrollment" in line and "Degrees Awarded" in line:
                for m in re.finditer(r"Fall (\d{4})\s*[–-]\s*([\d,]+)", line):
                    out[int(m.group(1))] = int(m.group(2).replace(",", ""))
                break
            if re.match(r"^[A-Z][^F]", line) and "Engineering" in line:
                break
    return out


def collect_msu() -> None:
    url = "https://engineering.msu.edu/academics/undergraduate/enrollment-data"
    label = "MSU College of Engineering, CSE Department — Undergraduate Enrollment Data (CS B.S.)"
    path = RAW / "msu-cse-enrollment.html"
    if not path.exists():
        fetch(url, path)
    enrollment = parse_msu_cse_page(path.read_text(errors="replace"))

    for fall_year, count in sorted(enrollment.items()):
        ay = f"{fall_year}-{str(fall_year + 1)[-2:]}"
        rows.append(Row(
            university="Michigan State University",
            csrankings_tier="top50",
            academic_year=ay,
            degree_level="bachelors",
            metric="total_enrollment",
            value=count,
            scope="MSU College of Engineering, CSE Department — Computer Science (B.S.) major. Fall 4th-week census headcount, as published by MSU CoE.",
            source_url=url,
            source_label=label,
            notes="enrollment reports use 4th week of the term, as provided to ASEE",
        ))


# ──────────────────────────────────────────────────────────────────────────────
# Georgia Tech — College of Computing Fall enrollment, 10 years
# Source: Georgia Tech IRP Annual Fact Book — UG and graduate enrollment by
# college, fall-term ten-year history tables.
#
# Year mapping: column headers are calendar years naming the Fall term, e.g.
# "2023" = Fall 2023 = AY 2023-24.
#
# Scope caveat: this is the WHOLE College of Computing (CS, Cybersecurity &
# Privacy, Interactive Computing, Computational Science & Engineering), and
# crucially INCLUDES the Online MS in CS (OMSCS), which scaled to 10,000+
# students. The master's enrollment growth is dominated by OMSCS and is NOT
# comparable to residential master's elsewhere. Surface this loudly in the UI.

GATECH_FB_URL = "https://irp.gatech.edu/files/FactBook/2025_FactBook_Final.pdf"
GATECH_FB_PATH = RAW / "gatech-fb-2025.pdf"


def parse_gatech_fb_enrollment(pdf_path: Path) -> dict:
    """Returns {'bachelors': {ay: count}, 'masters': {...}, 'phd': {...}}."""
    txt = pdftotext(pdf_path)
    out: dict[str, dict[str, int]] = {"bachelors": {}, "masters": {}, "phd": {}}

    # ── Undergraduate Enrollment by College, Fall Term History
    ug_match = re.search(
        r"Undergraduate Enrollment by College, Fall Term History\s*\n"
        r"College\s+((?:\d{4}\s+){9}\d{4})",
        txt,
    )
    ug_years: list[int] | None = None
    if ug_match:
        ug_years = [int(y) for y in ug_match.group(1).split()]
        # Find "College of Computing" line within ~30 lines after the header
        block_start = ug_match.end()
        block = txt[block_start:block_start + 4000]
        coc = re.search(r"College of Computing\s+([\d,\s]+?)(?:\n|$)", block)
        if coc:
            nums = re.findall(r"[\d,]+", coc.group(1))[:10]
            for y, n in zip(ug_years, nums):
                ay = f"{y}-{str(y + 1)[-2:]}"
                out["bachelors"][ay] = int(n.replace(",", ""))

    # ── Graduate Enrollment by College and Degree, Fall Term History
    grad_match = re.search(
        r"Graduate Enrollment by College and Degree, Fall Term History\s*\n"
        r"College\s+Degree\s+((?:\d{4}\s+){9}\d{4})",
        txt,
    )
    if grad_match:
        grad_years = [int(y) for y in grad_match.group(1).split()]
        block_start = grad_match.end()
        block = txt[block_start:block_start + 4000]
        # College of Computing has two rows: "MS" and "PhD"
        ms_match = re.search(
            r"College of Computing\s+MS\s+([\d,\s]+?)(?:\n|$)",
            block,
        )
        if ms_match:
            nums = re.findall(r"[\d,]+", ms_match.group(1))[:10]
            for y, n in zip(grad_years, nums):
                ay = f"{y}-{str(y + 1)[-2:]}"
                out["masters"][ay] = int(n.replace(",", ""))
        phd_match = re.search(
            r"PhD\s+([\d,\s]+?)(?:\n|$)",
            block,
        )
        if phd_match:
            nums = re.findall(r"[\d,]+", phd_match.group(1))[:10]
            for y, n in zip(grad_years, nums):
                ay = f"{y}-{str(y + 1)[-2:]}"
                out["phd"][ay] = int(n.replace(",", ""))

    return out


def collect_gatech() -> None:
    if not GATECH_FB_PATH.exists():
        fetch(GATECH_FB_URL, GATECH_FB_PATH)
    parsed = parse_gatech_fb_enrollment(GATECH_FB_PATH)
    label = "Georgia Tech IRP, 2025 Fact Book — Fall Enrollment by College, Ten-Year History"
    scope = (
        "College of Computing — ALL schools/programs combined "
        "(CS + Cybersecurity & Privacy + Interactive Computing + "
        "Computational Science & Engineering). The master's series "
        "INCLUDES the Online MS in CS (OMSCS), which scaled to 10,000+ "
        "students; master's growth here is dominated by OMSCS and is not "
        "comparable to residential master's programs elsewhere."
    )
    for level in ("bachelors", "masters", "phd"):
        for ay, count in sorted(parsed[level].items()):
            rows.append(Row(
                university="Georgia Tech",
                csrankings_tier="top10",
                academic_year=ay,
                degree_level=level,
                metric="total_enrollment",
                value=count,
                scope=scope,
                source_url=GATECH_FB_URL,
                source_label=label,
            ))


# ──────────────────────────────────────────────────────────────────────────────
# Carnegie Mellon — School of Computer Science Fall enrollment, by degree level
# Source: CMU Office of Institutional Research & Analysis (IRA) — annual
# "School of Computer Science Enrollment by Degree Level, Sex, and
# Race/Citizenship" PDF, posted under cmu.edu/ira/Enrollment/pdf/fall-YYYY-pdfs/.
#
# Each PDF reports the current Fall and the prior Fall side-by-side (so the
# Fall 2024 PDF gives both Fall 2024 and Fall 2023). We parse all four PDFs
# (Fall 2021–2024) and dedupe; values must agree across the two PDFs that
# contain them, which is a built-in consistency check.
#
# Scope caveat: the row label is "Total" for the WHOLE School of Computer
# Science, which at CMU is a multi-department college (CS, AI, ML, HCI,
# Robotics, Computational Biology, Software Research, Language Technologies).
# This is broader than just the CS major — comparable in spirit to Georgia
# Tech's College of Computing total, NOT to a CS-major-only count like MSU's.
# We surface this in the scope string. Note: unlike Georgia Tech, CMU SCS
# does NOT include an OMSCS-style mass-online-MS program, so master's growth
# here is mostly residential.
#
# A small "Other" column (non-degree-seeking students) appears Fall 2023+;
# we do not include it in any of the bachelors/masters/phd series.

CMU_SCS_PDFS = {
    # fall_year -> (url, local_filename)
    2021: ("https://www.cmu.edu/ira/Enrollment/pdf/fall-2021-pdfs/scs-enrollment-10.28.2021.pdf",  "cmu-scs-f21.pdf"),
    2022: ("https://www.cmu.edu/ira/Enrollment/pdf/fall-2022-pdfs/scs-enrollment_f22_2.9.2023.pdf", "cmu-scs-f22.pdf"),
    2023: ("https://www.cmu.edu/ira/Enrollment/pdf/fall-2023-pdfs/scs-enrollment-f23-06oct2023.pdf", "cmu-scs-f23.pdf"),
    2024: ("https://www.cmu.edu/ira/Enrollment/pdf/fall-2024-pdfs/scs-f24-enrollmet-08nov2024.pdf",  "cmu-scs-f24.pdf"),
}

CMU_SCS_INDEX_URL = "https://www.cmu.edu/ira/Enrollment/index.html"


def parse_cmu_scs_pdf(pdf_path: Path, current_year: int) -> dict[int, dict[str, int]]:
    """Returns {fall_year: {'bachelors': n, 'masters': n, 'phd': n}}.

    The PDF has a single "Total" row near the bottom. The columns are, in
    order: Total, Undergrad, Master's, PhD, [Other], (then the same group
    again for the prior year). The Fall 2021 PDF omits the "Other" column.
    """
    txt = pdftotext(pdf_path)
    m = re.search(r"^\s*Total\s+([\d,\s]+?)\s*$", txt, re.M)
    if not m:
        raise RuntimeError(f"Could not find Total row in {pdf_path.name}")
    nums = [int(n.replace(",", "")) for n in re.findall(r"[\d,]+", m.group(1))]

    # Decide whether the PDF has a 5-col-per-year layout (with "Other") or
    # 4-col-per-year (no "Other"). Fall 2021 PDF uses the older 4-col layout.
    if len(nums) == 8:
        per_year = 4
    elif len(nums) == 10:
        per_year = 5
    else:
        raise RuntimeError(
            f"Unexpected Total row column count ({len(nums)}) in {pdf_path.name}: {nums}"
        )

    cur = nums[0:per_year]
    prv = nums[per_year:per_year * 2]

    def unpack(g: list[int]) -> dict[str, int]:
        # g = [Total, Undergrad, Master's, PhD, (Other)?]
        return {"bachelors": g[1], "masters": g[2], "phd": g[3]}

    return {
        current_year: unpack(cur),
        current_year - 1: unpack(prv),
    }


def collect_cmu() -> None:
    label = "CMU IRA — School of Computer Science Enrollment by Degree Level (annual Fall PDF)"
    scope = (
        "School of Computer Science (whole college) — includes CS, AI, ML, "
        "HCI, Robotics, Computational Biology, Software Research, and "
        "Language Technologies departments. This is broader than just the "
        "CS major (analogous to Georgia Tech's College of Computing); but "
        "unlike Georgia Tech, the master's series here does NOT include a "
        "mass-online-MS program. \"Other\" (non-degree-seeking) students "
        "are excluded from the bachelors/masters/phd breakdown."
    )

    # fall_year -> {level -> (value, source_url)}
    seen: dict[int, dict[str, tuple[int, str]]] = {}
    for fall_year, (url, fname) in CMU_SCS_PDFS.items():
        path = RAW / fname
        if not path.exists():
            fetch(url, path)
        parsed = parse_cmu_scs_pdf(path, fall_year)
        for yr, levels in parsed.items():
            for level, value in levels.items():
                prior = seen.get(yr, {}).get(level)
                if prior is not None and prior[0] != value:
                    raise RuntimeError(
                        f"CMU SCS Fall {yr} {level} mismatch: "
                        f"{prior[0]} (from {prior[1]}) vs {value} (from {url})"
                    )
                # Prefer the PDF whose "current" year matches yr (richer detail
                # and matches the file that originated the value); fall back
                # to the first PDF that contained it.
                if prior is None or yr == fall_year:
                    seen.setdefault(yr, {})[level] = (value, url)

    for fall_year in sorted(seen):
        ay = f"{fall_year}-{str(fall_year + 1)[-2:]}"
        for level in ("bachelors", "masters", "phd"):
            value, src_url = seen[fall_year][level]
            rows.append(Row(
                university="Carnegie Mellon",
                csrankings_tier="top5",
                academic_year=ay,
                degree_level=level,
                metric="total_enrollment",
                value=value,
                scope=scope,
                source_url=src_url,
                source_label=label,
                notes="Fall census-date headcount; index page lists the latest term only — historical PDFs verified via Wayback Machine.",
            ))


# ──────────────────────────────────────────────────────────────────────────────
# University of Wisconsin–Madison — Computer Sciences major Fall enrollment
# Source: UW–Madison DAPIR (Data, Academic Planning & Institutional Research)
# public Tableau dashboard "Trends in Student Enrollments" → "Degree-Major
# Enrollment Comparison" sheet.
#
# Tableau viz URL (canonical):
#   https://viz.wisc.edu/#/views/TrendsinStudentEnrollments/Degree-MajorEnrollmentComparison
#
# Collection method: we cannot fetch this dashboard with urllib — it's a
# rendered Tableau viz. The values were extracted via Chrome by setting
# Major=Computer Sciences, Term=Fall, Time Period=Last 10 Years, then
# Tableau's "Download Crosstab as CSV" with five filter passes:
#   (1) Academic Level=Undergraduate                          → UG
#   (2) Academic Level=Graduate                               → Grad combined
#   (3) Academic Level=(All)                                  → Total
#   (4) Academic Level=Graduate × Degree Level of Major=Master's          → MS
#   (5) Academic Level=Graduate × Degree Level of Major=Research Doctorate → PhD
# All five CSVs are checked into data/raw/ and parsed here.
#
# Cross-checks (both run at parse time):
#   - PRIMARY:   UG + Grad == Total                exactly (Academic-Level partition).
#   - SECONDARY: 0 ≤ (MS + PhD) − Grad ≤ 25       per year. MS + PhD exceeds
#     Grad by 6–21 students/year because UW–Madison classifies some PhD
#     students as concurrently Master's-degree-seeking (a known artifact of
#     the "MS en route to PhD" pattern). The Degree-Level-of-Major slices
#     therefore double-count those students. The bound rejects re-exports
#     where the overlap blows up, which would signal a filter-state error.
#
# Scope: UW–Madison's CS major is housed in the College of Letters & Science
# (NOT the College of Engineering). The "Computer Sciences" major covers the
# B.S./B.A., M.S., and Ph.D. tracks. UW–Madison also has separate "Computer
# Engineering" and "Electrical and Computer Engineering" majors (in the CoE)
# which we EXCLUDE.

UW_MADISON_VIZ_URL = "https://viz.wisc.edu/#/views/TrendsinStudentEnrollments/Degree-MajorEnrollmentComparison"
UW_MADISON_UG_CSV  = ROOT / "data" / "raw" / "uw-madison-cs-undergrad-fall2016-2025.csv"
UW_MADISON_GR_CSV  = ROOT / "data" / "raw" / "uw-madison-cs-graduate-fall2016-2025.csv"
UW_MADISON_ALL_CSV = ROOT / "data" / "raw" / "uw-madison-cs-all-levels-fall2016-2025.csv"
UW_MADISON_MS_CSV  = ROOT / "data" / "raw" / "uw-madison-cs-masters-fall2016-2025.csv"
UW_MADISON_PHD_CSV = ROOT / "data" / "raw" / "uw-madison-cs-research-doctorate-fall2016-2025.csv"


def parse_uw_tableau_crosstab(path: Path) -> dict[int, int]:
    """Parse a Tableau-exported Computer Sciences crosstab.

    The export is UTF-16 with tab separators. Row 1 is "Fall" repeated; row 2
    has years; row 3 is the Computer Sciences data row. Returns
    {fall_year: count}.
    """
    text = path.read_bytes().decode("utf-16")
    lines = [ln.split("\t") for ln in text.splitlines() if ln.strip()]
    if len(lines) < 3:
        raise RuntimeError(f"Unexpected layout in {path.name}: {lines!r}")
    years_row = lines[1]
    data_row = lines[2]
    if data_row[0].strip() != "Computer Sciences":
        raise RuntimeError(
            f"{path.name} first data row is {data_row[0]!r}, expected 'Computer Sciences'"
        )
    out: dict[int, int] = {}
    for year_cell, val_cell in zip(years_row[1:], data_row[1:]):
        try:
            yr = int(year_cell.strip())
        except ValueError:
            continue
        out[yr] = int(val_cell.strip().replace(",", ""))
    return out


def collect_uw_madison() -> None:
    label = "UW–Madison DAPIR — Trends in Student Enrollments (public Tableau viz, Computer Sciences major)"
    scope = (
        "University of Wisconsin–Madison Computer Sciences major (College of "
        "Letters & Science — NOT the College of Engineering). Source is "
        "DAPIR's public 'Degree-Major Enrollment Comparison' Tableau viz, "
        "filtered to Major=\"Computer Sciences\". Excludes the separate "
        "\"Computer Engineering\" and \"Electrical and Computer Engineering\" "
        "majors. Master's and Ph.D. (Research Doctorate) come from the "
        "Degree-Level-of-Major filter and slightly overlap (6–21 students/year) "
        "because UW–Madison classifies some PhD students as concurrently "
        "Master's-degree-seeking ('MS en route to PhD'). The PhD line here is "
        "Research Doctorate — Clinical Doctorate students (none expected for "
        "CS) are excluded."
    )
    notes_common = (
        "Values extracted via Chrome from the Tableau Crosstab download on "
        "2026-05-01. UG + Grad-combined = Total exactly. MS + PhD exceeds "
        "Grad-combined by 6–21 students/year due to MS-en-route-to-PhD double-"
        "classification."
    )

    ug    = parse_uw_tableau_crosstab(UW_MADISON_UG_CSV)
    gr    = parse_uw_tableau_crosstab(UW_MADISON_GR_CSV)
    total = parse_uw_tableau_crosstab(UW_MADISON_ALL_CSV)
    ms    = parse_uw_tableau_crosstab(UW_MADISON_MS_CSV)
    phd   = parse_uw_tableau_crosstab(UW_MADISON_PHD_CSV)

    OVERLAP_BOUND = 25
    for yr in sorted(set(ug) | set(gr) | set(total) | set(ms) | set(phd)):
        # PRIMARY: UG + Grad == Total exactly (Academic-Level partition).
        if ug.get(yr, 0) + gr.get(yr, 0) != total.get(yr, 0):
            raise RuntimeError(
                f"UW–Madison {yr} primary check failed: "
                f"UG ({ug.get(yr)}) + Grad ({gr.get(yr)}) "
                f"!= Total ({total.get(yr)}); re-export the CSVs."
            )
        # SECONDARY: 0 ≤ (MS + PhD) − Grad ≤ OVERLAP_BOUND (Degree-Level slices
        # may double-count MS-en-route-to-PhD students; bound caps that overlap).
        delta = ms.get(yr, 0) + phd.get(yr, 0) - gr.get(yr, 0)
        if not (0 <= delta <= OVERLAP_BOUND):
            raise RuntimeError(
                f"UW–Madison {yr} secondary check failed: "
                f"(MS + PhD) − Grad = {delta}, expected 0..{OVERLAP_BOUND}; "
                f"check whether the Academic-Level filter was set correctly "
                f"when the MS/PhD CSVs were exported."
            )

    by_level = {"bachelors": ug, "masters": ms, "phd": phd}
    src_per_level = {
        "bachelors": str(UW_MADISON_UG_CSV.relative_to(ROOT)),
        "masters":   str(UW_MADISON_MS_CSV.relative_to(ROOT)),
        "phd":       str(UW_MADISON_PHD_CSV.relative_to(ROOT)),
    }
    for level, series in by_level.items():
        for fall_year, count in sorted(series.items()):
            ay = f"{fall_year}-{str(fall_year + 1)[-2:]}"
            rows.append(Row(
                university="University of Wisconsin–Madison",
                csrankings_tier="top30",
                academic_year=ay,
                degree_level=level,
                metric="total_enrollment",
                value=count,
                scope=scope,
                source_url=UW_MADISON_VIZ_URL,
                source_label=label,
                notes=f"{notes_common} Local raw CSV: {src_per_level[level]}.",
            ))


# ──────────────────────────────────────────────────────────────────────────────
# UMass Amherst — Computer Science major Fall enrollment, by degree level
# Source: UMass Amherst University Analytics and Institutional Research (UAIR)
# annual factbook — three "Students by Major" PDFs (one each for UG, MS, PhD),
# each containing a 10-year Fall history. Files are served at stable
# media/<id>/download URLs that UAIR overwrites yearly with the latest factbook.
#
# Each PDF lays out School/College sections; under "College of Information and
# Computer Sciences" (CICS) several rows appear:
#   UG:  Computer Science | Exploratory Track | Informatics
#   MS:  Computer Science | Computer Science (UWW)
#   PhD: Computer Science
#
# Scope choice: we extract the "Computer Science" row ONLY. We exclude:
#   - Informatics (separate CICS major, distinct curriculum)
#   - Exploratory Track (CICS undergraduate undeclared students)
#   - Computer Science (UWW) (UMass University Without Walls — small online
#     professional master's; ~10% of MS headcount in 2025). Excluded so the
#     master's series is residential-only and apples-to-apples with
#     UW–Madison and CMU's residential MS series.
# This is the strictest reading of "the CS program," consistent with how
# UW–Madison's CS major is reported. The CICS column total is therefore
# NOT what we record.

UMASS_PDFS = {
    # degree_level -> (url, local filename)
    "bachelors": ("https://www.umass.edu/uair/media/973/download", "umass-ug-by-major.pdf"),
    "masters":   ("https://www.umass.edu/uair/media/970/download", "umass-ms-by-major.pdf"),
    "phd":       ("https://www.umass.edu/uair/media/967/download", "umass-phd-by-major.pdf"),
}


def parse_umass_factbook(pdf_path: Path) -> dict[int, int]:
    """Parse a UAIR factbook 'Students by Major' PDF; return {fall_year: count}
    for the 'Computer Science' row under 'College of Information and Computer
    Sciences'. The lookahead `[\\d,\\-]` after the whitespace prevents matching
    the 'Computer Science (UWW)' row whose first non-whitespace token is '('."""
    txt = pdftotext(pdf_path)

    yr_header = re.search(r"((?:Fall\s+\d{4}\s*){5,})", txt)
    if not yr_header:
        raise RuntimeError(f"No 'Fall YYYY' header in {pdf_path.name}")
    years = [int(y) for y in re.findall(r"Fall\s+(\d{4})", yr_header.group(1))]

    cics = re.search(r"College of Information and Computer Sciences\b[^\n]*\n", txt)
    if not cics:
        raise RuntimeError(f"No CICS section in {pdf_path.name}")
    block = txt[cics.end(): cics.end() + 1500]

    cs_row = re.search(
        r"^[ \t]+Computer Science[ \t]+([\d,\-][\d,\-\s]*?)$",
        block, re.M,
    )
    if not cs_row:
        raise RuntimeError(f"No 'Computer Science' row under CICS in {pdf_path.name}")

    tokens = cs_row.group(1).split()
    if len(tokens) < len(years):
        raise RuntimeError(
            f"{pdf_path.name}: got {len(tokens)} CS values but expected {len(years)} years"
        )
    out: dict[int, int] = {}
    for y, t in zip(years, tokens[:len(years)]):
        t = t.replace(",", "")
        if t == "-":
            continue
        out[y] = int(t)
    return out


def collect_umass_amherst() -> None:
    label = "UMass Amherst UAIR — Annual Factbook, 'Students by Major' (UG/MS/PhD, 10-year Fall history)"
    scope = (
        "University of Massachusetts Amherst Computer Science major in the "
        "Manning College of Information & Computer Sciences (CICS). EXCLUDES "
        "the separate Informatics major (also in CICS), the Exploratory Track "
        "(undergraduate undeclared CICS students), and the small online "
        "'Computer Science (UWW)' professional master's program (~10% of "
        "CICS MS headcount in Fall 2025) so the master's series is "
        "residential-only. Values are Fall census-date headcount of "
        "degree-seeking students."
    )
    notes = (
        "UAIR overwrites each factbook PDF at the same media/<id>/download URL "
        "annually; the current file is the 2025-2026 factbook covering "
        "Fall 2016 to Fall 2025."
    )
    for level, (url, fname) in UMASS_PDFS.items():
        path = RAW / fname
        if not path.exists():
            fetch(url, path)
        series = parse_umass_factbook(path)
        for fall_year, count in sorted(series.items()):
            ay = f"{fall_year}-{str(fall_year + 1)[-2:]}"
            rows.append(Row(
                university="UMass Amherst",
                csrankings_tier="top30",
                academic_year=ay,
                degree_level=level,
                metric="total_enrollment",
                value=count,
                scope=scope,
                source_url=url,
                source_label=label,
                notes=notes,
            ))


# ──────────────────────────────────────────────────────────────────────────────
# Stony Brook University — Computer Science major Fall enrollment, by degree level
# Source: SBU Office of Institutional Research, Planning & Effectiveness (IRPE)
# annual factbook XLSX "Fall Headcount Enrollment by Level, College/School
# (Academic Group) and Major (Plan)".
#
# URL is stable: IRPE replaces the file year-over-year at the same media path
# (current file name encodes the latest term — F25 — but the directory layout
# has been consistent across editions).
#
# Workbook layout: a single wide sheet with row groupings:
#   Grand Total → Undergraduate (by college, then by major) → Graduate
#   (by college, then by program with sub-rows per degree level).
#
# A "merged-cell continuation" pattern is used in the graduate section:
# programs with multiple degree levels span 2+ rows — the first has the
# program name and one degree (e.g. Doctoral), and the next row has an empty
# label cell (visually merged) with the next degree (e.g. Master's). The
# parser carries forward the most-recent non-empty label as `current_program`
# so the unlabeled rows inherit it.
#
# Scope: SBU's CS dept lives in the College of Engineering & Applied Sciences
# (CEAS) and operates a separate Computer Engineering major (excluded), plus
# an "Area of Interest - Computer Science" UG admission status (excluded — it
# tracks intent-to-major freshmen, not declared majors). We extract the
# "Computer Science" plan exactly, which is the declared CS major.
#
# Note: the file is plainly labelled "2025 data are preliminary until reported
# to IPEDS in spring 2026." Fall 2025 values are kept but flagged in notes.

SBU_XLSX_URL = "https://stonybrook.edu/irpe/_media/Enrollment/FallbyLevelCollegeSchoolMajorF25.xlsx"
SBU_XLSX_PATH = RAW / "stonybrook-fall-by-level-college-major.xlsx"
SBU_INDEX_URL = "https://www.stonybrook.edu/commcms/irpe/factbook/data-and-reports.html"

_XL_NS = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def _xlsx_col_index(cell_ref: str) -> int:
    letters = ""
    for ch in cell_ref:
        if ch.isalpha():
            letters += ch
        else:
            break
    n = 0
    for ch in letters:
        n = n * 26 + (ord(ch) - ord("A") + 1)
    return n - 1


def _xlsx_load_rows(xlsx_path: Path) -> list[dict[int, str]]:
    """Return a flat list of {col_index: cell_text} dicts, one per row."""
    with zipfile.ZipFile(xlsx_path) as z:
        ss_root = ET.fromstring(z.read("xl/sharedStrings.xml"))
        shared = [
            "".join(t.text or "" for t in si.iter(f"{{{_XL_NS['s']}}}t"))
            for si in ss_root.findall("s:si", _XL_NS)
        ]
        sheet_root = ET.fromstring(z.read("xl/worksheets/sheet1.xml"))
    sheet_data = sheet_root.find("s:sheetData", _XL_NS)
    out: list[dict[int, str]] = []
    for row in sheet_data.findall("s:row", _XL_NS):
        cells: dict[int, str] = {}
        for c in row.findall("s:c", _XL_NS):
            ci = _xlsx_col_index(c.get("r"))
            t = c.get("t")
            v = c.find("s:v", _XL_NS)
            if v is None:
                continue
            cells[ci] = shared[int(v.text)] if t == "s" else (v.text or "")
        out.append(cells)
    return out


def parse_stony_brook_xlsx(xlsx_path: Path) -> dict[int, dict[str, int]]:
    """Returns {fall_year: {'bachelors': n, 'masters': n, 'phd': n}} for the
    Stony Brook 'Computer Science' major (CEAS)."""
    rows = _xlsx_load_rows(xlsx_path)

    years: list[int] = []
    year_cols: list[int] = []
    for cells in rows:
        if (cells.get(0) or "").strip().startswith("Level / Academic Group"):
            for ci in sorted(cells):
                if ci < 2:
                    continue
                m = re.match(r"Fall\s+(\d{4})", (cells.get(ci) or "").strip())
                if m:
                    years.append(int(m.group(1)))
                    year_cols.append(ci)
            break
    if not years:
        raise RuntimeError(f"{xlsx_path.name}: no 'Fall YYYY' header row")

    DEGREES = {"Bachelor's": "bachelors", "Master's": "masters", "Doctoral": "phd"}
    out: dict[int, dict[str, int]] = {y: {} for y in years}
    current_program = ""
    for cells in rows:
        label = (cells.get(0) or "").strip()
        deg = (cells.get(1) or "").strip()
        if label:
            current_program = label
        if current_program != "Computer Science":
            continue
        level = DEGREES.get(deg)
        if level is None:
            continue
        for y, ci in zip(years, year_cols):
            raw = (cells.get(ci) or "").strip()
            if not raw:
                continue
            value = int(raw.replace(",", ""))
            prior = out[y].get(level)
            if prior is not None and prior != value:
                raise RuntimeError(
                    f"{xlsx_path.name}: duplicate Computer Science {level} "
                    f"row for Fall {y} with conflicting values {prior} vs {value}"
                )
            out[y][level] = value

    missing = [(y, lvl) for y in years for lvl in ("bachelors", "masters", "phd") if lvl not in out[y]]
    if missing:
        raise RuntimeError(f"{xlsx_path.name}: missing CS values: {missing[:5]}…")
    return out


def collect_stony_brook() -> None:
    if not SBU_XLSX_PATH.exists():
        fetch(SBU_XLSX_URL, SBU_XLSX_PATH)
    parsed = parse_stony_brook_xlsx(SBU_XLSX_PATH)
    label = (
        "SBU IRPE — Fall Headcount Enrollment by Level, College/School "
        "and Major (annual factbook XLSX)"
    )
    scope = (
        "Stony Brook University Computer Science major in the College of "
        "Engineering & Applied Sciences (CEAS). Distinct from the separate "
        "Computer Engineering major (CEAS) and the 'Area of Interest - "
        "Computer Science' UG admission status (intent-to-major freshmen, "
        "not declared majors) — both excluded. Values are Fall headcount of "
        "students whose primary plan is Computer Science; double-majors are "
        "counted in each plan."
    )
    notes_common = (
        "IRPE replaces this XLSX at the same /irpe/_media/Enrollment/ path "
        "annually; current file is the F25 edition covering Fall 2014 to "
        "Fall 2025. Per the file's own header note, 2025 data are "
        "preliminary until reported to IPEDS in spring 2026."
    )
    for fall_year in sorted(parsed):
        ay = f"{fall_year}-{str(fall_year + 1)[-2:]}"
        for level in ("bachelors", "masters", "phd"):
            value = parsed[fall_year][level]
            note = notes_common
            if fall_year == 2025:
                note = "Fall 2025 marked PRELIMINARY in source. " + notes_common
            rows.append(Row(
                university="Stony Brook University",
                csrankings_tier="top50",
                academic_year=ay,
                degree_level=level,
                metric="total_enrollment",
                value=value,
                scope=scope,
                source_url=SBU_XLSX_URL,
                source_label=label,
                notes=note,
            ))


# ──────────────────────────────────────────────────────────────────────────────
# main

def write_csv(rows: list[Row]) -> None:
    fields = [
        "university", "csrankings_tier", "academic_year", "degree_level",
        "metric", "value", "scope", "source_url", "source_label", "notes",
    ]
    with open(CSV_OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in sorted(rows, key=lambda r: (r.university, r.academic_year, r.degree_level)):
            row = {k: getattr(r, k) for k in fields}
            if row["value"] is None:
                row["value"] = ""
            w.writerow(row)


def write_js(rows: list[Row]) -> None:
    by_uni: dict[str, dict] = {}
    for r in rows:
        u = by_uni.setdefault(r.university, {
            "tier": r.csrankings_tier,
            "scope": r.scope,
            "sources": [],
            "series": {},
        })
        src_idx = None
        for i, s in enumerate(u["sources"]):
            if s["url"] == r.source_url:
                src_idx = i
                break
        if src_idx is None:
            u["sources"].append({"label": r.source_label, "url": r.source_url})
            src_idx = len(u["sources"]) - 1
        year = u["series"].setdefault(r.academic_year, {})
        level = year.setdefault(r.degree_level, {})
        level[r.metric] = r.value
        level["source_idx"] = src_idx
        if r.notes:
            level["notes"] = r.notes

    js = "// Generated by scripts/fetch_university_data.py — do not edit by hand.\n"
    js += "// Every value's source URL is recorded in `sources[source_idx]` per row.\n"
    js += "window.UNIVERSITY_CS_DATA = " + json.dumps(by_uni, indent=2) + ";\n"
    JS_OUT.write_text(js)


def main() -> None:
    collect_gatech()
    collect_msu()
    collect_cmu()
    collect_uw_madison()
    collect_umass_amherst()
    collect_stony_brook()
    write_csv(rows)
    write_js(rows)

    print(f"Wrote {len(rows)} rows → {CSV_OUT.relative_to(ROOT)}")
    print(f"        {JS_OUT.relative_to(ROOT)}")
    by_u: dict[str, int] = {}
    for r in rows:
        by_u[r.university] = by_u.get(r.university, 0) + 1
    for u, n in sorted(by_u.items()):
        print(f"  {u}: {n} rows")

    if "--verify" in sys.argv:
        print("\n──── Verification (every value with source) ────")
        for r in sorted(rows, key=lambda r: (r.university, r.degree_level, r.academic_year)):
            v = "—" if r.value is None else f"{r.value:>6}"
            print(f"  {r.university:<42} {r.academic_year}  {r.degree_level:<9} {r.metric:<19} = {v}")
            print(f"    source: {r.source_url}")


if __name__ == "__main__":
    main()
