from flask import Flask, render_template, request, redirect
from lib.database_connection import DatabaseConnection
from lib.book_repository import BookRepository
from lib.book import Book
from lib.user_repository import UserRepository
from lib.user import User

# instantiate a Flask app object
app = Flask(__name__)

# Declares a route that listens for a GET request to the path /hello
# and a method to execute when that request comes in
@app.route('/hello', methods=['GET'])
def hello():
    return "Hello to you too"

# duplicate route
@app.route('/hello', methods=['GET'])
def hello_again():
    return "Hello, hello and hello again!"

# NEW PART END

@app.route('/books', methods=['GET'])
def get_books():
    connection = DatabaseConnection()
    connection.connect()
    book_repository = BookRepository(connection)
    books = book_repository.all()

    return render_template("books.html", books=books)

@app.route('/books', methods=['POST'])
def create_book():

    #makes a new data connection and connects to it
    connection = DatabaseConnection()
    connection.connect()

    #makes a new instance of BookRepository
    book_repository = BookRepository(connection)

    #gets the request body
    book_details = request.form

    #makes a new instance of book as it is requested by book repository
    book = Book(title=book_details["title"], author=book_details["author"])

    # saves the book into the database
    book_repository.create(book)

    #returns a 201 which means created
    return redirect("/books")



@app.route('/authors', methods = ['GET'])
def get_authors():
    return [
{
"name": "Julia Donaldson",
"dob": "1948-09-16"
},
{
"name": "Andrea Beaty",
"dob": "1961-10-08"
},
{
"name": "Kelly Barnhill",
"dob": "1973-01-01"
},
{
"name": "Zetta Elliott",
"dob": "1979-11-11"
}
]

@app.route("/", methods = ["GET"])
def index():
    return render_template("books.html")
# make the server run in response to `python app.py`
# on port 5001 (you'll learn more about what this means later)
# and use debug mode so that changing code restarts the app

@app.route("/users/new", methods=['GET'])
def user_signup_page():
    return render_template("signup_form.html")

@app.route("/users", methods=['POST'])
def add_new_user():

    connection = DatabaseConnection()
    connection.connect()

    user_repository = UserRepository(connection)

    user_details = request.form

    user = User(username=user_details["username"], password=user_details["password"])

    user_repository.create(user)

    return redirect("/books")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

