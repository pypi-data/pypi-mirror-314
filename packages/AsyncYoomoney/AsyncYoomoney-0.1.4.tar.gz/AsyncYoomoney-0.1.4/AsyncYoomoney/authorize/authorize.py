from typing import List
import aiohttp

from AsyncYoomoney.exceptions import (
    InvalidRequest,
    UnauthorizedClient,
    InvalidGrant,
    EmptyToken
)

class Authorize:
    @classmethod
    async def create(
            cls,
            client_id: str,
            redirect_uri: str,
            client_secret: str,
            scope: List[str],
            session: aiohttp.ClientSession = None
                  ):

        url = "https://yoomoney.ru/oauth/authorize?client_id={client_id}&response_type=code" \
              "&redirect_uri={redirect_uri}&scope={scope}".format(client_id=client_id,
                                                                  redirect_uri=redirect_uri,
                                                                  scope='%20'.join([str(elem) for elem in scope]),
                                                                  )

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        if session:
            async with session.post(url, headers=headers) as response:
                response = response
        else:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers) as response:
                    response = response

        if response.status == 200:
            print("Visit this website and confirm the application authorization request:")
            print(response.url)

        code = str(input("Enter redirected url (https://yourredirect_uri?code=XXXXXXXXXXXXX) or just code: "))
        try:
            code = code[code.index("code=") + 5:].replace(" ","")
        except:
            pass

        url = "https://yoomoney.ru/oauth/token?code={code}&client_id={client_id}&" \
              "grant_type=authorization_code&redirect_uri={redirect_uri}&client_secret={client_secret}".format(code=str(code), client_id=client_id, redirect_uri=redirect_uri, client_secret=client_secret )
        
        if session:
            async with session.post(url, headers=headers) as response:
                response = response
        else:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers) as response:
                    response = response

        response_json = await response.json()

        if "error" in response_json:
            error = response_json["error"]
            if error == "invalid_request":
                raise InvalidRequest()
            elif error == "unauthorized_client":
                raise UnauthorizedClient()
            elif error == "invalid_grant":
                raise InvalidGrant()

        if response_json['access_token'] == "":
            raise EmptyToken()

        print("Your access token:")
        print(response_json['access_token'])