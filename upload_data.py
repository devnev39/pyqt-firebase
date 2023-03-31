from database.app import db
import pandas as pd
import sys
import os

def delete_collection(coll_ref, batch_size):
    docs = coll_ref.list_documents(page_size=batch_size)
    deleted = 0

    for doc in docs:
        print(f'Deleting doc {doc.id} => {doc.get().to_dict()}')
        doc.delete()
        deleted = deleted + 1

    if deleted >= batch_size:
        return delete_collection(coll_ref, batch_size)

try:
    if len(sys.argv) < 2:
        raise Exception('Filename not provided !')

    filename = sys.argv[1]

    if(not filename.index('.xlsx')):
        raise Exception('Excel file not detected !')
    
    df = pd.read_excel(filename)

    delete_collection(db.collection('data'),64)

    for i in range(len(df)):
        db.collection('data').document(str(i)).set(df.iloc[i].to_dict())
    
    print('Written !')

except Exception as ex:
    print(ex)
