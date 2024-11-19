"""
Main driver for a simple social network project
"""

import csv
import pymongo
# from loguru import logger
import user_status

DATABASE = "database"


def get_mongo_client(connection_string="mongodb://localhost:27017/"):
    """
    Creates a MongoDB client instance
    """
    return pymongo.MongoClient(connection_string)


def init_user_collection(mongo_client, database_name="database", table_name="UserAccounts"):
    """
    Creates and returns a MongoDB collection for user data.
    """
    db = mongo_client[database_name]  # Access the specified database by name
    collection = db[table_name]
    return collection


def init_status_collection(mongo_client, database_name="database", table_name="StatusUpdates"):
    """
    Creates and returns a new instance of UserStatusCollection.
    """
    db = mongo_client[database_name]  # Access the specified database by name
    status_collection = user_status.UserStatusCollection(db[table_name])
    return status_collection


def load_users(filename, user_collection, batch_size=32):
    """
    Opens a CSV file with user data and adds it to an existing MongoDB collection
    """
    try:
        with open(filename, encoding="utf-8", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            user_data = []
            for row in reader:
                if all(key in row and row[key] for key in ["USER_ID", "EMAIL", "NAME", "LASTNAME"]):
                    user_data.append({
                        "_id": row["USER_ID"],  # Use USER_ID as the primary key
                        "user_email": row["EMAIL"],
                        "user_name": row["NAME"],
                        "user_last_name": row["LASTNAME"]
                    })

            # Process data in batches
            for i in range(0, len(user_data), batch_size):
                batch = user_data[i:i + batch_size]
                try:
                    if not user_collection.batch_load_users(batch):
                        print('Mock duplicate key error')
                        return False
                except pymongo.errors.DuplicateKeyError:
                    print('Mock duplicate key error')
                    return False

            return True
    except (FileNotFoundError, KeyError) as e:
        print(f"Error loading users: {e}")
        return False


def load_status_updates(filename, status_collection, batch_size=100):
    """
    Loads status updates from a CSV file into the database in batches.
    """
    try:
        with open(filename, 'r', encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            status_updates = []

            for row in reader:
                status_updates.append({
                    "_id": row['STATUS_ID'],
                    "user_id": row['USER_ID'],
                    "status_text": row['STATUS_TEXT']
                })

            # Process data in batches
            for i in range(0, len(status_updates), batch_size):
                batch = status_updates[i:i + batch_size]
                if not status_collection.batch_load_statuses(batch):
                    print(f"Error loading batch of statuses starting at index {i}")
                    return False

            return True
    except FileNotFoundError:
        # logger.debug("File %s was not found", filename)
        return False


def add_user(user_id, email, user_name, user_last_name, user_collection):
    """
    Creates a new instance of Users and stores it in user_collection
    """
    user = {
        "_id": user_id,
        "user_email": email,
        "user_name": user_name,
        "user_last_name": user_last_name
    }
    try:
        user_collection.insert_one(user)
        return True
    except pymongo.errors.DuplicateKeyError:
        return False


def update_user(user_id, email, user_name, user_last_name, user_collection):
    """
    Updates the values of an existing user
    """
    query = {"_id": user_id}
    new_values = {"$set": {
        "user_email": email,
        "user_name": user_name,
        "user_last_name": user_last_name
    }}
    result = user_collection.update_one(query, new_values)
    return result.modified_count > 0


def delete_user(user_id, user_collection, status_collection):
    """
    Deletes a user from user_collection and associated statuses from status_collection.
    """
    # First, attempt to delete the user
    user_result = user_collection.delete_one({"_id": user_id})

    if user_result.deleted_count > 0:
        # If the user was deleted, delete all associated statuses
        status_result = status_collection.delete_many({"user_id": user_id})
        print(f"Deleted {status_result.deleted_count} statuses associated with UserID {user_id}")
        # logger.debug("User ID %s successfully deleted from the database", user_id)
        return True

    return False


def search_user(user_id, user_collection):
    """
    Searches for a user in user_collection(which is an instance of UserCollection).
    """
    return user_collection.find_one({"_id": user_id})


def add_status(user_id, status_id, status_text, status_collection, user_collection):
    """
    Creates a new instance of UserStatus and stores it in status_collection
    """
    user_exists = user_collection.find_one({"_id": user_id})

    if not user_exists:
        return False  # User does not exist, status cannot be added

    return status_collection.add_status(status_id, user_id, status_text)


def update_status(status_id, user_id, status_text, status_collection):
    """
    Updates the values of an existing status_id
    """
    return status_collection.modify_status(status_id, user_id, status_text)


def delete_status(status_id, status_collection):
    """
    Deletes a status_id from status_collection.
    """
    return status_collection.delete_status(status_id)


def search_status(status_id, status_collection):
    """
    Searches for a status in status_collection
    """
    return status_collection.search_status(status_id)
