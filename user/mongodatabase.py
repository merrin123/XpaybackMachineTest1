from pymongo import MongoClient

# MongoDB Configuration
mongo_client = MongoClient('mongodb://localhost:27017')
mongo_db = mongo_client['userdb']
mongo_collection = mongo_db['users']