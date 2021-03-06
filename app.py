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


# Home
@app.route("/")
@app.route("/library")
def library():
    books = list(mongo.db.books.find().sort("book_title", 1))
    genre = list(mongo.db.genre.find())

    return render_template(
        "library.html", books=books, genre=genre)


# Search
@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    books = list(mongo.db.books.find({"$text": {"$search": query}}))
    genre = list(mongo.db.genre.find())
    return render_template(
        "library.html", books=books, genre=genre)


# Home page sort
@app.route("/library_author_sort")
def library_author_sort():
    books = list(mongo.db.books.find().sort("book_author", 1))
    genre = list(mongo.db.genre.find())

    return render_template(
        "library.html", books=books, genre=genre)


@app.route("/library_genre_sort")
def library_genre_sort():
    books = list(mongo.db.books.find().sort("genre_name", 1))
    genre = list(mongo.db.genre.find())

    return render_template(
        "library.html", books=books, genre=genre)


# Sign up
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


# Log in
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


# User profile
@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        user = mongo.db.users.find_one({"username": session["user"]})
        books = list(mongo.db.books.find(
            {"review_by": session["user"]}).sort("book_title", 1))
        return render_template(
            "profile.html", username=username, user=user, books=books)

    return redirect(url_for("login"))


# Log out
@app.route("/logout")
def logout():
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


# Add book
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


# Edit book
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


# Delete book
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


# Edit user profile
@app.route("/edit_profile/<user_id>", methods=["GET", "POST"])
def edit_profile(user_id):
    if request.method == "POST":
        first_name = request.form.get("first_name").lower()
        last_name = request.form.get("last_name").lower()
        username = request.form.get("username").lower()
        password = request.form.get("password")
        if first_name != "":
            mongo.db.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"first_name": first_name}})
        if last_name != "":
            mongo.db.users.update_one(
                {"_id": ObjectId(user_id)}, {"$set": {"last_name": last_name}})
        if username != "":
            mongo.db.users.update_one(
                {"_id": ObjectId(user_id)}, {"$set": {"username": username}})
        if password != "":
            hashed_password = generate_password_hash(
                request.form.get("password"))
            mongo.db.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"password": hashed_password}})
        flash("User profile successfully updated")
        session["user"] = request.form.get("username").lower()
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
        "edit_profile.html", user=user, userid=userid, username=username)


# Delete user profile
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


# Admin page
@app.route("/admin/<username>", methods=["GET", "POST"])
def admin(username):
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    users = list(mongo.db.users.find().sort("username", 1))
    books = list(mongo.db.books.find().sort("book_title", 1))
    return render_template(
        "admin.html", username=username, users=users, books=books)


# Admin edit all users
@app.route("/admin_edit_profile/<user_id>", methods=["GET", "POST"])
def admin_edit_profile(user_id):
    if request.method == "POST":
        first_name = request.form.get("first_name").lower()
        last_name = request.form.get("last_name").lower()
        username = request.form.get("username").lower()
        password = request.form.get("password")
        is_admin = request.form.get("is_admin")
        if first_name != "":
            mongo.db.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"first_name": first_name}})
        if last_name != "":
            mongo.db.users.update_one(
                {"_id": ObjectId(user_id)}, {"$set": {"last_name": last_name}})
        if username != "":
            mongo.db.users.update_one(
                {"_id": ObjectId(user_id)}, {"$set": {"username": username}})
        if password != "":
            hashed_password = generate_password_hash(
                request.form.get("password"))
            mongo.db.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"password": hashed_password}})
        admin_status = mongo.db.users.find_one(
            {"_id": ObjectId(user_id)})
        if is_admin != admin_status:
            mongo.db.users.update_one(
                {"_id": ObjectId(user_id)}, {"$set": {"is_admin": is_admin}})
        flash("User profile successfully updated")
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
        users = list(mongo.db.users.find().sort("username", 1))
        books = list(mongo.db.books.find().sort("book_title", 1))
        return render_template(
            "admin.html", users=users, books=books, username=username)

    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    this_user = mongo.db.users.find_one(
        {"username": user_id.lower()})

    return render_template(
        "admin_edit_profile.html", user=user, this_user=this_user)


# Admin delete users
@app.route("/admin_delete_user/<user_id>")
def admin_delete_user(user_id):
    mongo.db.users.remove({"_id": ObjectId(user_id)})
    list(mongo.db.books.remove({"review_by": session["user"]}))
    flash("User Successfully Deleted")
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    users = list(mongo.db.users.find().sort("username", 1))
    books = list(mongo.db.books.find().sort("book_title", 1))
    return render_template(
        "admin.html", users=users, books=books, username=username)


# Admin edit books
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
        users = list(mongo.db.users.find().sort("username", 1))
        books = list(mongo.db.books.find().sort("book_title", 1))
        return render_template(
            "admin.html", users=users, books=books, username=username)

    book = mongo.db.books.find_one({"_id": ObjectId(book_id)})
    genre = mongo.db.genre.find().sort("genre_name", 1)
    return render_template("admin_edit_book.html", book=book, genre=genre)


# Admin delete books
@app.route("/admin_delete_book/<book_id>")
def admin_delete_book(book_id):
    mongo.db.books.remove({"_id": ObjectId(book_id)})
    flash("Book Successfully Deleted")
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    users = list(mongo.db.users.find().sort("username", 1))
    books = list(mongo.db.books.find().sort("book_title", 1))
    return render_template(
        "admin.html", users=users, books=books, username=username)


# admin add genre
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
        flash("Genre successfully added")

    genre = list(mongo.db.genre.find().sort("genre_name", 1))
    return render_template("edit_genre.html", genre=genre)


# admin delete genre
@app.route("/delete_genre/<genre_id>")
def delete_genre(genre_id):
    mongo.db.genre.remove({"_id": ObjectId(genre_id)})
    flash("Genre Successfully Deleted")

    genre = list(mongo.db.genre.find().sort("genre_name", 1))
    return render_template("edit_genre.html", genre=genre)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)
