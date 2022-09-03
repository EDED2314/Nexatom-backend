from algorithms.recommendation import Atom, predict
from dotenv import load_dotenv
import os
import pymongo
import asyncio
load_dotenv()

key = os.getenv("MONGO")
client = pymongo.MongoClient(f"mongodb+srv://admin:{key}@cluster0.agyzg9a.mongodb.net/?retryWrites=true&w=majority")

async def updateUsers(atom: Atom):
    asyncio.sleep(1)
    processedArr = atom.labelsArr()
    
    
    
    db = client.test
    col = db.get_collection("users")
    for doc in col.find():
        print(doc)
        print(doc.get("name"))