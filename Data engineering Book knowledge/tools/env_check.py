"""
Environment sanity check for the DE Master Library extraction pipeline.
Run with the D-drive venv: .tools/venv/Scripts/python.exe tools/env_check.py

Everything (venv, pip cache, tesseract binary) lives under
D:\\Obsidian\\Data Engineering Learn\\.tools\\ — nothing touches C:.
"""
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TESSERACT_EXE = os.path.join(PROJECT_ROOT, ".tools", "tesseract", "tesseract.exe")

import pytesseract  # noqa: E402
pytesseract.pytesseract.tesseract_cmd = TESSERACT_EXE

import fitz  # pymupdf  # noqa: E402
import pdfplumber  # noqa: E402
from pypdf import PdfReader  # noqa: E402

if __name__ == "__main__":
    print("python:", sys.executable)
    print("pymupdf:", fitz.__doc__ and fitz.VersionBind)
    print("pdfplumber: ok")
    print("pypdf: ok")
    print("tesseract_cmd:", TESSERACT_EXE, "exists:", os.path.exists(TESSERACT_EXE))
    print("tesseract version:", pytesseract.get_tesseract_version())
