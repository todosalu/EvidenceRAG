import sys
from pathlib import Path
import unittest


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from evidencerag import Chunk, bm25_search, tokenize, weighted_rrf


class RetrievalTests(unittest.TestCase):
    def test_tokenize_keeps_english_terms(self) -> None:
        self.assertEqual(tokenize("Double-DQN 2026"), ["double", "dqn", "2026"])

    def test_tokenize_supports_chinese_unigrams_and_bigrams(self) -> None:
        tokens = tokenize("雷达抗干扰")
        self.assertIn("雷", tokens)
        self.assertIn("雷达", tokens)
        self.assertIn("干扰", tokens)

    def test_bm25_ranks_relevant_chinese_chunk_first(self) -> None:
        chunks = [
            Chunk("noise-1", "这段内容讨论数据清洗。"),
            Chunk("noise-2", "另一段内容讨论软件测试。"),
            Chunk("target", "本文研究雷达抗干扰策略与频率捷变。"),
        ]
        self.assertEqual(bm25_search("雷达抗干扰", chunks, limit=3)[0]["chunk_id"], "target")

    def test_weighted_rrf_prefers_vector_ranking(self) -> None:
        lexical = [{"chunk_id": "a"}, {"chunk_id": "b"}]
        vector = [{"chunk_id": "b"}, {"chunk_id": "a"}]
        fused = weighted_rrf([lexical, vector], weights=[0.5, 1.0], k=10)
        self.assertEqual([item["chunk_id"] for item in fused], ["b", "a"])

    def test_weighted_rrf_validates_configuration(self) -> None:
        with self.assertRaises(ValueError):
            weighted_rrf([[]], weights=[], k=10)


if __name__ == "__main__":
    unittest.main()
