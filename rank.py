import argparse

from src.ranking_engine import (
    RankingEngine
)

from src.submission_builder import (
    SubmissionBuilder
)


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--candidates",
        required=True
    )

    parser.add_argument(
        "--out",
        required=True
    )

    args = parser.parse_args()

    print(
        "Starting ranking..."
    )

    engine = RankingEngine()

    results = (
        engine.process_file(
            args.candidates
        )
    )

    ranked = (
        engine.rank(results)
    )

    builder = (
        SubmissionBuilder()
    )

    builder.build(
        ranked,
        args.out
    )

    print(
        "Ranking completed."
    )


if __name__ == "__main__":
    main()