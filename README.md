# GPTQuery – Modular Tool Framework

[![PyPI version](https://img.shields.io/pypi/v/gptquerytools.svg)](https://pypi.org/project/gptquerytools/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

GPTQuery is a modular Python framework for building, orchestrating, and deploying AI-powered tools across domains. It provides a clear, scalable architecture for integrating multiple AI providers (OpenAI, Perplexity, Claude, etc.) while maintaining robust error handling, throttling, and dynamic prompting.

## 📋 Project Description

The goal of this project is for researchers (or anyone) to create AI-powered tools using custom prompts that can be easily integrated into reserach pipelines. In theory, you can equally  use the libraries provided by `openai`, `anthropic`, or `perplexity`. However, the adavantages of this framework is that it handles `throttling`, `logging` and task specific post-processing. That is, when you create a tool following the proposed tool architecture you ensure robustness and transparency for sharing you specific tool\prompt with other researchers in a reliable way.

## 🏗️ Architecture Overview

GPTQuery is organized into **three main layers**:

1. **Core Infrastructure (`core/`)**
   - Clients, logging, and utilities.

2. **Processing Utilities (`processing/`)**  
   - Helpers for throttling, token management, and miscellaneous runtime functions.

3. **Task-Specific Tools (`tools/`)**  
   - Each tool lives in its own namespace (e.g., `tool_name`).  
   - Tools are subdivided into **submodules/steps**:
     - `task.py` → user-facing functions (`run_*`)  
     - `prompt.py` → AI prompt definitions  
     - `log.py` → logging utilities  
   - The tool’s `__init__.py` exposes the main public API.

**Example: A generic AI tool (`tool_example`)**

```shell
tool_example/
├── step_one/
│ ├── task.py # run_step_one
│ ├── prompt.py
│ └── log.py
├── step_two/
│ ├── task.py # run_step_two
│ ├── prompt.py
│ └── log.py
└── init.py # exposes run_step_one, run_step_two
```

## 🚀 Features

- **Multi-Provider Support**: Unified interface for OpenAI, Perplexity, Claude, and other AI APIs.  
- **Modular Tool Design**: Organize AI functionality into independent, reusable tool families.  
- **Task Step Separation**: Each tool can have multiple steps or functional modules.  
- **Smart Defaults**: Automatically selects optimal models or parameters per provider.  
- **Safe Data Operations**: Uses `@requires_columns` for safe DataFrame operations.
- **Advanced Throttling**: Token bucket and adaptive rate-limiters for API management.  
- **Robust Error Handling**: Preserves partial results and gracefully handles failures.  
- **Cost Optimization**: Integrates token management to reduce API costs.  

## 🛠️ Installation

Option 1: Install from PyPI (recommended)
Install the latest stable release directly from PyPI using pip:

```shell
pip install gptquerytools
```

Option 2: Clone the repository (for development and custom tools)
If you want to contribute or build custom tools based on GPTQuery, clone the repo and install dependencies:

```shell
# 1. Clone the repo:
git clone https://github.com/mauriciomm7/gptquery.git
cd gptquery
# 2. Install dependencies:
pip install -r requirements.txt
```

## 🎓 Citation

If you use this framework in academic research, please cite:

Mandujano Manríquez, M. (2025). *GPTQuery: Modular framework for building and orchestrating AI-powered research tools.*
GitHub: https://github.com/mauriciomm7/gptquery

```bibtex
@misc{mandujano2025gptquery,
  author       = {Mauricio Mandujano Manríquez},
  title        = {GPTQuery: Modular framework for building and orchestrating AI-powered research tools},
  year         = {2025},
  howpublished = {\url{https://github.com/mauriciomm7/gptquery}},
  note         = {GitHub repository}
}
```

## 🤝 Contrubuting

To integrate your tool into GPTQuery, please:

- Place your tool inside the `tools/` directory following the existing modular structure.

- Organize your tool with submodules for each step or feature, including:
  - `task.py` for core functionality.
  - `prompt.py` for AI prompts.
  - `log.py` for logging.

- Expose your tool’s API in its `__init__.py`.
- Write tests and update documentation as needed.
- Submit a pull request with clear explanations of your additions.

Thank you for contributing to GPTQuery!

## 🙏 Acknowledgments

- CI/CD automation using GitHub Actions — Automating build, test, and deployment workflows  
- [tokencost](https://pypi.org/project/tokencost/) — Token cost estimation for language models  
- [tiktoken](https://github.com/openai/tiktoken) — Tokenization library used for accurate token counts  
- [IPython](https://pypi.org/project/ipython/) — Interactive computing environment and enhanced Python shell

## 📄 License

This project is licensed under the [MIT License](./LICENSE).

## ✅ TODO

- [X] ADD GPTVisionClient that handles files.
- [ ] ADD Example of GPTVisionClient.
- [ ] ADD COL paramters to facing api such that it renames columns and never breaks contract?
- [ ] DOCS - UPDATE the codeblocks aesthetics, better spacing.
- [ ] DOCS - ADD copy-paste to codeblocks.
- [ ] UPDATE logger to make column naming easier.

Useful commands:

```shell
# Build Docs
mkdocs build 
mkdocs serve

# Build Package
rm -rf dist build *.egg-info
python -m build
twine upload dist/*
```
