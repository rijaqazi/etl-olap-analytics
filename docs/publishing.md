# Publication checklist

Suggested repository: **etl-olap-analytics**. This folder is separate from the existing sales dashboard portfolio.

Include the native `ssis`, `ssas`, and `powerbi` sources, documentation, validation tools, selected screenshots, and measured review outputs. Do not copy the three original Downloads folders directly into GitHub.

Before publishing:

- Review the technical report and setup requirements before publishing; describe the implementation and validation status accurately.
- Keep raw B1 inputs, the backup, original PDFs, `.vs`, bin, obj, .user files, and compiled builds out of the repository. The .gitignore covers these generated/local items.
- Keep Microsoft attribution. B1 redistribution remains unresolved and raw files are intentionally absent.
- Rebind the PBIX in Desktop if replacing its original live server reference. This preparation renamed the binary file without editing its internal connection.
- Select a license for your original code if desired. This does not establish rights over third-party data.

Create an empty repository under your own GitHub account, open this folder alone in VS Code, initialize its own Git repository, review/stage the intended files, commit, and publish. Do not initialize the parent workspace or overwrite the existing sales dashboard repository.

Suggested description: `SSIS data integration and dimensional loading with an AdventureWorks SSAS finance cube, MDX exploration, and a Power BI live report.`

Suggested topics: `ssis`, `ssas`, `sql-server`, `etl`, `data-warehousing`, `mdx`, `power-bi`.

After publication, verify native solution references, PBIX download, README images, documentation links, and dataset instructions from a fresh clone. A GitHub file listing alone does not establish that the pipeline builds or runs.
