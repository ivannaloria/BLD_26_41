# A4 — Team 41: cost estimation of structural changes

This tool estimates the construction and removal costs, in DKK, of the structural
changes identified by Team 40. It compares proposed renovation options using
grouped quantities and an external price database. Missing information remains
visible and unresolved costs are blank.

The original [A2 use case](../A2/README.md) concerned the cost of columns in
building #2604. The agreed A4 workflow extends the calculation to the beams,
columns, slabs and exterior walls supplied by Team 40. This version does not
calculate a percentage of the 35,000 DKK/m² project budget: the necessary agreed
budget floor area is not part of this input contract.

## Current status

The cost module and the two runners are implemented. The material classifier
and its database are reused from Team 42. Two real Team 40 workbooks are supplied
as reproducible examples. **The price database now contains 18 construction and
17 removal reference estimates**, with sources and calculations in its `Sources`
and `Rate_basis` sheets. These are documented proxies, not project-verified
quotations. Five steel categories and CLT removal remain unpriced. Empty rates
are never interpreted as free work. Historical references are indexed to 2026Q2;
current retail/work rates are November 2026 snapshots. Read `PRICE_GUIDE.md` and
the workbook assumptions before interpreting totals.

## Run the cost analysis from Excel

Use Python 3.12 or the course-supported Python version with an available
IfcOpenShell wheel. From the repository root:

```bash
cd A4
python -m venv .venv
# macOS / Linux:
source .venv/bin/activate
# Windows PowerShell instead:
# .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py examples/team40/changes_26-06-D-STR.xlsx examples/team40/changes_26-09-D-STR.xlsx
```

This cost-only command does not open IFC models or calculate emissions. It
creates a new `results/run-.../` folder every time, containing:

- Copies of the input workbooks with `COST_Summary`, `COST_Groups` and
  `COST_Problems` added. The original files are unchanged.
- `project_costs.xlsx`: a comparison of both variants, group detail, unresolved
  groups and the original Team 40 assumptions.
- One JSON cost result per variant, suitable for other analyses.

The overview separates calculated subtotals from totals for all received groups.
Full totals stay blank when the corresponding groups have unresolved costs.
No ranking of incomplete options is produced. Even when all received groups have
costs, the result excludes elements outside Team 40's scope.

To choose a different database or output directory:

```bash
python main.py path/to/changes.xlsx --database path/to/prices.xlsx --results-dir results
```

## Plug into the shared tool

The implementation preserves the supplied package's module names and contract:

```python
from cost_estimate.src.main import analyse, COMM_EXCEL

cost = analyse(changes["groups"])
# cost["groups"] is a list of dictionaries, not a DataFrame.
# Fields: GlobalId, CostCategory, Cost_DKK, CostProblem, plus audit details.
cost["total_new_DKK"], cost["total_removed_DKK"]
COMM_EXCEL(cost, xlsx_path)
```

`analyse()` accepts a list of dictionaries, a DataFrame or an Excel file with a
`Groups` sheet. It never writes, prints or opens an IFC. Returned values are JSON
compatible, with `None` for unresolved costs. Totals sum the calculated, rounded
group costs only. Consult the summary's coverage and problem count with them.

The independent module command updates the Excel file passed to it **in place**:

```bash
python -m cost_estimate.src.main path/to/working_copy.xlsx
```

For the full quantities → CO₂ → cost → shared report workflow, place the IFCs
locally under `A4/models/` or pass their paths:

```bash
python runall.py /path/to/B308X.ifc /path/to/26-06-D-STR.ifc /path/to/26-09-D-STR.ifc
```

`runall.py` is the unchanged runner from the supplied ZIP. It produces each
analysis's timestamped JSON, per-variant Excel files and
`results/project_results.xlsx`, including the manager's `Manual review` sheet.
Its `Complete` flag describes missing cost/CO₂ calculations, not verification of
retention, quantities, prices or exclusions. Its ranking is by CO₂, not cost.
The cost-only comparison is `project_costs.xlsx`.

## Structure and responsibilities

```text
A4/
  main.py                         Team 41 cost-only Excel runner
  runall.py                       supplied shared IFC runner, unchanged
  settings.py                     local IFC paths
  cost_estimate/
    src/main.py                   Team 41 implementation
    data/cost_database.xlsx       23-category Prices + Sources + Rate_basis
  embodied_carbon/
    src/main.py                   supplied Team 42 code, unchanged
    data/co2_database.xlsx        Team 42 Rules + Factors, unchanged
  model_changes/src/
    team40.py                     current Team 40 source, unchanged
    main.py                       local metadata adapter for the shared manager
    ifc_to_excel.py               supplied integration helper, unchanged
  project_report/src/main.py      supplied manager, unchanged
  examples/                       supplied example and Team 40 workbook snapshots
  tests/test_cost.py              Team 41 behaviour and integration tests
  UPSTREAM.json                   source URLs and checksums
  PRICE_GUIDE.md                  Danish rate sourcing and unit guidance
```

The adapter exposes model names and GlobalId overlap as top-level metadata,
which the manager expects but Team 40's latest source stores in `info`. It does
not change extraction, matching, quantities or groups. No external repository
is modified by installing or running this tool. Upstream code is included for
integration and attributed in `UPSTREAM.json` and `CHANGELOG.md`.

## Functions in the cost module

| Function | Purpose |
|---|---|
| `CAPT_GROUPS` | Read groups and validate their identifiers. |
| `CAPT_PRICES` | Read the category-based `Prices` sheet. |
| `CONN_MATERIAL` | Import Team 42's material classifier, unchanged. |
| `CHEK_NUMBER` | Check finite numeric input; reject booleans and invalid values. |
| `CALC_COST` | Primary calculation: selected quantity × selected unit price. |
| `CHEK_COST` | Select groups requiring manual review. |
| `COMM_COST` | Prepare totals, coverage and unresolved-group counts. |
| `COMM_EXCEL` | Add/replace the three cost sheets using Team 42's safe helper. |
| `COMM_FORMAT` | Fit and wrap the output sheets without restyling other teams' sheets. |
| `analyse` | Coordinate the analysis and return JSON-compatible results. |

`new` uses `price_DKK_per_unit`; `removed` uses `demolition_DKK_per_unit`.
`m3`, `m2`, `m` and `pcs` select `Volume_m3`, `Area_m2`, `Length_m` and `Count`.
Quantities are already group totals and are **not multiplied by Count again**.
Costs are rounded to whole DKK per group. A genuine numeric zero price is allowed;
an empty price is unresolved. Invalid statuses/units, duplicate category rates,
missing quantities and clear concrete/steel-section conflicts are flagged.
Optional `ifc_class` and `type_name` price columns restrict a rate to an exact
element class or section; a scope mismatch is unresolved.

## Assumptions and limits from Team 40

Both real comparisons have 0% shared GlobalIds. Matching instead uses class,
material, section and quantities, with 10 mm length and 1% area/volume tolerances.
Equivalent elements are assumed retained, independently of their location.
This cannot establish actual retention or detect removal and equivalent replacement.
Accordingly, `new` and `removed` are unmatched-quantity scenarios, not verified
construction or demolition instructions.

| Workbook | New groups | Removed groups | Equivalent elements |
|---|---:|---:|---:|
| `changes_26-06-D-STR.xlsx` | 145 | 20 | 139 |
| `changes_26-09-D-STR.xlsx` | 122 | 32 | 0 |

The scope excludes interior walls and walls requiring classification/foundation
review. Some excluded walls appear in `Info`, even when `Review` is empty.
Multi-material volumes are not split: the shared classifier marks these for
review. Geometry-derived quantities need verification. For example, some groups
in 26-06 have a concrete material but a steel section name; Team 41 flags that
conflict instead of assigning a concrete price automatically.

Category-based rates are an estimate: wall thickness, profile, element class,
installation conditions and demolition method can change the applicable rate.
Review classification and price scope before using totals. Missing prices,
unverified prices and excluded quantities prevent a defensible full project budget.
Site overheads, professional fees, contingency, VAT and other work are not added
automatically. Record the scope of every entered rate.

## Use in Advanced Building Design

Intended users are the Build analyst, structural designers, cost planners and
project managers comparing renovation options before budget approval. The tool
supports early design and pre-construction decisions; it does not prove that one
option is cheaper until comparable quantities and rates have been reviewed.

Team 40 needs IFC classes, material assignments, sections and applicable length,
area and volume data, or geometry from which quantities can be obtained. Team 41
requires their `Groups` dataset and external prices, not direct IFC access.
`information_requirements.ids` checks the material-assignment subset of those
IFC requirements. Geometry, reliable matching, classification and price suitability
still need the upstream checks and manual review; IDS alone cannot establish them.

## Validation

```bash
python -m unittest discover -s tests -v
```

Tests cover the expected synthetic concrete example (2.9313 m³ × 2,000 DKK/m³ =
5,863 DKK), separate demolition pricing, all units, missing/invalid data, material
classification, JSON output, empty input, Excel preservation and both real Team
40 datasets. Synthetic rates are created in temporary test files only; they are
not Danish market prices and never enter the production database.

See `CHANGELOG.md` for the actual integration checks performed for this release.
