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
        user = mongo.db.users.find_one({"username": session["user"]})
        books = list(mongo.db.books.find({"review_by": session["user"]}))
        return render_template(
            "profile.html", username=username, user=user, books=books)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    flash("You have been logged out")
    session.pop("user")
    # if session["is_admin"] == "on":
    # session.pop("is_admin")
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
            user = mongo.db.users.find_one({"username": session["user"]})
            books = list(mongo.db.books.find({"review_by": session["user"]}))
            return render_template(
                "profile.html", username=username, user=user, books=books)

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
        user = mongo.db.users.find_one({"username": session["user"]})
        books = list(mongo.db.books.find({"review_by": session["user"]}))
        return render_template(
            "profile.html", username=username, user=user, books=books)


@app.route("/edit_profile/<user_id>", methods=["GET", "POST"])
def edit_profile(user_id):
    this_user = mongo.db.users.find_one(
        {"username": session["user"].lower()})
    if request.method == "POST":
        if this_user['is_admin'] == "on":
            edit_user = {
                "first_name": request.form.get("first_name").lower(),
                "last_name": request.form.get("last_name").lower(),
                "username": request.form.get("username").lower(),
                "password": generate_password_hash(
                    request.form.get("password")),
                "is_admin": "on"
            }
        else:
            edit_user = {
                "first_name": request.form.get("first_name").lower(),
                "last_name": request.form.get("last_name").lower(),
                "username": request.form.get("username").lower(),
                "password": generate_password_hash(
                    request.form.get("password")),
                "is_admin": "off"
            }
        mongo.db.users.update({"_id": ObjectId(user_id)}, edit_user)
        session["user"] = request.form.get("username").lower()
        flash("User profile successfully updated")
        user = mongo.db.users.find_one({"username": session["user"]})
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
        books = list(mongo.db.books.find({"review_by": session["user"]}))
        return render_template(
            "profile.html", username=username, user=user, books=books)

    userid = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    user = mongo.db.users.find_one({"username": session["user"]})
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    return render_template(
        "edit_profile.html", user=user, userid=userid, username=username,
        this_user=this_user)


@app.route("/delete_user/<user_id>")
def delete_user(user_id):
    mongo.db.users.remove({"_id": ObjectId(user_id)})
    list(mongo.db.books.remove({"review_by": session["user"]}))
    flash("User Successfully Deleted")
    session.pop("user")
    books = list(mongo.db.books.find())
    genre = list(mongo.db.genre.find())
    return render_template(
            "library.html", books=books, genre=genre)


@app.route("/admin/<username>", methods=["GET", "POST"])
def admin(username):
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    users = list(mongo.db.users.find())
    books = list(mongo.db.books.find())
    return render_template(
        "admin.html", username=username, users=users, books=books)


@app.route("/admin_edit_profile/<user_id>", methods=["GET", "POST"])
def admin_edit_profile(user_id):
    this_user = mongo.db.users.find_one(
        {"username": user_id.lower()})
    if request.method == "POST":
        fname = request.form.get("first_name").lower()
        lname = request.form.get("first_name").lower()
        uname = request.form.get("username").lower()
        psswrd = generate_password_hash(
                request.form.get("password"))
        is_admin = request.form.get("is_admin")
        if fname != "":
            mongo.db.users.update_one(
                {"_id": ObjectId(user_id)}, {"$set": fname})
        if lname != "":
            mongo.db.users.update_one(
                {"_id": ObjectId(user_id)}, {"$set": lname})
        if uname != "":
            mongo.db.users.update_one(
                {"_id": ObjectId(user_id)}, {"$set": uname})
        if psswrd != "":
            mongo.db.users.update_one(
                {"_id": ObjectId(user_id)}, {"$set": psswrd})
        mongo.db.users.update_one(
            {"_id": ObjectId(user_id)}, {"$set": is_admin})
        # edit_user = {
        #     "first_name": request.form.get("first_name").lower(),
        #     "last_name": request.form.get("last_name").lower(),
        #     "username": request.form.get("username").lower(),
        #     "password": generate_password_hash(
        #         request.form.get("password")),
        #     "is_admin": request.form.get("is_admin")
        # }
        # mongo.db.users.update_one(
        #     {"_id": ObjectId(user_id)}, {"$set": edit_user})
        # mongo.db.users.update({"_id": ObjectId(user_id)}, edit_user)
        flash("User profile successfully updated")
        users = list(mongo.db.users.find())
        books = list(mongo.db.books.find())
        return render_template(
            "admin.html", users=users, books=books)

    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})

    return render_template(
        "admin_edit_profile.html", user=user, this_user=this_user)


@app.route("/admin/edit_book/<book_id>", methods=["GET", "POST"])
def admin_edit_book(book_id):
    if request.method == "POST":
        edit = {
            "book_title": request.form.get("book_title").lower(),
            "book_author": request.form.get("book_author").lower(),
            "genre_name": request.form.get("genre_name"),
            "book_cover": request.form.get("book_cover"),
            "book_review": request.form.get("book_review"),
            "review_by": request.form.get("review_by").lower()
        }
        mongo.db.books.update({"_id": ObjectId(book_id)}, edit)
        flash("Book successfully updated")
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]

        user = mongo.db.users.find_one({"username": session["user"]})
        books = list(mongo.db.books.find({"review_by": session["user"]}))
        return render_template(
            "admin.html", username=username, user=user, books=books)

    book = mongo.db.books.find_one({"_id": ObjectId(book_id)})
    genre = mongo.db.genre.find().sort("genre_name", 1)
    return render_template("admin_edit_book.html", book=book, genre=genre)


@app.route("/admin_delete_book/<book_id>")
def admin_delete_book(book_id):
    mongo.db.books.remove({"_id": ObjectId(book_id)})
    flash("Book Successfully Deleted")
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    user = mongo.db.users.find_one({"username": session["user"]})
    books = list(mongo.db.books.find({"review_by": session["user"]}))
    return render_template(
        "admin.html", username=username, user=user, books=books)


@app.route("/edit_genre", methods=["GET", "POST"])
def edit_genre():
    if request.method == "POST":
        existing_genre = mongo.db.genre.find_one(
            {"genre_name": request.form.get("add_genre_name").lower()})
        if existing_genre:
            flash("Genre already exists!")
            return redirect(url_for("sign_up"))
        add_genre = {
            "genre_name": request.form.get("add_genre_name").lower()
        }
        mongo.db.genre.insert_one(add_genre)
        flash("genre successfully added")
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
        users = list(mongo.db.users.find())
        books = list(mongo.db.books.find())
        return render_template(
            "admin.html", username=username, users=users, books=books)

    genre = list(mongo.db.genre.find().sort("genre_name", 1))
    return render_template("edit_genre.html", genre=genre)


@app.route("/delete_genre/<genre_id>")
def delete_genre(genre_id):
    genreid = request.form.get("genre_name")
    mongo.db.genre.remove(genreid)
    flash("Genre Successfully Deleted")
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    users = list(mongo.db.users.find())
    books = list(mongo.db.books.find({"review_by": session["user"]}))
    return render_template(
        "admin.html", username=username,
        users=users, books=books, genreid=genreid)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
