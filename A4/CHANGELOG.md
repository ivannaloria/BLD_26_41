# Changelog

## 2026-11-25 — Team 41 cost tool

- Implemented `cost_estimate/src/main.py` from the supplied Team 41 package,
  retaining `analyse(groups)`, JSON-compatible outputs, the primary `CALC_COST`
  function and separate `COMM_EXCEL` writing.
- Reused Team 42's material rules, classifier and sheet-writing helper without
  changing their source. Included its public CO₂ database so imports and the
  shared filter work immediately.
- Included Team 40's current comparison source unchanged, with a separate local
  adapter exposing metadata expected by the supplied manager. Included the
  supplied shared runner and manager unchanged. Sources and hashes are in
  `UPSTREAM.json`. No remote changes were made to Teams 40 or 42.
- Added a cost-only runner for one or more Excel files. It writes fresh output
  folders, preserves source workbooks and leaves incomplete full totals blank.
- Exposed quantities, units, prices, sources, verification and problem reasons
  in cost detail. Added checks for invalid data, duplicate rates and clear
  concrete-material/steel-section conflicts.
- Added an English README, Danish price-sourcing guidance and a limited IDS
  material-assignment requirement. This IDS does not replace geometry, quantity
  or matching checks.
- Preserved the supplied price database unchanged. No market prices or test
  values were inserted into it. Financial valuation remains pending documented
  project-appropriate construction and demolition rates.

Validation performed on Python 3.12 with pandas 2.2.3, openpyxl 3.1.5 and
IfcOpenShell 0.9.0.post1:

- 16 Team 41 behaviour/integration tests, including the 5,863 DKK synthetic
  concrete example, missing-data handling, JSON serialization and repeated Excel
  writes preserving Team 40 and Team 42 sheet values.
- Cost-only processing of the two supplied Team 40 workbooks: 165 and 154 groups,
  same group order and IDs, original files unchanged, unresolved full totals
  blank and 319 groups available for review with the empty price list.
- Full shared `runall.py` processing using B308X.ifc, 26-06-D-STR.ifc and
  26-09-D-STR.ifc obtained read-only from Team 40. Both variants completed the
  quantity/CO₂/cost/report pipeline and wrote per-analysis JSON and Excel output.
  The manager correctly reported incomplete valuation. IFC files and temporary
  test outputs are not committed.
- IDS validated against the official buildingSMART 1.0 content schema with its
  redundant XMLSchema-instance import omitted for libxml2 compatibility.
- Checked original upstream file checksums and visually reviewed the generated
  cost summary, group, problem and comparison sheets.

The original upstream project's seven tests and its synthetic IFC examples were
not in the supplied package or public A4 folder, so no claim is made that those
particular tests were run.
