from pydantic import BaseModel, Field
from typing import List

class AnimeRecommendationModel(BaseModel):
    title: str = Field(description="Anime title")
    plot: str = Field(description="2-3 sentence plot summary")
    reason: str = Field(description="Why it matches user preference")


class AnimeRecommendationList(BaseModel):
    summary: str = Field(description="Brief summary of the recommendations")
    recommendations: List[AnimeRecommendationModel]