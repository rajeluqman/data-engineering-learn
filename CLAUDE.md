# CLAUDE.md — SQL Learning Vault

> Auto-loaded context untuk Claude Code sessions. Jangan delete.

---

## 🎯 Goal

Belajar SQL dari beginner sampai DE-level. Target: boleh handle real project — data warehouse, incremental load, platform SQL (Databricks/Snowflake).

---

## 📂 Vault Structure

```
vault/sql/
  notes/          ← Isi content di sini setiap session
  problems/       ← Practice queries
  quiz/
    checkpoints/  ← Post-module drill files
    html/         ← Interactive quiz
  
vault/state/
  progress-sql.md ← Update setiap hujung session
  handoff-sql.md  ← Update setiap hujung session

shared/
  dialect-map.md
  errors-gotchas.md
  glossary.md
```

---

## 📚 Sources

| Module | Topic | Source | Timestamp |
|--------|-------|--------|-----------|
| M0 | Orientation | Baraa — Master SQL with Data | 07:38 |
| M1 | DQL Core | Baraa | 34:01 |
| M2 | DDL/DML + Keys | Baraa | 01:32:31 |
| M3 | Joins & Set Ops | Baraa | 02:47:57 |
| M4 | Functions | Baraa | 04:52:58 |
| M5 | Window Functions | Baraa | 08:50:11 |
| M6 | Subqueries & CTE | Baraa | 12:58:04 |
| M7 | Advanced Objects (Views/CTAS/Temp) | Baraa | 15:35:02 |
| M8 | Programmable Objects (SP/Trigger) | Baraa | 17:27:04 |
| M9 | Performance & Optimisation | Baraa | 18:23:42 |
| M10 | DE Project: Data Warehouse | Baraa | 23:21:04 |
| M11 | DE Platform SQL | Ansh Lamba — Big Data Engineer SQL | — |

Video Baraa: https://www.youtube.com/watch?v=SSKVgrwhzus

---

## 📍 Current Position

Baca `vault/state/progress-sql.md` dan `vault/state/handoff-sql.md` untuk latest position sebelum mula.

---

## 📋 Session Rules (ikut setiap kali)

### Masa belajar
1. Baca `handoff-sql.md` dulu — tahu exact next step
2. Ajar topic ikut Baraa transcript / Ansh Big Data
3. Isi `*(fill during session)*` dalam note file yang berkenaan
4. Bagi contoh SQL + analogi (PK=IC, FK=invoice, Index=phonebook, Partition=warehouse floor)
5. Lepas explain, bagi drill/quiz minimum 3 soalan sebelum teruskan

### Hujung session (WAJIB)
1. Update `vault/state/progress-sql.md` — tukar status module, tambah session log
2. Update `vault/state/handoff-sql.md` — tulis exact next step untuk session berikut
3. Simpan semua note changes

### Format note
- Bahasa: BM casual (lah, je, kan) + technical terms kekal English
- SQL code blocks wajib ada NULL handling & edge case notes
- Setiap concept: WHAT → WHY → WHEN (bila nak guna dalam DE project)

---

## ⚡ Quick Commands

- **"teruskan"** → baca handoff, sambung dari last position
- **"quiz M[n]"** → buat drill untuk module tu
- **"isi M[n]"** → fill note file untuk module tu dari transcript
- **"update state"** → update progress + handoff files sekarang
