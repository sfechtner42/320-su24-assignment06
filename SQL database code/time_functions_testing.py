"""
Performance testing for SQL database code
"""

import time
import main
from peewee import SqliteDatabase
from socialnetwork_model import UserModel, StatusModel

#pylint: disable = E0213, E1102, E1101, E0213, W0621, C0103, E0102, C0301, W0612
class TimeCode:
    """
    class to test speed of functions
    """
    def __init__(self, sqlite_db_name):
        """
        initialize timecode class
        """
        # set up sqlite database
        sqlite_db = SqliteDatabase(sqlite_db_name)
        self.sqlite_db = sqlite_db
        self.user_collection = main.users.UserCollection(sqlite_db)
        self.status_collection = main.user_status.UserStatusCollection(sqlite_db)

    def timeit(method):
        """
        timer decorator to test performance of functions
        code taken from class
        """
        def timed(*args, **kwargs):
            start = time.time()
            result = method(*args, **kwargs)
            end = time.time()
            total_time = round((end - start) * 1000, 3)
            print(f"Total time for {method.__name__} was {total_time} milliseconds")
            return result

        return timed

    def reset_tables(self):
        """
        reset tables
        """
        self.sqlite_db.drop_tables([UserModel, StatusModel])

    @timeit
    def add_user(self, user_id, user_email, user_name, user_last_name):
        """
        add new user
        """
        # run 3 times and report the last run
        for i in range(3):
            result = self.user_collection.add_user(user_id, user_email, user_name, user_last_name)
        return result

    @timeit
    def update_user(self, user_id, user_email, user_name, user_last_name):
        """
        update user
        """
        for i in range(3):
            result = self.user_collection.modify_user(user_id, user_email, user_name, user_last_name)
        return result

    @timeit
    def delete_user(self, user_id):
        """
        delete user
        """
        result = self.user_collection.delete_user(user_id)
        return result

    @timeit
    def search_user(self, user_id):
        """
        search user
        """
        for i in range(3):
            result = self.user_collection.search_user(user_id)
        return result

    @timeit
    def load_user_csv(self, path):
        """
        Loads users from a CSV file located at the specified path into the user collection.
        """
        result = main.load_users(path)
        if result:
            print(f"Successfully loaded users from {path}")
        else:
            print(f"Failed to load users from {path}")

    @timeit
    def load_status_csv(self, path):
        """
        Loads statuses from a CSV file located at the specified path into the status collection.
        """
        result = main.load_status_updates(path)
        if result:
            print(f"Successfully loaded statuses from {path}")
        else:
            print(f"Failed to load statuses from {path}")

    @timeit
    def add_status(self, status_id, user_id, status_text):
        """
        adds a status to the status collection
        """
        for i in range(3):
            result = main.add_status(status_id, user_id, status_text, self.status_collection)
        return result

    @timeit
    def update_status(self, status_id, user_id, status_text):
        """
        updates a status to the status collection
        """
        for i in range(3):
            result = main.update_status(status_id, user_id, status_text, self.status_collection)
        return result

    @timeit
    def delete_status(self, status_id):
        """
        deletes a status from the status collection
        """
        for i in range(3):
            result = main.delete_status(status_id, self.status_collection)
        return result

    @timeit
    def search_status(self, status_id):
        """
        search a status from the status collection
        """
        for i in range(3):
            result = main.search_status(status_id, self.status_collection)
        return result


if __name__ == "__main__":
    # time_code = TimeCode(":memory:")
    time_code = TimeCode("database.db")
    user_id = "test"
    user_email = "test@uw.edu"
    user_name = "test"
    user_last_name = "test"

    time_code.add_user(user_id, user_email, user_name, user_last_name)
    time_code.update_user(user_id, "test2@uw.edu", "test", "test")
    time_code.search_user(user_id)
    time_code.delete_user(user_id)

    status_id = "test1"
    status_text = "test status"
    time_code.add_status(status_id, user_id, status_text)
    time_code.update_status(status_id, user_id, "this is a modified status")
    time_code.search_status(status_id)
    time_code.delete_status(status_id)

    time_code.load_user_csv("accounts.csv")
    time_code.load_status_csv("status_updates.csv")

    time_code.reset_tables()