def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        # Fix (86377c7): Hard was 1-50 — smaller than Normal, so it was easier. Widened to 1-200.
        return 1, 200
    return 1, 100



def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def validate_in_range(guess: int, low: int, high: int):
    """
    Challenge 1: check that a parsed guess falls within the inclusive
    [low, high] range for the selected difficulty.

    Returns: (ok: bool, error_message: str | None)

    An out-of-range guess is rejected so the caller can show an error and
    skip counting it as an attempt.
    """
    if guess < low:
        return False, f"Too low — pick a number between {low} and {high}."

    if guess > high:
        return False, f"Too high — pick a number between {low} and {high}."

    return True, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"
    if guess == secret:
        return "Win", "🎉 Correct!"

    # Fix (b41f201): compare numerically only — old code coerced the secret to a
    # string on alternating attempts, which silently broke comparisons.
    # Fix (3c348db): hint direction was reversed (a too-high guess said "go higher").
    if guess > secret:
        return "Too High", "📉 GO LOWER!"

    return "Too Low", "📈 GO HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)     
        if points < 10:                            
            points = 10
        return current_score + points

    if outcome == "Too High":                       
        if attempt_number % 2 == 0:                  
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":                         
        return current_score - 5

    return current_score
