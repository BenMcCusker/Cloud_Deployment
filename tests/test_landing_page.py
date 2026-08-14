from playwright.sync_api import Page, expect
from lib.database_connection import DatabaseConnection

def test_has_title(page: Page):
    page.goto("http://127.0.0.1:5001/")

    h1 = page.locator("h1")

    expect(h1).to_have_text("The Office")


def test_contains_correct_text(page: Page):
    connection = DatabaseConnection()
    connection.connect()
    connection.seed("./seeds/book_store_seeds.sql")

    connection.execute("TRUNCATE TABLE users;")
    connection.execute("INSERT INTO users (username, password) VALUES ('test', '1234');")

    page.goto("http://localhost:5001/sessions/new")
    page.get_by_placeholder("username").fill("test")
    page.get_by_placeholder("password").fill("1234")
    page.get_by_role("button", name="Log In").click()

    page.goto("http://localhost:5001/books")

    list = page.locator("li")

    expected_books = [
    'The Gruffalo by Julia Donaldson',
    'Ada Twist, Scientist by Andrea Beaty',
    'The Girl Who Drank the Moon by Kelly Barnhill',
    'Dragons in a Bag by Zetta Elliott'
    ]

    actual_books = list.all_inner_texts()

    assert actual_books == expected_books

def test_adding_new_book(page: Page):
    connection = DatabaseConnection()
    connection.connect()
    connection.execute("TRUNCATE TABLE users;")
    connection.execute("INSERT INTO users (username, password) VALUES ('test', '1234');")

    page.goto("http://localhost:5001/sessions/new")
    page.get_by_placeholder("username").fill("test")
    page.get_by_placeholder("password").fill("1234")
    page.get_by_role("button", name="Log in").click()

    page.goto("http://localhost:5001/books")

    page.get_by_role("button", name="Add book").click()

    page.goto("http://localhost:5001/bookform")

    page.get_by_placeholder("Title").fill("BFG")
    page.get_by_placeholder("Author").fill("Roald Dahl")

    page.get_by_role("button", name="Submit").click()

    books = page.locator("li")

    new_book = books.all_inner_texts()[-1]
    assert new_book == "BFG by Roald Dahl"

def test_for_auth(page: Page):
    connection = DatabaseConnection()
    connection.connect()
    connection.execute("TRUNCATE TABLE users;")
    connection.execute("INSERT INTO users (username, password) VALUES ('test', '1234');")

    page.goto("http://localhost:5001/sessions/new")
    page.get_by_placeholder("username").fill("test")
    page.get_by_placeholder("password").fill("1234")
    page.get_by_role("button", name="Log in").click()

    assert page.url == "http://localhost:5001/books"

def test_unauth_add_book(page: Page):
    connection = DatabaseConnection()
    connection.connect()
    connection.execute("TRUNCATE TABLE users;")

    page.goto("http://localhost:5001/books")

    #Cant reach the books page without logging in so instantly sends to login page
    assert page.url == "http://localhost:5001/sessions/new"

def test_for_failed_auth(page: Page):
    connection = DatabaseConnection()
    connection.connect()
    connection.execute("TRUNCATE TABLE users;")

    page.goto("http://localhost:5001/sessions/new")
    page.get_by_placeholder("username").fill("test")
    page.get_by_placeholder("password").fill("1234")
    page.get_by_role("button", name="Log in").click()

    assert page.url == "http://localhost:5001/sessions"