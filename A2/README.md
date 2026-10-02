# A2 - BIM Analyst group 41
## A2a: Coding confidence
**Group: 41**

**Confidence in python: 2 - Neutral**

**Focus Area: Build analyst**

## A2b: Identify Claim
**Selected building:** #2604

**Claim / issue to check:**

Cost estimation of new columns and load-bearing walls for the structural design. 

**Description of the claim:**

The report for building #2604 involves removing non-load-bearing walls and adding new floors, which require new or modified columns and load-bearing walls. We want to extract and calculate the actual cost of these new structural elements from the BIM model and to later verify the project budget of 35,000 dkk/m².

## A2c: Use Case
**How would you check this claim?**

We would check this claim by first analyzing the strcutural data from the Ifc model, and identifying new columns and load-bearing walls. We would extract their dimensions, material types, and quantities. 

**When would this claim need to be checked?**

This claim would need to be checked in the **pre-construction phase**, after an early design for the building has been submitted and cost determination is still in progress. 

**What information does this claim rely on?**

*- Structural data (from IFC model):* new columns and load-bearing walls, including dimensions, material type, quantities, and relevant design properties.

*- Cost data (from product datasheet):* Unit costs data is needed to determine the price for each new  element added.

**What phase?**

Pre-construction and design phase, before a final budget approval; detail costs estimates are essential to ensure the project remains within budget. It can also be used in the planning phase for an early cost analysis and estimates. 

**What BIM purpose is required?**

The primary BIM purpose is **Quantity Take-off and Cost Estimation** to extract column and wall dimensions from the IFC model and calculate total construction cost. A secondary purpose of the tool would be to communicate (to the project manager, contractors, or clients) the comparison of the generated costs against the project building constraint. 

## A2d: Scope the Use Code
![BPMN diagram](diagram.svg)

## A2e: Tool idea

Our idea is to develop a tool that automatically calculates the cost of new columns and load-bearing walls from an IFC model. The tool extracts structural elements, calculates their dimensions and quantities, and applies unit costs to determine total material expenses. The tool generates a cost report for structural elements, enabling verification against the project budget of 35,000 dkk/m².

**Business and societal value**

The value of the tool can be measured directly in monetary value, as the cost estimation can help avoid scenarios in which calculations could be made incorrectly or the building was overdesigned. 

**- Cost accuracy:** Provides precise cost calculations based on the actual BIM model, rather than estimates. 

**- Budget verification:** Confirms structural costs align with the budget constraint early in the design phase.

**- Efficiency:** Automates cost calculation that would otherwise require manual measurements and estimation.










