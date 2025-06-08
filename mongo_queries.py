from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["stocks"]
collection = db["profiles"]

# Show one document
sample = collection.find_one()
print("📋 One company profile from MongoDB:\n", sample)

# Count all documents
count = collection.count_documents({})
print(f"\n📊 Total documents in MongoDB: {count}")
