# Week 1 Data Quality Report

## Dataset Information

- Input file: `Reviews_fixed.csv`
- Output file: `Reviews_cleaned.csv`
- Original rows: 359,052
- Final clean rows: 358,122
- Total rows removed: 930

## Problems Found

- Missing review values: 0
- Empty reviews removed: 0
- Reviews below 3 characters removed: 64
- Duplicate reviews removed: 866
- Invalid or missing dates in final data: 0
- Reviews with possible broken characters remaining: 4

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

- Label `1`: 321,550 reviews (89.79%)
- Label `-1`: 36,572 reviews (10.21%)

## Final Result

The cleaned dataset is ready for Week 2 chunking, embeddings and vector database processing.
