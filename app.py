import sys, random
from flask import Flask, render_template, request, redirect, url_for, flash
from db import get_user, create_user, update_password, R
from auth import hash_text, verify_text, normalize_answer
from utils import audit_log, load_questions_from_csv, load_users_from_csv

app = Flask(__name__)
app.secret_key = "supersecretkey"  # needed for flash messages


# ---------------- CLI Optional Reset ----------------
if len(sys.argv) > 1:
    if sys.argv[1] == "--reset-questions":
        print("[INFO] Forcing reset of security questions...")
        load_questions_from_csv("security_questions.csv")
        sys.exit(0)

    elif sys.argv[1] == "--reset-users":
        print("[INFO] Forcing reset of test users...")
        load_users_from_csv("ICT320 - Task 2 - Initial Database-1.csv")
        sys.exit(0)


# ---------------- Auto-Seed (runs once) ----------------
if R.llen("security_questions") == 0:
    print("[INFO] No questions found in Redis. Seeding...")
    load_questions_from_csv("security_questions.csv")

if not R.keys("user:*"):  # no users exist yet
    print("[INFO] No users found in Redis. Seeding test users...")
    load_users_from_csv("ICT320 - Task 2 - Initial Database-1.csv")


# ---------------- Routes ----------------
@app.route("/")
def index():
    return redirect(url_for("login"))


# ---------- Login ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = request.form["login"].strip().lower()
        pw = request.form["password"].strip()
        user = get_user(login)

        if not user:
            flash("User not found")
            audit_log("login", login, "fail", "no such user")
            return redirect(url_for("login"))

        if verify_text(pw, user["password"]):
            flash(f"Welcome, {user['firstname']}!")
            audit_log("login", login, "success")
            return redirect(url_for("login"))
        else:
            flash("Incorrect password")
            audit_log("login", login, "fail", "wrong password")
            return redirect(url_for("login"))

    return render_template("login.html")


# ---------- Register ----------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        login = request.form["login"].strip().lower()
        firstname = request.form["firstname"].strip()
        pw = request.form["password"].strip()
        ans = normalize_answer(request.form["security_a"].strip())

        # pick a random question from Redis
        idx = random.randint(0, R.llen("security_questions") - 1)
        q = R.lindex("security_questions", idx)

        pw_hash = hash_text(pw)
        a_hash = hash_text(ans)

        if create_user(login, firstname, pw_hash, q, a_hash):
            flash("Account created successfully. Please login.")
            audit_log("register", login, "success")
            return redirect(url_for("login"))
        else:
            flash("User already exists")
            audit_log("register", login, "fail", "duplicate user")
            return redirect(url_for("register"))

    # GET request → show form with random question
    idx = random.randint(0, R.llen("security_questions") - 1)
    q = R.lindex("security_questions", idx)
    return render_template("register.html", question=q)


# ---------- Forgot Password ----------
@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    if request.method == "POST":
        login = request.form["login"].strip().lower()
        user = get_user(login)

        if not user:
            flash("No such user")
            audit_log("forgot", login, "fail", "no such user")
            return redirect(url_for("forgot"))

        # show question stage
        return render_template("forgot.html", stage="verify", question=user["security_q"], login=login)

    return render_template("forgot.html", stage="email")


@app.route("/forgot_verify", methods=["POST"])
def forgot_verify():
    login = request.form.get("login", "").strip().lower()
    ans = normalize_answer(request.form["answer"].strip())
    newpw = request.form["newpw"].strip()
    user = get_user(login)

    if not user:
        flash("No such user")
        audit_log("forgot", login, "fail", "no such user")
        return redirect(url_for("forgot"))

    if verify_text(ans, user["security_a"]):
        pw_hash = hash_text(newpw)
        update_password(login, pw_hash)
        flash("Password reset successful. Please login.")
        audit_log("forgot", login, "success")
        return redirect(url_for("login"))
    else:
        flash("Incorrect answer")
        audit_log("forgot", login, "fail", "wrong answer")
        return redirect(url_for("forgot"))


# ---------- Exit (optional) ----------
@app.route("/exit")
def exit_app():
    flash("Goodbye!")
    audit_log("exit", "-", "success")
    func = request.environ.get("werkzeug.server.shutdown")
    if func:
        func()
    return "Server shutting down..."


# ---------------- Run App ----------------
if __name__ == "__main__":
    app.run(debug=True)
