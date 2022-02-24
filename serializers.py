import pydantic
import re


PATTERN_EMAIL = re.compile(r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])""")
PATTERN_PASSWORD = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")


class AdvertisementSerializerPost(pydantic.BaseModel):
    title: str
    description = ''


class AdvertisementSerializerPatch(pydantic.BaseModel):
    title = ''
    description = ''


class UserSerializer(pydantic.BaseModel):
    username: str
    email: str
    password: str

    @pydantic.validator("email")
    def correct_email(value: str):
        if not PATTERN_EMAIL.match(value):
            raise ValueError("incorrect email")
        return value

    @pydantic.validator("password")
    def password_strong(value: str):
        if not PATTERN_PASSWORD.match(value):
            raise ValueError("password is to easy")
        return value
