# Integrating Team 41 into the shared A4 folder

This note concerns Team 41 only. Keep the manager's shared architecture and
its existing `runall.py`, `settings.py` and other teams' modules unchanged.

1. Copy `cost_estimate/src/main.py` and
   `cost_estimate/data/cost_database.xlsx` into the corresponding shared paths.
   Keep the package's existing `__init__.py` files.
2. Ensure `embodied_carbon/data/co2_database.xlsx` is the agreed Team 42 version.
   Every `Prices.category` must match a `Factors.category` exactly. Do not rename
   categories or introduce a second material translator.
3. Keep exactly the six agreed columns in `Prices`. Extra source information
   belongs in `Sources`, `Rate_basis` or `Category_notes` within the same workbook.
   Leave unknown prices blank; `verified = no` means not verified for the project.
4. Place IFC files in the manager's local `models/` folder with the names already
   configured in `settings.py`. Never upload the IFCs or generated result files.
5. From A4, run:

   ```bash
   python -m pip install -r requirements.txt
   python -m unittest discover tests
   python runall.py
   ```

6. In `results/project_results.xlsx`, check the `Cost TOTAL DKK` and
   `Groups without cost` columns in `Overview`. Every unresolved cost must have
   a group entry and reason in `Manual review`. Review price assumptions before
   interpreting calculated subtotals as a final budget.

The manager calls:

```python
from cost_estimate.src.main import analyse, COMM_EXCEL

cost = analyse(changes["groups"])
COMM_EXCEL(cost, xlsx_path)
```

The return keys are `total_new_DKK`, `total_removed_DKK`, `summary` and `groups`.
Each group has exactly `GlobalId`, `CostCategory`, `Cost_DKK`, `CostProblem`.
Missing costs are `None`, with a short reason. Importing the module has no
analysis side effects. `analyse()` reads inputs and calculates; only
`COMM_EXCEL()` writes the cost sheets.

JSON results are saved by `runall.py` under timestamped run folders. Do not write
files manually in `cost_estimate/results/`. The agreed reference is
`Team41_package actualizado.zip`, also referred to as A4.zip. It contains no
`tests/test_tool.py`. Team 41's tests do not replace shared tests; if the manager
later provides an additional shared suite, run it alongside the Team 41 suite.
