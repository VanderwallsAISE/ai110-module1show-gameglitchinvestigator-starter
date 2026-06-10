# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

### What did the game look like the first time you ran it?

The game loaded successfully and displayed a number guessing interface with difficulty settings, a guess input box, a hint option, a score tracker, and a Developer Debug Information panel. At first glance, everything appeared functional, but after testing different difficulty levels and playing several rounds, I noticed multiple inconsistencies between the displayed information and the actual game behavior. I decided to document these issues before making any code changes.

### List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

 The first bug I noticed was that the difficulty settings did not behave as expected. Hard difficulty used a smaller range (1-50) than Normal difficulty (1-100), which    made Hard mode easier instead of harder.

The second bug was that the displayed range message always showed "Guess a number between 1 and 100" even after changing the difficulty level. The displayed range did not match the selected difficulty.

As I continued testing the game, I found several additional issues. The attempts counter started one lower than expected when the app first loaded, the New Game button did not fully reset the game state, hint messages often pointed in the wrong direction, out-of-range guesses such as -1 and 1700 were accepted, the "Out of attempts!" message appeared while one attempt still remained, and the displayed score did not always match the score shown in the developer debug information.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Select Hard difficulty | Hard mode should have a larger range than Normal mode | Hard mode uses range 1-50 while Normal uses 1-100, making Hard easier | None |
| Select Hard difficulty | Main game message should update to selected range (e.g., 1-50) | Message still displays "Guess a number between 1 and 100" | None |
| Open app for first time (Normal difficulty) | Attempts left should equal attempts allowed (8) | Settings shows 8 attempts allowed, but game displays 7 attempts left | None |
| Click New Game after losing | Game state should fully reset (attempts, messages, history, score) | Previous game state remains and game does not fully reset | None |
| Guess 3 when secret number is higher | Hint should say "Go Higher" | Hint logic sometimes points in the wrong direction | None |
| Enter -1 or 1700 | Invalid guess should be rejected because it is outside the allowed range | Game accepts the value and processes it normally | None |
| Reach final remaining attempt | Out-of-attempts message should appear only after all attempts are used | "Out of attempts!" message appears while one attempt is still remaining | None |
| Lose game and compare score with Developer Debug Info | Displayed score should match debug score | Loss message score does not always match debug information | None |

---

## 2. How did you use AI as a teammate?

### Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
I used ChatGPT and Claude Code during this project. I primarily used AI to discuss bugs, improve my bug reports, understand the project requirements, and prepare my debugging plan. I still tested the application manually and verified the behavior myself before making any code changes.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
