from datetime import datetime


class FeatureEngineer:

    RETRIEVAL_TERMS = {
        "retrieval",
        "ranking",
        "recommendation",
        "relevance",
        "vector search",
        "semantic search",
        "information retrieval",
        "candidate matching",
        "embeddings",
        "faiss",
        "milvus",
        "pinecone",
        "chromadb",
        "hybrid search",
        "rag",
        "qdrant",
        "weaviate",
        "opensearch",
        "elasticsearch"
    }

    PRODUCTION_RETRIEVAL_TERMS = {
        "embedding drift",
        "index refresh",
        "retrieval quality",
        "retrieval evaluation",
        "hybrid retrieval",
        "reranking",
        "relevance tuning",
        "semantic retrieval"
    }

    ML_TERMS = {
        "llm",
        "fine-tuning",
        "fine tuning",
        "lora",
        "nlp",
        "transformer",
        "rag",
        "machine learning",
        "deep learning"
    }

    PRODUCTION_TERMS = {
        "production",
        "deployed",
        "deployment",
        "serving",
        "monitoring",
        "inference",
        "latency",
        "ab testing",
        "real users",
        "evaluation",
        "pipeline",
        "kafka",
        "spark",
        "airflow"
    }

    EVALUATION_TERMS = {
        "ndcg",
        "mrr",
        "map",
        "ranking metrics",
        "ranking evaluation",
        "relevance evaluation",
        "offline evaluation",
        "online evaluation",
        "offline-to-online correlation",
        "ab testing",
        "a/b testing",
        "experiment analysis"
    }

    PYTHON_TERMS = {
        "python",
        "flask",
        "fastapi",
        "pyspark"
    }

    PRODUCT_COMPANIES = {
        "google",
        "amazon",
        "meta",
        "microsoft",
        "uber",
        "swiggy",
        "zomato",
        "flipkart",
        "atlassian",
        "airbnb"
    }

    SERVICE_COMPANIES = {
        "wipro",
        "infosys",
        "tcs",
        "mindtree",
        "hcl",
        "tech mahindra",
        "cognizant"
    }

    def build_features(self, candidate):

        features = {}

        profile = candidate.get("profile", {})
        skills = candidate.get("skills", [])
        history = candidate.get("career_history", [])
        signals = candidate.get("redrob_signals", {})

        features["experience_score"] = self._experience_score(profile)

        features["retrieval_score"] = self._retrieval_score(
            skills,
            history
        )

        features["production_ml_score"] = self._production_ml_score(
            skills,
            history
        )

        features["python_score"] = self._python_score(
            skills,
            history
        )

        features["product_company_score"] = self._company_score(
            history
        )

        features["behavior_score"] = self._behavior_score(
            signals
        )

        features["evaluation_score"] = self._evaluation_score(
            history
        )

        features["external_validation_score"] = self._external_validation_score(
            signals
        )

        features[
            "market_demand_score"
        ] = self._market_demand_score(
            signals
        )

        features["github_score"] = max(
            signals.get("github_activity_score", 0),
            0
        ) / 100

        features["location_score"] = (
            1.0 if signals.get(
                "willing_to_relocate", False
            ) else 0.5
        )

        return features

    def _experience_score(self, profile):

        years = profile.get(
            "years_of_experience",
            0
        )

        if 5 <= years <= 8:
            return 1.0

        if 3 <= years < 5:
            return 0.7

        if 8 < years <= 12:
            return 0.6

        return 0.3

    def _retrieval_score(self, skills, history):

        score = 0

        for s in skills:
            name = s["name"].lower()

            if any(
                term in name
                for term in self.RETRIEVAL_TERMS
            ):
                score += 1

        for h in history:
            text = h.get(
                "description",
                ""
            ).lower()

            for term in self.RETRIEVAL_TERMS:
                if term in text:
                    score += 2

        return min(score / 10, 1.0)

    def _production_ml_score(self, skills, history):

        score = 0

        for s in skills:
            name = s["name"].lower()

            if any(
                term in name
                for term in self.ML_TERMS
            ):
                score += 1

        for h in history:
            text = h.get(
                "description",
                ""
            ).lower()

            for term in self.PRODUCTION_TERMS:
                if term in text:
                    score += 1

        return min(score / 10, 1.0)

    def _python_score(self, skills, history):

        score = 0

        for s in skills:
            if s["name"].lower() in self.PYTHON_TERMS:
                score += 1

        for h in history:
            text = h.get(
                "description",
                ""
            ).lower()

            if "python" in text:
                score += 2

        return min(score / 10, 1.0)

    def _company_score(self, history):

        score = 0

        for h in history:

            company = h.get(
                "company",
                ""
            ).lower()

            if company in self.PRODUCT_COMPANIES:
                score += 5

            if company in self.SERVICE_COMPANIES:
                score -= 3

        return max(min(score / 10, 1), 0)

    def _behavior_score(self, signals):

        score = 0

        if signals.get(
            "open_to_work_flag",
            False
        ):
            score += 2

        score += min(
            signals.get(
                "recruiter_response_rate",
                0
            ) * 3,
            2
        )

        score += min(
            signals.get(
                "interview_completion_rate",
                0
            ) * 2,
            2
        )

        score += min(
            signals.get(
                "saved_by_recruiters_30d",
                0
            ) / 10,
            2
        )

        return min(score / 8, 1.0)
    
    def _market_demand_score(self,signals):

        score = 0

        score += min(
            signals.get(
                "saved_by_recruiters_30d",
                0
            ) / 10,
            1
        )

        score += min(
            signals.get(
                "search_appearance_30d",
                0
            ) / 500,
            1
        )

        return min(
            score / 2,
            1
        )

    def _evaluation_score(
        self,
        history
    ):

        score = 0

        for job in history:

            text = job.get(
                "description",
                ""
            ).lower()

            for term in self.EVALUATION_TERMS:

                if term in text:
                    score += 2

        return min(
            score / 10,
            1
        )

    def _external_validation_score(
        self,
        signals
    ):

        score = 0

        github = max(
            signals.get(
                "github_activity_score",
                0
            ),
            0
        )

        score += min(
            github / 20,
            1
        )

        score += min(
            signals.get(
                "endorsements_received",
                0
            ) / 100,
            1
        )

        score += min(
            signals.get(
                "connection_count",
                0
            ) / 500,
            1
        )

        if signals.get(
            "linkedin_connected",
            False
        ):
            score += 0.5

        return min(
            score / 3.5,
            1
        )