from collections import Counter
from pathlib import Path

import pandas as pd

try:
    from src.cleaning import clean_text
except ModuleNotFoundError:
    from cleaning import clean_text


PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "cleaned"
    / "Reviews_fixed.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "cleaned"
    / "Reviews_cleaned.csv"
)

REPORT_FILE = (
    PROJECT_ROOT
    / "reports"
    / "week_1_data_quality_report.md"
)

CHUNK_SIZE = 25_000
MINIMUM_REVIEW_LENGTH = 3


def main() -> None:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Input dataset was not found:\n{INPUT_FILE}"
        )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Remove an incomplete file from an earlier run.
    if OUTPUT_FILE.exists():
        OUTPUT_FILE.unlink()

    total_original_rows = 0
    total_final_rows = 0
    missing_reviews = 0
    empty_reviews_removed = 0
    short_reviews_removed = 0
    duplicate_reviews_removed = 0
    possible_broken_text = 0
    invalid_dates = 0

    seen_reviews: set[str] = set()
    final_label_counts: Counter = Counter()

    print("Starting Week 1 dataset cleaning...\n")

    chunks = pd.read_csv(
        INPUT_FILE,
        encoding="utf-8",
        chunksize=CHUNK_SIZE,
        low_memory=False,
    )

    for chunk_number, chunk in enumerate(chunks, start=1):
        if "Review" not in chunk.columns:
            raise ValueError(
                "The Review column was not found. "
                f"Available columns: {chunk.columns.tolist()}"
            )

        rows_in_chunk = len(chunk)
        total_original_rows += rows_in_chunk

        missing_reviews += int(
            chunk["Review"].isna().sum()
        )

        # Clean every review using the functions from cleaning.py.
        chunk["Review"] = chunk["Review"].map(clean_text)

        empty_mask = chunk["Review"].eq("")
        empty_reviews_removed += int(empty_mask.sum())

        short_mask = (
            chunk["Review"].ne("")
            & chunk["Review"].str.len().lt(
                MINIMUM_REVIEW_LENGTH
            )
        )
        short_reviews_removed += int(short_mask.sum())

        # Keep reviews that have enough useful text.
        valid_mask = (
            chunk["Review"].str.len()
            >= MINIMUM_REVIEW_LENGTH
        )

        chunk = chunk.loc[valid_mask].copy()

        # Remove duplicate reviews, including duplicates across chunks.
        keep_rows = []

        for review in chunk["Review"]:
            if review in seen_reviews:
                keep_rows.append(False)
                duplicate_reviews_removed += 1
            else:
                seen_reviews.add(review)
                keep_rows.append(True)

        chunk = chunk.loc[keep_rows].copy()

        possible_broken_text += int(
            chunk["Review"].str.contains(
                r"Ã|Â|�",
                regex=True,
                na=False,
            ).sum()
        )

        if "Date" in chunk.columns:
            parsed_dates = pd.to_datetime(
                chunk["Date"],
                errors="coerce",
            )

            invalid_dates += int(
                parsed_dates.isna().sum()
            )

        if "Label" in chunk.columns:
            label_counts = chunk["Label"].value_counts(
                dropna=False
            )

            final_label_counts.update(
                label_counts.to_dict()
            )

        write_header = chunk_number == 1

        chunk.to_csv(
            OUTPUT_FILE,
            mode="a",
            index=False,
            header=write_header,
            encoding="utf-8",
        )

        total_final_rows += len(chunk)

        print(
            f"Chunk {chunk_number} completed | "
            f"Original rows processed: "
            f"{total_original_rows:,} | "
            f"Clean rows saved: "
            f"{total_final_rows:,}"
        )

    create_report(
        total_original_rows=total_original_rows,
        total_final_rows=total_final_rows,
        missing_reviews=missing_reviews,
        empty_reviews_removed=empty_reviews_removed,
        short_reviews_removed=short_reviews_removed,
        duplicate_reviews_removed=duplicate_reviews_removed,
        possible_broken_text=possible_broken_text,
        invalid_dates=invalid_dates,
        label_counts=final_label_counts,
    )

    print("\nDataset cleaning completed successfully.")
    print(f"\nClean dataset saved at:\n{OUTPUT_FILE}")
    print(f"\nQuality report saved at:\n{REPORT_FILE}")


def create_report(
    total_original_rows: int,
    total_final_rows: int,
    missing_reviews: int,
    empty_reviews_removed: int,
    short_reviews_removed: int,
    duplicate_reviews_removed: int,
    possible_broken_text: int,
    invalid_dates: int,
    label_counts: Counter,
) -> None:
    removed_rows = (
        total_original_rows - total_final_rows
    )

    label_lines = []

    for label, count in label_counts.items():
        percentage = (
            count / total_final_rows * 100
            if total_final_rows
            else 0
        )

        label_lines.append(
            f"- Label `{label}`: "
            f"{count:,} reviews "
            f"({percentage:.2f}%)"
        )

    label_section = "\n".join(label_lines)

    report = f"""# Week 1 Data Quality Report

## Dataset Information

- Input file: `{INPUT_FILE.name}`
- Output file: `{OUTPUT_FILE.name}`
- Original rows: {total_original_rows:,}
- Final clean rows: {total_final_rows:,}
- Total rows removed: {removed_rows:,}

## Problems Found

- Missing review values: {missing_reviews:,}
- Empty reviews removed: {empty_reviews_removed:,}
- Reviews below {MINIMUM_REVIEW_LENGTH} characters removed: {short_reviews_removed:,}
- Duplicate reviews removed: {duplicate_reviews_removed:,}
- Invalid or missing dates in final data: {invalid_dates:,}
- Reviews with possible broken characters remaining: {possible_broken_text:,}

## Cleaning Performed

- Repaired text-encoding problems
- Converted HTML characters into readable text
- Removed hidden control characters
- Removed web links
- Normalized repeated spaces, tabs and line breaks
- Preserved valid punctuation and multilingual text
- Removed empty reviews
- Removed very short reviews
- Removed duplicate reviews

## Final Label Distribution

{label_section}

## Final Result

The cleaned dataset is ready for Week 2 chunking, embeddings and vector database processing.
"""

    REPORT_FILE.write_text(
        report,
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()