# Lab 5 Reflection

## 1. What was the purpose of this lab?

The purpose was to use static analysis tools to inspect a real Python program, distinguish genuine defects from style findings, fix both security and correctness problems, and verify that the cleaned program still performs its intended hostel operations.

## 2. What did Pylint, Flake8, and Bandit help reveal?

Pylint was useful for identifying maintainability issues such as naming, missing docstrings, unused imports, and mutable defaults. Flake8 concentrated on formatting and syntax-adjacent style violations such as blank lines and line length. Bandit identified security risks including Flask debug mode and remote logging. I also found behavioral bugs that analyzers could not detect, including capacity overflow and incorrect vacancy calculation.

## 3. What issues did you fix and why were they important?

I replaced unsafe YAML loading, disabled Flask debug and remote logging, removed embedded credential material, escaped web input, and corrected room allocation logic. The logic fixes enforce gender compatibility and bed capacity, remove vacated occupants, prevent duplicate reallocation errors, calculate vacant beds correctly, and sort students by seniority. These changes prevent crashes, data corruption, unsafe room assignments, and exposed application surfaces.

## 4. What did you learn and what would you do in future projects?

I learned that a passing program is not necessarily a correct or secure program, and that static analysis reports must be reviewed critically rather than treated as the only source of truth. In future projects, I would add tests and run static analyzers continuously during development, use safe serializers and secure framework settings by default, and keep security findings separate from lower-severity style findings.
