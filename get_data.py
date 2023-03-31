from src.database.app import db

docs = db.collection('data').stream().to_dict()
for doc in docs:
    print(doc.to_dict())