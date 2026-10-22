"""Measure matching accuracy on the test files in data/.   Run:  python evaluate.py

data/lost_reports.csv   - fake lost reports      (id, category, color, brand, description, location, event_time)
data/found_reports.csv  - fake found reports     (same columns)
data/true_matches.csv   - the correct answers    (lost_id, found_id)

Prints top-1 and top-3 accuracy for three methods, which is the comparison in the proposal:
attribute-only vs text-only vs combined.
"""
import csv
from pathlib import Path

import matching

DATA = Path(__file__).parent / "data"


def read_csv(name):
    with open(DATA / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def accuracy(lost_rows, found_rows, truth, attribute_share, text_share):
    top1 = top3 = 0
    for lost in lost_rows:
        ranked = matching.rank_matches(lost, found_rows, top_n=3,
                                       attribute_share=attribute_share, text_share=text_share)
        ids = [r["found"]["id"] for r in ranked]
        correct = truth.get(lost["id"])
        top1 += bool(ids) and ids[0] == correct
        top3 += correct in ids
    n = len(lost_rows)
    return top1 / n, top3 / n


def main():
    lost_rows = read_csv("lost_reports.csv")
    found_rows = read_csv("found_reports.csv")
    truth = {r["lost_id"]: r["found_id"] for r in read_csv("true_matches.csv")}

    methods = [
        ("Attribute only", 1.0, 0.0),
        ("Text only", 0.0, 1.0),
        ("Combined", None, None),     # uses the shares in config.py
    ]
    print(f"{len(lost_rows)} lost reports, {len(found_rows)} found reports\n")
    print(f"{'Method':<16}{'Top-1':>8}{'Top-3':>8}")
    for name, a, t in methods:
        top1, top3 = accuracy(lost_rows, found_rows, truth, a, t)
        print(f"{name:<16}{top1:>8.0%}{top3:>8.0%}")


if __name__ == "__main__":
    main()
