# EU Law Citations Processing

This set of tools were created to extract EU Law citations from text following a standarized approach. It works best when you first scrape citations from metadata and provide them as a baseline for the LLM to extract them.


## Basic Usage Description


### 🔧 VALIDATE whether all in-text citations are listed

The first tool, `run_validate_basic()`, expects a text column (`question_text`) that may contain in-text EU law citations, and separately, a single string listing all citations (`potential_citations`). For each row, the function combines the text with this list of citations to create the user message (`user_msg`). Using these dynamic user messages and a tool-specific system prompt, it determines whether any citations are missing or if all are covered by the provided list.

```python
from gptquery.tools.tool_eulaw_citations import run_validate_basic
df = ...  # DataFrame with 'question_text' and 'potential_citations'
df_out = run_validate_basic(df, api_key="your-openai-key")
print(df_out['is_complete'])  # "complete" or "incomplete"
```

### 🔧 EXTRACT EU Law in-text citations

The second tool is `run_extract_basic()` which expects that you provide a text column (`question_text`) where there may be in-text EU Law citations and separately, as a single string, a list of all citations (`potential_citations`). For each row, the prompt function combines the text of `question_text` with this list of citations to make the user message `user_msg`.

```python
from gptquery.tools.tool_eulaw_citations import run_extract_basic
df = ...  # DataFrame with 'question_text' and 'potential_citations'
df_out = run_extract_basic(df, api_key="your-openai-key")
print(df['missing_citations']) 
>>> #Result DataFrame has new 'missing_citations' column:
>>> [[], ["citation1"], ["citation1", "citation2"], ["ERROR"]]
```

For this tool you can specify the level fo granularity to either:

- `"full"` – Only check if the instrument is cited
- `"article"` – Must match article numbers
- `"paragraph"` – Must match paragraphs and points

```python
df_out = run_extract_basic(df, 
                            api_key="your-openai-key", 
                            granularity="article")
print(df['missing_citations']) 
#Result DataFrame has new 'missing_citations' column:
>>> [[], ["citation1"], ["citation1", "citation2"], ["ERROR"]]
```

### 🔧 SELECT EU Law in-text citations

```python
from gptquery.tools.tool_eulaw_citations import run_select_basic
df = ...  # DataFrame with 'question_text' and 'potential_citations'
df_result = run_select_basic(df, "openai-api-key")
# Result DataFrame has new 'selected_citations' column:
>>> [[], ["citation1"], ["citation1", "citation2"], ["ERROR"]]
```

## 📤 Input/Output Schema

All the tools 

**Input Columns**:

| Column              | Type | Description                                  |
|---------------------|------|----------------------------------------------|
| `question_text`     | str  | The legal question to analyze                |
| `potential_citations` | str  | Newline-separated CELEX-format citations     |

**Output Columns**:

- `is_complete` → "complete" or "incomplete"
- `missing_citations` → list of citation strings
- `selected_citations` → list of citation IDs


## 💾 Example Dataframe

| iuropa_referral_question_id   | question_text                                                                                                             | potential_citations                         |
|:------------------------------|:--------------------------------------------------------------------------------------------------------------------------|:--------------------------------------------|
| REF_2007_0522DE_Q001          | Is additional note 5(b) to Chapter 20 of the Combined Nomenclature (1) to be interpreted as meaning that the term ‘fruit… | 31987R2658,annex I,note 5 point (a)         |
|                               |                                                                                                                           | 31987R2658,annex I,note 5 point (b)         |
| REF_2007_0522DE_Q002          | Is additional note 5(b) to Chapter 20 of the Combined Nomenclature to be interpreted as meaning that the term ‘fruit jui… | 31987R2658,annex I,note 5 point (a)         |
|                               |                                                                                                                           | 31987R2658,annex I,note 5 point (b)         |
| REF_2007_0522DE_Q003          | If both the preceding questions are answered in the affirmative, is additional note 5(b) to Chapter 20 of the Combined N… | 31987R2658,annex I,note 5 point (a)         |
|                               |                                                                                                                           | 31987R2658,annex I,note 5 point (b)         |
| REF_2008_0022DE_Q001          | Is Article 24(2) of Directive 2004/38 of the European Parliament and of the Council of 29 April 2004 (1) compatible with… | 32004L0038,main,body article 24 paragraph 2 |
|                               |                                                                                                                           | 32004L0038,main,body article 6              |
|                               |                                                                                                                           | 12006E012,main,body article 12              |
|                               |                                                                                                                           | 12006E039,main,body article 39              |
| REF_2008_0039DE_Q003          | If the answer is ‘yes’, is the national court required to take account of the prohibition of discrimination having the e… | 31989L0104,main,body article 3              |