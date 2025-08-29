import csv, sys, os
os.makedirs(os.path.dirname(sys.argv[2]), exist_ok=True)
inp = sys.argv[1]   # path to SMSSpamCollection
out = sys.argv[2]   # path to ls_sms_unlabeled.csv
with open(inp, encoding="utf-8") as f, open(out, "w", newline="", encoding="utf-8") as g:
    w = csv.writer(g); w.writerow(["id","text"])
    for i, line in enumerate(f, 1):
        parts = line.rstrip("\n").split("\t", 1)
        text = parts[1] if len(parts) == 2 else parts[0]
        w.writerow([f"sms-{i:05d}", text])
print("Wrote", out)
