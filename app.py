import os
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

app = Flask("test-app")
code = ""


@app.route("/")
def hello():
    code = request.args.get("code")
    state = request.args.get("state")
    print("auth called. code is " + code)
    if state == "itme":
        import requests, base64

        encoded_data = base64.b64encode(
            bytes("%s:%s" % (CLIENT_ID, CLIENT_SECRET), "ISO-8859-1")
        ).decode("ascii")
        authorization_header_string = "Basic %s" % encoded_data

        headers = {"Authorization": authorization_header_string}
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
        }

        r = requests.post(
            "https://accounts.spotify.com/api/token", headers=headers, data=data
        )

        print(r.json())
        # return r.json()
    # return code


@app.route("/auth")
def auth():
    code = request.args.get("code")
    state = request.args.get("state")
    print("auth called. code is " + code)
    if state == "itme":
        import requests, base64

        encoded_client_string = base64.b64encode(CLIENT_ID + ":" + CLIENT_SECRET)
        headers = {"Authorization": "Basic %s" % encoded_client_string}
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
        }

        requests.post(
            "https://accounts.spotify.com/api/token", headers=headers, data=data
        )

        # print(r.json())
        # return r.json()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
