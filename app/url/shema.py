import pydantic


class CreateUrl(pydantic.BaseModel):
    path: str
