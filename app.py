import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/library")
def library():
    books = list(mongo.db.books.find())
    genre = list(mongo.db.genre.find())
    # if "user" in session:
    #     print(session["user"])
    #     user = mongo.db.users.find_one({"username": session["user"].lower()})
    # else:
    #     user = None

    return render_template(
        "library.html", books=books, genre=genre)


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Looks like you've already signed up!")
            return redirect(url_for("sign_up"))

        sign_up = {
            "first_name": request.form.get("first_name").lower(),
            "last_name": request.form.get("last_name").lower(),
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "is_admin": "off"
        }
        mongo.db.users.insert_one(sign_up)

        session["user"] = request.form.get("username").lower()
        flash("Welcome to The Book Club, {}!".format(
            request.form.get("first_name")))
        return redirect(url_for("profile", username=session["user"]))
    return render_template("sign_up.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                this_user = mongo.db.users.find_one(
                    {"username": session["user"].lower()})
                if this_user['is_admin'] == "on":
                    session["is_admin"] = "on"
                else:
                    session["is_admin"] = "off"
                return redirect(url_for(
                    "profile", username=session["user"]))

            else:
                flash("We don't recognise your username and/or password")
                return redirect(url_for("login"))

        else:
            flash("We don't recognise your username and/or password")
            return redirect(url_for("login"))
    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        users = list(mongo.db.genre.find())
        books = list(mongo.db.books.find({"review_by": session["user"]}))
        return render_template(
            "profile.html", username=username, users=users, books=books)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    flash("You have been logged out")
    session.pop("user")
    if session["is_admin"] == "on":
        session.pop("is_admin")
    return redirect(url_for("login"))


@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        book = {
            "book_title": request.form.get("book_title").lower(),
            "book_author": request.form.get("book_author").lower(),
            "genre_name": request.form.get("genre_name"),
            "book_cover": request.form.get("book_cover"),
            "book_review": request.form.get("book_review"),
            "review_by": session["user"]
        }
        mongo.db.books.insert_one(book)
        flash("Book successfully added")
        return redirect(url_for("library"))

    genre = mongo.db.genre.find().sort("genre_name", 1)
    return render_template("add_book.html", genre=genre)


@app.route("/edit_book/<book_id>", methods=["GET", "POST"])
def edit_book(book_id):
    if request.method == "POST":
        edit = {
            "book_title": request.form.get("book_title").lower(),
            "book_author": request.form.get("book_author").lower(),
            "genre_name": request.form.get("genre_name"),
            "book_cover": request.form.get("book_cover"),
            "book_review": request.form.get("book_review"),
            "review_by": session["user"]
        }
        mongo.db.books.update({"_id": ObjectId(book_id)}, edit)
        flash("Book successfully updated")
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
        if session["user"]:
            users = list(mongo.db.genre.find())
            books = list(mongo.db.books.find({"review_by": session["user"]}))
            return render_template(
                "profile.html", username=username, users=users, books=books)

    book = mongo.db.books.find_one({"_id": ObjectId(book_id)})
    genre = mongo.db.genre.find().sort("genre_name", 1)
    return render_template("edit_book.html", book=book, genre=genre)


@app.route("/delete_book/<book_id>")
def delete_book(book_id):
    mongo.db.books.remove({"_id": ObjectId(book_id)})
    flash("Book Successfully Deleted")
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    if session["user"]:
        users = list(mongo.db.genre.find())
        books = list(mongo.db.books.find({"review_by": session["user"]}))
        return render_template(
            "profile.html", username=username, users=users, books=books)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
