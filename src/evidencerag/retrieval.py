from collections import defaultdict
from dataclasses import dataclass, field
import re
from typing import Any, Sequence

from rank_bm25 import BM25Okapi


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)


def tokenize(text: str) -> list[str]:
    normalized = text.lower()
    tokens = re.findall(r"[a-z0-9]+", normalized)

    # ponytail: unigram/bigram heuristic; use a trained segmenter only if
    # Chinese retrieval evaluation shows this simple path is insufficient.
    for segment in re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff]+", normalized):
        tokens.extend(segment)
        tokens.extend(segment[index : index + 2] for index in range(len(segment) - 1))
    return tokens


def bm25_search(query: str, chunks: Sequence[Chunk], limit: int = 10) -> list[dict[str, Any]]:
    if not chunks or limit <= 0:
        return []
    query_tokens = tokenize(query)
    if not query_tokens:
        return []

    scores = BM25Okapi([tokenize(chunk.text) for chunk in chunks]).get_scores(query_tokens)
    ranked = sorted(range(len(chunks)), key=lambda index: scores[index], reverse=True)
    return [
        {
            "chunk_id": chunks[index].chunk_id,
            "text": chunks[index].text,
            "metadata": chunks[index].metadata,
            "score": float(scores[index]),
        }
        for index in ranked[:limit]
    ]


def weighted_rrf(
    rankings: Sequence[Sequence[dict[str, Any]]],
    weights: Sequence[float],
    k: int = 10,
) -> list[dict[str, Any]]:
    if len(rankings) != len(weights):
        raise ValueError("rankings and weights must have the same length")
    if k <= 0 or any(weight < 0 for weight in weights):
        raise ValueError("k must be positive and weights must be non-negative")

    items: dict[str, dict[str, Any]] = {}
    scores: dict[str, float] = defaultdict(float)
    for ranking, weight in zip(rankings, weights, strict=True):
        for rank, item in enumerate(ranking, start=1):
            chunk_id = str(item["chunk_id"])
            items.setdefault(chunk_id, dict(item))
            scores[chunk_id] += weight / (k + rank)

    fused = [{**item, "combined_score": scores[chunk_id]} for chunk_id, item in items.items()]
    return sorted(fused, key=lambda item: item["combined_score"], reverse=True)
