"""Compatibility adapter for the shared runner; Team 40 source is unchanged.

Team 40's current return dictionary stores model names and GlobalId overlap in
info. The supplied manager expects those three values as top-level keys.
"""

from model_changes.src.team40 import CAPT_ELEMENTS, COMM_EXCEL
from model_changes.src.team40 import analyse as team40_analyse


def analyse(model, existing, names=("existing", "proposed")):
    """Keep all Team 40 results and expose metadata expected by the manager."""
    result = team40_analyse(model, existing, names=names)
    info = {row["Item"]: row["Value"] for row in result["info"]}
    result.update(existing_model=names[0], proposed_model=names[1],
                  shared_ids=float(str(info["Shared GlobalIds"]).rstrip("%")) / 100)
    return result
