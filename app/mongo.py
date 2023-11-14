from pymongo import MongoClient

class MongoDatabase:
    def __init__(self, mongo_uri, db_name, collection_name):
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.url_collection = self.db[collection_name]

    def save(self, original_url, short_url, expiration_time):
        """
            Save mongo document for URLs
        """

        doc = {"original_url": original_url, "short_url": short_url, "ts": expiration_time}

        self.url_collection.insert_one(doc)

    def find_by_original(self, original_url):
        """
            Find the mongo document for a given original URL
        """

        filter = {"original_url": original_url}

        return self.url_collection.find_one(filter)

    def find_by_short(self, short_url):
        """
            Find the mongo document for a given short URL
        """
        filter = {"short_url": short_url}

        return self.url_collection.find_one(filter)
