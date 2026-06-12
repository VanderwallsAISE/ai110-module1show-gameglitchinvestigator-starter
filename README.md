# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

### Game Purpose

The purpose of this project is to create a number guessing game where the player must guess a secret number within a limited number of attempts. The application uses Streamlit for the user interface and stores game state using session_state.

### Bugs Found

During testing, I discovered several issues:
- Hard difficulty used a smaller range than Normal difficulty.
- The displayed range did not update when difficulty changed.
- Hint messages were reversed and gave the wrong direction.
- The secret number could be treated as a string, causing comparison issues.
- Invalid guesses could affect game behavior.
- The New Game button did not fully reset all game state values.

### Fixes Applied

To fix these issues, I moved core game logic into `logic_utils.py`, corrected the difficulty ranges, fixed the hint directions, ensured numeric comparisons were used consistently, added input validation, improved state reset behavior, and created automated pytest tests to verify the fixes. I also added edge-case tests and enhanced the user interface with metrics, feedback messages, and guess history.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. The user opens the Streamlit app and selects a difficulty level from the sidebar.
2. The app displays the correct number range and attempts allowed for the selected difficulty.
3. The user enters a guess and clicks **Submit Guess**.
4. If the guess is too high, the game tells the user to go lower; if the guess is too low, it tells the user to go higher.
5. If the user enters invalid input, the app shows an error message without counting it as a valid guess.
6. When the user guesses the secret number, the game displays a win message with the final score.
7. The user can click **New Game** to reset the secret number, attempts, score, status, and guess history.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
====================================================================================================== test session starts ======================================================================================================
platform win32 -- Python 3.14.2, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Users\istea\Desktop\Code_path\CODE_PATH COURSE SUMMER 2026\AI110 FOUNDATIONS OF ENGINEERING\Code_Path AI110 __Project\ai110-module1show-gameglitchinvestigator-starter
plugins: anyio-4.13.0
collected 18 items                                                                                                                                                                                                               

tests\test_game_logic.py ..................                                                                                                                                                                                [100%]

====================================================================================================== 18 passed in 0.05s =======================================================================================================
```

## 🧪 Test Results

```text
========================================================================== test session starts ============================                              
platform win32 -- Python 3.14.2, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Users\istea\Desktop\Code_path\CODE_PATH COURSE SUMMER 2026\AI110 FOUNDATIONS OF ENGINEERING\Code_Path AI110 __Project\ai110-module1show-gameglitchinvestigator-starter
plugins: anyio-4.13.0
collected 51 items

tests\test_game_logic.py ...................................................                                                                                        [100%]

================================================== 51 passed in 0.09s=============================================== 
```



## 🚀 Stretch Features

### Challenge 1: Out-of-Range Guess Validation

Guesses outside the active difficulty range are now rejected before they can
affect the game, and the edge cases are covered by tests. All existing pytest
tests still pass.

- **Range validation** — a guess below the selected **low** value or above the
  selected **high** value now shows an error message and is **not** counted as an
  attempt (it doesn't increment the attempt counter or get added to history).
- **Edge-case tests** — added pytest coverage for empty input, non-numeric input,
  decimals (truncated toward zero), negative numbers, and very large values, plus
  boundary checks confirming the low/high bounds are inclusive.

**Files changed:**
- **`logic_utils.py`** — added a `validate_in_range(guess, low, high)` helper that
  returns `(ok, error_message)`.
- **`app.py`** — wired the range check into the submit flow so out-of-range guesses
  show an error and don't count as an attempt.
- **`tests/test_game_logic.py`** — added the range-validation and edge-case tests.

### Challenge 4: Enhanced Game UI

All enhancements below are presentation-only and live in **`app.py`** — the core
game logic (`logic_utils.py`) and game rules were left unchanged, and all pytest
tests still pass.

- **Metric cards** — a row of at-a-glance `st.metric` cards showing the selected
  **Difficulty**, the active **Range**, **Attempts left**, and the current **Score**.
- **Color-coded feedback** — the per-guess hint is now styled by outcome:
  **Too High** uses a warning (amber) message, **Too Low** uses an info (blue)
  message, and a **Win** uses a success (green) message.
- **Hot / Warm / Cold proximity** — after a valid, in-range guess the app shows how
  close the guess is to the secret: **🔥 Very Hot** within 5, **🌤️ Warm** within 15,
  and **❄️ Cold** otherwise. It is intentionally *not* shown after invalid or
  out-of-range guesses (those return before the proximity check).
- **Guess history table** — previous guesses are listed in a clean `st.dataframe`,
  displayed only once at least one valid guess has been made.

The existing **Developer Debug Info** section was kept intact.
