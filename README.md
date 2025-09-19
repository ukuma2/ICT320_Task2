# ICT320 Task 2 – Secure Login Prototype

## 📌 Overview
This project is a proof-of-concept **login system** for the *“Find a Campsite”* app.  
It demonstrates how Redis can be used as a **key–value database** to support secure, scalable user authentication.  

The system implements:
- ✅ User registration with randomised security questions  
- ✅ Login with bcrypt password hashing and verification  
- ✅ Forgot password flow with security question/answer reset  
- ✅ Audit logging of all login/registration/reset attempts  
- ✅ Initial database seeding from CSV  
- ✅ Automated testing using `pytest`  

---

## 📂 Project Structure
```
ICT320_Task2/
│── app.py                        # Flask app routes and endpoints
│── auth.py                       # Password/security hashing and verification
│── db.py                         # Redis database functions
│── utils.py                      # Logging and CSV loader utilities
│── test_app.py                   # Automated pytest suite
│── templates/                    # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── forgot.html
│── static/
│   └── style.css                 # Simple CSS styling
│── ICT320 - Task 2 - Initial Database-1.csv   # Initial users for testing
│── security_questions.csv        # Security question list
│── login_log.txt                 # Audit log file
│── requirements.txt              # Python dependencies
│── README.md                     # Project documentation (this file)
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/ukuma2/ICT320_Task2.git
cd ICT320_Task2
```

### 2. (Optional) Create & activate a virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 Running the Application
1. Start the Flask app:
   ```bash
   python app.py
   ```

2. Open your browser and go to:  
   [http://127.0.0.1:5000](http://127.0.0.1:5000)

3. Available features:
   - Register new account  
   - Login with existing account  
   - Reset password via security question  
   - View logs in `login_log.txt`  

---

## 🧪 Testing
Automated tests are provided with `pytest`.  
Run them with:

```bash
pytest -v test_app.py
```

This suite validates:
- Password hashing & verification (`bcrypt`)  
- User registration and duplicate handling  
- Login (success, wrong password, user not found)  
- Forgot password and reset flow  

---

## 🗄️ Database Notes
- Redis is used as the backend key–value store.  
- Users are stored as **Redis hashes**:
  ```
  user:<email>
     firstname → <string>
     password  → <bcrypt hash>
     security_q → <string>
     security_a → <bcrypt hash>
  ```
- Security questions are loaded into a Redis list from `security_questions.csv`.  
- Initial test users are seeded from `ICT320 - Task 2 - Initial Database-1.csv`.  

---

## 🔒 Security Features
- Passwords and security answers stored as **bcrypt hashes**, not plaintext.  
- Login/reset attempts logged in `login_log.txt`.  
- Error handling for duplicate users, wrong passwords, and incorrect answers.  

---

## 📈 Future Improvements
- Multi-factor authentication (MFA)  
- Rate limiting to prevent brute-force attacks  
- Deployment with Docker + Redis cluster for scalability  

---

## 📚 References
- Grinberg, M. (2018). *Flask web development: Developing web applications with Python* (2nd ed.). O’Reilly Media. https://www.oreilly.com/library/view/flask-web-development/9781491991725/  
- Redis. (2025). *Redis documentation*. https://redis.io/documentation  
- OWASP. (2021). *Authentication cheat sheet*. https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html  

---

## 👤 Author
**Utkarsh Kumar**  
Student ID: 1166627  
University of the Sunshine Coast  

