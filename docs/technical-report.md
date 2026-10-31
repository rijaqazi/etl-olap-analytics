# ETL and OLAP Analytics: technical report

## Purpose

Demonstrate file and SQL data integration, dimensional loading, and multidimensional finance analysis using SSIS, SQL Server, SSAS, and Power BI. This report describes the saved implementation and its limits. It replaces a procedural task narrative with an engineering description grounded in the source files.

## Integration track

Four SSIS projects are included. CsvAggregation uses a Flat File Source, Aggregate, and Flat File Destination. SpreadsheetConsolidation combines two Excel sources with Union All, aggregates the result, and writes an Excel destination. This is row concatenation followed by aggregation, not a Merge Join.

SalesUpsert reads two CSV sources and a separate SQL source table. Union All and Aggregate produce product totals. A Lookup checks the destination table, routing matches to `UPDATE dbo.sales SET totalSales = ? WHERE product = ?` and nonmatches to an INSERT command. The source SQL database is separate from the destination. Whether its rows overlap the CSVs is not documented, so input overlap must be tested rather than assumed.

DimensionalWarehouse includes direct loads of Branch, Category, Channel, Country, Product, and Region reference data. It also contains six Slowly Changing Dimension components and a sales flow that unions six regional files, converts types, performs four lookups, and writes FactTable_Sales.

The saved control flow has one precedence constraint from the fact-loading flow (`Data Flow Task 1`) to the SCD flow (`Data Flow Task`). The initial reference-data load (`Loading Data into SQL Server`) is not connected to this sequence. This does not reliably enforce dimension loading before fact lookup processing. Correct the sequence and choose either a controlled initial-load path or a repeatable dimension-maintenance path before running against an empty target.

The original destination DDL is absent. Source component metadata identifies table/column names but does not prove the deployed keys, constraints, indexes, or slowly changing history design. Historical screenshots document loading and an attribute-change demonstration; they do not establish complete Type 2 history tracking.

## File-level validation

The consolidated B1 sample has 100 sales rows and 100 distinct order IDs. Regional file counts are 11, 11, 7, 22, 10, and 39. A multiset comparison confirms that their union matches the consolidated sample, without adding or dropping rows. Loading both versions together would duplicate the same source population.

Order dates parse as month/day/year and range from 2010-02-02 through 2017-05-22. All ship dates parse; none precedes its order date. There are no missing values or exact duplicate rows in the supplied CSV files. All sales references match the provided region, country, product, and channel ID lookups.

The lookup files contain 7 regions, 76 countries, 16 product IDs, 2 channels, 3 branches, and 3 category labels. Four product labels repeat under different IDs. Keep IDs as keys; duplicate display labels are not evidence that records should be deleted. Region ID 7 has no observed sales in this sample. That is a coverage fact, not a data-loss conclusion.

Revenue arithmetic from the sample is 137,348,768.31; cost is 93,180,569.91; their difference is 44,168,198.40 in unspecified source monetary units. These are Python-derived sample controls, not executed SQL totals or verified company revenue. Currency is absent. The source, authenticity, and redistribution rights of B1 remain unverified.

## Finance OLAP track

The SSAS project models AdventureWorksDW2019 finance data. Its five dimensions are Account, Date, Department Group, Organization, and Scenario. The Fact Finance measure group contains Amount, Finance Key, and Fact Finance Count. A second measure group exposes date attributes as numeric measures and Dim Date Count.

Amount is the financial field. Finance Key identifies fact records and is not a useful summed business KPI. Date numbers and calendar years also should not be offered as additive business measures. Review account-specific aggregation, parent-child account rollups, unary/custom member behavior, scenario scope, and time behavior before interpreting financial totals. Summing every account and scenario is not automatically revenue, profit, or a valid financial statement total.

The saved cube has no MdxScript element. Original screenshot evidence demonstrates exploratory queries, including slicing/subselects, aggregation, ordering, and ranking. Standalone original query files are absent. The examples in `mdx/` are newly reconstructed diagnostic queries and have not been executed in the current environment. YTD/QTD calculations and a suitable typed calendar hierarchy still require implementation and validation if they are to be advertised.

## Power BI

FinanceAnalytics.pbix is the supplied report, renamed without changing its binary content. Its saved Connections entry is `analysisServicesDatabaseLive`, pointing at the original SSAS server and catalog. The file has no imported DataModel member. It therefore requires a reachable, deployed and processed cube; it is not a self-contained imported dashboard.

The report has one page and five visuals: a Finance Key pie chart by department group, Amount by an account hierarchy level, Amount by department and organization, a finance-row-count donut by organization/ownership, and an account table. The screenshot contains live results from the original environment. It does not prove the connection can be refreshed now.

The strongest redesign would replace identifier sums with validated Amount or record-count measures, use a clear financial question, require a Scenario selection, label the date range and units, and replace crowded pies with ranked bars or a matrix. Business insights should follow a fresh SQL-to-cube-to-visual reconciliation.

## Documentation corrections

| Earlier narrative | Evidence-based description |
| --- | --- |
| Multiple CSVs merged using Merge Join and Derived Column | The saved two-source example reads Excel and uses Union All plus Aggregate. |
| CSV-to-SQL example is a simple bulk load | The saved package also reads SQL and uses Lookup with row-by-row update/insert commands. |
| Dimensions include customers | No customer source or customer dimension is present in the reviewed files. |
| OLAP cube analyzes product sales | The saved cube models finance accounts, departments, organizations, dates, and scenarios. |
| Power BI imports cube data | The saved PBIX uses a live SSAS connection. |
| Daily/hourly automation is established | Agent is discussed and historical service/deployment evidence exists, but a job/schedule export is absent. |
| All multidimensional functions and YTD/QTD are validated | Selected query screenshots exist; exhaustive function coverage and time calculations are not established. |
| Real-time, scalable analytics | A historical prototype is demonstrated; latency, volume, performance, and scheduling guarantees were not measured. |

## Preparation changes

SSIS project labels were made descriptive; relative solution references were updated. Editable personal machine names and paths were replaced with example connections. User-specific sensitive project verifiers were removed, and SSIS protection was set to DontSaveSensitive. SSAS data-source examples now use a database catalog rather than treating a backup path as a live data source. A named impersonation account was removed; the intended runtime service identity must be configured and granted appropriate read access locally.

These are source preparation changes, not a new successful deployment. Original files in Downloads were not overwritten. Academic cover pages, personal registration details, the original PDFs, local caches, compiled builds, and the database backup are not in the publication folder. Microsoft notices in source components remain intact.

## Validation boundary

Completed: CSV profiling and reconciliation, XML parsing, native project-file reference checks, PBIX layout/connection inspection, and visual review of historical document evidence. Not completed: restoring the supplied backup, opening/building the edited solutions in Visual Studio, executing SSIS, deploying/processing SSAS, refreshing the live PBIX, or validating scheduling and business totals in the current environment.

## References

- [Microsoft AdventureWorks sample databases](https://learn.microsoft.com/en-us/sql/samples/adventureworks-install-configure?view=sql-server-ver16)
- [SSAS aggregate functions and ByAccount behavior](https://learn.microsoft.com/en-us/analysis-services/multidimensional-models/use-aggregate-functions?view=sql-analysis-services-2025)
- [SSAS finance account dimensions](https://learn.microsoft.com/en-us/analysis-services/multidimensional-models/database-dimensions-finance-account-of-parent-child-type?view=sql-analysis-services-2025)
