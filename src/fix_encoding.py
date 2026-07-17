from pathlib import Path

import pandas as pd
from ftfy import fix_text


PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_FILE = PROJECT_ROOT / "data" / "raw" / "Reviews.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "cleaned" / "Reviews_fixed.csv"


def main() -> None:
    if not RAW_FILE.exists():
        raise FileNotFoundError(f"File not found: {RAW_FILE}")

    # latin1 can read all byte values without a decoding error
    dataframe = pd.read_csv(
        RAW_FILE,
        encoding="latin1",
        low_memory=False,
    )

    if "Review" not in dataframe.columns:
        raise ValueError(
            "Review column not found. "
            f"Available columns: {dataframe.columns.tolist()}"
        )

    print("Rows loaded:", len(dataframe))
    print("\nBefore fixing:")
    print(dataframe["Review"].head(5).to_string(index=False))

    dataframe["Review"] = dataframe["Review"].apply(
        lambda value: fix_text(value) if isinstance(value, str) else value
    )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    dataframe.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8",
    )

    print("\nAfter fixing:")
    print(dataframe["Review"].head(5).to_string(index=False))

    print(f"\nFixed dataset saved here:\n{OUTPUT_FILE}")


if __name__ == "__main__":
    main()