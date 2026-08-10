from lib.user import User

class UserRepository:

    # We initialise with a database connection
    def __init__(self, connection):
        self._connection = connection

    # Retrieve all artists
    def all(self):
        rows = self._connection.execute('SELECT * from users')
        users = []
        for row in rows:
            item = User(row["username"], row["password"], row["id"])
            users.append(item)
        return users

    # Find a single artist by their id
    def find(self, username):
        user_details = self._connection.execute(
            'SELECT * from users WHERE username = %s', [username]
            )

        if len(user_details) == 0:
            return None

        user_details = user_details[0]
        
        return User(user_details["username"], 
                    user_details["password"], 
                    user_details["id"]
                    )

    # Create a new artist
    # Do you want to get its id back? Look into RETURNING id;
    def create(self, user):
        self._connection.execute('INSERT INTO users (username, password) VALUES (%s, %s)', [
            user.username, user.password])
        return None

    # Delete an artist by their id
    def delete(self, user_id):
        self._connection.execute(
            'DELETE FROM users WHERE id = %s', [user_id])
        return None