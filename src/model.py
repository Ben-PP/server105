from pydantic import BaseModel,Field

class LoginSchema(BaseModel):
    username: str = Field(default=None)
    password: str = Field(default=None)
    class Config:
        the_schema = {
            "login_demo": {
                "username":"ben",
                "password":"hashedpassword",
            }
        }

class LogoutSchema(BaseModel):
    jwt: str = Field(default=None)
    class Config:
        the_schema = {
            "logout_demo": {
                "jwt":"jwttoken",
            }
        }