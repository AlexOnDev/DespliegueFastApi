from pymongo import MongoClient

# BD Local
# db_client = MongoClient().local

# BD Remota
db_client = MongoClient("mongodb+srv://test:test@cluster0.2ooeo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0").test