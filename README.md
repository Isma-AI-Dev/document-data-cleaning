# Document Data Cleaning Project

This project prepares a real-world text dataset for cleaning, testing, and later processing.

## Week 1

The first week focuses on:

- Setting up the Python environment
- Collecting and validating a text dataset
- Writing text-cleaning functions
- Testing the cleaning functions
- Producing a clean dataset
- Creating a data-quality report

## Environment Setup

Create the Python environment:

```bash
python -m venv .venv

## Label Distribution

The dataset contains 359,052 reviews:

- `1` represents a genuine review: 322,167 reviews (89.73%)
- `-1` represents a fake review: 36,885 reviews (10.27%)

The dataset has an imbalanced label distribution, with fewer fake reviews
than genuine reviews.
## Dataset Download

The dataset files are not stored directly in this GitHub repository because
they exceed GitHub's file-size limit.

- Raw dataset: https://drive.google.com/file/d/1catABWJLC1kvIX9kAXrcuhfnYkdqsWG9/view?usp=drive_link
- Encoding-repaired dataset: https://drive.google.com/file/d/1K4v5tZTLDlVxdP0ZcuAoytiIcssJPsMA/view?usp=drive_link

Place the downloaded files in these locations:

- `data/raw/Reviews.csv`
- `data/cleaned/Reviews_fixed.csv`