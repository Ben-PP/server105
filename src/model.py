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

class ChangePwdSchema(BaseModel):
    old_password: str = Field(default=None)
    new_password: str = Field(default=None)
    class Config:
        the_schema = {
            "change_pwd_demo": {
                "old_password":"oldpassword",
                "new_password":"newpassword",
            }
        }

class AddUserSchema(BaseModel):
    uid: str = Field(default=None)
    pwd: str = Field(default=None)
    can_make_transactions: bool = Field(default=None)
    is_admin: bool = Field(default=None)
    class Config:
        the_schema = {
            "AddUserSchema_demo": {
                "uid":"Unique username",
                "pwd":"Password for the user",
                "can_make_transaction":"bool",
                "is_admin":"bool",
            }
        }

class RemoveUserSchema(BaseModel):
    uid: str = Field(default=None)
    class Config:
        the_schema = {
            "RemoveUserSchemaDemo": {
                "uid":"uid of the user to be removed",
            }
        }

class EditUserSchema(BaseModel):
    uid: str = Field(default=None)
    can_make_transactions: bool = Field(default=None)
    is_admin: bool =Field(default=None)
    class Config:
        the_schema = {
            "EditUserSchemaDemo": {
                "uid":"uid of the user to be edited",
                "can_make_transactions":"bool",
                "is_admin":"bool",
            }
        }