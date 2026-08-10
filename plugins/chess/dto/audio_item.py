from pydantic import BaseModel


class AudioItem(BaseModel):
    start: float
    end: float
    character: str
    emotion: str
    text: str
    audio: str