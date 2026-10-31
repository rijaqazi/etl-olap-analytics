# Setup and reproduction

The reviewed source is a historical prototype with generalized connection examples. No edited package has been executed as part of the file review.

## Required tools

- A SQL Server Database Engine instance compatible with the chosen AdventureWorks backup.
- Visual Studio with SQL Server Integration Services Projects for SSIS and Analysis Services Projects for SSAS.
- An SSIS execution runtime and the OLE DB providers used by the packages.
- An SSAS instance running **Multidimensional** mode. A Database Engine instance or a Tabular-only instance cannot replace it.
- Power BI Desktop for the live-connected report.
- Python 3 for the CSV validation tool, which uses the standard library only.

The supplied SSIS source reports product version 16.0.5685.0. Confirm the installed extensions and target runtime before accepting any project upgrade. SQL Native Client 11 and ACE OLE DB 16 are referenced in the saved packages. Provider installation and bitness must match the execution environment; replacing a provider requires a rebuild and runtime test.

## Inputs

Acquire AdventureWorksDW2019 from [Microsoft's official download instructions](https://learn.microsoft.com/en-us/sql/samples/adventureworks-install-configure?view=sql-server-ver16). Restore a database backup through SSMS or an appropriately reviewed RESTORE script; do not use a .bak path as a normal database connection's Initial File Name.

The original locally supplied backup is not published and has not been verified against the official release. There is no need to publish a database backup to showcase the source project.

Keep permitted B1 CSV inputs under `data/b1/` locally. For package examples, the generalized connection paths use `C:\ETLPortfolio\data\b1\`. Copy files there or update all relevant connection managers through Visual Studio. Preserve the six regional subfolders. Do not load both those regional inputs and SalesRecords-ALL.csv into the same fact population.

The other examples also expect files that were not supplied:

| Project | Missing input or prerequisite |
| --- | --- |
| CsvAggregation | `t1 - Sheet1.csv`; the saved destination name is `t2 - Sheet1.csv` |
| SpreadsheetConsolidation | `SRC_1.xlsx`, `SRC_2.xlsx`, and an appropriate `DEST.xlsx` destination/sheet |
| SalesUpsert | `ankara_sales.csv`, `istanbul_sales.csv`, source database/table `sql_source_db.dbo.sales`, and destination `destination.dbo.sales` |
| DimensionalWarehouse | Target table definitions in `StarSchema_DB`; B1 is available locally but not redistributed |

Schema and value assumptions for missing fixtures must be recovered from the original implementation or documented explicitly if new test fixtures are created. Do not label replacement test data as the original inputs.

## SSIS

1. Open the descriptive .sln file within the relevant `ssis/` folder.
2. Review the target server version and provider availability.
3. Configure flat-file/Excel paths and LOCALHOST SQL connection examples for your environment.
4. Export/recreate the **actual** target DDL with keys, constraints, types, and indexes.
5. For DimensionalWarehouse, correct the initial dimension-load and fact-load precedence first. Review how SCD maintenance and initial append loads interact.
6. Run with a controlled fixture, retain rejected rows, record input/output counts, and test a second identical run.

SSIS project protection was changed to DontSaveSensitive for sharing, and user-key verifiers were removed. Supply any required secrets through a local protected configuration or deployment environment. The current source still uses literal example paths; environment parameterization remains future work.

## SSAS

1. Open `ssas/FinanceCube/MultidimensionalProject2.sln`.
2. Configure data sources for the restored AdventureWorksDW2019 catalog and your local SQL provider.
3. Configure the deployment target for your Multidimensional instance. The saved catalog name is `MultidimensionalProject2`, and the cube name is `Adventure Works DW2019_financeview`.
4. Review data-source impersonation. The WarehouseSource example uses the service identity; that identity needs suitable database access configured locally. No account permissions were changed during this review.
5. Build, deploy, and process. Record processing errors and dimension key violations.
6. Run the SQL and MDX diagnostics and review the results against the technical report.

## Power BI

Open `powerbi/FinanceAnalytics.pbix`. It is a live-connected report and retains the original server reference. In Desktop, update the Analysis Services connection to the server and catalog used for the processed cube. The file's original connection was inspected but has not been changed or tested here.

Replace the Finance Key pie chart, add explicit scenario/date controls, and label units before publishing corrected screenshots. A live connection does not mean the ETL itself operates in real time.

## Validation record

Keep input checksums, package build results, row reconciliations, repeat-load tests, cube processing logs, SQL/MDX comparisons, and final report screenshots. The current `reports/` files document the source review and Python file checks only.
