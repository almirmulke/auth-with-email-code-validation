from fastapi import APIRouter, Body, Depends, Request, status

from controllers.authentication import AuthenticationController
from middlwares.authentication import authentication_middlware
from schemas.authentication import (
    AccountActivationSchema,
    UserSignUpReturnSchema,
    UserSignUpSchema,
)

auth_router = APIRouter(prefix="/auth")
protected_auth_router = APIRouter(prefix="/auth", dependencies=[Depends(authentication_middlware)])


@auth_router.post(
    "/sign-up", status_code=status.HTTP_201_CREATED, response_model=UserSignUpReturnSchema
)
async def sign_up_user(
    user_data: UserSignUpSchema = Body(),
    authentication_controller=Depends(AuthenticationController),
):
    return await authentication_controller.sign_up(user_data)


@protected_auth_router.put("/activate-account", status_code=status.HTTP_200_OK)
async def activate_account(
    request: Request,
    activation_data: AccountActivationSchema = Body(),
    authentication_controller=Depends(AuthenticationController),
):
    print("Called")
    await authentication_controller.activate_user_account(
        request.user, activation_data.activation_code
    )
