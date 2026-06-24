import json
from tqdm import tqdm
from src.semantic_matcher import SemanticMatcher
from src.jd_parser import JDParser
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

    def __init__(self,jd_path):
        with open(
            jd_path,
            "r"
        ) as f:

            self.jd_text = f.read()
        self.jd_requirements = (
            JDParser(
                self.jd_text
            ).extract_requirements()
        )

        self.fe = FeatureEngineer()

        self.hp = HoneypotDetector()

        self.semantic_matcher = SemanticMatcher()
        self.semantic_matcher.encode_jd(
            self.jd_text
        )

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
                
                semantic_score = 0

                features = (
                    self.fe.build_features(
                        candidate,
                        self.jd_requirements,
                        semantic_score
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
                        features["retrieval_score"] * 0.10
                        +
                        features["production_ml_score"] * 0.10
                    )

                score += rerank_bonus


                results.append(
                    {   
                        "candidate": candidate,
                        "candidate_id":
                        candidate[
                            "candidate_id"
                        ],
                        "score":
                        score,
                        "reasoning":
                        "",
                        "features": features,
                    }
                )

        return results

    def rank(
        self,
        results
    ):
        results = (
            self.semantic_rerank(
                results,
                top_k=2000
            )
        )

        for item in results:

            candidate_num = int(
                item["candidate_id"]
                .replace("CAND_", "")
            )

            item["score"] += (
                candidate_num * 1e-12
            )

        results.sort(
            key=lambda x: (
                -x["score"],
                x["candidate_id"]
            )
        )

        return results

    def semantic_rerank(
        self,
        results,
        top_k=2000
    ):

        print(
            f"Semantic reranking top {top_k}..."
        )

        candidates = sorted(
            results,
            key=lambda x: x["score"],
            reverse=True
        )[:top_k]

        candidate_objects = [
            x["candidate"]
            for x in candidates
        ]

        semantic_scores = (
            self.semantic_matcher.score_batch(
                candidate_objects
            )
        )

        for item, semantic_score in zip(
            candidates,
            semantic_scores
        ):

            item["score"] += (
                float(semantic_score)
                *
                self.scorer.weights[
                    "semantic_score"
                ]
            )

            item["features"][
                "semantic_score"
            ] = float(
                semantic_score
            )

            item["reasoning"] = (
                    self.reasoning.generate(
                    item["candidate"],
                    item["features"],
                    item["score"]
                )
            )

        return results