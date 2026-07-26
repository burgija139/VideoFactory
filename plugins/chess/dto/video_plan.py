from typing import List, Literal
from pydantic import BaseModel, Field
from plugins.chess.dto.timeline_item import TimelineItem

class VideoPlan(BaseModel):
    title: str = Field(default="Chess Puzzle")

    speakers_count: Literal["1", "2"] = Field(
        description="Number of characters. If show_moves is False, this MUST be '1' (Solo Narrator contacting the audience)."
    )

    timeline: List[TimelineItem]

    intro_seconds: int = Field(
        default=5,
        description="Duration of the intro in seconds."
    )

    # 🔄 IZMENJENO: Čist prekidač. Ako je False, nema prikazivanja poteza na ekranu (Challenge format)
    show_moves: bool = Field(
        default=True, 
        description="If True, moves are rendered. If False, the board stays static as a puzzle challenge for the audience."
    )

    timer_enabled: bool = Field(default=False)
    timer_duration: int = Field(default=5)

    pacing: Literal["slow", "medium", "fast"] = Field(default="medium")
    style: Literal["viral", "educational", "dramatic"] = Field(default="viral")