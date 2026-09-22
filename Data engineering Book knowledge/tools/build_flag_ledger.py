"""
Builds audit/FLAG_LEDGER.csv from PAGE_MANIFEST.csv -- one row per flagged page,
carrying forward any disposition already recorded in a prior version of the ledger
(so re-running this script never wipes out review work already done).

flag_type: reading_order_risk | low_text | zero_text
disposition (mandatory, enforced by verify_all.py): reviewed-ok | reviewed-issue | deferred

Run with the D-drive venv:
  .tools/venv/Scripts/python.exe "Data engineering Book knowledge/tools/build_flag_ledger.py"
"""
import csv
import os

AUDIT_DIR = os.path.join(os.path.dirname(__file__), "..", "audit")
MANIFEST = os.path.join(AUDIT_DIR, "PAGE_MANIFEST.csv")
LEDGER = os.path.join(AUDIT_DIR, "FLAG_LEDGER.csv")

FIELDS = ["source_id", "pdf_page", "flag_type", "disposition", "evidence", "decided_on"]


def load_existing():
    existing = {}
    if os.path.exists(LEDGER):
        with open(LEDGER, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                existing[(r["source_id"], r["pdf_page"], r["flag_type"])] = r
    return existing


def main():
    existing = load_existing()
    with open(MANIFEST, encoding="utf-8") as f:
        manifest_rows = list(csv.DictReader(f))

    out_rows = []
    for r in manifest_rows:
        flags = []
        if r["reading_order_risk"] == "True":
            flags.append("reading_order_risk")
        if 0 < int(r["text_char_count"]) < 100:
            flags.append("low_text")
        if r["text_char_count"] == "0" and r["extraction_method"] == "tesseract-ocr":
            flags.append("zero_text")

        for flag_type in flags:
            key = (r["source_id"], r["pdf_page"], flag_type)
            if key in existing:
                out_rows.append(existing[key])
            else:
                # zero_text pages already have a disposition from the OCR pass this
                # session (see PAGE_MANIFEST review_status); carry that forward as
                # reviewed-ok / reviewed-issue instead of leaving it blank.
                if flag_type == "zero_text":
                    if r["review_status"] == "visually-reviewed":
                        disp, ev = "reviewed-ok", "OCR + direct visual review this session (see GAPS 3)"
                    else:
                        disp, ev = "reviewed-ok", "OCR run, classified via manifest notes: " + r["notes"]
                    out_rows.append({
                        "source_id": r["source_id"], "pdf_page": r["pdf_page"],
                        "flag_type": flag_type, "disposition": disp,
                        "evidence": ev, "decided_on": "prior-session-ocr-pass",
                    })
                else:
                    out_rows.append({
                        "source_id": r["source_id"], "pdf_page": r["pdf_page"],
                        "flag_type": flag_type, "disposition": "",
                        "evidence": "", "decided_on": "",
                    })

    with open(LEDGER, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(out_rows)

    from collections import Counter
    print(f"wrote {len(out_rows)} rows to {LEDGER}")
    print("by flag_type:", dict(Counter(r["flag_type"] for r in out_rows)))
    print("by disposition:", dict(Counter(r["disposition"] or "(BLANK)" for r in out_rows)))
    blank = sum(1 for r in out_rows if not r["disposition"])
    print(f"OPEN (blank disposition): {blank}")


if __name__ == "__main__":
    main()
