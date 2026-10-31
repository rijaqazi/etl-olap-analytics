# Finance Analytics report

`FinanceAnalytics.pbix` is the original one-page report, renamed while preserving its binary content. It uses an Analysis Services **live connection** to the existing finance cube. There is no imported DataModel member in the file, so users need a reachable processed cube and must update the original server connection in Desktop.

The five visuals cover department-group Finance Key sums, Amount by account hierarchy, department/organization Amount, organization/ownership finance-record counts, and account detail. The identifier-sum chart is an identified defect and should be replaced before business presentation. Scenario, account rollup, date scope, and financial units require validation.

The source screenshot is historical. This review did not refresh the report or alter the PBIX. See [the technical report](../docs/technical-report.md).
