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

- [x] Describe the game's purpose.
- [x] Detail which bugs you found.
- [x] Explain what fixes you applied.
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

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
