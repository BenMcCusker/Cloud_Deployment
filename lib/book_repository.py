from lib.book import Book

class BookRepository:

    # We initialise with a database connection
    def __init__(self, connection):
        self._connection = connection

    # Retrieve all artists
    def all(self):
        rows = self._connection.execute('SELECT * from books')
        books = []
        for row in rows:
            item = Book(row["title"], row["author"], row["id"])
            books.append(item)
        return books

    # Find a single artist by their id
    def find(self, book_id):
        rows = self._connection.execute(
            'SELECT * from books WHERE id = %s', [book_id])
        row = rows[0]
        return Book(row["id"], row["title"], row["author"])

    # Create a new artist
    # Do you want to get its id back? Look into RETURNING id;
    def create(self, book):
        self._connection.execute('INSERT INTO books (title, author) VALUES (%s, %s)', [
            book.title, book.author])
        return None

    # Delete an artist by their id
    def delete(self, book_id):
        self._connection.execute(
            'DELETE FROM books WHERE id = %s', [book_id])
        return None