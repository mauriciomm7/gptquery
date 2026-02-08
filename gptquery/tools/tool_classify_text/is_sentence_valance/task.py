# gptquery\gptquery\tools\tool_classify_text\is_agent_target
"""
Is agent snippet classification  task execution with external throttling and robust error handling.
"""
import pandas as pd
from typing import Optional, Callable, Any
from ....core.client import GPTClient
from ....processing.utils import validate_required_columns, report_progress_step, report_final
from ....processing.error_constants import PROCESSING_ERROR, API_ERROR
from .prompts.default import IS_SETENCE_SYSTEM_MESSAGE
from .log import IsAgentTarget

# # Create logger instance
logger = IsAgentTarget()

@logger.log_execution
def run_is_sentence_valance(df: pd.DataFrame, 
                             prompt_func: Callable, 
                             api_key: str, 
                             model: str,
                             throttler: Optional[Any] = None, 
                             provider: str = "openai", 
                             verbose: bool = True, 
                             system_message: str = "", 
                             **kwargs) -> pd.DataFrame:
    """ """
        
    # VALIDATE required columns before starting
    validate_required_columns(df, prompt_func)
    
    # IMPORT only when needed
    if throttler is None:
        from ....processing.throttling import SimpleThrottler
        throttler = SimpleThrottler(rpm=50) # type: ignore
    
    # INITIALIZE multi-provider client
    client = GPTClient(api_key, model, provider)
    
    # PREPARE to collect results
    results = []
    total_rows = len(df)
    if verbose:
        print(f"Starting {run_is_sentence_valance.__name__} of {total_rows} rows using {provider}...")
    
    # PROCESS each row
    for i, (idx, row) in enumerate(df.iterrows()):
        try:
            # Apply throttling
            if throttler:
                throttler.wait_if_needed()
            
            # Generate user message only (dynamic content)
            user_message = prompt_func(**row.to_dict(), **kwargs)
            
            # Make API call with system/user message separation
            result = client.extract(
                text=user_message,                         # User message (dynamic question data)
                prompt=system_message,                     # System message (static instructions)
                model=model,
                temperature=0.0,                           # Deterministic for extraction
                max_tokens=kwargs.get('max_tokens', 5000)  # Extraction may need more tokens
            )
            # PROCESS the result
            processed_result = _process_output(result)
            results.append(processed_result)
        except Exception:
            # Unexpected errors - return 'ERROR'
            results.append(API_ERROR)
            if verbose:
                print(f"Unexpected error at row {i+1} ({provider})")
        
        # Progress updates every 10%
        if verbose:
            report_progress_step(i, total_rows)
    
    # Create result DataFrame
    result_df = df.copy()
    result_df['is_agent'] = results
    
    # Final Stats
    if verbose:
        report_final(results, len(results))
    return result_df


def _process_output(result: str):
    """
    PROCESS LLM output for guided outputs.
    """
    # Handle the weird cases
    if not result or result not in ['1','0']:
        print (f"{PROCESSING_ERROR} SEE :{result}")
        return PROCESSING_ERROR
    # CAST as integers
    out_value = int(result)
    return out_value


def run_is_sentence_valance_basic(df: pd.DataFrame, 
                                   api_key: str, 
                                   provider: str = "openai",
                                   model: str = "gpt-4.1-mini",
                                   system_message: str = IS_SETENCE_SYSTEM_MESSAGE, 
                                   **kwargs) -> pd.DataFrame:
    """
    Convenience function for basic affiliation extraction with default prompt and multi-provider support.
    """
    from .prompts.default import prompt_is_sentence_valance
    
    return run_is_sentence_valance(
        df=df,
        prompt_func=prompt_is_sentence_valance,
        api_key=api_key,
        provider=provider,
        model=model,
        system_message=system_message,
        **kwargs
    )
