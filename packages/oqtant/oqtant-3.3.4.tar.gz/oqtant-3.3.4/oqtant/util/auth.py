# Copyright 2024 Infleqtion
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import base64
import hashlib
import os
import webbrowser
from multiprocessing import Queue

import requests
import uvicorn
from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import RedirectResponse
from ipyauth import Auth, ParamsAuth0

from oqtant.settings import Settings
from oqtant.util.server import ThreadServer

settings = Settings()

app = FastAPI(title="Login API", openapi_url="/openapi.json")
router = APIRouter()


def generate_random(length: int) -> str:
    """Method to generate a random base64 string

    Args:
        length (int): The length to make the string

    Returns:
        str: The generated base64 string
    """
    return base64.urlsafe_b64encode(os.urandom(length)).decode("utf-8").replace("=", "")


verifier = generate_random(80)


def generate_challenge(verifier: str) -> str:
    """Method to generate a base64 string to serve as an auth0 challenge

    Args:
        verifier (str): A base64 string to create the challenge off of

    Returns:
        str: The generated challenge
    """
    hashed = hashlib.sha256(verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(hashed).decode("utf-8").replace("=", "")


def get_authentication_url(auth_server_port: int) -> None:
    """Method to generate the auth0 authentication url

    Args:
        auth_server_port (int): The port of the server auth0 should redirect to
    """
    code_challenge = generate_challenge(verifier)
    auth_url = "".join(
        [
            f"https://{settings.auth0_domain}/authorize",
            "?response_type=code",
            f"&scope={settings.auth0_scope}",
            f"&audience={settings.auth0_audience}",
            f"&code_challenge={code_challenge}",
            "&code_challenge_method=S256",
            f"&client_id={settings.auth0_client_id}",
            f"&redirect_uri=http://localhost:{auth_server_port}",
        ]
    )
    return auth_url


queue = Queue()


@app.get("/")
async def main(request: Request, code: str) -> str:
    """Main route to handle user authentication

    Args:
        request (fastapi.Request): The request object
        code (str): The code provided by auth0 to be verified

    Returns:
        str: Message on whether the user successfully authenticated
    """
    resp = await get_token(verifier, code, request.url.port)
    token = resp["access_token"]
    queue.put({"token": token})
    if token:
        return "Successfully authenticated, you may close this tab now"
    else:
        return "Failed to authenticate, please close this tab and try again"


@app.get("/login")
def login(request: Request) -> RedirectResponse:
    """Route to initiate the authentication process

    Args:
        request (Request): The request object

    Returns:
        RedirectResponse: A redirect to auth0 universal login
    """
    return RedirectResponse(
        url=get_authentication_url(auth_server_port=request.url.port)
    )


async def get_token(verifier: str, code: str, auth_server_port: int) -> dict:
    """Method to get an authentication token from auth0 after a user authenticates

    Args:
        verifier (str): The base64 string to provide along with the code challenge
        code (str): The code challenge returned from auth0
        auth_server_port (int): The port the local server is running on

    Returns:
        dict: The json response from auth0, should contain the authentication token
    """
    url = f"https://{settings.auth0_domain}/oauth/token"
    headers = {"content-type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "authorization_code",
        "client_id": settings.auth0_client_id,
        "code_verifier": verifier,
        "code": code,
        "redirect_uri": f"http://localhost:{auth_server_port}",
    }
    resp = requests.post(
        url, headers=headers, data=data, allow_redirects=False, timeout=(5, 30)
    )
    return resp.json()


def get_user_token(auth_server_port: int = 8080) -> str:
    """Method to initiate the user authentication process

    Args:
        auth_server_port (int, optional): The port to run the server on locally

    Returns:
        str: The authentication token
    """
    allowed_ports = [8080, 8081, 8082, 8083, 8084, 8085]
    if auth_server_port not in allowed_ports:
        raise ValueError(f"{auth_server_port} not in allowed ports: {allowed_ports}")
    server_config = uvicorn.Config(
        app=app, host="localhost", port=auth_server_port, log_level="error"
    )
    server = ThreadServer(config=server_config)
    with server.run_in_thread():
        webbrowser.open(f"http://localhost:{auth_server_port}/login")
        token = queue.get(block=True)
    return token["token"]


def notebook_login() -> Auth:
    """Method to get an authenticate widget

    Returns:
        ipyauth.Auth: The authentication widget
    """
    p = ParamsAuth0(
        domain=settings.auth0_domain,
        client_id=settings.auth0_client_id,
        redirect_uri=settings.auth0_notebook_redirect_uri,
        audience=settings.auth0_audience,
        response_type=settings.auth0_response_type,
        scope=settings.auth0_scope,
    )
    a = Auth(params=p)
    return a
