class HoneypotDetector:

    CONSULTING_COMPANIES = {
        "tcs",
        "infosys",
        "wipro",
        "cognizant",
        "accenture",
        "capgemini",
        "mindtree",
        "hcl"
    }

    def detect(self, candidate):

        score = 0

        profile = candidate.get(
            "profile",
            {}
        )

        skills = candidate.get(
            "skills",
            []
        )

        history = candidate.get(
            "career_history",
            []
        )

        years = profile.get(
            "years_of_experience",
            0
        )

        # Consulting-only career detection
        consulting_count = 0

        for job in history:

            company = job.get(
                "company",
                ""
            ).lower()

            if company in self.CONSULTING_COMPANIES:
                consulting_count += 1

        if (
            len(history) > 0
            and consulting_count == len(history)
        ):
            score += 3

        # Job hopper detection
        if len(history) >= 2:

            total_months = sum(
                h.get(
                    "duration_months",
                    0
                )
                for h in history
            )

            avg_tenure = (
                total_months /
                len(history)
            )

            if avg_tenure < 18:
                score += 2

        # LangChain-only profiles
        skills_text = " ".join(
            [
                skill.get(
                    "name",
                    ""
                ).lower()
                for skill in skills
            ]
        )

        if (
            "langchain" in skills_text
            and "retrieval" not in skills_text
            and "ranking" not in skills_text
        ):
            score += 2

        # Research-heavy profiles
        research_words = {
            "research",
            "paper",
            "publication",
            "laboratory",
            "phd"
        }

        research_count = 0

        for job in history:

            text = job.get(
                "description",
                ""
            ).lower()

            for word in research_words:

                if word in text:
                    research_count += 1

        if (
            research_count >= 3
            and len(history) <= 2
        ):
            score += 3

        # Architecture-heavy profiles
        title = profile.get(
            "current_title",
            ""
        ).lower()

        if any(
            x in title
            for x in [
                "enterprise architect",
                "solution architect",
                "director",
                "vp engineering",
                "head of engineering"
            ]
        ):
            score += 2

        # CV / Speech dominant profiles
        cv_count = 0
        nlp_count = 0

        for skill in skills:

            skill_name = skill.get(
                "name",
                ""
            ).lower()

            if any(
                x in skill_name
                for x in [
                    "image",
                    "vision",
                    "speech",
                    "tts",
                    "gan"
                ]
            ):
                cv_count += 1

            if any(
                x in skill_name
                for x in [
                    "nlp",
                    "retrieval",
                    "llm",
                    "ranking"
                ]
            ):
                nlp_count += 1

        if (
            cv_count >= 3
            and cv_count > (nlp_count * 2)
        ):
            score += 3

        # Suspicious advanced skills
        for skill in skills:

            duration = skill.get(
                "duration_months",
                0
            )

            proficiency = skill.get(
                "proficiency",
                ""
            ).lower()

            if (
                proficiency == "advanced"
                and duration < 3
            ):

                endorsements = skill.get(
                    "endorsements",
                    0
                )

                if (
                    endorsements > 50
                    and duration < 3
                ):
                    score += 2
                else:
                    score += 1

        # Unrealistic career profile
        if (
            years > 15
            and len(history) < 2
        ):
            score += 2

        if (
            years < 2
            and len(skills) > 30
        ):
            score += 2

        return score

    def penalty(self, candidate):

        score = self.detect(
            candidate
        )

        if score >= 8:
            return 20

        if score >= 5:
            return 12

        if score >= 2:
            return 5

        return 0