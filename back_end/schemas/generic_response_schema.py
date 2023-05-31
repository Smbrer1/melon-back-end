from pydantic import BaseModel, Field


class GenericDelete(BaseModel):
    item: dict = Field(default={"itemName": "itemValue"})
    success: bool
