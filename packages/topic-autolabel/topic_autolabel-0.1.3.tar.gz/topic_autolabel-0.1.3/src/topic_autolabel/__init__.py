from typing import List, Optional

import pandas as pd

from .core.data_loader import load_data
from .core.labeler import TopicLabeler


def process_file(
    filepath: Optional[str],
    text_column: str,
    df: Optional[pd.DataFrame] = None,
    model_name: str = "meta-llama/Llama-3.1-8B-Instruct",
    num_labels: Optional[int] = 5,
    candidate_labels: Optional[List[str]] = None,
    batch_size: Optional[int] = 8,
) -> pd.DataFrame:
    """
    Process a file and add topic labels to it.

    Args:
        filepath: Path to the CSV file
        text_column: Name of the column containing text to process
        model_name: Name of the HuggingFace model to use
        num_labels: Number of labels to generate (if candidate_labels is None)
        candidate_labels: List of predefined labels to choose from (optional)

    Returns:
        DataFrame with a new 'label' column containing the generated labels
    """
    try:
        assert filepath is not None or df is not None
    except AssertionError:
        raise ValueError("One of filepath or df must be passed to the function.")

    # Load the data
    if df is None:
        df = load_data(filepath, text_column)

    # Initialize the labeler
    labeler = TopicLabeler(model_name=model_name, batch_size=batch_size)

    # Generate labels
    labels = labeler.generate_labels(
        df[text_column].tolist(),
        num_labels=num_labels,
        candidate_labels=candidate_labels,
    )

    # Add labels to dataframe
    df["label"] = labels

    return df


__all__ = ["process_file"]
