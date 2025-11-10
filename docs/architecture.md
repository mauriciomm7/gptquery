# Project Architecture

## GPTQuery Architecture

```shell
gptquery/                      
├── __init__.py                # Core package exports (e.g., GPTClient)
│
├── core/                      
│   ├── __init__.py            
│   ├── client.py              
│   └── execution_logger.py    
│
├── estimation/                
│   ├── __init__.py            
│   ├── cost_estimator.py      
│   ├── prompt_generator.py    
│   └── tokens.py              
│
├── processing/                
│   ├── __init__.py            
│   ├── throttling.py          
│   └── utils.py               
│
├── tools/                     
│   ├── __init__.py            # Exposes top-level tools (aliases)
│   │
│   ├── tool_eulaw_citations/  # Unified EU law citations tool
│   │   ├── __init__.py        # Exports main public API
│   │   ├── validate_citations/
│   │   │   ├── __init__.py
│   │   │   ├── task.py        # run_validate_basic
│   │   │   ├── prompt.py
│   │   │   └── log.py
│   │   ├── extract_citations/
│   │   │   ├── __init__.py
│   │   │   ├── task.py        # run_extract_basic
│   │   │   ├── prompt.py
│   │   │   └── log.py
│   │   └── select_citations/
│   │       ├── __init__.py
│   │       ├── task.py        # run_select_basic
│   │       ├── prompt.py
│   │       └── log.py
│   │
│   ├── future_tool_one/       # Future tool #1
│   │   ├── __init__.py        # Exports main public API for this tool
│   │   ├── step_a/
│   │   │   ├── __init__.py
│   │   │   ├── task.py
│   │   │   ├── prompt.py
│   │   │   └── log.py
│   │   └── step_b/
│   │       ├── __init__.py
│   │       ├── task.py
│   │       ├── prompt.py
│   │       └── log.py
│   │
│   └── future_tool_two/       # Future tool #2
│       ├── __init__.py        # Exports main public API for this tool
│       ├── step_x/
│       │   ├── __init__.py
│       │   ├── task.py
│       │   ├── prompt.py
│       │   └── log.py
│       └── step_y/
│           ├── __init__.py
│           ├── task.py
│           ├── prompt.py
│           └── log.py
│
└── utils/                     
    ├── __init__.py
    ├── data_prep.py           # Data preparation modules
    └── (other utility modules)
```

## Project & Docs Structure

```shell
gptquery/
├── gptquery/              # source code
├── docs/                  # ← documentation lives here
│   ├── index.md           # main README-style overview
│   ├── quickstart.md      # install & run examples
│   ├── architecture.md    # how modules & layers fit together
│   ├── tools/             # per-tool docs (optional, auto-generated later)
│   │   ├── eulaw_citations.md
│   │   └── future_tool_one.md
│   └── api_reference.md   # short docstrings export
├── README.md              # landing summary
├── LICENSE
└── pyproject.toml
```
