# Quick Start

The goal of this package is to enable reserachers (or anyone) to create tractable AI tools that were used to

**Basic Objects**

- `prompt_contructor_function()`
 - SYSTEM_MESSAGE

- `LoggerClass()`

- `task_running_function()`


## 🎮 Usage

## Multi-Provider Calls

```python
# OpenAI GPT-4
result_openai = run_validate_basic(df, openai_key, provider="openai", model="gpt-4o")

# Perplexity Sonar
result_perplexity = run_validate_basic(df, perplexity_key, provider="perplexity", model="sonar-pro")

# Claude 3.5 Sonnet  
result_claude = run_validate_basic(df, claude_key, provider="claude", model="claude-3-5-sonnet-20241022")
```

See [docs/](./docs) for detailed usage and architecture.


## Provider-Specific and Costum Throttling Configuration

```python
from processing.throttling import TokenBucketThrottler
from gptquery.tools.tool_eulaw_citations import run_extract
from gptquery.tools.tool_eulaw_citations.extract_citations.prompts.default import (prompt_extract_basic)

# OpenAI with custom throttling
throttler = TokenBucketThrottler(rpm=30)

df_out = run_extract(
         df,
         prompt_func=prompt_validate_completeness,
         api_key="your-openai-key",
         provider="openai",
         throttler=throttler,
         model="gpt-4.1-mini",
         granularity="article",
         progress=True )
df_out

# Perplexity with online search capability
df_pplx = run_validate(
          df,
          prompt_func=prompt_validate_completeness,
          api_key="your-perplexity-key", 
          provider="perplexity",
          model="llama-3.1-sonar-large-128k-online",  # Real-time web search
          granularity="full")
df_pplx
```
