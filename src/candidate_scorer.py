import yaml


class CandidateScorer:

    def __init__(self, weight_file):

        with open(weight_file) as f:
            self.weights = yaml.safe_load(f)

    def score(
        self,
        features,
        honeypot_penalty=0
    ):

        score = 0

        score += (
            features.get(
                "semantic_score",
                0
            )   
            *
            self.weights.get(
                "semantic_score",
                0
            )
        )

        score += (
            features.get(
                "jd_match_score",
                0
            )
            * 0.10
        )

        score += (
            features["experience_score"]
            * self.weights["experience_score"]
        )

        score += (
            features["retrieval_score"]
            * self.weights["retrieval_score"]
        )

        score += (
            features["production_ml_score"]
            * self.weights["production_ml_score"]
        )

        score += (
            features["product_company_score"]
            * self.weights["product_company_score"]
        )

        score += (
            features["python_score"]
            * self.weights["python_score"]
        )

        score += (
            features["behavior_score"]
            * self.weights["behavior_score"]
        )

        score += (
            features["evaluation_score"]
            * self.weights["evaluation_score"]
        )

        score += (
            features["external_validation_score"]
            * self.weights["external_validation_score"]
        )

        score += (
            features["market_demand_score"]
            * self.weights[
                "market_demand_score"
            ]
        )

        score += (
            features["github_score"]
            * self.weights["github_score"]
        )

        score += (
            features["location_score"]
            * self.weights["location_score"]
        )

        score = score * 100

        score -= honeypot_penalty

        return round(score, 4)
