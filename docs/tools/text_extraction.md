# Extract Entities from EU Legal Text

This is a set of tools created to extract author names and affiliations from unstructured text data (e.g., first pages of legal documents or academic papers).

## Basic Usage Description

### 👤 EXTRACT Author Names

The first tool, `run_extract_authors_basic()`, expects a text column (`first_page_text`) that may contain author names. For each row, the function generates a user message via the default prompt function and sends it to the GPT client. Results are returned as a list of comma-separated author name strings.

```python
from gptquery.tools.tool_text_extraction import run_extract_authors_basic
df = ...  # DataFrame with 'first_page_text'
df_out = run_extract_authors_basic(df, api_key="your-openai-key")
print(df_out['author_names'])
# [["Katarzyna Zieleskiewicz", "Bartlomiej Kurcz"], [], ["ERROR"]]
```

### 🏫 EXTRACT Author Affiliations

The second tool, `run_extract_affiliations_basic()`, also expects a `first_page_text` column. For each row, it extracts institution and organization names. Results are returned as a list of semicolon-delimited affiliation strings.

```python
from gptquery.tools.tool_text_extraction import run_extract_affiliations_basic
df = ...  # DataFrame with 'first_page_text'
df_out = run_extract_affiliations_basic(df, api_key="your-openai-key")
print(df_out['affiliations'])
# [["University of Groningen", "Court of Justice of the EU"], [], ["ERROR"]]
```

### 📤 Input/Output Schema

**Input Columns**:

| Column | Type | Description |
|---|---|---|
| `first_page_text` | str | Raw text from the first page of a document, expected to contain author names and/or affiliations |

**Output Columns**:

- `author_names` → list of author name strings (comma-split); `[]` if none found; `["ERROR"]` on failure
- `affiliations` → list of institution/organization strings (semicolon-split); `[]` if none found; `["ERROR"]` on failure

### 💾 Example DataFrame

| doc_id | first_page_text | author_names | affiliations |
|---|---|---|---|
| DOC_001 | "Written observations submitted by Katarzyna Zieleskiewicz, University of Groningen..." | `["Katarzyna Zieleskiewicz"]` | `["University of Groningen"]` |
| DOC_002 | "Submitted on behalf of the Commission by J. Hottiaux, acting as agent..." | `["J. Hottiaux"]` | `["European Commission"]` |
| DOC_003 | *(cover page only, no author block)* | `[]` | `[]` |