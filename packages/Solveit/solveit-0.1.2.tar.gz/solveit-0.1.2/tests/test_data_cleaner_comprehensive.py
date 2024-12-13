import pytest
import pandas as pd
import numpy as np
import os
import tempfile
from pathlib import Path
from solveit.data.cleaner import DataCleaner

@pytest.fixture
def complex_df():
    return pd.DataFrame({
        'Name': ['John', 'Jane', 'John', 'Bob', None, 'Alice'],
        'Age': [25, 30, 25, None, 45, 1000],
        'Salary': [50000, None, 50000, 60000, 75000, 80000],
        'Department': ['IT', 'HR', 'IT', 'Finance', None, 'IT']
    })

def test_complete_workflow(complex_df):
    cleaner = DataCleaner()
    
    # Save to temporary files
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = Path(tmpdir) / "input.csv"
        output_path = Path(tmpdir) / "output.csv"
        excel_path = Path(tmpdir) / "output.xlsx"
        
        # Test CSV handling
        complex_df.to_csv(input_path, index=False)
        
        # Test the complete cleaning process
        cleaner.process_file(
            input_path=input_path,
            output_path=output_path,
            operations=[
                ('remove_duplicates', {}),
                ('handle_missing_values', {
                    'strategy': 'mean',
                    'custom_values': {'Department': 'Unknown', 'Name': 'Anonymous'}
                }),
                ('remove_outliers', {
                    'columns': ['Age', 'Salary'],
                    'method': 'zscore',
                    'threshold': 2.0
                })
            ]
        )
        
        # Load and verify results
        result_df = pd.read_csv(output_path)
        
        # Verify duplicate removal
        assert len(result_df) < len(complex_df)
        assert not result_df.duplicated().any()
        
        # Verify missing value handling
        assert not result_df['Age'].isna().any()
        assert not result_df['Salary'].isna().any()
        assert not result_df['Department'].isna().any()
        assert 'Unknown' in result_df['Department'].values
        
        # Verify outlier removal
        assert 1000 not in result_df['Age'].values
        
        # Test Excel handling
        cleaner.save_file(result_df, excel_path)
        excel_df = pd.read_excel(excel_path)
        pd.testing.assert_frame_equal(result_df, excel_df)

def test_error_handling():
    cleaner = DataCleaner()
    
    # Test invalid file path
    with pytest.raises(FileNotFoundError):
        cleaner.load_file("nonexistent.csv")
    
    # Test invalid file format
    with tempfile.NamedTemporaryFile(suffix='.txt') as tmp:
        with pytest.raises(ValueError):
            cleaner.load_file(tmp.name)
    
    # Test invalid operation
    with tempfile.NamedTemporaryFile(suffix='.csv') as input_file, \
         tempfile.NamedTemporaryFile(suffix='.csv') as output_file:
        pd.DataFrame({'A': [1]}).to_csv(input_file.name, index=False)
        with pytest.raises(ValueError):
            cleaner.process_file(
                input_path=input_file.name,
                output_path=output_file.name,
                operations=[('invalid_operation', {})]
            )

def test_custom_value_handling(complex_df):
    cleaner = DataCleaner()
    
    result = cleaner.handle_missing_values(
        complex_df,
        strategy='custom',
        custom_values={
            'Name': 'Unknown',
            'Department': 'General',
            'Age': 0,
            'Salary': 0
        }
    )
    
    assert 'Unknown' in result['Name'].values
    assert 'General' in result['Department'].values
    assert 0 in result['Age'].values
    assert 0 in result['Salary'].values 