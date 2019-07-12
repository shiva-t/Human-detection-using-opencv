from google.cloud import firestore

def getFlag():
 db = firestore.Client()
 collec = db.collection('switch')
 docs = collec.get()
 for doc in docs:
  flag = doc.get('status')
 return flag