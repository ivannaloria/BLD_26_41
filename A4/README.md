# A4 — shared renovation tool

## Team 41 — cost_estimate

Team 41 estimates construction and removal costs in DKK from Team 40's grouped
changes. It does not open IFC files. The manager calls the analysis through the
unchanged shared `runall.py` and joins it with the quantity and CO₂ results.

Our deliverables are `cost_estimate/src/main.py` and
`cost_estimate/data/cost_database.xlsx`. Shared modules, `runall.py` and
`settings.py` are not part of this Team 41 update.

### Run the shared tool

From the A4 folder, use Python 3.12 or a course-supported version:

```bash
python -m pip install -r requirements.txt
python -m unittest discover tests
python runall.py
```

Place the IFC models locally in `models/`, using the filenames already configured
in `settings.py`. Do not commit IFC files or generated results. Team 41 does not
change the manager's model paths or options. The existing runner also accepts
explicit model paths; see its `--help` if needed.

The runner calls each analysis and saves fresh JSON runs in
`cost_estimate/results/<variant>/run-<UTC>-<id>/result.json`. It writes
`results/changes_<variant>.xlsx` and `results/project_results.xlsx`. Open the latter
and inspect `Overview` → `Cost TOTAL DKK` and `Groups without cost`. Groups with
a `CostProblem` appear in `Manual review`. No result files are created by hand.

### Shared Python contract

```python
from cost_estimate.src.main import analyse, COMM_EXCEL

result = analyse(changes["groups"])
COMM_EXCEL(result, xlsx_path)
```

`analyse(groups, database=COST_DATABASE)` returns exactly these top-level keys:
`total_new_DKK`, `total_removed_DKK`, `summary` and `groups`. Each group record
contains exactly `GlobalId`, `CostCategory`, `Cost_DKK` and `CostProblem`, keeping
Team 40's group IDs and order. A missing or unusable price/quantity gives
`Cost_DKK = None` and a short problem reason. Results contain no DataFrames or
NaN and can be saved with `json.dumps(result, allow_nan=False)`.

Importing the module does not read input databases, open IFCs, print or write.
`analyse()` only reads inputs and calculates. Excel writing is separate.
`CAPT_CO2DATA`, `CONN_MATERIAL` and `COMM_SHEETS` remain imported from
`embodied_carbon.src.main`; cost and carbon use the same material translator.

The calculation is `quantity × price_DKK_per_unit` for `new`, or
`quantity × demolition_DKK_per_unit` for `removed`, rounded to whole DKK per
group. Units `m3`, `m2`, `m` and `pcs` select `Volume_m3`, `Area_m2`, `Length_m`
and `Count`. Group quantities are already totals: do not multiply by Count again.
Totals sum successfully calculated groups only, so inspect the problem count
before using them as a budget.

`CALC_COST` is the single primary C function. The helpers follow the course
TYPE_ELEMENT convention: `CAPT_GROUPS`, `CAPT_PRICES`, imported `CONN_MATERIAL`,
`CHEK_NUMBER`, `CHEK_COST`, `COMM_RECORDS`, `COMM_COST`, `COMM_EXCEL` and
`COMM_FORMAT`. All input datasets are passed as arguments.

### Price workbook and sources

`Prices` has exactly six columns, in the required order:

```text
category | unit | price_DKK_per_unit | demolition_DKK_per_unit | source | verified
```

All 23 names match the `Factors` categories in Team 42's database, exactly and
in the same order. All current units are `m3`. The workbook contains 18
construction and 17 removal reference rates. Unknown rates remain blank; a
legitimate numeric zero is not used as a substitute for missing information.

- `Sources`: publisher, URL, locator, original date, how each reference is used.
- `Rate_basis`: quoted amounts, VAT/quantity conversions and index formulas.
- `Category_notes`: per-category year, VAT assumptions, applicability and limits.
- `README`: workbook instructions and coverage counts.

Sources include Rambøll's published Molio-derived concrete-frame benchmark,
Bolius wall costs, Danish timber retailers, Danish-edition NUMIQ labour rates,
and a CLT economics presentation hosted by Danske Byggeøkonomer. Historical
rates are updated using Danmarks Statistik BYG43 to its latest available quarter,
2026Q2. Current retail/work references are November 2026 snapshots. This is not
a uniform tender-date valuation. Full citations and calculations are inside
the workbook; no direct access to licensed current Molio items is claimed.

All `verified` fields remain `no`: the references have been checked, but their
application to this project has not been verified. Concrete strength classes
share a frame-average proxy; timber uses reference sections; several masonry
categories use explicit material analogues. Source quarters are assigned where
only a year is supplied. VAT exclusion is assumed when the old source is silent.
No missing fabrication, crane, propping, waste disposal, overhead, contingency
or design allowance is invented. See `PRICE_GUIDE.md`.

The categories requiring prices are:

| Category — exactly as Team 42 | Construction | Removal |
|---|---|---|
| Concrete C20/25 | Reference estimate | Reference estimate |
| Concrete C25/30 | Reference estimate | Reference estimate |
| Concrete C30/37 | Reference estimate | Reference estimate |
| Concrete C35/45 | Reference estimate | Reference estimate |
| Concrete C40/50 | Reference estimate | Reference estimate |
| Concrete C45/55 | Reference estimate | Reference estimate |
| Concrete (class not specified) | Reference estimate | Reference estimate |
| Precast concrete wall 20 cm | Reference estimate | Reference estimate |
| Precast hollow-core slab 22 cm | Reference estimate | Reference estimate |
| Precast hollow-core slab 32 cm | Reference estimate | Reference estimate |
| Reinforcement steel | Unknown — blank | Unknown — blank |
| Structural steel | Unknown — blank | Unknown — blank |
| Structural steel welded | Unknown — blank | Unknown — blank |
| Structural steel hollow section | Unknown — blank | Unknown — blank |
| Light steel profiles | Unknown — blank | Unknown — blank |
| Glulam | Reference estimate | Reference estimate |
| CLT | Reference estimate | Unknown — blank |
| Solid timber | Reference estimate | Reference estimate |
| Brick | Reference estimate | Reference estimate |
| Sand-lime brick | Reference estimate | Reference estimate |
| Aerated concrete | Reference estimate | Reference estimate |
| Lightweight aggregate block | Reference estimate | Reference estimate |
| Concrete block | Reference estimate | Reference estimate |

The five steel categories and CLT removal still require applicable Molio items or
project quotations. After changing `Rate_basis`, recalculate and save the workbook
in Excel/LibreOffice before running Python: pandas/openpyxl read formula caches.
Do not add extra columns to `Prices`; put source metadata in `Category_notes`.

### Excel output and independent check

`COMM_EXCEL()` adds/replaces only `COST_Summary`, `COST_Groups` and
`COST_Problems`, using Team 42's helper and retaining other teams' sheets. The
group sheets have the four shared output columns; quantities remain in `Groups`.

For an independent check, first copy a Team 40 workbook to a working file, then:

```bash
python -m cost_estimate.src.main path/to/working_copy.xlsx
```

This command adds the cost sheets to that working file in place. It does not
create the manager's JSON run folders; the shared runner does that.

### Assumptions, scope and limitations

The A2 use case concerned columns in building #2604 and their share of a
35,000 DKK/m² budget. The agreed shared A4 workflow covers the beams, columns,
slabs and exterior walls supplied by Team 40. A budget percentage is not calculated
because an agreed project-budget area is not supplied by the group contract.

Both real comparisons have 0% shared GlobalIds. Team 40 matches properties and
quantities instead, assuming equivalent elements are retained. `new`/`removed`
therefore represent unmatched-quantity scenarios, not verified construction or
demolition activities. There are 165 groups for 26-06 and 154 for 26-09. The
latter has no matched equivalent elements. Review Team 40's `Info`, `Review` and
`Matches` before drawing a financial conclusion.

Multi-material groups cannot be priced automatically without split quantities.
Some excluded walls are listed in `Info` even when `Review` is empty. Team 41
flags clear concrete-material/steel-section conflicts and incomplete volumes.
Unresolved groups are not free work; unverified proxies are not final quotations.

Intended users are Build analysts, structural designers, cost planners and
project managers comparing renovation options before budget approval. Inputs
are group identifiers, status, material and a valid quantity in the price unit.
The included IDS checks only the upstream material-assignment subset. It does
not establish reliable quantities, matching or price applicability.

### Verification and provenance

Run `python -m unittest discover tests`. Team 41's tests cover the exact public
contract, six-column schema, import behaviour, JSON compatibility, missing/invalid
data, the synthetic 5,863 DKK example and preservation of existing Excel sheets.
Synthetic prices are temporary test fixtures, never production rates.

`HOW_TO_ADD_YOUR_PART.md` explains how to transfer just Team 41's two deliverables
into the manager's shared folder. `UPSTREAM.json` records the original integration
snapshots already present in this working copy. The agreed reference package is
the supplied `Team41_package actualizado.zip` (also referred to as A4.zip).
Its runner and Team 42 module remain unchanged. That ZIP contains no
`tests/test_tool.py`; the executed suite is Team 41's 17 tests, together with
the full shared-runner integration check.
