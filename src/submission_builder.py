import csv


class SubmissionBuilder:

    def build(
        self,
        ranked_results,
        output_file
    ):

        top100 = ranked_results[:100]

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

                writer.writerow(
                    [
                        row["candidate_id"],
                        rank,
                        round(
                            row["score"] / 100,
                            5
                        ),
                        row["reasoning"]
                    ]
                )

                rank += 1

        print(
            f"Saved to {output_file}"
        )