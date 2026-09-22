# A2 - BIM Analyst group 41
## A2a: Coding confidence
**Group: 41**

**Confidence in python: 2 - Neutral**

**Focus Area: Build analyst**

## A2b: Identify Claim
**Selected building:** #2604

**Claim / issue to check:**
Evaluate each column and wall that cannot sustain new loads to decide if it should be reinforced in-place or removed and replaced to find the best option that balances structural performance, budget, and environmental impact. 

**Description of the claim:**
The report for building #2604 states that structural reuse is maximised to limit additional material consumption and reduce embodied carbon, with a CO₂ limit of 40 kg CO₂-eq/m²/year to achieve a DGNB Gold certification. The proposed project of the report involves removing non-load-bearing walls and adding new floors, which create additional loads on existing structural elements. We want to verify, for each structural element that cannot sustain the new loads, whether reinforcing it in-place or replacing it represents the best outcome that meets the sustainability target, structural requirements, and project bugdet simulataneously.

## A2c: Use Case
**How would you check this claim?**
We would check this claim by first analyzing the strcutural data from the Ifc model, identifying all columns and walls. Then we would calculate the new loads and for each inadequate element, create 2 scenarios: reinforce in-place or remove and replace. We would calculate the demolition volume, disposal, labor and material cost, and the embodied carbon. Out of these results, we would create a decision matrix to choose the best outcome for the building´s goals. 

**When would this claim need to be checked?**
This claim would need to be checked in the **early design phase**, when identifying elements that can be problematic.

**What information does this claim rely on?**
*- Structural data:* Existing columns and beams (dimensions, current capacity and reinforcement details).
*- Load data:*
**What phase?**
**What BIM purpose is required?**

