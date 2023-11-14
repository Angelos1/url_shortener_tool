import time
import string
import random
from mongo import MongoDatabase

class UrlShortener:
    def __init__(self, mongo_uri, db_name, collection_name, expiration_time):
        self.db = MongoDatabase(mongo_uri, db_name, collection_name)
        self.expiration_time = expiration_time
        self.short_url_prefix = "camarasoft.com/"

    def generate_short_url(self):
        """
            The function to generate a random short url.

            Generates a shortened url that is not already mapped from another URL
            in our database.

            Takes no parameters

            Returns:
                    produced_short_url (str): A short url
        """
        # All letters in the alphabet
        letters = string.ascii_lowercase + string.ascii_uppercase
        while True:
            # Choose 6 letters randomly
            random_letters = random.choices(letters, k=6)
            # Create the short URL
            produced_short_url = self.short_url_prefix + "".join(random_letters)
            # Get url mongo document by short url
            short_url = self.db.find_by_short(produced_short_url)
            if not short_url:
                return produced_short_url

    def url_is_expired(self, ts):
        """
        The function to check whether a timestamp is expired taking into account the expiration time we set.

        Takes as input a timestamp returns whether the timestamp is expired.

        Parameters:
            ts (float): Timestamp of a url mapping

        Returns:
            is_expired (bool): Boolean value to indicate whether it is expired or not.
        """
        # Check if ts is expired
        is_expired = time.time() - ts > self.expiration_time

        return is_expired

    def minify(self, original_url):
        """
        The function to shorten a url and store a document of the format
        {original_url : <url>, short_url: <short url>, ts: <timestamp>}
        in the database .

        Checks if the  URL exists and is not expired
        If yes, returns the corresponding short URL
        Otherwise,
            return a message indicating that the URL is expired or
            if it is not expired it generates a new shortened URL for it, stores
            {original_url : <url>, short_url: <short url>, ts: <timestamp>} in the database
            and returns the generated url.

        Parameters:
            ts (float): Timestamp of a url mapping

        Returns:
             (str): "Url_Expired" if url is expired or short url
        """
        # Check if URL is already in the database
        existing_record = self.db.find_by_original(original_url)

        if existing_record:
            if not self.url_is_expired(existing_record["ts"]):
                return existing_record["short_url"]
            else:
                return "Url_Expired"
        else:
            # Generate a shortened URL
            short_url = self.generate_short_url()
            # Save the URL in the database
            self.db.save(original_url, short_url, time.time() + self.expiration_time)
            return short_url

    def expand(self, short_url):
        """
        The function expand a shortened url

        Checks if the shortened URL exists and is not expired.
        If yes, return the corresponding original URL.
        Otherwise, return a message indicating that the URL doesn't exist or is expired.

        Parameters:
            short_url (float): Timestamp of a url mapping

        Returns:
             (str): "Url_Expired" if url is expired or "Url_Not_Exist" if short url doesn't exist in the database or
                    the original url.
        """

        # Check if short URL is already in the database
        existing_record = self.db.find_by_short(short_url)

        if existing_record:
            if not self.url_is_expired(existing_record["ts"]):
                return existing_record["original_url"]
            else:
                return "Url_Expired"
        else:
            return "Url_Not_Exists"