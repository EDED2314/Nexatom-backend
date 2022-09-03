from cgitb import small
from algorithms.recommendation import Atom, predict
from dotenv import load_dotenv
import os
import pymongo
import asyncio
import numpy as np
from bson.objectid import ObjectId
load_dotenv()

key = os.getenv("MONGO")
client = pymongo.MongoClient(f"mongodb+srv://admin:{key}@cluster0.agyzg9a.mongodb.net/?retryWrites=true&w=majority")

async def updateUser(atom: Atom, _id:str):
    await asyncio.sleep(1)
    processedArr = atom.labelsArr().tolist()
    
    db = client.test
    col = db.get_collection("users")
    col.update_one({"_id": ObjectId(f'{_id}')},{"$set":{"proccessed":processedArr}})
    print("updated")

async def findRec(_id:str):
    await asyncio.sleep(1)
    db = client.test
    col = db.get_collection("users")
    recIds = []
    diffs = []
    results = col.find({"_id": ObjectId(f'{_id}')})
    for result in results:
        theUserArry = np.array(result.get("proccessed"))
        break
    for doc in col.find():
        atomArr1 = np.array(doc.get("proccessed"))
        if doc.get("_id") != ObjectId(f'{_id}'):
            diffs.append({doc.get("_id"):np.linalg.norm(theUserArry - atomArr1)})
    
    for i in range(3):
        smallId = ObjectId('63137875afd8bc0b8143642e')
        smallestDiff = -1
        for diff in diffs:
            for _id, diff in diff.items():
                if smallestDiff == -1 and smallId == ObjectId('63137875afd8bc0b8143642e'):
                    smallestDiff = diff
                    smallId = _id
                elif smallestDiff > diff:
                    smallestDiff = diff
                    smallId = _id
            recIds.append(smallId)
            del diff[smallId]
                

    return recIds
