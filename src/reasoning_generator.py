from datetime import datetime


class ReasoningGenerator:

    def generate(
        self,
        candidate,
        features,
        final_score
    ):

        profile = candidate.get("profile", {})
        skills = candidate.get("skills", [])
        signals = candidate.get(
            "redrob_signals",
            {}
        )

        role = profile.get(
            "current_title",
            "Professional"
        )

        years = profile.get(
            "years_of_experience",
            0
        )

        recruiter_rate = signals.get(
            "recruiter_response_rate",
            0
        )

        jd_core_skills = {
            "retrieval",
            "ranking",
            "recommendation",
            "search",
            "embeddings",
            "milvus",
            "faiss",
            "pinecone",
            "chromadb",
            "rag",
            "llm",
            "nlp",
            "python",
            "machine learning",
            "qdrant",
            "weaviate",
            "opensearch",
            "elasticsearch"
        }

        matched_skills = []

        for skill in skills:

            skill_name = skill.get(
                "name",
                ""
            )

            lower_skill = skill_name.lower()

            if any(
                term in lower_skill
                for term in jd_core_skills
            ):
                matched_skills.append(
                    skill_name
                )

        skill_count = len(
            set(matched_skills)
        )

        primary_skills = list(
            dict.fromkeys(
                matched_skills
            )
        )[:3]

        if primary_skills:

            return (
                f"{role} with "
                f"{years:.1f} yrs; "
                f"{skill_count} AI core skills "
                f"({', '.join(primary_skills)}); "
                f"response rate "
                f"{recruiter_rate:.2f}"
            )

        return (
            f"{role} with "
            f"{years:.1f} yrs; "
            f"{skill_count} AI core skills; "
            f"response rate "
            f"{recruiter_rate:.2f}"
        )