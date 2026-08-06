from playwright.sync_api import Page, expect
from lib.database_connection import DatabaseConnection

def test_has_title(page: Page):
    page.goto("http://127.0.0.1:5001")

    h1 = page.locator("h1")

    expect(h1).to_have_text("My Books")


def test_contains_correct_text(page: Page):
    connection = DatabaseConnection()
    connection.connect()
    connection.seed("./seeds/book_store_seeds.sql")

    page.goto("http://127.0.0.1:5001/books")

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
    page.goto("http://127.0.0.1:5001/books")

    page.get_by_placeholder("Title").fill("BFG")
    page.get_by_placeholder("Author").fill("Roald Dahl")

    page.get_by_role("button", name="Submit").click()

    books = page.locator("li")

    new_book = books.all_inner_texts()[-1]
    assert new_book == "BFG by Roald Dahl"
