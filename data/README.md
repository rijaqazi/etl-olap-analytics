# Data sources and handling

## B1

B1 was supplied with the existing project. Its original source, currency, and redistribution license are unknown. The author confirms ownership of the project code but cannot confirm B1's provenance. Raw B1 files are excluded from the public project.

Expected local files: Branch.csv, Category.csv, Channel.csv, Country.csv, Product.csv, Reigon.csv, SalesRecords-ALL.csv, and R1/R1.csv through R6/R6.csv. The original spelling `Reigon.csv` is preserved because the existing package references it.

The consolidated file and regional files describe the same 100-record sales population. They are alternatives for validation/loading, not additive sources. Region, country, product, and channel values are lookup IDs. Product labels repeat under different IDs. There is no customer identifier, source currency, or Branch/Category key in the sales rows.

## AdventureWorks

Download AdventureWorksDW2019 through [Microsoft's official documentation](https://learn.microsoft.com/en-us/sql/samples/adventureworks-install-configure?view=sql-server-ver16) or its linked [SQL Server samples release](https://github.com/microsoft/sql-server-samples/releases/tag/adventureworks). It is a sample database, not a real company's supplied operating database. Retain the relevant Microsoft license/attribution notices.

The locally supplied .bak is excluded and has not been restored or checksum-matched to an official release during this review.

## Other demonstration fixtures

The smaller SSIS examples reference CSV and XLSX inputs not contained in the supplied three folders. See [setup](../docs/setup.md). Recover those inputs or clearly label new replacement test fixtures before claiming full reproducibility.
