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
    col.update_one({"_id": ObjectId(f'{_id}')},{"$set":{"processed":processedArr}})
    print("updated")

async def findRec(_id:str):
    db = client.test
    col = db.get_collection("users")
    recIds = []
    diffs = []
    results = col.find({"_id": ObjectId(f'{_id}')})
    for result in results:
        theUserArry = np.array(result.get("processed"))
        break
    for doc in col.find():
        atomArr1 = np.array(doc.get("processed"))
        if doc.get("_id") != ObjectId(f'{_id}'):
            diffs.append({doc.get("_id"):np.linalg.norm(theUserArry - atomArr1)})
    
    for i in range(3):
        smallId = None
        smallestDiff = -1
        for diff in diffs:
            for _id, difff in diff.items():
                if smallestDiff == -1 and smallId == None:
                    smallestDiff = difff
                    smallId = _id
                elif smallestDiff > difff:
                    smallestDiff = difff
                    smallId = _id
        if not smallId is None:
            recIds.append(str(smallId))
            diffs.remove({smallId:smallestDiff})
            smallId = None
            smallestDiff = -1
        else:
            continue
                

    return recIds
