import csv


class SubmissionBuilder:

    def build(
        self,
        ranked_results,
        output_file
    ):

        top100 = ranked_results[:100]
        max_score = top100[0]["score"]

        with open(
            output_file,
            "w",
            newline="",
            encoding="utf-8"
        ) as f:

            writer = csv.writer(f)

            writer.writerow(
                [
                    "candidate_id",
                    "rank",
                    "score",
                    "reasoning"
                ]
            )

            rank = 1

            for row in top100:
                normalized_score = round(
                    row["score"] / max_score,
                    8
                )
                writer.writerow(
                    [
                        row["candidate_id"],
                        rank,
                        normalized_score,
                        row["reasoning"]
                    ]
                )

                rank += 1

        print(
            f"Saved to {output_file}"
        )