from flask import Flask, render_template
from database.db import init_db, seed_db, close_db

app = Flask(__name__)


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/login")
def login():
    return render_template("login.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    return "Logout — coming in Step 3"


@app.route("/profile")
def profile():
    return "Profile page — coming in Step 4"


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"

# ------------------------------------------------------------------ #
# Terms and Conditions Route
# ------------------------------------------------------------------ #

@app.route("/terms")
def terms():
    """Render the Terms and Conditions page.

    This page provides generic legal information for the Spendly
    personal expense tracking application.
    """
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    """Render the Privacy Policy page.

    This page outlines how user data is collected, used, stored, and
    shared within the Spendly personal expense tracking application.
    """
    return render_template("privacy.html")


if __name__ == "__main__":
    # Initialize database and seed demo data on startup
    with app.app_context():
        init_db()
        seed_db()
    # Register teardown to close DB connections after each request
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        # Flask may provide a connection via g, but our app doesn't use g.
        # We simply ensure any open connections are closed.
        # In this simple app, we don't keep a global connection, so nothing to do.
        pass

    app.run(debug=True, port=5001)
