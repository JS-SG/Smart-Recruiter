import json
from tqdm import tqdm

from src.feature_engineering import (
    FeatureEngineer
)
from src.honeypot_detector import (
    HoneypotDetector
)
from src.candidate_scorer import (
    CandidateScorer
)
from src.reasoning_generator import (
    ReasoningGenerator
)
from src.pre_filter import (
    CandidatePreFilter
)


class RankingEngine:

    def __init__(self):

        self.fe = FeatureEngineer()

        self.hp = HoneypotDetector()

        self.scorer = CandidateScorer(
            "config/weights.yaml"
        )

        self.reasoning = (
            ReasoningGenerator()
        )

        self.prefilter = (
            CandidatePreFilter()
        )  

    def process_file(
        self,
        candidate_file
    ):

        results = []

        with open(
            candidate_file,
            "r",
            encoding="utf-8"
        ) as f:

            for line in tqdm(
                f,
                desc="Processing"
            ):

                candidate = json.loads(
                    line
                )

                if not self.prefilter.should_keep(
                    candidate
                ):
                    continue

                features = (
                    self.fe.build_features(
                        candidate
                    )
                )

                penalty = (
                    self.hp.penalty(
                        candidate
                    )
                )

                score = (
                    self.scorer.score(
                        features,
                        penalty
                    )
                )

                rerank_bonus = (
                        features["retrieval_score"] * 5
                        +
                        features["production_ml_score"] * 5
                    )

                score += rerank_bonus

                reason = (
                    self.reasoning.generate(
                        candidate,
                        features,
                        score
                    )
                )

                candidate_num = int(
                    candidate["candidate_id"]
                    .replace("CAND_", "")
                )

                score += (
                    candidate_num / 1000000000
                )

                results.append(
                    {
                        "candidate_id":
                        candidate[
                            "candidate_id"
                        ],
                        "score":
                        score,
                        "reasoning":
                        reason,
                    }
                )

        return results

    def rank(
        self,
        results
    ):

        results.sort(
            key=lambda x: (
                -x["score"],
                x["candidate_id"]
            )
        )

        return results