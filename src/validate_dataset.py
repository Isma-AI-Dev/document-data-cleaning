from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATASET_PATH = (
    PROJECT_ROOT
    / "data"
    / "cleaned"
    / "Reviews_fixed.csv"
)

REPORT_PATH = (
    PROJECT_ROOT
    / "reports"
    / "day2_dataset_report.txt"
)


def main() -> None:
    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_PATH}"
        )

    print("Loading dataset...")

    dataframe = pd.read_csv(
        DATASET_PATH,
        encoding="utf-8",
        low_memory=False,
    )

    required_columns = [
        "User_id",
        "Product_id",
        "Rating",
        "Date",
        "Review",
        "Label",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in dataframe.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    review_text = dataframe["Review"].fillna("").astype(str)
    stripped_reviews = review_text.str.strip()

    total_rows = len(dataframe)
    total_columns = len(dataframe.columns)

    missing_reviews = int(dataframe["Review"].isna().sum())
    empty_reviews = int(stripped_reviews.eq("").sum())

    duplicate_rows = int(dataframe.duplicated().sum())

    duplicate_reviews = int(
        stripped_reviews[
            stripped_reviews.ne("")
        ].duplicated().sum()
    )

    label_counts = dataframe["Label"].value_counts(
        dropna=False
    )

    rating_counts = dataframe["Rating"].value_counts(
        dropna=False
    ).sort_index()

    broken_character_count = int(
        stripped_reviews.str.contains(
            r"Ã|Â|�",
            regex=True,
            na=False,
        ).sum()
    )

    review_lengths = stripped_reviews[
        stripped_reviews.ne("")
    ].str.len()

    shortest_review = (
        int(review_lengths.min())
        if not review_lengths.empty
        else 0
    )

    longest_review = (
        int(review_lengths.max())
        if not review_lengths.empty
        else 0
    )

    average_review_length = (
        round(float(review_lengths.mean()), 2)
        if not review_lengths.empty
        else 0
    )

    parsed_dates = pd.to_datetime(
        dataframe["Date"],
        errors="coerce",
    )

    invalid_dates = int(parsed_dates.isna().sum())

    report = f"""
DAY 2 DATASET VALIDATION REPORT
===============================

DATASET INFORMATION
-------------------
Dataset file: {DATASET_PATH.name}
Total rows: {total_rows:,}
Total columns: {total_columns}
Minimum required rows: 5,000
Size requirement passed: {total_rows >= 5_000}

COLUMN NAMES
------------
{chr(10).join(f"- {column}" for column in dataframe.columns)}

REVIEW QUALITY
--------------
Missing reviews: {missing_reviews:,}
Empty reviews: {empty_reviews:,}
Duplicate reviews: {duplicate_reviews:,}
Complete duplicate rows: {duplicate_rows:,}
Reviews with possible broken characters: {broken_character_count:,}

REVIEW LENGTH
-------------
Shortest review: {shortest_review:,} characters
Longest review: {longest_review:,} characters
Average review length: {average_review_length:,} characters

DATE QUALITY
------------
Invalid or missing dates: {invalid_dates:,}

LABEL COUNTS
------------
{label_counts.to_string()}

RATING COUNTS
-------------
{rating_counts.to_string()}
""".strip()

    REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    REPORT_PATH.write_text(
        report,
        encoding="utf-8",
    )

    print("\n" + report)
    print(f"\nReport saved at:\n{REPORT_PATH}")


if __name__ == "__main__":
    main()