import sys
import os

# this line is a bit of a hack which allows us to import app without changing anything else
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from lib.database_connection import DatabaseConnection

# # a descriptive test name
# def test_get_books_returns_a_200():
#     # here's where we make the test client

#     client = app.test_client()

#     # here's where we make the request
#     response = client.get("/books")

#     # here's where we assert that the response's status code is 200
#     assert response.status_code == 200


# a descriptive test name
# def test_get_books_returns_all_the_books():

#     client = app.test_client()
#     response = client.get("/books")

#     # here's where we assert that the response body contains all the books
#     # note that we need to call .json on the response
#     page = response.get_data(as_text=True)

#     assert "The Gruffalo" in page
#     assert "Ada Twist, Scientist" in page
#     assert "The Girl Who Drank the Moon" in page
#     assert "Dragons in a Bag" in page

# def test_get_authors():

#     client = app.test_client()
#     response = client.get("/authors")

#     page = response.get_data(as_text = True)

#     assert "Julia Donaldson" in page

def test_create_user_is_saved_to_database():

    client = app.test_client()

    connection = DatabaseConnection()
    connection.connect()

    connection.execute('TRUNCATE TABLE users;')

    response = client.post('/users', data= {
        'username': 'testuser',
        'password': 'password123'
    })

    assert response.status_code == 302

    result = connection.execute('SELECT * FROM users WHERE username = %s',
                                ['testuser']
    )

    assert len(result) == 1
    assert result[0]['username'] == 'testuser'

def test_auth():

    client = app.test_client()

    connection = DatabaseConnection()
    connection.connect()

    connection.execute('TRUNCATE TABLE users;')

    response = client.post('/sessions', data= {
        'username': 'testuser',
        'password': '1234'

    })

    assert response.status_code == 302

    assert response.headers['Location'].endswith('/sessions/new')