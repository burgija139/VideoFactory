from typing import Literal

from pydantic import BaseModel, Field


class TimelineItem(BaseModel):
    time: float = Field(description="Absolute time in seconds when the text appears on screen and when the voiceover starts.")
    text: str = Field(description="Text spoken by the character and shown on screen (maximum 10 words).")
    type: Literal["intro", "timer", "moves", "ending"] = Field(description="Type of event")

    character: Literal[
        "naruto",
        "sasuke"
    ]

    emotion: Literal[
        "natural",
        "excited",
    ]
