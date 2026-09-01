# Benchmark

## Question

How do BM25, BGE, equal-weight RRF, and heuristic reranking compare under the same scientific-evidence retrieval protocol?

## Dataset and protocol

- Source: SciFact official evidence annotations.
- Corpus: 1,000 scientific-paper abstracts.
- Index: 8,718 sentence-level chunks.
- Queries: 300 scientific claims with official evidence sentences.
- Candidate depth: Top 50 per route; metrics reported at Top 5.
- Metrics: Recall@k, MRR@5, nDCG@5, and Precision@5.

This benchmark evaluates English abstract-sentence retrieval. It does not establish performance on full PDFs, Chinese queries, tables, formulas, answer generation, or production latency.

## Aggregate results

| Route | Recall@1 | Recall@3 | Recall@5 | MRR@5 | nDCG@5 | Precision@5 |
|---|---:|---:|---:|---:|---:|---:|
| BM25 | 0.3129 | 0.4865 | 0.5930 | 0.5562 | 0.5156 | 0.2027 |
| BGE | 0.3388 | **0.6195** | **0.7355** | **0.6503** | **0.6271** | **0.2593** |
| Equal-weight RRF | **0.3505** | 0.5827 | 0.7038 | 0.6390 | 0.6020 | 0.2393 |
| RRF + heuristic reranking | 0.2988 | 0.4414 | 0.5624 | 0.5376 | 0.4907 | 0.1973 |

Relative to BM25, BGE improved Recall@5 by 24.03% and MRR@5 by 16.92%. Equal-weight RRF remained below BGE on Recall@5, MRR@5, and nDCG@5. Heuristic reranking degraded the evaluated route and is not presented as an improvement.

## Follow-up holdout result

Using 112 training queries to select `k=10` and a BM25:BGE weight ratio of `0.5:1`, weighted RRF was frozen and evaluated on 188 development queries. It improved Recall@5/MRR@5 by 8.19%/7.24% relative to equal-weight RRF. Its small point-estimate lead over BGE had confidence intervals crossing zero, so no stable superiority over BGE is claimed.

## Reproducibility boundary

Aggregate methodology and results are public. Full model assets, raw per-query analyses, private domain-paper chunks, and unpublished experimental artifacts are intentionally withheld and are not distributed through this public repository.

## QASPER structured full-paper retrieval

### Dataset and protocol

- Source: QASPER v0.3 development split with official answer and evidence annotations.
- Scope: known-paper retrieval over structured full-paper text.
- Documents: 100 papers, with at most one selected question per paper.
- Index: 4,830 abstract or body-paragraph chunks.
- Queries: 100 answerable questions with automatically aligned text evidence.
- Alignment: exact paragraph match after lowercasing and whitespace normalization.
- Routes: BM25, `BAAI/bge-small-en-v1.5`, weighted RRF (`k=10`, BM25:BGE=`0.5:1`), and `cross-encoder/ms-marco-MiniLM-L6-v2` reranking the weighted-RRF Top 20.
- Aggregation: macro average; best score across official answer annotations.

The deterministic selection scanned 120 questions. Eighteen had no text evidence and two could not be aligned automatically; no new manual labels were created.

### Aggregate results

| Route | Recall@1 | Recall@3 | Recall@5 | MRR@5 | nDCG@5 | Precision@5 | Evidence F1@5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| BM25 | 0.1973 | 0.3506 | 0.4831 | 0.3503 | 0.3577 | 0.1200 | 0.1862 |
| BGE | 0.2575 | 0.4623 | 0.5879 | 0.4223 | 0.4439 | 0.1480 | 0.2277 |
| Weighted RRF | 0.2325 | 0.4573 | 0.6029 | 0.4217 | 0.4464 | 0.1520 | 0.2339 |
| Cross-Encoder rerank | **0.3089** | **0.5620** | **0.6995** | **0.5092** | **0.5292** | **0.1780** | **0.2722** |

Cross-Encoder reranking improved the Recall@5 point estimate by 16.02% and Evidence F1@5 by 16.37% over weighted RRF. It produced the highest point estimate on every reported metric. Offline batched CPU reranking took 91.568 seconds, or 915.682 ms per query amortized. No significance test was run, so the gain is not presented as statistically validated.

### Boundary

This evaluates text-evidence retrieval within a known structured full paper. It does not validate PDF parsing, page mapping, figure/table evidence, cross-paper retrieval, or answer generation. Evidence marked `FLOAT SELECTED` is excluded. Evidence F1@5 is whitespace-normalized paragraph F1 at a fixed Top 5, not answer F1.

Sources: [QASPER paper](https://aclanthology.org/2021.naacl-main.365/), [official dataset](https://huggingface.co/datasets/allenai/qasper), [Cross-Encoder model card](https://huggingface.co/cross-encoder/ms-marco-MiniLM-L6-v2).
