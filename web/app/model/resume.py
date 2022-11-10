from pydantic import BaseModel


class Item(BaseModel):
    markdown: str


class SavePdfRequest(Item):
    user_id: int


class UpdateFilePathRequest(BaseModel):
    filepath: str
