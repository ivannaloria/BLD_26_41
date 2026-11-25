# Danish cost database — units, scope and provenance

Fill `cost_estimate/data/cost_database.xlsx`, sheet `Prices`. Keep all 23 category
names unchanged: they are shared with Team 42's classifier. Both price columns
must use the same `unit` within a category row. Leave unavailable rates empty.

## Sources

[Molio Prisdata](https://molio.dk/produkter/digitale-vaerktojer/prisdata/) provides
Danish trade and building-element rates for construction and renovation. Its
published [price books](https://molio.dk/produkter/boger/prisboger) distinguish
those levels. Access the appropriate licensed item or obtain a contractor quote;
the public product pages do not supply the category rates needed by this tool.

Record the exact source item, edition/date, unit and work scope for every rate.
Do not copy a material-only supplier price into the supply-and-install column
unless the missing installation costs have also been established and documented.
Do not use a whole-house demolition rate for selective structural removal.

Molio's [2024 renovation introduction](https://molio.dk/media/n0cnj2fr/renovering_bygningsdele_brutto_intro.pdf)
describes rates excluding VAT and certain site overheads. This is a methodology
reference, not a source of current project rates: confirm exclusions in the actual
edition and item selected. Do not automatically apply its allowances to this project.

No numeric market rates were entered for this release. Public pages inspected
did not establish comparable supply-and-install and demolition rates for all
the shared material categories. No subscription content or assumed prices has
been substituted.

## Choose units that fit the rate and quantities

| Categories | Practical basis | Conditions |
|---|---|---|
| Concrete C20/25 through C45/55; unspecified concrete | `m3` | Establish whether placement, formwork and reinforcement are included. Strength alone is insufficient to price every element. |
| Precast concrete wall 20 cm | `m2` when rate is per wall area | Must actually be the specified thickness and product; establish delivery and erection scope. |
| Precast hollow-core slabs 22 / 32 cm | `m2` when rate is per floor area | Confirm thickness, span, toppings, delivery and crane/installation scope. |
| Reinforcement steel | Usually quoted per kg or tonne | This tool has no mass input. Do not enter a kg rate as `m3`. A documented conversion is only valid for actual steel volume, not reinforced-concrete volume. |
| Structural steel; welded; hollow section; light profiles | Usually mass-based, or `m` for an exact section | A single per-metre rate cannot cover different profiles. Use only a documented volume conversion or an explicitly scoped section rate. |
| Glulam; CLT; solid timber | `m3`, or `m2` / `m` for a fixed product | Match thickness/section, grade, fabrication and erection scope. |
| Brick; sand-lime brick; aerated concrete; lightweight aggregate block; concrete block | `m2` for fixed wall construction, or documented `m3` | A per-m² rate depends on thickness, finishes and work type. The same material category can occur in multiple elements. |

These are unit choices, not prices or automatic conversions. The supplied
template defaults to `m3`; change a row only when a documented rate supports
the new unit. A broad category may need a better price breakdown before it can
be priced; leave incompatible groups unresolved rather than average rates.

The four supported units are `m3`, `m2`, `m`, `pcs`. For mass-based steel quotes,
a manual conversion would be `DKK/kg × documented kg/m³`, only for the correct
steel volume and pricing scope. Record both the original quote and density
source. The tool performs no density conversion and does not infer reinforcement.

## Record provenance

Required columns remain:

- `price_DKK_per_unit`: construction supply plus installation.
- `demolition_DKK_per_unit`: the agreed selective removal/demolition scope.
- `source`: enough information to locate **both** rates; label construction and
  demolition separately when they come from different sources.
- `verified`: `yes` only after the team has checked units, scope and provenance.

Useful optional columns include `construction_source`, `demolition_source`,
`price_year`, `vat_basis`, `location`, `included_work` and `excluded_work`.
The code carries the shared `source` and `verified` into the results and flags
missing sources/unverified values as price warnings. It can restrict a rate
using optional `ifc_class` and `type_name` columns with exact values.

Use a consistent year, geographical basis and VAT treatment for option
comparisons. Do not label results “excluding VAT” unless all used rates have
been checked on that basis. The module does not adjust inflation, exchange
rates, VAT, contingencies, salvage credits or overheads.

For demolition, establish whether the quote covers dismantling, temporary
support, loading, transport, waste fees and hazardous materials. For new work,
establish delivery, labour, lifting equipment and relevant temporary works.
Avoid charging reinforcement or installation twice when a composite rate already
includes them.
