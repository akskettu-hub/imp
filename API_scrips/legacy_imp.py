import os
import requests
from dotenv import load_dotenv
import json
import jwt  # pip install pyjwt
from jwt import PyJWKClient


def saveTokens(access_token, refresh_token, path="legacy_tokens.json"):
    with open(path, "w") as f:
        json.dump({"access_token": access_token, "refresh_token": refresh_token}, f)


def loadTokens(path="legacy_tokens.json"):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    else:
        return None


def getAccessToken():
    load_dotenv()

    url = (
        "https://account.readcoop.eu/auth/realms/readcoop/protocol/openid-connect/token"
    )
    data = {
        "grant_type": "password",
        "username": os.getenv("TRANSKRIBUS_USERNAME"),
        "password": os.getenv("PASSWORD"),
        "client_id": "transkribus-api-client",
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = requests.post(url, data=data, headers=headers, timeout=30)

    print("Status:", response.status_code)
    print("Body preview:", response.text[:200])

    response.raise_for_status()

    payload = response.json()
    access_token = payload.get("access_token")
    refresh_token = payload.get("refresh_token")

    print("access_token:", access_token[:100])
    print("refresh_token:", refresh_token[:100])
    saveTokens(access_token, refresh_token)

    return access_token


def refreshAccessToken():
    print("refreshing tokens")

    tokens = loadTokens()
    if not tokens:
        raise Exception("Could not find tokens.json")

    url = (
        "https://account.readcoop.eu/auth/realms/readcoop/protocol/openid-connect/token"
    )

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "grant_type": "refresh_token",
        "refresh_token": tokens["refresh_token"],
        "client_id": "processing-api-client",
    }

    response = requests.post(url, data=data, headers=headers, timeout=30)

    print("Status:", response.status_code)
    print("Body preview:", response.text[:200])

    response.raise_for_status()

    payload = response.json()
    access_token = payload.get("access_token")
    refresh_token = payload.get("refresh_token")

    print("access_token:", access_token[:100])
    print("refresh_token:", refresh_token[:100])
    saveTokens(access_token, refresh_token)

    return access_token


def handleAccess():
    tokens = loadTokens()

    if tokens:
        return tokens["access_token"]

    else:
        access_token = getAccessToken()
        if not access_token:
            raise Exception("Tokens not found despite refetching")
        return access_token


def getJobStatus(jobId):
    print("getting job status:")

    access_token = handleAccess()

    url = f"https://transkribus.eu/processing/v1/processes/{jobId}"
    print(url)

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    print(headers)

    response = requests.get(url, headers=headers, timeout=30)

    print("Status:", response.status_code)
    print("Body preview:", response.text)


def test():
    access_token = handleAccess()
    token = access_token
    payload = jwt.decode(token, options={"verify_signature": False})
    print(payload)


def getCollections():
    print("getting collections:")

    access_token = handleAccess()
    url = "https://transkribus.eu/TrpServer/rest/collections"
    print(url)

    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    # print(headers)

    response = requests.get(url, headers=headers, timeout=30)

    print("Status:", response.status_code)
    print("Body preview:", response.text)


def getDocument():
    print("getting documents:")

    access_token = handleAccess()
    url = "https://transkribus.eu/TrpServer/rest/collections/2197393/11313899/fulldoc"
    print(url)

    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    # print(headers)

    response = requests.get(url, headers=headers, timeout=30)

    # print("Status:", response.status_code)
    # print("Body:", response.text)

    response.raise_for_status()

    payload = response.json()
    print(json.dumps(payload, indent=4))


def getJob():
    print("getting collections:")

    access_token = handleAccess()
    url = "https://transkribus.eu/TrpServer/rest/jobs/18833341"
    print(url)

    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    # print(headers)

    response = requests.get(url, headers=headers, timeout=30)

    # print("Status:", response.status_code)
    # print("Body:", response.text)

    response.raise_for_status()

    payload = response.json()
    print(json.dumps(payload, indent=4))


def getDocumentXML():
    print("getting doc xml:")

    access_token = handleAccess()
    url = "https://transkribus.eu/TrpServer/rest/collections/2197393/11313899/1/list"
    print(url)

    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    # print(headers)

    response = requests.get(url, headers=headers, timeout=30)

    print("Status:", response.status_code)
    print("Body:", response.text)


if __name__ == "__main__":
    # getAccessToken()
    # refreshAccessToken()	18833341
    # test = handleAccess()
    # print(test)
    getAccessToken()
    # getJobStatus(18833341)
    # test()
    # getCollections()
    getDocumentXML()
