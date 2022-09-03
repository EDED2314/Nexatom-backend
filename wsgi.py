from flask import Flask, jsonify, request, render_template
import aiohttp
import os
import json
from flask_cors import CORS
from algorithms.recommendation import predict
from scrapers.stackoverflow.stackoverflow import StackoverflowInfo
from scrapers.github.github import GithubInfo
from algorithms.database_com import updateUsers,Atom

app = Flask(__name__, template_folder="templates")
app.config["SECRET_KEY"] = f"{os.urandom(24).hex()}"
CORS(app, support_credentials=True)



@app.route("/")
def home():
    return "hello word"


@app.route("/api/stackoverflow/getBadges", methods=["GET"])
async def getStackoverflowBadges():
    if request.method == "POST":
        return jsonify({"code":"405", "message":"method not allowed"})
    # you need uhh user_url
    async with aiohttp.ClientSession() as session:
        userUrl = request.args.get("userurl")
        if not userUrl is None:
            info = StackoverflowInfo(userUrl)
            bagdes = await info.findBadges(session)
            return jsonify(bagdes)
        else:
            return jsonify({"code": "400", "message": "please provide stackoverflow user url"})


@app.route("/api/stackoverflow/getTags", methods=["GET"])
async def getStackoverflowTags():
    if request.method == "POST":
        return jsonify({"code":"405", "message":"method not allowed"})
    # you need uhh user_url
    async with aiohttp.ClientSession() as session:
        userUrl = request.args.get("userurl")
        if not userUrl is None:
            info = StackoverflowInfo(userUrl)
            tags = await info.findTags(session)
            return jsonify(tags)
        else:
            return jsonify({"code": "400", "message": "please provide stackoverflow user url"})
        
@app.route("/api/github/pfp", methods=['GET'])
async def getGithubPfp():
    if request.method == "POST":
        return jsonify({"code":"405", "message":"method not allowed"})
    async with aiohttp.ClientSession() as session:
        username = request.args.get("username")
        if not username is None:
            info = GithubInfo(username)
            b64String = await info.getpfp(session)
            return jsonify({"code":"200","image":b64String.decode('utf-8')})
        else:
            return jsonify({"code": "400", "message": "please provide github username"})

@app.route('/api/github/langs', methods=['GET'])
async def getGithubMostUsedLangs():
    async with aiohttp.ClientSession() as session:
        username = request.args.get("username")
        if not username is None:
            info = GithubInfo(username)
            langs = await info.getLangs(session)
            return jsonify(langs)
        else:
            return jsonify({"code": "400", "message": "please provide github username"})
            
@app.route('/api/algo/storeData', methods=["POST"])
def createThenStoreProcessedUserData():
    experience = int(request.args.get("exp"))
    timezone = request.args.get("tz")
    lang1 = request.args.get("lang1")
    lang1 = lang1.replace("\'", "\"")
    lang2 = request.args.get("lang2")
    lang2 = lang1.replace("\'", "\"")
    lang3 = request.args.get("lang3")
    lang3 = lang1.replace("\'", "\"")
    majors = request.args.get("majors")
    atom1 = Atom(experience, timezone, json.loads(lang1), json.loads(lang2), json.loads(lang3), majors, 0.5)
    atom2 = Atom(10, "GMT+10.5", {"python":"40"}, {"rust":"20"}, {"dart":"10"}, ["computer science", "mathematics"],0.5)
    x = predict(atom1, atom2)
    return jsonify({"code":"200", "message":"success", "sim":x})
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)