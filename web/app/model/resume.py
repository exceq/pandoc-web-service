from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Item(BaseModel):
    markdown: str


class SavePdfRequest(Item):
    user_id: int


class UpdateFilePathRequest(BaseModel):
    filepath: str


class FileDto(BaseModel):
    id: int
    filename: Optional[str]
    created: datetime
