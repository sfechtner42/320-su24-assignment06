"""
Classes for user information for the social network project
revised to work with database
"""

# pylint: disable=R0903

from loguru import logger

# set-up logging for users.py
logger.remove()
logger.add("log_file_{time:YYYY_MMM_DD}.log")


# logger.add(sys.stderr, level="ERROR")
# logger.info("users.py is imported")
# logger.error("Problem here users.py")
# logger.debug("Debug here users.py")


class UserCollection():
    '''
    Contains a collection of Users objects
    '''

    def __init__(self, database):
        self.database = database
        logger.debug("User database successfully linked")

    def add_user(self, user_id, email, user_name, user_last_name):
        '''
        Adds a new user to the collection
        '''
        if self.search_user(user_id):
            # Rejects new user if user id already exists
            logger.debug("User ID %s already exists in the database", user_id)
            return False
        data = {"_id": user_id,
                "user_email": email,
                "user_name": user_name,
                "user_last_name": user_last_name}
        self.database.insert_one(data)
        logger.debug("User ID %s successfully added to database", user_id)
        return True

    def batch_load_users(self, data):
        """
        Adds new users to the collection with a batch load
        """
        for row in data:
            if self.search_user(row["_id"]):
                # Rejects new user batch if it contains a duplicate
                logger.debug("User ID %s already exists in the database", row['_id'])
                return False
        self.database.insert_many(data)
        return True

    def modify_user(self, user_id, email, user_name, user_last_name):
        '''
        Modifies an existing user
        '''
        results = self.search_user(user_id)
        if not results:
            logger.debug("User ID %s does not exist in the database", user_id)
            return False
        data = {"_id": user_id,
                "user_email": email,
                "user_name": user_name,
                "user_last_name": user_last_name}
        self.database.update_one(results, {"$set": data})
        logger.debug("User ID %s successfully modified in the database", user_id)
        return True

    def delete_user(self, user_id):
        '''
        Deletes an existing user
        '''
        if not self.search_user(user_id):
            logger.debug("User ID %s does not exist in the database", user_id)
            return False
        self.database.delete_one({"_id": user_id})
        logger.debug("User ID %s successfully deleted from the database", user_id)
        return True

    def search_user(self, user_id):
        '''
        Searches for user data
        '''
        results = self.database.find_one({"_id": user_id})
        if not results:
            logger.debug("User ID %s was not found in the database", user_id)
            return False
        logger.debug("User ID %s was found in the database", user_id)
        return results
