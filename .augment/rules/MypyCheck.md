---
type: "manual"
---

I will provide you with a Python file that needs type checking and fixes. Please follow these steps:

1. First, examine the Python file I provide to understand its structure and current state
2. Run mypy type checking on the file to identify all type-related issues
3. Analyze each mypy error or warning message carefully
4. Fix all type issues found by mypy, which may include:

   - Adding missing type annotations for function parameters, return types, and variables
   - Fixing incorrect type annotations
   - Resolving type compatibility issues
   - Adding necessary imports for typing constructs (e.g., from typing import List, Dict, Optional, etc.)
   - Handling None/Optional types properly
   - Fixing any other type-related problems

5. After making the fixes, run mypy again to verify that all issues have been resolved
6. Ensure the code still functions correctly after the type fixes

Please make minimal changes focused only on resolving the mypy issues while preserving the original functionality of the code. If you encounter any ambiguous cases where the intended type is unclear, ask for clarification before proceeding.
