# AGENTS.md

## Purpose

This file is the implementation guide for coding agents working on this repository.

The project is a Windows-first desktop application in Python that extracts structured data from invoice PDFs and exports the results to Excel.

## Product Goal

Build a desktop tool that lets the user:

1. Select a folder containing invoice PDFs.
2. Click `Extract`.
3. See progress while files are processed.
4. Save an Excel file at the end.

The main business output is a report grouped by:

- `city`
- `item description`
- `sum of item quantity`
- `sum of item total value`

## Important Reality About The Sample PDFs

The sample PDFs used for discovery did not expose useful text through simple PDF text extraction with `PyPDF2`.

Assume the MVP is OCR-first.

That means the implementation should be designed around:

- PDF rasterization
- OCR text extraction
- layout-aware parsing
- normalization
- aggregation

Do not assume text-selectable PDFs for the initial implementation.

## Scope Of The MVP

The MVP must support:

- selecting an input folder
- scanning `.pdf` files
- processing files in the background without freezing the UI
- extracting `city`
- extracting item rows
- extracting `item description`
- extracting `item quantity`
- extracting `item total value`
- exporting a detailed sheet
- exporting a grouped summary sheet
- exporting an error sheet

## Non-Goals For The MVP

Do not spend time on these unless explicitly requested:

- cloud services
- SEFAZ integration
- database integration
- in-app manual editing of extracted rows
- advanced fiscal validation beyond what is needed for the report
- native Excel PivotTable generation

## Output Contract

The Excel output must contain these sheets.

### 1. `Base_Itens`

One row per extracted item line.

Required columns:

- `arquivo_pdf`
- `status_extracao`
- `cidade`
- `numero_documento`
- `data_emissao`
- `item_descricao`
- `item_qtd`
- `item_valor_total`
- `observacoes`

### 2. `Resumo_Cidade_Item`

One row per `cidade + item_descricao`.

Required columns:

- `cidade`
- `item_descricao`
- `soma_item_qtd`
- `soma_item_valor_total`

This sheet should be easy to read and logically match the reference image:

- city as the primary grouping
- item as the secondary grouping
- quantity sum
- total value sum
- grand total at the end when practical

### 3. `Erros`

One row per failed or partially failed file.

Required columns:

- `arquivo_pdf`
- `tipo_erro`
- `mensagem`
- `etapa`

## Parsing Rules

- Treat item descriptions as variable user data.
- Do not hardcode the sample item names as a closed list.
- Use the sample invoices only to infer layout patterns, anchors, spacing, and line structure.
- Prefer layout-driven and rule-driven parsing over document-specific hacks.
- Keep normalization logic separate from OCR logic.
- Keep aggregation logic separate from parsing logic.

## OCR And PDF Strategy

Recommended stack:

- `PySide6` for the desktop UI
- `PyMuPDF` for PDF rendering
- `pytesseract` with local Tesseract for OCR
- `pypdf` for metadata and lightweight PDF checks
- `pandas` + `openpyxl` for Excel export

Recommended OCR pipeline:

1. Open the PDF.
2. Render pages to images at OCR-friendly resolution.
3. Apply light preprocessing only when needed.
4. Run OCR.
5. Reconstruct text lines as faithfully as possible.
6. Parse city and item rows.
7. Normalize quantities and currency values.
8. Aggregate by `city + item`.

## Architecture Expectations

Keep the code modular and layered.

Recommended structure:

```text
src/
  app/
  ui/
  application/
  domain/
  infrastructure/
tests/
docs/
```

Responsibilities:

- `ui/`: window, dialogs, progress updates, user actions
- `application/`: batch orchestration, progress state, workflow coordination
- `domain/`: models, validation, normalization rules
- `infrastructure/pdf/`: rendering and PDF helpers
- `infrastructure/ocr/`: OCR engine and image preprocessing
- `infrastructure/parser/`: city and item row parsing
- `infrastructure/aggregation/`: grouped summary generation
- `infrastructure/export/`: Excel writer

## UI Requirements

The UI must include:

- folder selection
- extract button
- progress bar
- current status message
- save-file dialog at the end

The UI must remain responsive while processing.

Use:

- `QThread`, or
- `QRunnable` with `QThreadPool`

Do not run OCR or batch parsing on the main UI thread.

## Error Handling Rules

- A single file failure must not stop the whole batch.
- Record errors per file.
- Partial extraction is acceptable if it is clearly marked.
- If no useful item rows are extracted from a file, it must appear in `Erros`.

## Data Handling Rules

- All processing must remain local.
- Do not send invoice data to external APIs.
- Preserve numeric meaning carefully.
- Parse Brazilian-style currency and quantity values safely.
- Keep empty values empty instead of inventing placeholders like `N/A`, except for explicit status fields.

## Implementation Priorities

Build the project as a vertical slice first.

Recommended order:

1. Project skeleton and app entry point.
2. Main window with folder selection and progress UI.
3. Background batch worker.
4. PDF discovery.
5. PDF rendering + OCR service.
6. Item extraction models.
7. City parser.
8. Item row parser.
9. Aggregation service.
10. Excel exporter.
11. Tests with anonymized sample PDFs.

## Testing Expectations

Add tests for:

- city extraction
- item row extraction
- quantity normalization
- currency normalization
- OCR-to-parser integration
- aggregation correctness
- Excel export structure

Focus first on deterministic tests around parsing and aggregation.

## Code Quality Guidelines

- Prefer small modules with single responsibility.
- Prefer pure functions for parsing and normalization where possible.
- Avoid tightly coupling UI code to OCR/parsing code.
- Keep vendor-specific assumptions isolated and documented in code comments only when necessary.
- Use clear names in English for code, modules, and tests.
- Keep comments short and only where they add real value.

## Documentation Sync Rule

If implementation decisions materially change the architecture, output format, or MVP scope, update these files as part of the same change:

- `README.md`
- `docs/visao-produto.md`
- `docs/requisitos.md`
- `docs/especificacao-campos.md`
- `docs/arquitetura.md`
- `docs/plano-desenvolvimento.md`

## Definition Of Done For Early Milestones

An implementation step is only considered complete when:

- the UI flow still works
- the code remains modular
- file-level failures are handled
- the expected Excel sheet structure is preserved
- relevant tests are added or updated
