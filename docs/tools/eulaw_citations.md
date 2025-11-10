# EU Law Citations Processing

## 📋 Tools Description

### 🔧 VALIDATE whether all in-text citations are listed (OpenAI - Default)

The fist tool `run_validate_basic()` expects that you provide a text column (`question_text`) where there may be in-text EU Law citations and separately, as as single string, a list of all citation (`potential_citations`). For each row the prompt function combines the text of text with this list of citations to make the user message `user_msg`. Using these dyanmic user messages and the same tool specific system prompt, it returns whether there are any missing citations or all are covered by the provided list.

```python
from gptquery.tools.tool_eulaw_citations import run_validate_basic
df = ...  # DataFrame with 'question_text' and 'potential_citations'
df_out = run_validate_basic(df, api_key="your-openai-key")
print(df['is_complete'])  # "complete" or "incomplete"
```

### 🔧 EXTRACT EU Law in-text citations (OpenAI - Default)

The second tool is `run_extract_basic()` which expects that you provide a text column (`question_text`) where there may be in-text EU Law citations and separately, as a single string, a list of all citations (`potential_citations`). For each row, the prompt function combines the text of `question_text` with this list of citations to make the user message `user_msg`.

```python
from gptquery.tools.tool_eulaw_citations import run_extract_basic
df = ...  # DataFrame with 'question_text' and 'potential_citations'
df_out = run_validate_basic(df, api_key="your-openai-key")
print(df['missing_citations']) 
>>> #Result DataFrame has new 'missing_citations' column:
>>> [[], ["citation1"], ["citation1", "citation2"], ["ERROR"]]
```

For this tool you can specify the level fo granularity to either:

- `"full"` – Only check if the instrument is cited
- `"article"` – Must match article numbers
- `"paragraph"` – Must match paragraphs and points

```python
df_out = run_validate_basic(df, 
                            api_key="your-openai-key", 
                            granularity="article")
print(df['missing_citations']) 
#Result DataFrame has new 'missing_citations' column:
>>> [[], ["citation1"], ["citation1", "citation2"], ["ERROR"]]
```

### 🔧 SELECT EU Law in-text citations (OpenAI - Default)

```python
from gptquery.tools.tool_eulaw_citations import run_select_basic
df = ...  # DataFrame with 'question_text' and 'potential_citations'
df_result = run_select_basic(df, "openai-api-key")
# Result DataFrame has new 'selected_citations' column:
>>> [[], ["citation1"], ["citation1", "citation2"], ["ERROR"]]
```

## 📤 Input/Output Schema

**Input Columns**:

| Column              | Type | Description                                  |
|---------------------|------|----------------------------------------------|
| `question_text`     | str  | The legal question to analyze                |
| `potential_citations` | str  | Newline-separated CELEX-format citations     |

**Output Columns**:

- `is_complete` → "complete" or "incomplete"
- `missing_citations` → list of citation strings
- `selected_citations` → list of citation IDs
