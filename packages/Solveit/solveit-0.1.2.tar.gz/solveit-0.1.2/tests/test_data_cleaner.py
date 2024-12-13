import pytest
import pandas as pd
import numpy as np
from solveit.data.cleaner import DataCleaner

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        'A': [1, 2, 2, None, 4, 100],
        'B': ['x', 'y', 'y', None, 'z', 'w'],
        'C': [1.1, 2.2, 2.2, 3.3, None, 4.4]
    })

def test_remove_duplicates(sample_df):
    cleaner = DataCleaner()
    result = cleaner.remove_duplicates(sample_df)
    assert len(result) == 5  # One duplicate row removed

def test_handle_missing_values_mean(sample_df):
    cleaner = DataCleaner()
    result = cleaner.handle_missing_values(sample_df, strategy='mean')
    assert not result['A'].isna().any()
    assert result['A'].iloc[3] == sample_df['A'].mean()

def test_remove_outliers(sample_df):
    cleaner = DataCleaner()
    result = cleaner.remove_outliers(
        sample_df,
        columns=['A'],
        method='zscore',
        threshold=2.0
    )
    assert len(result) == 5  # Outlier value 100 removed 