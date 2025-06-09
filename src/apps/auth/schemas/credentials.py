from pydantic import BaseModel


class CredentialsSchema(BaseModel):
    username: str
    password: str
