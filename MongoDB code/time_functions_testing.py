"""
Performance testing for MongoDB
"""

import time
from pymongo import MongoClient
import main
import users
import user_status


#pylint: disable = E0213, E1102, E1101, E0213, W0621, C0103, E0102
class TimeCode():
    """
    class to test speed of functions
    """

    def __init__(self, user_db_name, status_db_name):
        # set up MongoDB database
        client = MongoClient(host="localhost", port=27017)
        self.db = client.database
        self.user_collection = users.UserCollection(self.db[user_db_name])
        self.status_collection = user_status.UserStatusCollection(self.db[status_db_name])

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

    def reset_tables(self, user_db_name, status_db_name):
        """
        reset tables
        """
        self.db[user_db_name].drop()
        self.db[status_db_name].drop()

    @timeit
    def load_user_csv(self, path):
        """
        Loads users from a CSV file located at the specified path into the user collection.
        """
        # Ensure the path is correct and call the load_users function
        main.load_users(path, self.user_collection)

    @timeit
    def add_user(self, user_id, user_email, user_name, user_last_name):
        """
        Adds a new user to the user collection.
        """
        self.user_collection.add_user(user_id, user_email, user_name, user_last_name)

    @timeit
    def update_user(self, user_id, user_email, user_name, user_last_name):
        """
        updates a user in the user collection.
        """
        self.user_collection.modify_user(user_id, user_email, user_name, user_last_name)

    @timeit
    def delete_user(self, user_id):
        """
        Deletes a user from user_collection and associated statuses from status_collection.
        """
        # First, attempt to delete the user
        user_result = self.user_collection.database.delete_one({"_id": user_id})

        if user_result.deleted_count > 0:
            # If the user was deleted, delete all associated statuses
            self.status_collection.database.delete_many({"user_id": user_id})
            return True

        return False

    @timeit
    def search_user(self, user_id):
        """
        searches a user in database
        """
        self.user_collection.search_user(user_id)

    @timeit
    def load_user_csv(self, path):
        """
        Loads users from a CSV file located at the specified path into the user collection.
        """
        main.load_users(path, self.user_collection)

    @timeit
    def load_status_csv(self, path):
        """
        Loads statuses from a CSV file located at the specified path into the status collection.
        """
        main.load_status_updates(path, self.status_collection)

    @timeit
    def add_status(self, status_id, user_id, status_text):
        """
        Adds a new status to the status collection.
        """
        self.status_collection.add_status(status_id, user_id, status_text)

    @timeit
    def update_status(self, status_id, user_id, status_text):
        """
        updates a status in the status collection.
        """
        return self.status_collection.modify_status(status_id, user_id, status_text)

    @timeit
    def delete_status(self, status_id):
        """
        deletes a status from the status collection.
        """
        # return self.status_collection.delete_status(status_id)
        result = self.status_collection.delete_status(status_id)
        print(f"Deletion result: {result}")
        return result

    @timeit
    def search_status(self, status_id):
        """
        searches a status in database
        """
        result = self.status_collection.search_status(status_id)
        print(f"Search result: {result}")
        return result
        # return self.status_collection.search_status(status_id)


if __name__ == "__main__":
    time_code = TimeCode("TimeUserAccounts", "TimeStatusUpdates")
    user_id = "test"
    user_email = "test@uw.edu"
    user_name = "test"
    user_last_name = "user"

    time_code.add_user(user_id, user_email, user_name, user_last_name)
    time_code.update_user(user_id, "test2@uw.edu", "Test", "Test")
    time_code.search_user(user_id)
    time_code.delete_user(user_id)

    time_code.user_collection.add_user(user_id, user_email, user_name, user_last_name)
    status_id = "Test1"
    status_text = "testing"
    time_code.add_status(status_id, user_id, status_text)
    time_code.update_status(status_id, user_id, "this is a modified status")
    time_code.search_status(status_id)
    time_code.delete_status(status_id)

    time_code.reset_tables("TimeUserAccounts", "TimeStatusUpdates")
    time_code = TimeCode("TimeUserAccounts", "TimeStatusUpdates")

    time_code.load_user_csv("accounts.csv")
    time_code.load_status_csv("status_updates.csv")
