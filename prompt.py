"""You are helping me upgrade an existing RAG ingestion pipeline to a new, approved
Postgres schema design. Work in my repo. Do not drop or rewrite anything until I
approve the plan.

STACK
- Python, LangGraph, PostgreSQL + pgvector (0.8.x), Google Cloud Storage for files.
- Embeddings: gemini-embedding-2 at 768 dimensions. No task_type field: send queries as
  "task: question answering | query: {text}" and stored text as
  "title: {path_label} | text: {chunk_text}". No task prefix on image input.
  text-embedding-004 is retired, so vectors from it cannot be reused.
- Sources: PDF files, Confluence pages, Excel sheets.

WHAT EXISTS TODAY
- Ingestion code in this repo.
- Existing table(s): [paste \d output or CREATE TABLE of the current table]

TARGET SCHEMA (approved; the DDL is the source of truth)
[paste the full DDL from the "Appendix: DDL and retrieval query" section of the doc]

Summary of the target:
- Stage 1, final: documents (one row per source item, with links, owner and ACL),
  document_versions (every version, stored original in GCS, extraction status and
  coverage), document_contents (one row per page, text element and image, with
  page_no, page_label, section_no, heading_path, bounding box, source_link, links,
  asset_uri, OCR text, caption, image description).
- Stage 2: chunks (one row per retrieval unit, per version, with lineage content_ids,
  path_label, file_name, page_numbers, section_no, error_code, tags, source_link).
- Stage 3: retrieval_index (the only table search reads: one row per chunk per
  embedding model, with copied filter and citation fields, full-text column, RLS).
- Audit: ingestion_runs, ingestion_events, retrieval_logs, retrieval_hits.

STEP 0 - INSPECT AND REPORT (no code changes yet)
1. Read the ingestion code and the current table(s). Describe the current flow:
   sources, parsing, chunking, embedding model and dimensions, metadata kept.
2. Write a gap analysis against the target: a table of current -> target for every
   table and column, plus code modules that must change, be added or be retired.
3. List what can be backfilled from existing data (documents, versions, chunk text)
   and what must be re-extracted or re-embedded.
4. List your questions. Do not guess at anything unclear. Stop and wait for me.

STEP 1 - MIGRATIONS (after I approve step 0)
- Use numbered, reversible migrations (Alembic if the repo uses it, otherwise SQL
  files). Make them idempotent.
- Create the new tables next to the old one. Do not drop or rename the old table
  until the new pipeline passes the checks in step 5 and I say so.
- Backfill documents and document_versions (version 1) from existing data where
  possible. Set run_id from a backfill row in ingestion_runs.
- Show me every migration before running it. Never run destructive SQL without asking.

STEP 2 - EXTRACTION (stage 1 tables)
- Connectors: PDF (file share / SharePoint / Drive), Confluence (page id, title,
  space, parent breadcrumb, author, owner, created date, current version number,
  date, author and message, labels, restrictions, attachments, web link; resolve
  account ids to display names and store both), Excel (one table_row per row,
  cells with headers in raw).
- Snapshot every version's original to GCS; record raw_snapshot_uri, size and hash.
  Skip a document when its content hash is unchanged.
- PDF passes, per page: triage (text layer vs scanned) -> text layer with positions,
  outline, page labels, document info and link annotations (PyMuPDF) -> layout model
  (Docling, Unstructured hi_res or Document AI) -> OCR for scanned pages and inside
  images -> crop and store images, skip decorative ones (tiny, or same hash on
  most pages) -> vision check per page with Gemini Flash ("what is missing or
  wrong?") -> reconcile.
- Headings, in order of trust: PDF outline, numbering patterns ("2.3", "Issue:",
  "Resolution:", "Error 2:"), font size/weight, layout model title class. Validate
  the tree: no gaps in numbering, every error under an issue/resolution, every
  error has a fix.
- Write one page row per page (full text + rendered PNG), text element rows, and
  image rows (caption, generated description labelled with its model, OCR text,
  parent_content_id = the error it illustrates).
- Gate: every page has a row, coverage >= 0.95, heading tree valid, table cell
  counts match, all links captured, vision check clean. Otherwise mark the version
  'partial', log it in ingestion_events, and never switch it on.

STEP 3 - CHUNKING (stage 2)
- A LangGraph conditional edge decides in code: FAQ with issue/error sections or
  > ~500 tokens -> one error_chunk per error (with all its fix steps and the text
  of its images) + one overview per heading; otherwise one qa chunk. Every FAQ
  also gets a question chunk and 3-5 paraphrase chunks. Other documents: one chunk
  per heading section (400-600 tokens, 10-15% overlap, never split a list or table).
  Excel: one chunk per row as "Column: value" lines.
- Fill path_label, file_name, page_numbers (union of its contents), section_no,
  error_code, tags, source_link, content_ids, embed_text, content_hash.

STEP 4 - EMBEDDING AND VERSION SWITCH (stage 3)
- Stage the new version hidden (is_active = false). Before calling Gemini, reuse
  any stored vector with the same content_hash and model. Use the Batch API.
- Switch in one short transaction: new version active, old inactive,
  documents.current_version updated. Never hold a transaction open during API calls.
- Deletes: status = 'deleted', then cascade. ACL-only changes: copy acl_groups,
  no re-embedding. Purge old versions after the retention period but keep
  document_versions, the GCS original, ingestion_events and retrieval logs.
- Log every run in ingestion_runs and every document outcome in ingestion_events.

STEP 5 - RETRIEVAL AND CHECKS
- Use the hybrid query from the doc (vector top 50 + full-text top 50, RRF k=60,
  best chunk per group_id). Connect as a non-owner role with SELECT only, and set
  app.user_groups per request so row-level security applies.
- Log each question in retrieval_logs and each hit, with its citation snapshot,
  in retrieval_hits.
- Tests: unit tests for page triage, heading tree, image linking, chunking rules;
  integration tests on Postgres + pgvector for constraints, cascade delete,
  hidden-then-switch versioning, embedding reuse, RLS, and the trace-back query.
- Regression set: about 20 hand-checked PDFs; fail the build if text coverage or
  headings get worse.

RULES
- One step at a time. Show the diff and test results, then wait for my go-ahead.
- Keep the code modular (one module per stage) and put thresholds, model names,
  dimensions and chunk sizes in config.
- No secrets in code or logs; keep the existing behaviour working until cut-over."""