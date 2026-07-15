import sys

import numpy as np
import pandas as pd
import pytest
from charset_normalizer import from_bytes


def verify_environment() -> None:
    print("Python version:", sys.version.split()[0])
    print("Pandas version:", pd.__version__)
    print("NumPy version:", np.__version__)
    print("Pytest version:", pytest.__version__)

    sample_numbers = np.array([10, 20, 30])
    print("NumPy test result:", sample_numbers.mean())

    sample_data = pd.DataFrame(
        {
            "text": ["First document", "Second document"],
            "label": [0, 1],
        }
    )

    print("\nPandas test:")
    print(sample_data)

    encoding_test = from_bytes("Environment verified".encode("utf-8")).best()

    if encoding_test is None:
        raise RuntimeError("Encoding verification failed.")

    print("\nEncoding test:", str(encoding_test))
    print("\nEnvironment verification successful.")


if __name__ == "__main__":
    verify_environment()