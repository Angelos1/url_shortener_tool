import argparse
import os
from dotenv import load_dotenv
from shortener import UrlShortener

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
db_name = os.getenv("DB")
collection_name = os.getenv("COLLECTION")
expiration_time = 20

url_shortener = UrlShortener(MONGO_URI, db_name, collection_name, expiration_time)
parser = argparse.ArgumentParser(description="URL Shortener Tool")
parser.add_argument("--minify", help="Shorten a URL", type=str)
parser.add_argument("--expand", help="Expand a shortened URL")
args = parser.parse_args()

if args.minify:

    result = url_shortener.minify(args.minify)

    if result == "Url_Expired":
        print(f"Shortened URL is expired")
    else:
        print(f"Shortened URL: {result}")

elif args.expand:

    result = url_shortener.expand(args.expand)

    if result == "Url_Expired":
        print(f"Expanded URL is expired")
    else:
        print(f"Expanded URL: {result}")