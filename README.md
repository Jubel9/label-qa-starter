# label-qa-starter
![CI](https://github.com/Jubel9/label-qa-starter/actions/workflows/ci.yml/badge.svg)
Minimal tools to QA text classification labels exported from *Label Studio*.

## Structure
```
label-qa-starter/
├─ data/
│  ├─ raw/
│  │  └─ SMSSpamCollection        # original UCI TSV (label<TAB>text)
│  ├─ ls_sms_unlabeled.csv        # derived id,text for Label Studio import
│  ├─ ls_export_v1_r1.csv         # 1st pass labels (ham/spam/unclear)
│  ├─ ls_export_v1_r2.csv         # 2nd pass labels (independent pass)
│  ├─ ls_export_sample.csv        # tiny demo file for validator
│  └─ ls_export_sample_v2.csv     # tiny demo + label2 for κ demo
├─ tools/
│  └─ sms_to_csv.py               # converts UCI TSV → id,text CSV (no labels)
├─docs/
│  └─ quality_notes.md            # Notes for quality of the annotation
├─ examples/
│  └─ README.md                   # Worked examples (with rationales)
├─ validate_labels.py             # CSV/JSON/JSONL validator (schema/dupes/empties)
├─ agreement_labels.py            # Cohen’s κ + confusion matrix
├─ requirements.txt               # scikit-learn
├─ RUBRIC.md                      # Label definition, decision rules, tie-breakers, and edge-cases
└─ README.md
```

## Setup
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Validate a Label Studio CSV export
```bash
python validate_labels.py --path data/ls_export_sample.csv --format csv --id-col id --text-col text --label-col label
```

## Compute Cohen's κ (same file two columns)
```bash
python agreement_labels.py --file-a data/ls_export_sample_v2.csv --col-a label --col-b label2
```

## Compute Cohen's κ (two files)
```bash
python agreement_labels.py --file-a data/ls_export_sample.csv --file-b data/ls_export_sample_v2.csv --col-a label --col-b label
```

## CSV Schema
Required columns: id,text,label (optional: label2 for second pass).

## Notes
- Change `--label-col` if your project uses a different `from_name` (e.g., `sentiment`).
- Exported file can be **CSV**, **JSON**, or **JSONL** (API). This tool supports all three.

## Dataset
SMSSpamCollection (https://archive.ics.uci.edu/dataset/228/sms%2Bspam%2Bcollection)

## Result
*Aug 29, 2025 (JST)*
- items: 800/5574 (SMSSpamCollection)
- label set: ["ham","spam","unclear"]
- κ = 0.967
- confusion matrix:
    [[670   0   0]
    [  2 121   0]
    [  5   0   2]]
    rater A class counts: ham=670, spam=123, unclear=7 (sums of matrix rows).
- Edge cases:
    1. Some messages have “…” in the middle, which causes confusion; this might be due to truncation or because the original message actually contains ellipses.
    2. Some advertising messages are convincing enough to be overlooked as `ham`; if not read carefully, they may be mistakenly labeled as `ham`.
    3. Some messages are not identifiable as correct English, probably because they were sent long ago and use slang, causing misunderstanding of the meaning of the words.