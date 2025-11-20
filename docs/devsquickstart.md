# Developers Guide

This guide is inteded for users that want to create their own AI-power reserach tools. It will walk you through the basic components of this package and how to structure your own tool so that it can be succesully deployed in the main package API.

## 📥 Clone the gptquery Project

Clone the repository to build custom tools based on GPTQuery, clone the repo and install dependencies:

```shell
# 1. Clone the repo:
git clone https://github.com/mauriciomm7/gptquery.git
cd gptquery
# 2. Install as editable package:
pip install -e .
```

## 🧱 Building Blocks

The building blocks of this package are three: 1) `GPTClient()`, 2) `Throttler()`, 3) `ExecutionLogger()`.

### GPTClient

The GPTClient class is the core interface for interacting with multiple GPT-based API providers (currently supporting OpenAI, Perplexity, and Claude). It standardizes the process of sending and receiving chat completions across different APIs, handling authentication, model validation, request formatting, retries, and error management under a unified abstraction.

The logic of this GPTClient is that you initialize it with the parameters you want, and once you’ve done so, you can run queries repeatedly using the same configuration — without needing to reauthenticate, reselect the provider, or redefine the model each time.

```python
from gptquery.core import GPTClient
# 1. Initialize a client 
client = GPTClient(api_key="sk-123", 
                   provider="openai", 
                   default_model="gpt-4.1-mini")

# 2. Loop through list of items
for user_message in texts:
    result = client.extract(
                text=user_message,           # User message (dynamic question data)
                prompt=system_message)       # System message (static instructions)
```

Without persistent initialization, you’d be rebuilding all headers and configs per iteration — inefficient and more likely to trigger rate limits.

### Throttler

Now, that you can now run many queries using a basic loop, you may still want to run them in paralell but without hitting any of the tokens per minute (TKM), or requests per minute (RPM). Here is where the Throttler functions come in handy. In this package there are three but for simplicity I will showcase `SimpleThrottler()` as is enough for most scenarios.

```python
from gptquery.core import GPTClient
from gptquery.processing import GPTClient

# Initialize the GPT client
client = GPTClient(model="gpt-4.1-mini", temperature=0)

# Initialize a simple throttler to control request rate
throttler = SimpleThrottler(max_requests_per_minute=60)

# Example list of prompts
prompts = [] # <-- Assume list of prompts
results = []
for prompt in prompts:
    throttler.wait_for_slot()  # ENSURES we stay within rate limits
    result = client.query(prompt)
    results.append(result)
```

### ExecutionLogger

Unlike the first two components, `ExecutionLogger` focuses on logging the execution details of your tools. It saves structured JSON logs to a `logs/` directory in the user’s working folder, useful for auditing, debugging, and transparency.

```python
from gptquery.core.execution_logger import ExecutionLogger

class ToolLogger(ExecutionLogger):
    def __init__(self):
        super().__init__("tool_name")

    def log_execution(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            duration = time.time() - start
            self.save_execution_log({"execution_time": duration})
            return result
        return wrapper
```

Then once you built the tool-specific logging class you can add it as a decorator class for every time you run the class.

```python
# Initialize the ToolLogger
logger = ToolLogger()

@logger.log_execution
def my_function(data):
    # Your processing here
    return data
```

## 🔨 Creating an AI-Powered Tool

Under the project dir you will find a `tools/` directory which is where the GPI Tools live. These task-specific tools have the following structure:

- **Task-Specific Tools (`tools/`)**
  - Each tool lives in its own namespace (e.g., `tool_name`).  
  - Tools are subdivided into **submodules/steps**:
    - `prompt.py` → AI prompt definitions
    - `task.py` → user-facing functions (`run_*`)  
    - `log.py` → logging utilities  
  - The tool’s `__init__.py` exposes the main public API.

### `prompt.py`

The first step in creating a tool is to createa a `prompt.py`. This will contain the prompt constructor fucntion and system prompt. The prompt constructor will take text specific paramentes that will be used to generate the `user_msg`. You can think of these paramters as the columns from a dataframe entry. When building this fucntion you can pass the `@requires_columns()` decorator to make sure that when you call the fucntion it receives the correct parameters. When building this function, you can apply the @requires_columns() decorator to ensure it receives the correct parameters when called. This is important because it guarantees that the tool call follows a contract by requiring all necessary inputs, preventing runtime errors and ensuring consistent behavior.

```python
# tool_name/step_one/prompt.py

@requires_columns("first_page_text")
def prompt_extract_affiliations(first_page_text: str) -> str:
    user_message = f"""TEXT TO ANALYZE:
{first_page_text}

EXTRACTION TASK: Extract all institutions or organizations associated with the authors. 
Include universities, ministries, commissions, research institutes, or other organizations. 
Separate each institution with a comma. Ignore faculties, departments, research groups, addresses, or individual offices."""
    return user_message.strip()
```

The static system message is `system_message`

```python
# tool_name/step_one/prompt.py
SYSTEM_MSG = """
This is is the static message that will be passes as system_message for every call.
You can use multiline formatting as long as you use the triple quotation marks.

And even add '\n' new lines directly.
"""
```

### `task.py`



### `log.py`

