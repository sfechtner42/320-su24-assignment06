"""
classes to manage the user status messages
"""
import pymongo


# from loguru import logger


# set-up logging for user_status.py
# logger.remove()
# logger.add("log_file_{time:YYYY_MMM_DD}.log")
# logger.add(sys.stderr, level="ERROR")

class UserStatusCollection:
    """
    Collection of UserStatus messages
    """

    def __init__(self, database):
        self.database = database
        # logger.debug("Status database successfully linked")

    def add_status(self, status_id, user_id, status_text):
        """
        Adds a new status to the collection
        """
        if self.search_status(status_id):
            return False
        status = {
            "_id": status_id,
            "user_id": user_id,
            "status_text": status_text
        }
        self.database.insert_one(status)
        return True

    def batch_load_statuses(self, data):
        """
        Adds new statuses to the collection with a batch load
        """
        try:
            self.database.insert_many(data, ordered=False)
        except pymongo.errors.BulkWriteError as error:
            write_errors = error.details['writeErrors']
            for error in write_errors:
                if error['code'] != 11000:  # If not a DuplicateKeyError
                    # Handle unexpected errors
                    print(f"Unexpected error in batch: {error}")
                    return False
        return True

    def modify_status(self, status_id, user_id, status_text):
        """
        Modifies a status message if the status_id and user_id match.

        The new user_id and status_text are assigned to the existing message
        only if the provided user_id matches the user_id associated with the status_id.
        """
        # Search for the existing status
        existing_status = self.search_status(status_id)

        if not existing_status:
            # Rejects a status that does not exist
            # logger.debug("Status ID %s does not exist in the database", status_id)
            return False

        if existing_status.get("user_id") != user_id:
            # Rejects if user_id does not match
            # logger.debug("User ID %s does not match the status ID %s", user_id, status_id)
            return False

        # Proceed with updating the status
        data = {"status_text": status_text}
        self.database.update_one({"_id": status_id}, {"$set": data})
        # logger.debug("Status ID %s successfully updated in the database", status_id)
        return True

    def delete_status(self, status_id):
        """
        Deletes the status message with id, status_id
        """
        if not self.search_status(status_id):
            # logger.debug("Status ID %s does not exist in the database", status_id)
            return False
        self.database.delete_one({"_id": status_id})
        # logger.debug("Status ID %s successfully deleted from the database", status_id)
        return True

    def delete_many(self, query):
        """
        Deletes multiple statuses from the collection based on the query.
        """
        return self.database.delete_many(query)

    def search_status(self, status_id):
        '''
        Find and return a status message by its status_id

        Returns an empty UserStatus object if status_id does not exist
        '''
        query = {"_id": status_id}
        result = self.database.find_one(query)
        if not result:
            # logger.debug("Status ID %s was not found in the database", status_id)
            return False
        # logger.debug("Status ID %s was found in the database", status_id)
        return result
