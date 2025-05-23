from flask import redirect, render_template, session
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

def apology(message):
    return render_template("apology.html", message = message)

def test(x,y):
    z = generate_password_hash(x, method='pbkdf2:sha256')
    print(z)
    print(check_password_hash(z,y))
def main():
    x = "George"
    y = "George"
    test(x,y)
    

if __name__ == "__main__":
    main()