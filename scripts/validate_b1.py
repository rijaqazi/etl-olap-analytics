"""Read-only validation of locally supplied B1 CSVs. Standard library only.

This profiles the provided sample; it does not establish data provenance,
currency, database constraints, package execution, or redistribution rights.
"""
from pathlib import Path
from collections import Counter
from datetime import datetime
from decimal import Decimal, InvalidOperation
import argparse
import csv
import hashlib
import json


def read_csv(path):
    with path.open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        rows = list(reader)
        if any(None in row or any(v is None for v in row.values()) for row in rows):
            raise ValueError(f'Malformed CSV row width: {path.name}')
        return reader.fieldnames, rows


def validate(root):
    if not (root / 'SalesRecords-ALL.csv').exists() and (root / 'B1').is_dir():
        root = root / 'B1'
    lookup_files = {'region': ('Reigon.csv', 'R_ID'), 'country': ('Country.csv', 'C_ID'),
                    'product': ('Product.csv', 'I_ID'), 'channel': ('Channel.csv', 'S_ID'),
                    'branch': ('Branch.csv', 'B_ID'), 'category': ('Category.csv', 'C_ID')}
    files = [root / name for name, _ in lookup_files.values()]
    files += [root / 'SalesRecords-ALL.csv'] + [root / f'R{i}/R{i}.csv' for i in range(1, 7)]
    missing = [p.relative_to(root).as_posix() for p in files if not p.exists()]
    if missing:
        raise FileNotFoundError('Required local sample files are missing: ' + ', '.join(missing))
    tables = {}; profiles = {}
    for path in files:
        headers, data = read_csv(path)
        name = path.relative_to(root).as_posix()
        tables[name] = data
        profiles[name] = {'rows': len(data), 'columns': headers,
            'missing_values': sum(not v.strip() for row in data for v in row.values()),
            'exact_duplicate_excess': len(data)-len({tuple(row.items()) for row in data}),
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
    rows = tables['SalesRecords-ALL.csv']
    required = {'Region', 'Country', 'Item Type', 'Sales Channel', 'Order Date',
                'Order ID', 'Ship Date', 'Units Sold', 'Unit Price', 'Unit Cost'}
    if not required.issubset(profiles['SalesRecords-ALL.csv']['columns']):
        raise ValueError('Sales header does not match the documented sample schema.')
    regional = [row for i in range(1, 7) for row in tables[f'R{i}/R{i}.csv']]
    lookup_keys = {kind: {row[key] for row in tables[name]} for kind, (name, key) in lookup_files.items()}
    duplicate_lookup_ids = {kind: len(tables[name])-len(lookup_keys[kind]) for kind, (name, key) in lookup_files.items()}
    orphans = {kind: sum(row[column] not in lookup_keys[kind] for row in rows)
               for kind, column in [('region', 'Region'), ('country', 'Country'),
                                    ('product', 'Item Type'), ('channel', 'Sales Channel')]}
    dates = []; earlier = 0; invalid_dates = 0; invalid_numeric = 0
    revenue = Decimal(0); cost = Decimal(0)
    for row in rows:
        try:
            order = datetime.strptime(row['Order Date'], '%m/%d/%Y').date()
            ship = datetime.strptime(row['Ship Date'], '%m/%d/%Y').date()
            dates.append(order); earlier += ship < order
        except ValueError:
            invalid_dates += 1
        try:
            units = Decimal(row['Units Sold']); price = Decimal(row['Unit Price']); unit_cost = Decimal(row['Unit Cost'])
            if not all(x.is_finite() for x in (units, price, unit_cost)):
                raise InvalidOperation
            revenue += units * price; cost += units * unit_cost
        except (ValueError, InvalidOperation):
            invalid_numeric += 1
    same = Counter(tuple(row.items()) for row in rows) == Counter(tuple(row.items()) for row in regional)
    unique_orders = len({row['Order ID'] for row in rows})
    passed = (same and not invalid_dates and not invalid_numeric and not earlier
              and not any(orphans.values()) and not any(duplicate_lookup_ids.values())
              and unique_orders == len(rows)
              and not any(p['missing_values'] or p['exact_duplicate_excess'] for p in profiles.values()))
    result = {'status': 'PASS' if passed else 'REVIEW', 'sales_rows': len(rows),
        'regional_rows': len(regional), 'regional_multiset_equals_all': same,
        'distinct_order_ids': unique_orders, 'duplicate_lookup_ids': duplicate_lookup_ids,
        'foreign_key_orphans': orphans, 'invalid_dates': invalid_dates,
        'ship_before_order': earlier, 'invalid_numeric_rows': invalid_numeric,
        'order_date_min': str(min(dates)) if dates and not invalid_dates else None,
        'order_date_max': str(max(dates)) if dates and not invalid_dates else None,
        'revenue_source_units': str(revenue) if not invalid_numeric else None,
        'cost_source_units': str(cost) if not invalid_numeric else None,
        'gross_profit_source_units': str(revenue-cost) if not invalid_numeric else None,
        'currency': 'Not specified', 'provenance': 'Unverified supplied sample', 'files': profiles}
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = validate(args.data_root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(f"{result['status']}: {result['sales_rows']} sales rows; {result['regional_rows']} regional rows; output {args.output}")
    raise SystemExit(0 if result['status'] == 'PASS' else 1)
