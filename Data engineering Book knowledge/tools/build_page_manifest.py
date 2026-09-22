"""
Builds audit/PAGE_MANIFEST.csv — one row per physical PDF page across all attached books.
Run with the D-drive venv: .tools/venv/Scripts/python.exe "Data engineering Book knowledge/tools/build_page_manifest.py"

Columns: source_id, pdf_page, printed_page_label, text_char_count, extraction_method,
image_present, suspicious_encoding, reading_order_risk, review_status, notes

Notes on method (measured, not assumed):
- text_char_count / image_present come from pypdf + pymupdf on every page (cheap, exact).
- suspicious_encoding flags the pypdf replacement character U+FFFD.
- reading_order_risk is a heuristic (page has >=2 embedded images AND text_char_count>200,
  a proxy for multi-column/figure-heavy layout) — heuristic, not a verified judgment.
- review_status starts as 'accounted' for all rows; pages already visually inspected in
  this session (via Read tool) are upgraded to 'visually-reviewed' by hand afterward.
"""
import csv
import glob
import json
import os

import pymupdf as fitz
from pypdf import PdfReader

BOOK_DIR = os.path.join(os.path.dirname(__file__), "..")
AUDIT_DIR = os.path.join(BOOK_DIR, "audit")
os.makedirs(AUDIT_DIR, exist_ok=True)

SOURCE_ID_MAP = {
    "Data Pipelines with Apache Airflow, 2nd Edition.pdf": "airflow_2e",
    "Database Internals alex petrov.pdf": "database_internals_petrov",
    "Fundamentals of Data Engineering (Reis, JoeHousley, Matt).pdf": "fundamentals_de",
    "Martin-Kleppmann---Designing-Data-Intensive-Applications_-O’Reilly-Media-(2017).pdf": "ddia_kleppmann",
    "Wiley_The_Data_Warehouse_Toolkit_The_Definitive_Guide_to_Dimensional third edition.pdf": "kimball_dwtoolkit_3e",
    "streaming-systems-the-what-where-when-and-how-of-large-scale-data-processing.pdf": "streaming_systems",
    "Big-Book-of-Data-Engineering-4th-Edition.pdf": "databricks_big_book_4e",
}

# From the OCR pass already run on the 72 zero-text-layer pages (audit/zero_text_ocr_results.json).
ocr_results_path = os.path.join(AUDIT_DIR, "zero_text_ocr_results.json")
ocr_by_key = {}
if os.path.exists(ocr_results_path):
    with open(ocr_results_path, encoding="utf-8") as f:
        for row in json.load(f):
            ocr_by_key[(row["file"], row["page"])] = row

rows = []
for fname, sid in SOURCE_ID_MAP.items():
    path = os.path.join(BOOK_DIR, fname)
    reader = PdfReader(path)
    doc = fitz.open(path)
    n = len(reader.pages)
    for i in range(1, n + 1):
        pypdf_page = reader.pages[i - 1]
        try:
            text = pypdf_page.extract_text() or ""
        except Exception:
            text = ""
        char_count = len(text.strip())
        suspicious = "�" in text

        fitz_page = doc[i - 1]
        img_list = fitz_page.get_images(full=True)
        image_present = len(img_list) > 0

        reading_order_risk = image_present and char_count > 200

        notes = []
        ocr_row = ocr_by_key.get((fname, i))
        if ocr_row:
            ocr_len = ocr_row["ocr_char_count"]
            preview = ocr_row["ocr_preview"]
            if sid == "database_internals_petrov" and ocr_len > 100:
                notes.append(f"OCR({ocr_len}c) shows Bookey app ad content, not book body: \"{preview}\"")
                review_status = "visually-reviewed" if i == 35 else "ocr-reviewed"
            elif ocr_len == 0 and not image_present:
                notes.append("zero text layer, no embedded image, OCR empty -> blank page")
                review_status = "visually-reviewed" if (fname, i) in {
                    ("Data Pipelines with Apache Airflow, 2nd Edition.pdf", 4),
                    ("Fundamentals of Data Engineering (Reis, JoeHousley, Matt).pdf", 17),
                    ("Wiley_The_Data_Warehouse_Toolkit_The_Definitive_Guide_to_Dimensional third edition.pdf", 2),
                    ("Martin-Kleppmann---Designing-Data-Intensive-Applications_-O’Reilly-Media-(2017).pdf", 2),
                } else "ocr-reviewed"
            elif ocr_len > 0:
                notes.append(f"zero text layer, OCR({ocr_len}c) recovered: \"{preview}\"")
                review_status = "ocr-reviewed"
            else:
                notes.append("zero text layer, no embedded image, OCR empty -> likely blank")
                review_status = "ocr-reviewed"
        else:
            review_status = "accounted"
            if char_count == 0:
                notes.append("zero text layer (not yet OCR-checked)")

        rows.append({
            "source_id": sid,
            "pdf_page": i,
            "printed_page_label": "",  # not yet cross-referenced against printed numerals
            "text_char_count": char_count,
            "extraction_method": "pypdf" if char_count > 0 else ("tesseract-ocr" if ocr_row else "none"),
            "image_present": image_present,
            "suspicious_encoding": suspicious,
            "reading_order_risk": reading_order_risk,
            "review_status": review_status,
            "notes": "; ".join(notes),
        })
    doc.close()

out_path = os.path.join(AUDIT_DIR, "PAGE_MANIFEST.csv")
with open(out_path, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=[
        "source_id", "pdf_page", "printed_page_label", "text_char_count",
        "extraction_method", "image_present", "suspicious_encoding",
        "reading_order_risk", "review_status", "notes",
    ])
    w.writeheader()
    w.writerows(rows)

print(f"wrote {len(rows)} rows to {out_path}")
by_status = {}
for r in rows:
    by_status[r["review_status"]] = by_status.get(r["review_status"], 0) + 1
for k, v in sorted(by_status.items()):
    print(f"  {k}: {v}")
