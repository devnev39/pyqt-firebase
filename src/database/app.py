import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('src/database/firebase_auth.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
