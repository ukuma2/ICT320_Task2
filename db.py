import redis

# ---------------- Redis Connection ----------------
# Direct connection to Redis Cloud (your actual instance details)
R = redis.Redis(
    host="redis-15027.c80.us-east-1-2.ec2.redns.redis-cloud.com",
    port=15027,
    password="7ZFqIGrVzQJvDLzDnFWuOVIUd3qT9QVP",
    decode_responses=True
)

# Quick connection check (fail fast if Redis is unreachable)
try:
    R.ping()
except redis.exceptions.ConnectionError as e:
    print("[ERROR] Cannot connect to Redis. Check host/port/password.")
    raise e


# ---------------- Helper Functions ----------------
def user_key(login: str) -> str:
    """Return the Redis key name for a user, normalised to lowercase."""
    return f"user:{login.strip().lower()}"


def get_user(login: str):
    """Retrieve a user hash from Redis. Returns dict if exists, else None."""
    uk = user_key(login)
    return R.hgetall(uk) if R.exists(uk) else None


def create_user(login: str, firstname: str, pw_hash: str, q: str, a_hash: str) -> bool:
    """
    Create a new user hash in Redis.
    Returns False if the user already exists, True on success.
    Fields: firstname, password (bcrypt hash), security_q, security_a (bcrypt hash).
    """
    uk = user_key(login)
    if R.exists(uk):
        return False
    R.hset(uk, mapping={
        "firstname": firstname,
        "password": pw_hash,
        "security_q": q,
        "security_a": a_hash
    })
    return True


def update_password(login: str, pw_hash: str) -> bool:
    """
    Update the password hash for an existing user.
    Returns True if updated, False if the user does not exist.
    """
    uk = user_key(login)
    if not R.exists(uk):
        return False
    R.hset(uk, "password", pw_hash)
    return True


def update_security_answer(login: str, a_hash: str) -> bool:
    """
    Update the security answer hash for an existing user.
    Returns True if updated, False if the user does not exist.
    """
    uk = user_key(login)
    if not R.exists(uk):
        return False
    R.hset(uk, "security_a", a_hash)
    return True
