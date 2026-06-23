class CandidatePreFilter:

    REJECT_TITLES = {
        "marketing",
        "sales",
        "hr",
        "recruiter",
        "operations manager",
        "graphic designer",
        "content writer",
        "mechanical engineer",
        "civil engineer",
        "marketing manager",
        "content writer",
        "seo specialist",
        "brand manager",
        "graphic designer"
    }

    def should_keep(self, candidate):

        profile = candidate.get("profile", {})

        title = profile.get(
            "current_title",
            ""
        ).lower()

        summary = profile.get(
            "summary",
            ""
        ).lower()

        years = profile.get(
            "years_of_experience",
            0
        )

        if years < 3:
            return False

        if years > 15:
            return False

        if ("marketing" in summary):
            return False

        for bad_title in self.REJECT_TITLES:

            if bad_title in title:
                return False

        ai_terms = [
            "machine learning",
            "ml",
            "ai",
            "retrieval",
            "ranking",
            "search",
            "recommendation",
            "llm",
            "nlp"
        ]

        found = sum(
            1
            for term in ai_terms
            if term in summary
        )

        return found >= 1