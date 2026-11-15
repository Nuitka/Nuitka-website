import argparse
import csv
from collections import defaultdict

parser = argparse.ArgumentParser(description="Sum a CSV column per group.")
parser.add_argument("file")
parser.add_argument("--group", default="region")
parser.add_argument("--column", default="amount")
args = parser.parse_args()

totals = defaultdict(float)
with open(args.file, newline="") as f:
    for row in csv.DictReader(f):
        totals[row[args.group]] += float(row[args.column])

for group, total in sorted(totals.items()):
    print(f"{group:<10} {total:>12,.2f}")
