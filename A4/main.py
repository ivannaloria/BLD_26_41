"""Cost-only runner for existing Team 40 Excel files; IFC models are not opened.

Example: python main.py examples/team40/*.xlsx
Each invocation creates a fresh results/run-... folder and preserves its inputs.
Use runall.py for the complete IFC -> quantities -> CO2 -> cost workflow.
"""

import argparse
import json
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from cost_estimate.src.main import COST_DATABASE, RESULT_COLUMNS, COMM_EXCEL, COMM_FORMAT, analyse
from embodied_carbon.src.main import COMM_SHEETS

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description="Estimate costs from Team 40 Groups sheets.")
    parser.add_argument("inputs", nargs="+", type=Path, help="Team 40 Excel file(s)")
    parser.add_argument("--database", type=Path, default=COST_DATABASE)
    parser.add_argument("--results-dir", type=Path, default=ROOT / "results")
    args = parser.parse_args()
    inputs = [path.resolve() for path in args.inputs]
    if any(not path.is_file() for path in inputs):
        parser.error("Every input must be an existing Excel file.")
    if len({path.stem.removeprefix("changes_") for path in inputs}) != len(inputs):
        parser.error("Input filenames must have distinct stems to identify variants.")

    # Analyse every source before creating output; analysis never writes inputs.
    results = [(path, analyse(path, database=args.database)) for path in inputs]
    args.results_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output = Path(tempfile.mkdtemp(prefix=f"run-{stamp}-", dir=args.results_dir))
    overview, details, notes = [], [], []
    for source, result in results:
        variant = source.stem.removeprefix("changes_")
        target = output / source.name
        shutil.copy2(source, target)
        COMM_EXCEL(result, target)
        groups = pd.DataFrame(result["groups"], columns=RESULT_COLUMNS)
        groups.insert(0, "Variant", variant)
        details.append(groups)
        missing = groups["CostProblem"].notna()
        missing_new = int((missing & groups["Status"].eq("new")).sum())
        missing_removed = int((missing & groups["Status"].eq("removed")).sum())
        overview.append({
            "Variant": variant,
            "Construction DKK (all new groups)": None if missing_new else result["total_new_DKK"],
            "Demolition DKK (all removed groups)": None if missing_removed else result["total_removed_DKK"],
            "Total DKK (all received groups)": None if missing.any() else result["total_new_DKK"] + result["total_removed_DKK"],
            "Calculated subtotal DKK": result["total_new_DKK"] + result["total_removed_DKK"],
            "Groups": len(groups), "Groups calculated": int(groups["Cost_DKK"].notna().sum()),
            "Groups with problems": int(missing.sum()),
            "Groups with price warnings": int(groups["CostWarning"].notna().sum()),
            "Valuation coverage": "PARTIAL - see Manual review" if missing.any() else "All received groups valued",
        })
        with pd.ExcelFile(source) as book:
            if "Info" in book.sheet_names:
                info = pd.read_excel(book, sheet_name="Info").copy()
                # The supplied example uses Field; current Team 40 files use Item.
                if "Field" in info and "Item" not in info:
                    info = info.rename(columns={"Field": "Item"})
                info.insert(0, "Variant", variant)
                notes.append(info)
        (output / f"cost_{variant}.json").write_text(
            json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8")

    all_groups = pd.concat(details, ignore_index=True)
    overview_df = pd.DataFrame(overview)
    overview_df["Scope"] = "Preliminary unmatched-quantity scenario; excluded elements are not valued."
    report_path = output / "project_costs.xlsx"
    # This is a NEW report, never one of Team 40's existing workbooks.
    with pd.ExcelWriter(report_path, engine="openpyxl", mode="w") as writer:
        overview_df.to_excel(writer, sheet_name="Overview", index=False)
    COMM_SHEETS(report_path, {
        "Overview": overview_df,
        "Cost groups": all_groups,
        "Manual review": all_groups.loc[all_groups["CostProblem"].notna()],
        "Assumptions": pd.concat(notes, ignore_index=True) if notes else pd.DataFrame(
            [{"Item": "Scope", "Value": "No input Info sheet supplied; confirm quantity assumptions."}]),
    }, header_colour="8A5A00")
    COMM_FORMAT(report_path, ["Overview", "Cost groups", "Manual review", "Assumptions"])
    print(overview_df[["Variant", "Groups", "Groups calculated", "Valuation coverage"]].to_string(index=False))
    print(f"\nResults: {output.resolve()}")
    if all_groups["CostProblem"].notna().any():
        print("Valuation is partial. Blank full totals are unresolved, not zero-cost work.")


if __name__ == "__main__":
    main()
