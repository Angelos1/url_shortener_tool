from unittest.mock import MagicMock, patch
import sys
import os
import time

# Add the app directory to the sys.path so that mongo module is importable from shortener.py in
# the local environment (my PC)
root_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root_dir + "/app")

from app.shortener import UrlShortener


def test_minify_url_not_shortened_yet():
    """
    Test for the case where the original URL already does not exist so we need to genarate
    a short URL for it and save it

    The MongoDatabase.find_by_original method is mocked so as the UrlSortener.generate_short_url

    """
    original_url = "https://www.example.com/f1/jdhjhfjs"

    # Creating a MagicMock object to simulate MongoDatabase
    mongo_mock = MagicMock()

    # Creating an instance of UrlShortener
    url_shortener = UrlShortener("mongo_uri", "db_name", "collection_name", expiration_time=60)

    # Mocking the MongoDB database with the mocked object
    url_shortener.db = mongo_mock

    # Mocking find_by_original method for this test
    mongo_mock.find_by_original.return_value = None

    # Mocking UrlShortener.generate_short_url method for this test
    with patch.object(UrlShortener, 'generate_short_url') as mock_method:
        # Mocking the return value of the method inside UrlShortener
        mock_method.return_value = "camarasoft.com/jLoiuP"

        # Testing minify function
        short_url = url_shortener.minify(original_url)

        # Assertion for the return value or expected behavior
        assert short_url == "camarasoft.com/jLoiuP"


def test_minify_url_already_shortened_not_expired():
    """
    Test for the case where the URL already exists in the db and it is not expired
    i.e. is_expired = time.time() - ts < self.expiration_time

    """

    original_url = "https://www.example.com/f1/jdhjhfjs"

    # Creating a MagicMock object to simulate MongoDatabase
    mongo_mock = MagicMock()

    # Creating an instance of UrlShortener
    url_shortener = UrlShortener("mongo_uri", "db_name", "collection_name", expiration_time=60)

    # Mocking the MongoDB database with the mocked object
    url_shortener.db = mongo_mock

    # Mocking find_by_original for this test
    mongo_mock.find_by_original.return_value = {"original_url": "https://www.example.com/f1/jdhjhfjs",
                                                "short_url": "camarasoft.com/dgyrnK",
                                                "ts": time.time() - 20
                                                # makes the difference between time.time() and timestamp of record less than expiration time
                                                }

    # Testing minify function
    short_url = url_shortener.minify(original_url)

    # Assertion for the return value or expected behavior
    assert short_url == "camarasoft.com/dgyrnK"


def test_minify_url_already_shortened_expired():
    """
    Test for the case where the URL already exists in the db and it is expired
    i.e. is_expired = time.time() - ts > self.expiration_time

    """

    original_url = "https://www.example.com/f1/jdhjhfjs"

    # Creating a MagicMock object to simulate MongoDatabase
    mongo_mock = MagicMock()

    # Creating an instance of UrlShortener
    url_shortener = UrlShortener("mongo_uri", "db_name", "collection_name", expiration_time=60)

    # Mocking the MongoDB database with the mocked object
    url_shortener.db = mongo_mock

    # Mocking find_by_original for this test
    mongo_mock.find_by_original.return_value = {"original_url": "https://www.example.com/f1/jdhjhfjs",
                                                "short_url": "camarasoft.com/dgyrnK",
                                                "ts": time.time() - 70
                                                # makes the difference between time.time() and timestamp of record bigger than expiration timee
                                                }

    # Testing minify function
    short_url = url_shortener.minify(original_url)

    # Assertion for the return value or expected behavior
    assert short_url == "Url_Expired"


def test_expand_url_not_exists():
    """
    Test for the case where the short URL does not exist exists in the db
    """

    short_url = "camarasoft.com/dgyrnK"

    # Creating a MagicMock object to simulate MongoDatabase
    mongo_mock = MagicMock()

    # Creating an instance of UrlShortener
    url_shortener = UrlShortener("mongo_uri", "db_name", "collection_name", expiration_time=60)

    # Mocking the MongoDB database with the mocked object
    url_shortener.db = mongo_mock

    # Mocking find_by_short for this test
    mongo_mock.find_by_short.return_value = None

    # Testing expand function
    short_url = url_shortener.expand(short_url)

    # Assertion for the return value or expected behavior
    assert short_url == "Url_Not_Exists"
