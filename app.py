import random
import streamlit as st


from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    validate_in_range,
    check_guess,
    update_score
)

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")             
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    # Fix (3824ab6 / 4703d4a): seed the secret from the active difficulty range (was hardcoded 1-100).
    st.session_state.secret = random.randint(low, high)   

if "attempts" not in st.session_state:
    # Fix (27f071d): start at 0 — was initialized to 1, eating an attempt before the first guess.
    st.session_state.attempts = 0                         

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

# Challenge 4: at-a-glance metric cards (UI only — no game-logic changes).
attempts_remaining = max(0, attempt_limit - st.session_state.attempts)
m1, m2, m3, m4 = st.columns(4)
m1.metric("Difficulty", difficulty)
m2.metric("Range", f"{low}–{high}")
m3.metric("Attempts left", attempts_remaining)
m4.metric("Score", st.session_state.score)

st.subheader("Make a guess")

# Fix (e0335df): show the real difficulty range here — was hardcoded "between 1 and 100".
st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"  
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    # Fix (3824ab6): fully reset state — New Game used to leave score/status/history stale.
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)  
    st.session_state.score = 0                           
    st.session_state.status = "playing"                 
    st.session_state.history = []                        
    st.success("New game started.")    
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    
    ok, guess_int, err = parse_guess(raw_guess)
    in_range, range_err = (False, None)
    if ok:
        # Challenge 1: reject guesses outside the active difficulty range.
        in_range, range_err = validate_in_range(guess_int, low, high)

    if not ok:
        st.error(err)
    elif not in_range:
        # Out-of-range guess: show an error and do NOT count it as an attempt.
        st.error(range_err)
    else:
        # Fix (4703d4a): only count the attempt after a valid parse, and store the parsed int (not raw text).
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        # Fix (b41f201): keep the secret as an int — removed the alternating str() coercion.
        secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)

        # Challenge 4: color-code the hint by outcome.
        # Too High -> warning, Too Low -> info, Win -> success.
        if show_hint:
            if outcome == "Win":
                st.success(message)
            elif outcome == "Too High":
                st.warning(message)
            else:  # "Too Low"
                st.info(message)

        # Challenge 4: Hot/Warm/Cold proximity feedback. Only reached on a
        # valid, in-range guess (invalid/out-of-range guesses returned earlier).
        # Skipped on a win, where the exact answer is already celebrated below.
        if outcome != "Win":
            distance = abs(guess_int - secret)
            if distance <= 5:
                st.markdown("### 🔥 Very Hot!")
            elif distance <= 15:
                st.markdown("### 🌤️ Warm")
            else:
                st.markdown("### ❄️ Cold")

        st.session_state.score = update_score(
            current_score=st.session_state.score,      
            outcome=outcome,                          
            attempt_number=st.session_state.attempts, 
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts > attempt_limit: # 
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

# Challenge 4: clean guess-history table — only shown once a valid guess exists.
if st.session_state.history:
    st.subheader("Guess History")
    history_rows = [
        {"Guess #": number, "Value": value}
        for number, value in enumerate(st.session_state.history, start=1)
    ]
    st.dataframe(history_rows, hide_index=True, use_container_width=True)

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
