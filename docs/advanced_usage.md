# ⚗️ Advanced Usage

When you create a new tool you should make a function `*_basic()` that has all the presets required making the tool call work following default settings. However, for testing purposes or for custom pipelines you should be able to use the `run_*` function. This set-up affords flexibility and ease for both basic and power users as the basic is just a wrapper with defaults for the base main run fucntion.

## 🔀 Multi-Provider Tool Calls


```python
# OpenAI GPT-4
result_openai = run_validate_basic(df, 
                                  openai_key, 
                                  provider="openai", 
                                  model="gpt-4o")

# Perplexity Sonar
result_perplexity = run_validate_basic(df, 
                                      perplexity_key, 
                                      provider="perplexity", 
                                      model="sonar-pro")

# Claude 3.5 Sonnet  
result_claude = run_validate_basic(df, 
                                  claude_key, 
                                  provider="claude", 
                                  model="claude-3-5-sonnet-20241022")
```



```python
# RUN using perplexity with online search capability
df_pplx = run_validate(
          df,
          prompt_func=prompt_validate_completeness,
          api_key="your-perplexity-key", 
          provider="perplexity",
          model="llama-3.1-sonar-large-128k-online",  # Real-time web search
          granularity="full")
df_pplx
```


## Custom Throttling Configuration

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
```

## 💰 Cost Estimation Utilities

As you start to work with Large Language Models APIs in a regular basis you will soon realize that costs are not trivial. Thus, running a quick cost estimation will inform whether you can run a pipeline over an entire dataset or not. For this this package contains two utilities built upon  [tokencost](https://pypi.org/project/tokencost/) and [tiktoken](https://github.com/openai/tiktoken) that use up to date cost information and tokenization make this possible.

- `def estimate_costs_for_models()`

```python
## 1. COST Analysis cmlr_snippets_df for 2000 snippets
from gptquery.estimation.cost_estimator import (estimate_costs_for_models)
from gptquery.tools.tool_classify_text.is_agent_target.prompts.default import (prompt_is_agent_target,
                                                                               SNIPPETS_SYSTEM_MESSAGE)
## 2. FROM Sample data on CMLR snippets
cmlr_snippets_df = pd.read_csv("data/uot25rev/cmlr_snippets_sample.parquet")

# 3. MODELS to tests
MODELS = ["gpt-4.1-mini", "gpt-5", "gpt-5-mini","gpt-5-nano" ]

## 4. COST estimation 
costs = estimate_costs_for_models(cmlr_snippets_df,
                                  prompt_is_agent_target,
                                  models=MODELS,
                                  system_msg=SNIPPETS_SYSTEM_MESSAGE,
                                  expected_response_length= "1")

```

- `create_cost_matrix()`

```python
## 1. CREATE COST MATRIX
from gptquery.estimation.cost_estimator import (create_cost_matrix)
create_cost_matrix(costs)
```

![Example of Matrix Output](assets\advanded_usage_matrix.png)
