from typing import Literal

from pydantic import BaseModel, Field


AssetType = Literal[
    "banner_memed",
    "article_pharmacist",
    "flyer",
]


class SuggestedTheme(BaseModel):
    id: str

    title: str

    problem_context: str

    product_connection: str

    rationale: str

    relevant_pages: list[int] = Field(
        default_factory=list
    )

    available_product_claims: int = 0

    suggested_assets: list[AssetType] = Field(
        default_factory=list
    )


class MonographAnalysis(BaseModel):
    document_name: str

    product_name: str

    document_summary: str

    themes: list[SuggestedTheme] = Field(
        default_factory=list
    )