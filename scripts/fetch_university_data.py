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

Schools intentionally excluded:
    - CMU: IRA publishes degrees-granted PDFs but no per-CS-Dept enrollment.
    - UIUC: DMI Statistical Abstract PDFs only contain degrees-by-CIP, not
      enrollment-by-CIP. The separate enrollment HTML is by-curriculum and
      multi-year coverage is not stable.
    - UMD: The cited department article only quotes degrees, not enrollment.
    - UC Berkeley: EECS "By the Numbers" page reports a single Fall snapshot
      with no multi-year history.

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
from dataclasses import dataclass
from pathlib import Path

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
