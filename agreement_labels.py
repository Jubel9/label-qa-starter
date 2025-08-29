#!/usr/bin/env python3
import argparse, csv, json, os
from sklearn.metrics import cohen_kappa_score, confusion_matrix

def load_col(path, fmt, col):
    vals = []
    if fmt == "csv":
        with open(path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                vals.append(row.get(col))
    elif fmt == "jsonl":
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                obj = json.loads(line)
                vals.append(obj.get(col))
    elif fmt == "json":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            data = data.get("tasks", data.get("data", []))
        for obj in data:
            v = obj.get(col)
            if v is None and "." in col:
                top, sub = col.split(".", 1)
                v = (obj.get(top) or {}).get(sub)
            vals.append(v)
    return vals

def detect(path):
    ext = os.path.splitext(path.lower())[1]
    return "csv" if ext==".csv" else "jsonl" if ext==".jsonl" else "json"

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--file-a", required=True)
    ap.add_argument("--file-b")
    ap.add_argument("--col-a", default="label")
    ap.add_argument("--col-b", default="label2")
    args = ap.parse_args()

    fmt_a = detect(args.file_a)
    a = load_col(args.file_a, fmt_a, args.col_a)

    if args.file_b:
        fmt_b = detect(args.file_b)
        b = load_col(args.file_b, fmt_b, args.col_b)
    else:
        b = load_col(args.file_a, fmt_a, args.col_b)

    uniq = sorted(set([x for x in a+b if x is not None]))
    idx = {u:i for i,u in enumerate(uniq)}
    ai = [idx.get(x) for x in a]
    bi = [idx.get(x) for x in b]

    kappa = cohen_kappa_score(ai, bi)
    cm = confusion_matrix(ai, bi, labels=list(range(len(uniq))))
    print("Labels:", uniq)
    print("Cohen's \u03BA:", round(kappa, 3))
    print("Confusion matrix:\n", cm)
