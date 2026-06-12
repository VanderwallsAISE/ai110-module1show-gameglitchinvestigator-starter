# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

<!-- Describe the goal you asked the agent to accomplish -->

**What did the agent do?**

<!-- List the steps the agent took (files edited, commands run, etc.) -->

**What did you have to verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Negative numbers | Complete Challenge 1 by adding edge-case pytest tests for invalid and out-of-range guesses. | Test that guesses below the selected range are rejected by `validate_in_range()`. | Yes | Negative numbers like `-1` should not be accepted because the game ranges start at 1. |
| Decimals | Complete Challenge 1 by adding edge-case pytest tests for decimals and unusual numeric input. | Test that decimal strings are parsed consistently by `parse_guess()`. | Yes | Decimal input could behave unexpectedly, so I wanted to verify how the parser handles it. |
| Extremely large values | Complete Challenge 1 by adding edge-case pytest tests for very large guesses. | Test that huge numeric guesses parse but fail range validation. | Yes | Large numbers should not break the game or count as valid guesses outside the selected range. |
| Empty input | Complete Challenge 1 by adding edge-case pytest tests for missing input. | Test that an empty string returns an error from `parse_guess()`. | Yes | A blank guess should show an error instead of counting as an attempt. |
| Non-numeric input | Complete Challenge 1 by adding edge-case pytest tests for text input. | Test that values like `"abc"` are rejected by `parse_guess()`. | Yes | Text input should not crash the game or count as a valid guess. |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
<!-- Paste the prompt you gave the AI -->
```

**Linting output before:**

```
<!-- Paste relevant linter warnings/errors -->
```

**Changes applied:**

<!-- Describe what you changed based on the AI's suggestions -->

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->
