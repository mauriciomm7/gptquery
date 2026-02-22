# Classify EU Legal Scholarship

This is a set of tools created to classify text snippets from EU legal scholarship, determining whether a listed entity is the grammatical subject (agent) of a sentence or clause.

## Basic Usage Description

### ✔️ VALIDATE Whether Listed Entity Is Subject in Sentence

The tool `run_is_sentence_valance_basic()` expects a text column containing a sentence or snippet and a column identifying the candidate entity. For each row, the prompt function combines these into a user message. The LLM returns `1` if the entity is the agent/subject of the sentence, or `0` if it is not.

```python
from gptquery.tools.tool_classify_text import run_is_sentence_valance_basic
df = ...  # DataFrame with required text columns
df_out = run_is_sentence_valance_basic(df, api_key="your-openai-key")
print(df_out['is_agent'])
# [1, 0, 1, "PROCESSING_ERROR"]
```

### 📤 Input/Output Schema

**Input Columns** *(required by the prompt function)*:

| Column | Type | Description |
|---|---|---|
| `sentence_text` | str | The sentence or clause to classify |
| `entity` | str | The candidate entity to check as grammatical subject |

**Output Column**:

- `is_agent` → `1` if the entity is the subject/agent of the sentence, `0` if not, `"PROCESSING_ERROR"` if the LLM returns an unexpected value, `"API_ERROR"` on request failure

### 💾 Example DataFrame

| sentence_text | entity | is_agent |
|---|---|---|
| "The Commission submitted observations on the admissibility of the request." | Commission | `1` |
| "The request was submitted to the Commission by the referring court." | Commission | `0` |
| "Member States must transpose the Directive by 31 December." | Member States | `1` |
| *(malformed/empty row)* | — | `"PROCESSING_ERROR"` |

> **Note:** Unlike the extraction tools, `is_agent` returns a scalar integer per row (not a list), and invalid LLM outputs (`result not in ['1', '0']`) are caught and flagged as `"PROCESSING_ERROR"` rather than silently coerced.