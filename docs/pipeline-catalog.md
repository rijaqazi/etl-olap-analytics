# Pipeline catalog

| Project | Native source | Inputs | Transformation and output | Runtime status |
| --- | --- | --- | --- | --- |
| CsvAggregation | `ssis/CsvAggregation/Package.dtsx` | One CSV | Aggregate to Flat File Destination | Missing original input; edited source not executed |
| SpreadsheetConsolidation | `ssis/SpreadsheetConsolidation/Package.dtsx` | Two Excel worksheets | Union All, Aggregate, Excel Destination | Missing workbooks/template; edited source not executed |
| SalesUpsert | `ssis/SalesUpsert/Package.dtsx` | Two CSVs plus `sql_source_db.dbo.sales` | Union All, Aggregate, Lookup, update/insert into `destination.dbo.sales` | Missing fixtures/DDL; edited source not executed |
| DimensionalWarehouse | `ssis/DimensionalWarehouse/Package.dtsx` | Six reference CSVs and R1–R6 sales inputs | Direct dimension loads, SCD attribute processing, conversions, four lookups, fact insert | B1 files profiled; original DDL absent and sequencing needs correction |
| FinanceCube | `ssas/FinanceCube/` | AdventureWorksDW2019 | Account/date/department/organization/scenario dimensions, finance and date measure groups | Source reviewed; deployment/processing not repeated |
| FinanceAnalytics | `powerbi/FinanceAnalytics.pbix` | Live SSAS connection | Five visuals on one report page | Original layout inspected; connection not refreshed |

## Known source references

DimensionalWarehouse names `dbo.Branch`, `dbo.Category`, `dbo.CHANNEL_1`, `dbo.Country`, `dbo.Product`, `dbo.Region`, and `dbo.FactTable_Sales` in connection/component metadata. This is not a substitute for actual CREATE TABLE definitions.

The sales lookup flow uses Country, Region, Product, and Channel. Branch and Category reference files exist, but the supplied sales records have no Branch/Category foreign-key fields. Do not invent those relationships from names alone. No customer dimension is present.

## Source preparation boundaries

Project filenames and labels were renamed consistently. Machine-specific editable connections were generalized, sensitive user-key verifiers removed, and native XML parsing checked. Original source and historical screenshots remain the evidence for behavior; package builds, execution ordering fixes, provider upgrades, parameterization, and performance improvements are not claimed as completed.
