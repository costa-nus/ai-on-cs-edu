# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repo purpose

A small data + visualization repo tracking U.S. computer science education enrollment in the post-ChatGPT period (Nov 2022 onward), using only verified primary sources (CRA Taulbee Survey, NCES IPEDS).

## No build system

There is no package manager, no build step, no test suite. `index.html` at the repo root is a single self-contained dashboard (inline CSS, inline SVG, Google Fonts via CDN) — open it directly in a browser, or deploy the repo as-is to GitHub Pages. The `.nojekyll` marker disables Jekyll on Pages so files are served verbatim. Do not propose adding Vite/webpack/npm scaffolding unless the user asks.

## The data-vs-dashboard duality (most important thing to know)

`data/cs-enrollment-verified.csv` is the source of truth, but **the dashboard does not read it**. Every number shown in `index.html` is hardcoded in two places:

1. SVG `<polyline points="...">` / `<circle cx cy>` attributes that draw the chart lines and dots.
2. `<table>` cells that show the underlying values.

When updating data, you must edit the CSV **and** propagate the same numbers into the dashboard's SVG geometry and tables. A change to the CSV alone will silently leave the dashboard stale. There is no script that regenerates the HTML from the CSV.

The dashboard chart series are indexed to AY 2019-20 = 100 (absolute scales differ by an order of magnitude across degree levels), so SVG y-coordinates are derived from the indexed value, not the raw number.

## Data integrity rules

These are project conventions, not generic advice — treat them as hard constraints:

- **Every cell must trace to a source.** Each CSV row has a `source_id` that references an entry in `SOURCES.md`. Do not add a row without adding (or pointing at) a corresponding source entry.
- **Missing data stays blank.** Unknown values are left empty with a `notes` column explanation like `not extracted`. Never estimate, interpolate, or impute.
- **Do not mix scopes silently.** Bachelor's and PhD numbers come from CRA Taulbee (~144 U.S. CS-PhD-granting departments). Master's numbers come from NCES IPEDS (all U.S. institutions, broader CIP 11 "Computer and Information Sciences" category). The CSV's `scope` column makes this explicit; preserve that distinction in any new rows or chart annotations.
- **Stocks vs flows.** Total enrollment is a stock; new enrollment and degrees conferred are flows. The dashboard splits them into two panels deliberately — don't combine them on a single axis.

## Update cadence

- New CRA Taulbee Survey: typically released ~May each year. The next expected release covering AY 2024-25 is ~May 2026.
- NCES Digest tables: updated late summer/fall of the year following the academic year covered.
- A single Taulbee report covers two academic years (prior year's enrollment/degrees + current year's new students), so most cells can be cross-checked against two consecutive reports.

## Dashboard

Only one dashboard exists — `index.html` at the repo root (the file previously known as `dashboards/cs-enrollment-stocks-vs-flows-v4.html`, promoted to be the GitHub Pages entry point). Earlier iterations were deleted; do not try to resurrect them. If the user asks for a variant, ask whether to overwrite `index.html` or create a sibling file with a descriptive name.
