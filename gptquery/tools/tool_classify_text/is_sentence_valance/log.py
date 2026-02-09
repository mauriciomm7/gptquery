# gptquery\gptquery\tools\tool_classify_text\is_agent_target\log.py
import time
import functools
from ....processing.error_constants import PROCESSING_ERROR, API_ERROR, ERROR
from typing import Any
from ....core.execution_logger import ExecutionLogger

class IsAgentTarget(ExecutionLogger):
    """IS Agent Target specific logging implementation."""
        
    def __init__(self):
        super().__init__("is_agent_target")
        
    def log_execution(self, func):
        """Tool-specific decorator for is_agent_target."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                execution_stats = {
                    "model": kwargs.get("model"),
                    "parameters": {
                        "temperature": kwargs.get("temperature", 0.0),
                        "max_tokens": kwargs.get("max_tokens", 10000)
                    },
                    "execution_stats": {
                        "total_rows":  len(kwargs["df"]),
                        "execution_time_seconds": round(execution_time, 2),
                        "successful_operations": self._count_successful_operations(result),
                        "error_count": self._count_errors(result)
                    },
                    "system_message": kwargs.get("system_message")
                }
                
                self.save_execution_log(execution_stats)
                return result
                
            except Exception as e:
                execution_time = time.time() - start_time
                error_stats = {
                    "model": kwargs.get("model", "gpt-4.1-mini"),
                    "execution_stats": {
                        "execution_time_seconds": round(execution_time, 2),
                        "error": str(e),
                        "status": "failed"
                    }
                }
                self.save_execution_log(error_stats)
                raise
        
        return wrapper
    
    def _count_successful_operations(self, result: Any) -> int:
        """Count successful affiliation extraction operations."""
        if not hasattr(result, 'is_agent'):
            return 0
        # ERROR STRINGS for text exactness
        error_strings = {ERROR, API_ERROR, PROCESSING_ERROR}
        return sum(1 for r in result['is_agent'] if r not in error_strings) 

    
    def _count_errors(self, result: Any) -> int:
        """Count error operations."""
        if not hasattr(result, 'is_agent'):
            return 0
        # ERROR STRINGS for text exactness
        error_strings = {ERROR, API_ERROR, PROCESSING_ERROR}
        return sum(1 for r in result['is_agent'] if r in error_strings)
