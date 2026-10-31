# Data dictionary

## B1 sales sample

One record is an order-like sample sales row. The provided 100 rows have unique Order IDs; this observation does not establish a universal invoice-line grain for a larger source.

| CSV field | Observed meaning | Validation |
| --- | --- | --- |
| Region | Reference to Reigon.csv R_ID | All 100 match; six of seven IDs occur |
| Country | Reference to Country.csv C_ID | All 100 match |
| Item Type | Reference to Product.csv I_ID | All 100 match; display labels are not unique |
| Sales Channel | Reference to Channel.csv S_ID | 50 Offline and 50 Online records |
| Order Date | Order date text | Month/day/year; all parse |
| Order ID | Source sample order identifier | 100 distinct values in 100 rows |
| Ship Date | Shipping date text | All parse; none earlier than order date |
| Units Sold | Numeric quantity | Used with decimal arithmetic for validation totals |
| Unit Price | Numeric unit selling price | Currency not specified |
| Unit Cost | Numeric unit cost | Currency not specified |

Derived sample revenue = Units Sold × Unit Price. Derived cost = Units Sold × Unit Cost. Their difference is sample gross profit arithmetic, not net profit. B1's source, authenticity, currency, and sharing rights are unverified.

Branch and Category contain three generic reference values each. The sales records do not supply fields linking to them. Product has 16 IDs with 12 distinct labels; preserve those IDs rather than merging on a repeated name.

## Finance cube

| Source object | Role |
| --- | --- |
| FactFinance | Financial facts linked to date, organization, department group, scenario, and account |
| FinanceKey | Fact record identifier; inappropriate as a summed business KPI |
| Amount | Financial fact amount; interpret only within validated account, scenario, time, and unit scope |
| Fact Finance Count | Row-count measure for finance-record diagnostics |
| DimAccount | Chart of accounts, account type, parent-child/custom member information |
| DimDate | Calendar attributes; should not expose calendar numbers as useful additive financial measures |
| DimDepartmentGroup | Department group classification |
| DimOrganization | Organization and ownership attributes |
| DimScenario | Scenario classification; select explicitly for comparable financial analysis |

The deployed SQL schema and cube behavior must be verified after restoration/processing. This dictionary describes inspected definitions, not a live database query.
