# Demo

## Two-minute verification path

1. Upload a permitted sample PDF.
2. Parse it into page-aware chunks and build the index.
3. Ask a question whose answer is present in the document.
4. Inspect the retrieved evidence and citation details.
5. Open the cited source chunk/page.
6. Export the result as Markdown, HTML, and Word-compatible output.

![EvidenceRAG interface](../assets/evidencerag-demo.png)

## Verified local behavior

The isolated offline replay was executed three consecutive times. Each round processed the same five-page sample, produced 36 chunks, returned five evidence/citation items, resolved citation details, and exported all three report formats.

This verifies repeatability of the selected local workflow on one machine and sample. It is not a production-concurrency, cross-dataset, or enhanced-model quality claim.

## Interview availability

The complete local application, full evaluation outputs, and source-level walkthrough can be shown during interviews. They are not distributed through this public repository.
