from flask import Flask, jsonify, request, render_template
import aiohttp
import os
import json
from flask_cors import CORS
from scrapers.stackoverflow.stackoverflow import StackoverflowInfo
from scrapers.github.github import GithubInfo


app = Flask(__name__, template_folder="templates")
app.config["SECRET_KEY"] = f"{os.urandom(24).hex()}"
CORS(app, support_credentials=True)



@app.route("/")
def home():
    return "hello word"


@app.route("/api/stackoverflow/getBadges", methods=["GET"])
async def getStackoverflowBadges():
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
    # you need uhh user_url
    async with aiohttp.ClientSession() as session:
        userUrl = request.args.get("userurl")
        if not userUrl is None:
            info = StackoverflowInfo(userUrl)
            tags = await info.findTags(session)
            return jsonify(tags)
        else:
            return jsonify({"code": "400", "message": "please provide stackoverflow user url"})
        
@app.route("/api/github/pfp")
async def getGithubPfp():
    async with aiohttp.ClientSession() as session:
        username = request.args.get("username")
        if not username is None:
            info = GithubInfo(username)
            b64String = await info.getpfp(session)
            return jsonify({"code":"200","image":b64String.decode('utf-8')})
        else:
            return jsonify({"code": "400", "message": "please provide github username"})
            
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)