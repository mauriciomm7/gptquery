# Quick Start

The goal of this package is to enable reserachers (or anyone) to create tractable AI tools that were used in for preocessing the data of any research paper. This quickstart guide is inteded for end-users of these tools. If you wnat to create your own tool check out [developers guide](./devsquickstart.md).

## Installation

Install the latest stable release directly from PyPI using pip:

```Shell
pip install gptquerytools
```

## 🔑 Authentication

Use [**python-dotenv**](https://pypi.org/project/python-dotenv/) (Python) to load the environment variable from a .env file:

```python
from pathlib import Path
from dotenv import load_dotenv

# LOAD environment variables from <name>.env file
SECRETS_FILE = Path(r"C:\LocalSecrets\master.env")
load_dotenv(str(SECRETS_FILE))

# ASSIGN the values of the environment variables
openai_key = str(os.getenv("OPENAI_UIO24EMC_KEY"))
```

Now everytime you make a tool call you just have to provide the api key that you want to use.

## 🎮 1. EU Law Citations Proccessing

The following examples correspond to the EU Law Citations Tools. For full details see [full docs](./tools/eulaw_citations.md).

- **Example 1**: Validate whether all in-text citations from `question_text` are in `potential_citations`:

```python
from gptquery import run_validate_basic
new_validate_df = run_validate_basic(df_validation, 
                                     api_key=openai_key, 
                                     model="gpt-4.1-mini")
print(new_validate_df['is_complete'])  
>>> # RESULT Dataframe new col:
>>> [["complete"], ["incomplete"], ["ERROR"]]
```

- **Example 2**: Extract missing in-text citations from `question_text` that are NOT listed in `potential_citations`:

```python
from gptquery import run_extract_basic
df_out = run_extract_basic(df_validation,
                           api_key=openai_key, 
                           model="gpt-4.1-mini"))
print(df_out['missing_citations'])
>>> # Result DataFrame has new 'missing_citations' column:
>>> [[], ["citation1"], ["citation1", "citation2"], ["ERROR"]]
```

## 🎮 2. Text Extracting Tools


## 💰 Cost Estimation Utilities

