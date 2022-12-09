from pydantic import BaseModel,Field

class LoginSchema(BaseModel):
    username: str = Field(default=None)
    password: str = Field(default=None)
    class Config:
        the_schema = {
            "login_demo": {
                "username":"ben",
                "password":"password",
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

class ChangePwdSchema(BaseModel):
    uid: str = Field(default=None)
    old_password: str = Field(default=None)
    new_password: str = Field(default=None)
    class Config:
        the_schema = {
            "change_pwd_demo": {
                "uid":"ben",
                "old_password":"oldpassword",
                "new_password":"newpassword",
            }
        }