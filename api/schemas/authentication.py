import pydantic


class UserSignUpSchema(pydantic.BaseModel):
    email: str
    password: str


class UserSignUpReturnSchema(pydantic.BaseModel):
    email: str


class AccountActivationSchema(pydantic.BaseModel):
    activation_code: int
