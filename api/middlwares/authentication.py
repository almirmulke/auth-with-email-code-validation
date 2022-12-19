from fastapi import Depends, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from services.authentication import AuthenticationService


async def authentication_middlware(
    request=Request,
    credentials: HTTPBasicCredentials = Depends(HTTPBasic()),
    authentication_service: AuthenticationService = Depends(AuthenticationService),
):
    user = await authentication_service.get_user_by_basic_auth(
        credentials.username, credentials.password
    )
    request.user = user
