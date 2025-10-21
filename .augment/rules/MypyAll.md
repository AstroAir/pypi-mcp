---
type: "manual"
---

Run mypy type checking across the entire pypi-mcp project and systematically fix all type-related errors that are found. Please follow these steps:

1. First, run mypy on the entire project to identify all type checking errors
2. Analyze the errors and categorize them by type (missing type annotations, incorrect types, import issues, etc.)
3. Create a plan to address each category of errors systematically
4. Fix the errors one by one, ensuring that:
   - Type annotations are added where missing
   - Incorrect type annotations are corrected
   - Import statements are fixed if needed
   - Any mypy configuration issues are resolved
5. After making fixes, re-run mypy to verify that the errors have been resolved
6. Continue this process until mypy runs cleanly with no errors
7. Suggest running tests after the fixes to ensure functionality is preserved

Please be thorough and methodical in addressing all type checking issues to improve the project's type safety.
