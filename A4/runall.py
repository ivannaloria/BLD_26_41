"""
runall.py - shared runner (course node-comply-template, extended for our tool)

Run from the A4 folder:
    python runall.py                                   # uses the paths in settings.py
    python runall.py existing.ifc variantA.ifc [variantB.ifc ...]

Differences from the course template, because our tool compares models and the teams build
on each other:
  * it opens TWO OR MORE models: the existing building once, then every proposed version;
  * the analyses are a chain, not independent: Team 40's groups are passed to Teams 42 and 41,
    and the manager's report receives all three results.
Everything else follows the template: each analysis has analyse(...) in <name>/src/main.py,
returns JSON-compatible data, and every run is saved as
<name>/results/<variant>/run-<UTC-time>-<suffix>/result.json without overwriting earlier runs.

For people who don't open IFC or JSON, it also writes Excel files to results/:
    results/changes_<variant>.xlsx    Team 40 sheets + CO2_* sheets + COST_* sheets
    results/project_results.xlsx      Overview, Manual review, one sheet per variant (grows)
"""

import argparse
import json
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from settings import EXISTING_MODEL_PATH, PROPOSED_MODEL_PATHS
from model_changes.src.main import CAPT_ELEMENTS, analyse as compare_versions, COMM_EXCEL as excel_changes
from embodied_carbon.src.main import analyse as calculate_carbon, COMM_EXCEL as excel_carbon
from cost_estimate.src.main import analyse as calculate_cost, COMM_EXCEL as excel_cost
from project_report.src.main import analyse as build_report, COMM_WORKBOOK

ROOT = Path(__file__).resolve().parent


def save_result(result, results_dir):
    # Reject unsupported values before creating a run folder.   (unchanged from the template)
    content = json.dumps(result, indent=2, allow_nan=False)
    results_dir = Path(results_dir)
    results_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = Path(tempfile.mkdtemp(prefix=f"run-{timestamp}-", dir=results_dir))
    output = run_dir / "result.json"
    output.write_text(content + "\n", encoding="utf-8")
    return output


def resolve(path):
    path = Path(path)
    return path if path.is_absolute() else ROOT / path


def run_variant(existing_elements, existing_name, proposed_path, results_dir=None):
    """Runs the four analyses for one proposed model and saves their results."""
    import ifcopenshell
    variant = proposed_path.stem
    model = ifcopenshell.open(str(proposed_path))                  # opened for reading only
    out = lambda name: (ROOT / name / "results" if results_dir is None else Path(results_dir) / name) / variant

    changes = compare_versions(model, existing_elements, names=(existing_name, proposed_path.name))
    carbon = calculate_carbon(changes["groups"])                     # Team 42 receives Team 40's data
    cost = calculate_cost(changes["groups"])                         # Team 41 receives Team 40's data
    report = build_report(changes, carbon, cost, variant)

    for name, result in [("model_changes", changes), ("embodied_carbon", carbon),
                         ("cost_estimate", cost), ("project_report", report)]:
        print(f"  {name}: Result saved to: {save_result(result, out(name)).resolve()}")

    excel_dir = ROOT / "results" if results_dir is None else Path(results_dir)
    excel_dir.mkdir(parents=True, exist_ok=True)
    xlsx = excel_dir / f"changes_{variant}.xlsx"
    excel_changes(changes, xlsx)
    excel_carbon(carbon, xlsx)
    excel_cost(cost, xlsx)
    COMM_WORKBOOK(report, excel_dir / "project_results.xlsx")
    return report["overview"]


def main():
    parser = argparse.ArgumentParser(description="Compare an existing IFC with proposed versions.")
    parser.add_argument("models", nargs="*", type=Path,
                        help="existing.ifc followed by one or more proposed .ifc "
                             "(defaults to the paths in settings.py)")
    parser.add_argument("--results-dir", type=Path,
                        help="Optional output root; writes <root>/<analysis-name>/<variant>/run-.../result.json")
    args = parser.parse_args()

    if args.models:
        if len(args.models) < 2:
            parser.error("Give the existing model and at least one proposed model.")
        existing, proposed = args.models[0], args.models[1:]
    else:
        existing, proposed = EXISTING_MODEL_PATH, PROPOSED_MODEL_PATHS
    existing, proposed = resolve(existing), [resolve(p) for p in proposed]
    for path in [existing, *proposed]:
        if not path.is_file():
            parser.error(f"IFC file not found: {path}  (set the paths in settings.py or pass them)")

    import ifcopenshell
    print(f"Reading existing model {existing.name} ...")
    existing_elements = CAPT_ELEMENTS(ifcopenshell.open(str(existing)))   # read once for all variants

    failed = []
    for path in proposed:
        print(f"-> {path.stem}")
        try:
            ov = run_variant(existing_elements, existing.name, path, args.results_dir)
        except Exception as error:               # an error is reported, never turned into a zero
            print(f"  FAILED: {error}")
            failed.append(path.name)
            continue
        print(f"  {ov['kgCO2e TOTAL']} kgCO2e, {ov['Cost TOTAL DKK']} DKK, Complete: {ov['Complete']}")
        if ov["Warnings"] != "none":
            print(f"  WARNING: {ov['Warnings']}")

    if failed:
        sys.exit(f"\nFailed variants (no results written for them): {', '.join(failed)}")
    print(f"\nExcel results in {ROOT / 'results' if args.results_dir is None else args.results_dir}")


if __name__ == "__main__":
    main()
