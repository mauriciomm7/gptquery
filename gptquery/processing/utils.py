# gptquery\processing\utils.py

"""
DataFrame validation utilities for GPT query processing.
TODO 
[ ] MAYBE restructure so that logging is its own directory.

"""
import pandas as pd
from typing import Callable, List
from .error_constants import (ERROR,API_ERROR,PROCESSING_ERROR)
# from functools import wraps

def requires_columns(*columns):
    """
    Decorator to specify required DataFrame columns for prompt functions.
    
    Usage:
        @requires_columns('question_text', 'potential_citations')
        def my_prompt_function(question_text, potential_citations, **kwargs):
            return "prompt text"
    
    Args:
        *columns: Column names required by the prompt function
        
    Returns:
        Decorated function with REQUIRED_COLUMNS attribute
    """
    def decorator(func):
        func.REQUIRED_COLUMNS = list(columns)
        return func
    return decorator

def validate_required_columns(df: pd.DataFrame, prompt_func: Callable) -> None:
    """
    Validate that DataFrame has all required columns for the given prompt function.
    
    Args:
        df: DataFrame to validate
        prompt_func: Prompt function with REQUIRED_COLUMNS attribute (from @requires_columns decorator)
        
    Raises:
        ValueError: If required columns are missing from DataFrame
        AttributeError: If prompt function doesn't have REQUIRED_COLUMNS attribute
    """
    # Check if function has REQUIRED_COLUMNS attribute (from decorator)
    if not hasattr(prompt_func, 'REQUIRED_COLUMNS'):
        raise AttributeError(
            f"Prompt function '{prompt_func.__name__}' must be decorated with @requires_columns"
        )
    
    required_columns = prompt_func.REQUIRED_COLUMNS
    df_columns = set(df.columns)
    required_set = set(required_columns)
    
    # Find missing columns
    missing_columns = required_set - df_columns
    
    if missing_columns:
        missing_list = sorted(list(missing_columns))
        expected_list = sorted(required_columns)
        raise ValueError(
            f"Missing columns: {missing_list}. Expected columns: {expected_list}"
        )

def validate_row_data(row: pd.Series, required_columns: List[str]) -> None:
    """
    Validate that a row has non-null values in required columns.
    
    Args:
        row: DataFrame row to validate
        required_columns: List of column names that must have values
        
    Raises:
        ValueError: If any required column has null/NaN values
    """
    for col in required_columns:
        if pd.isna(row[col]) or row[col] is None:
            raise ValueError(f"Row has null/NaN value in required column: '{col}'")

def get_prompt_required_columns(prompt_func: Callable) -> List[str]:
    """
    Get required columns from a prompt function.
    
    Args:
        prompt_func: Prompt function with REQUIRED_COLUMNS attribute
        
    Returns:
        List of required column names
        
    Raises:
        AttributeError: If prompt function doesn't have REQUIRED_COLUMNS attribute
    """
    if not hasattr(prompt_func, 'REQUIRED_COLUMNS'):
        raise AttributeError(
            f"Prompt function '{prompt_func.__name__}' must be decorated with @requires_columns"
        )
    
    return prompt_func.REQUIRED_COLUMNS.copy()


def report_final(results: list, total_rows: int):
    """
    Prints a summary of processing results.
    
    Args:
        results (list): List of processed outputs (0, 1, or error strings like 'ERROR', 'PROCESS - ERROR').
        total_rows (int): Total number of rows processed.
    """
    error_strings = {ERROR,API_ERROR,PROCESSING_ERROR}
    error_count = sum(1 for r in results if r in error_strings)
    successful_extractions = total_rows - error_count
    
    print(f"  Successful classifications: {successful_extractions}")
    print(f"  Errors: {error_count}")
    print(f"  Total rows processed: {total_rows}")

def report_progress_step(i, total_rows):
    """
    Prints progress updates every 10% of total rows.
    
    Args:
        i (int): Current index (0-based) of processing.
        total_rows (int): Total number of rows being processed.
    """
    # Calculate step size for 10% updates
    step = max(1, total_rows // 10)
    
    if (i + 1) % step == 0 or (i + 1) == total_rows:
        percentage = ((i + 1) / total_rows) * 100
        print(f"Progress: {i+1}/{total_rows} ({percentage:.1f}%)")
