#!/usr/bin/env python3
import argparse, csv, json, os, sys
from collections import Counter

def iter_records(path, fmt, text_col, label_col, id_col):
    if fmt == "csv":
        with open(path, newline="", encoding="utf-8") as f:
            rdr = csv.DictReader(f)
            for i, row in enumerate(rdr, 2):
                yield i, { "id": row.get(id_col), "text": row.get(text_col), "label": row.get(label_col) }
    elif fmt == "jsonl":
        with open(path, "r", encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                s = line.strip()
                if not s:
                    yield i, None; continue
                try:
                    obj = json.loads(s)
                except json.JSONDecodeError:
                    yield i, None; continue
                yield i, { "id": obj.get(id_col), "text": obj.get(text_col), "label": obj.get(label_col) }
    elif fmt == "json":
        with open(path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                raise SystemExit("ERROR: bad JSON file")
        if isinstance(data, dict):
            data = data.get("tasks", [])
        for idx, obj in enumerate(data, 1):
            text = obj.get(text_col)
            if text is None and "." in text_col:
                top, sub = text_col.split(".", 1)
                text = (obj.get(top) or {}).get(sub)
            yield idx, { "id": obj.get(id_col), "text": text, "label": obj.get(label_col) }
    else:
        raise SystemExit(f"Unsupported format: {fmt}")

def detect_format(path, explicit):
    if explicit:
        return explicit
    ext = os.path.splitext(path.lower())[1]
    if ext == ".csv": return "csv"
    if ext == ".jsonl": return "jsonl"
    if ext == ".json": return "json"
    return "csv"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", required=True)
    ap.add_argument("--format", choices=["csv","json","jsonl"])
    ap.add_argument("--id-col", default="id")
    ap.add_argument("--text-col", default="text")
    ap.add_argument("--label-col", default="label")
    ap.add_argument("--max-errors", type=int, default=10)
    args = ap.parse_args()

    fmt = detect_format(args.path, args.format)
    errors, ids = [], Counter()
    total = 0

    for lineno, rec in iter_records(args.path, fmt, args.text_col, args.label_col, args.id_col):
        total += 1
        if rec is None:
            errors.append((lineno, "parse error"))
            continue
        rid, txt, lab = rec["id"], rec["text"], rec["label"]
        if rid in (None, ""): errors.append((lineno, "missing id"))
        if txt in (None, ""): errors.append((lineno, "empty text"))
        if lab in (None, ""): errors.append((lineno, "empty label"))
        ids[rid] += 1

    dup_ids = [k for k,c in ids.items() if k not in (None,"") and c>1]
    print(f"Format: {fmt}")
    print(f"Total rows: {total}")
    print(f"Unique ids: {len([k for k in ids if k not in (None,'')])}")
    print(f"Duplicate ids: {len(dup_ids)}")
    if dup_ids: print("First duplicate ids:", dup_ids[:5])
    print(f"Errors found: {len(errors)}")
    for ln, msg in errors[:args.max_errors]:
        print(f"Line {ln}: {msg}")
    sys.exit(1 if errors or dup_ids else 0)

if __name__ == "__main__":
    main()
