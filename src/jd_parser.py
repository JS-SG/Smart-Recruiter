import re


class JDParser:

    def __init__(self, jd_text: str):
        self.jd_text = jd_text.lower()

    def extract_requirements(self):

        retrieval_keywords = [
            "retrieval",
            "search",
            "ranking",
            "recommendation",
            "relevance",
            "matching",
            "vector database",
            "embeddings",
        ]

        ml_keywords = [
            "machine learning",
            "ml",
            "llm",
            "nlp",
            "fine tuning",
            "evaluation",
        ]

        required = []

        for kw in retrieval_keywords + ml_keywords:
            if kw in self.jd_text:
                required.append(kw)

        return {
            "required_keywords": required
        }