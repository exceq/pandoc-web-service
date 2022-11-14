from datetime import datetime

from pydantic import BaseModel


class Item(BaseModel):
    markdown: str


class SavePdfRequest(Item):
    user_id: int


class UpdateFilePathRequest(BaseModel):
    filepath: str


class FileDto(BaseModel):
    id: int
    filename: str
    created: datetime
