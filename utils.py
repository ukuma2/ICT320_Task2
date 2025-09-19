import csv, logging, random
from datetime import datetime
from db import R, user_key
from auth import hash_text, normalize_answer

# ---------------- Logging Setup ----------------
LOG_FILE = "login_log.txt"

logger = logging.getLogger("auth_log")
logger.setLevel(logging.INFO)
if not logger.handlers:  # avoid duplicate logs if re-imported
    fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
    fh.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
    logger.addHandler(fh)


def audit_log(event: str, login: str, outcome: str, reason: str = ""):
    """
    Write an audit entry for login/register/reset attempts.
    Example: event=login login=jane@example outcome=success reason=ok
    """
    logger.info(f"event={event} login={login} outcome={outcome} reason={reason}")


# ---------------- Security Questions Loader ----------------
def load_questions_from_csv(path: str):
    """
    Load security questions from a CSV into Redis list 'security_questions'.
    Clears any old ones first.
    Expected columns: id, question
    """
    R.delete("security_questions")
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            q = row["question"].strip()
            if q:
                R.rpush("security_questions", q)
    print(f"[INFO] Loaded security questions from {path} into Redis")


# ---------------- User Loader (test CSV) ----------------
def load_users_from_csv(path: str):
    """
    Load sample users from CSV into Redis.
    Supports CSVs with 'username' or 'login' as the login column.
    Expected columns:
      username/login, firstname, password, (optional) security_q, security_a
    - If security_q missing, assign a random one from Redis list.
    - If security_a missing, generate a placeholder answer (e.g., 'Milo').
    - Hash passwords and answers if plaintext.
    """
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            # Handle both 'username' and 'login'
            login = (row.get("login") or row.get("username") or "").strip().lower()
            firstname = row.get("firstname", "").strip()
            pw = row.get("password", "").strip()
            q = row.get("security_q", "").strip()
            a = row.get("security_a", "").strip()

            # Assign a random question if missing
            if not q:
                idx = random.randint(0, R.llen("security_questions") - 1)
                q = R.lindex("security_questions", idx)

            # Generate placeholder answer if missing
            if not a:
                a = random.choice(["Milo", "Brisbane", "Civic", "Blue", "Pineapple"])

            # Hash password if not already hashed
            if pw and not pw.startswith("$2b$"):
                pw = hash_text(pw)

            # Hash answer if not already hashed
            if a and not a.startswith("$2b$"):
                a = hash_text(normalize_answer(a))

            # Store into Redis
            R.hset(user_key(login), mapping={
                "firstname": firstname,
                "password": pw,
                "security_q": q,
                "security_a": a
            })

            print(f"[LOADED] {login} → Redis key=user:{login}")

    print(f"[INFO] User data loaded from {path}")
