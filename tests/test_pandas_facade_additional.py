"""Additional tests for the PandasFacade class to improve coverage."""

import os
import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from calculator.history.facade import PandasFacade


@pytest.fixture
def sample_dataframe():
    """Create a sample DataFrame for testing."""
    data = [
        {'a': 1, 'b': 2, 'operation': 'add', 'result': 3, 'date': '2023-01-01'},
        {'a': 4, 'b': 5, 'operation': 'add', 'result': 9, 'date': '2023-01-02'},
        {'a': 7, 'b': 3, 'operation': 'subtract', 'result': 4, 'date': '2023-01-03'},
        {'a': 6, 'b': 2, 'operation': 'multiply', 'result': 12, 'date': '2023-01-04'},
        {'a': 10, 'b': 2, 'operation': 'divide', 'result': 5, 'date': '2023-01-05'}
    ]
    return pd.DataFrame(data)


def test_merge_dataframes():
    """Test merging two DataFrames."""
    # Create two DataFrames to merge
    df1 = pd.DataFrame({'key': ['A', 'B', 'C'], 'value1': [1, 2, 3]})
    df2 = pd.DataFrame({'key': ['A', 'B', 'D'], 'value2': [4, 5, 6]})
    
    # Test inner merge
    merged_inner = PandasFacade.merge_dataframes(df1, df2, on='key')
    assert len(merged_inner) == 2  # Only A and B are in both DataFrames
    assert 'value1' in merged_inner.columns
    assert 'value2' in merged_inner.columns
    
    # Test outer merge
    merged_outer = PandasFacade.merge_dataframes(df1, df2, on='key', how='outer')
    assert len(merged_outer) == 4  # A, B, C, and D
    assert 'value1' in merged_outer.columns
    assert 'value2' in merged_outer.columns
    
    # Test with empty DataFrame
    empty_df = pd.DataFrame()
    with pytest.raises(Exception):
        PandasFacade.merge_dataframes(empty_df, df2, on='key')


def test_group_by(sample_dataframe):
    """Test grouping a DataFrame."""
    # Group by operation and aggregate
    agg_dict = {'result': ['sum', 'mean', 'count']}
    grouped = PandasFacade.group_by(sample_dataframe, 'operation', agg_dict)
    
    # Verify the grouped DataFrame
    assert len(grouped) == 4  # 4 unique operations
    assert 'operation' in grouped.columns
    assert ('result', 'sum') in grouped.columns
    assert ('result', 'mean') in grouped.columns
    assert ('result', 'count') in grouped.columns
    
    # Test with empty DataFrame
    empty_df = pd.DataFrame()
    empty_grouped = PandasFacade.group_by(empty_df, 'operation', agg_dict)
    assert empty_grouped.empty


def test_generate_chart(sample_dataframe):
    """Test generating charts from a DataFrame."""
    # Test bar chart
    bar_chart = PandasFacade.generate_chart(sample_dataframe, 'bar', 'operation', 'result')
    assert isinstance(bar_chart, str)
    assert len(bar_chart) > 0
    
    # Test line chart
    line_chart = PandasFacade.generate_chart(sample_dataframe, 'line', 'operation', 'result')
    assert isinstance(line_chart, str)
    assert len(line_chart) > 0
    
    # Test pie chart
    pie_chart = PandasFacade.generate_chart(sample_dataframe, 'pie', 'operation')
    assert isinstance(pie_chart, str)
    assert len(pie_chart) > 0
    
    # Test histogram
    hist_chart = PandasFacade.generate_chart(sample_dataframe, 'hist', 'result')
    assert isinstance(hist_chart, str)
    assert len(hist_chart) > 0
    
    # Test with invalid chart type
    invalid_chart = PandasFacade.generate_chart(sample_dataframe, 'invalid', 'operation', 'result')
    assert invalid_chart == ""
    
    # Test with empty DataFrame
    empty_df = pd.DataFrame()
    empty_chart = PandasFacade.generate_chart(empty_df, 'bar', 'operation', 'result')
    assert empty_chart == ""


def test_pivot_table_edge_cases(sample_dataframe):
    """Test pivot table with edge cases."""
    # Test with non-existent columns
    pivot = PandasFacade.pivot_table(sample_dataframe, 'non_existent', 'result')
    assert pivot.empty
    
    pivot = PandasFacade.pivot_table(sample_dataframe, 'operation', 'non_existent')
    assert pivot.empty
    
    # Test with empty DataFrame
    empty_df = pd.DataFrame()
    pivot = PandasFacade.pivot_table(empty_df, 'operation', 'result')
    assert pivot.empty
