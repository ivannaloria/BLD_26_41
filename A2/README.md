# A2 - BIM Analyst group 41
## A2a: Coding confidence
**Group: 41**

**Confidence in python: 2 - Neutral**

**Focus Area: Build analyst**

## A2b: Identify Claim
**Selected building:** #2604

**Claim / issue to check:**

Cost estimation of new columns for the structural design. 

**Description of the claim:**

The report for building #2604 involves removing non-load-bearing walls and adding new floors, which require new or modified columns. We want to extract and calculate the actual cost of these new structural elements from the BIM model and determine what percentage of the project budget of 35,000 dkk/m² they represent. 

## A2c: Use Case
**How would you check this claim?**

We would check this claim by analysing the structural columns in the IFC model. The user will be able to select the existing columns that need to be modified or replaced, as well as the new columns required for the added floors. Using python, the tool will extract the relevant information for the selected columns, such as dimensions, geometry, material type, and quantities, and combine this information with external cost data provided by the user to estimate their cost. The tool will also extract the floor area from the model to calculate the total project budget based on 35,000 DKK/m². Finally, the structural cost will be divided by the total budget to show what percentage of the project budget the structural elements represent.

**When would this claim need to be checked?**

This claim would need to be checked in the **pre-construction phase**, after an early design for the building has been submitted and cost determination is still in progress. 

**What information does this claim rely on?**

*- Structural data (from IFC model):* columns grouped by type, including dimensions, material type, number of columns, and relevant design properties.

*- Cost data (from user and project report):* Unit costs data is needed to determine the price for each new  element added, considering a project budget of  35,000 DKK/m². 

*- Area data (from IFC model):* Floor area to calculate the total budget. 

**What phase?**

Pre-construction and design phase, before a final budget approval; detailed costs estimates are essential to ensure the project remains within budget. It can also be used in the planning phase for an early cost analysis and estimates. 

**What BIM purpose is required?**

The primary BIM purposes are **Gather and Analyse.** The tool gathers column types from the IFC model of selected columns by the user, as well as the building's floor area. It then analyses this information with unit cost data to estimate the strucutral cost and calculate what percentage of the total budget they represent.
A secondary purpose of the tool would be to **Communicate** (to the project manager, contractors, or clients) how much of the budget is assigned to the selected structural elements. 

## A2d: Scope the Use Code
![BPMN diagram](diagram.svg)

## A2e: Tool idea

Our idea is to develop a tool that automatically calculates the cost of columns from an IFC model. The tool extracts columns, groups them by type, and calculates their dimensions and quantities. The user enters a unit price for each column type and the tool then generates a cost report, enabling to calculate what percentage of the project budget these elements represent.

**Business and societal value**

The value of the tool can be measured directly in monetary value, as the cost estimation can help avoid scenarios in which calculations could be made incorrectly or the building was overdesigned. 

**- Cost accuracy:** Provides precise cost calculations based on the actual BIM model, rather than estimates. 

**- Budget verification:** Shows early in the design phase what share of the budget is taken up by columns. 

**- Efficiency:** Automates cost calculation that would otherwise require manual measurements and estimation.

## A2f: Information Requirements

**What information do we need to extract from the model?**

To perform the cost estimation, the tool needs to access the structural columns contained in the IFC model. For each column type, the tool will extract the information required to determine its quantities and characteristics. 

The following information is required:

*- Element type:* To identify structural columns (`IfcColumn`).

*- Element identification:* To identify each individual column and allow the user to select the columns considered for replacement.

*- Dimensions and geometry:* To determine the size and geometry of each selected column.

*- Material type:* To identify the material associated with each column.

*- Material quantity / volume:* To determine the amount of material required for the selected columns.

*- Replacement information:* To define the characteristics of proposed replacement columns, such as dimensions or new material type.

**Where is this information in IFC?** (to be confirmed)

Columns can be identified using `IfcColumn`.

Each IFC element contains identification information, such as `GlobalId`, which can be used as part of the comparison between the existing and proposed models.

Material information can be obtained through the material associations of the elements, for example through `IfcRelAssociatesMaterial`.

Quantities such as volume can be obtained from IFC quantity sets when available. If the required quantities are not explicitly stored in the model, they can alternatively be calculated from the element geometry.

The **unit cost data is external information** and will therefore not be extracted from the IFC models. It will be entered manually by the user. 

**Is it in the model?**

The structural columns required for the analysis are available in the IFC model. However, the presence and consistency of the required information, particularly dimensions, material information, and volume, will need to be checked.

The tool will retrieve the available columns from the IFC model and allow the user to select the columns that are considered for replacement.

The information describing the proposed replacement, such as the new material or dimensions, will need to be provided by the user or obtained from the proposed design model, depending on the final implementation of the tool.

The unit cost data is not expected to be contained in the IFC model and will therefore be provided by the user.

**Do you know how to get it in IfcOpenShell?**

Partially. We know that IfcOpenShell can be used to retrieve the structural columns from an IFC model. For example:

```python
columns = model.by_type("IfcColumn")
```
## A2g: Identify appropriate software license

**License:** GNU General Public License v3.0 **(GPL-3.0)**


















