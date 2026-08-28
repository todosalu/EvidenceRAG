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

Aggregate methodology and results are public. Full model assets, raw per-query analyses, private domain-paper chunks, and unpublished experimental artifacts are intentionally withheld. They can be inspected in an interview demonstration.
