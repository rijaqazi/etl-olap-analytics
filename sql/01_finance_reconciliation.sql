/* Read-only diagnostics for the official AdventureWorksDW2019 schema.
   Added for reproduction; not executed during source review.
   AmountAudit is raw fact arithmetic, NOT a financial statement/revenue KPI.
   Review account rollups, scenario scope, and aggregation behavior in SSAS. */
USE AdventureWorksDW2019;
GO
SET NOCOUNT ON;
IF OBJECT_ID(N'dbo.FactFinance',N'U') IS NULL
    THROW 51001, 'Restore and verify AdventureWorksDW2019 before running this query.', 1;

-- Establish scenario keys before applying scenario filters in analysis.
SELECT ScenarioKey, ScenarioName FROM dbo.DimScenario ORDER BY ScenarioKey;

-- This count is the baseline for the cube Fact Finance Count measure.
SELECT COUNT_BIG(*) AS FinanceFactRows FROM dbo.FactFinance;

-- Observe exact scopes instead of combining every scenario into one KPI.
SELECT d.CalendarYear, s.ScenarioKey, s.ScenarioName, a.AccountType,
       COUNT_BIG(*) AS FinanceFactRows,
       SUM(CONVERT(decimal(28,4), f.Amount)) AS AmountAudit
FROM dbo.FactFinance AS f
JOIN dbo.DimDate AS d ON d.DateKey=f.DateKey
JOIN dbo.DimScenario AS s ON s.ScenarioKey=f.ScenarioKey
JOIN dbo.DimAccount AS a ON a.AccountKey=f.AccountKey
GROUP BY d.CalendarYear,s.ScenarioKey,s.ScenarioName,a.AccountType
ORDER BY d.CalendarYear,s.ScenarioKey,a.AccountType;

-- List missing foreign-key targets explicitly. A zero rowset is expected.
SELECT f.FinanceKey,
       CASE WHEN d.DateKey IS NULL THEN 1 ELSE 0 END AS MissingDate,
       CASE WHEN a.AccountKey IS NULL THEN 1 ELSE 0 END AS MissingAccount,
       CASE WHEN s.ScenarioKey IS NULL THEN 1 ELSE 0 END AS MissingScenario,
       CASE WHEN o.OrganizationKey IS NULL THEN 1 ELSE 0 END AS MissingOrganization,
       CASE WHEN g.DepartmentGroupKey IS NULL THEN 1 ELSE 0 END AS MissingDepartment
FROM dbo.FactFinance AS f
LEFT JOIN dbo.DimDate AS d ON d.DateKey=f.DateKey
LEFT JOIN dbo.DimAccount AS a ON a.AccountKey=f.AccountKey
LEFT JOIN dbo.DimScenario AS s ON s.ScenarioKey=f.ScenarioKey
LEFT JOIN dbo.DimOrganization AS o ON o.OrganizationKey=f.OrganizationKey
LEFT JOIN dbo.DimDepartmentGroup AS g ON g.DepartmentGroupKey=f.DepartmentGroupKey
WHERE d.DateKey IS NULL OR a.AccountKey IS NULL OR s.ScenarioKey IS NULL
   OR o.OrganizationKey IS NULL OR g.DepartmentGroupKey IS NULL;
GO
