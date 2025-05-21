import pymongo
import environ
import os
env = environ.Env()
environ.Env.read_env(os.path.join(os.path.dirname(__file__), '.env'))

url = env('DB_URL')

client = pymongo.MongoClient(url)
db = client["Antlegs"]