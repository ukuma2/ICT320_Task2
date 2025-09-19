import bcrypt

def hash_text(plain: str) -> str:
    """
    Hash a plaintext string (e.g., password or security answer) using bcrypt.
    Returns the hashed value as a UTF-8 string.
    """
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_text(plain: str, hashed: str) -> bool:
    """
    Verify a plaintext string against a stored bcrypt hash.
    Returns True if they match, False otherwise.
    """
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        # Handles cases where hash is invalid or corrupted
        return False


def normalize_answer(ans: str) -> str:
    """
    Normalise a security answer for case-insensitive comparison.
    Example: ' Brisbane  ' -> 'brisbane'
    """
    return ans.strip().lower()
