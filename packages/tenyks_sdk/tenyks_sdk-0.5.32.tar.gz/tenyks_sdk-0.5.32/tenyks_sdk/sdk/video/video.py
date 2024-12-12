from typing import Dict

from pydantic import BaseModel, Field


class VideoClip(BaseModel):

    video_key: str = Field(
        description="Key of the video the clip belongs to",
        examples=["video_1"],
    )
    timestamp: float = Field(
        description="The timestamp of the clip in seconds",
        examples=[25.0],
    )
    duration: float = Field(
        description="The duration of the clip in seconds",
        examples=[12.0],
    )

    @classmethod
    def from_video_response(
        cls,
        video_dict: Dict,
    ) -> "VideoClip":
        return cls(video_key=video_dict["video_key"], 
                   timestamp=video_dict["timestamp"], 
                   duration=video_dict["duration"])
