from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class SemanticMatcher:

    def __init__(self):
        self.jd_embedding = None
        self.model = SentenceTransformer(
            "./models/all-MiniLM-L6-v2"
        )

    def encode_jd(
        self,
        jd_text
    ):

        self.jd_embedding = self.model.encode(
            jd_text
        )
    

    def build_candidate_text(
        self,
        candidate
    ):

        profile = candidate.get(
            "profile",
            {}
        )

        history = candidate.get(
            "career_history",
            []
        )

        skills = candidate.get(
            "skills",
            []
        )

        text_parts = []

        text_parts.append(
            profile.get(
                "headline",
                ""
            )
        )

        text_parts.append(
            profile.get(
                "summary",
                ""
            )
        )

        for skill in skills:

            text_parts.append(
                skill.get(
                    "name",
                    ""
                )
            )

        for job in history:

            text_parts.append(
                job.get(
                    "title",
                    ""
                )
            )

            text_parts.append(
                job.get(
                    "description",
                    ""
                )
            )

        return " ".join(text_parts)

    def score_batch(
        self,
        candidates
    ):
        texts = []

        for c in candidates:

            texts.append(
                self.build_candidate_text(
                    c
                )
            )

        embeddings = (
            self.model.encode(
                texts,
                batch_size=128,
                show_progress_bar=False
            )
        )
        scores = cosine_similarity(
            embeddings,
            [self.jd_embedding]
        ).flatten()

        return scores

    def score(
        self,
        candidate
    ):

        candidate_text = self._candidate_text(
            candidate
        )

        candidate_embedding = self.model.encode(
            candidate_text
        )

        similarity = cosine_similarity(
            [self.jd_embedding],
            [candidate_embedding]
        )[0][0]

        similarity = max(
            0,
            similarity
        )

        return float(similarity)