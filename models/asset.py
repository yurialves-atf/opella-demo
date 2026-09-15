from typing import Literal

from pydantic import BaseModel, Field


class EvidenceBlock(BaseModel):
    metric: str | None = None
    message: str


class ContentSection(BaseModel):
    title: str
    text: str


class ClaimEvidence(BaseModel):
    claim: str
    source_page: int
    source_evidence: str


class CreativeConcept(BaseModel):
    main_message: str
    visual_direction: str


class AssetContent(BaseModel):
    headline: str
    subheadline: str = ""

    sections: list[ContentSection] = Field(default_factory=list)

    key_points: list[str] = Field(default_factory=list)

    evidence_blocks: list[EvidenceBlock] = Field(default_factory=list)

    product_message: str = ""
    cta: str = ""
    disclaimer: str = ""


class Grounding(BaseModel):
    claims: list[ClaimEvidence] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class Review(BaseModel):
    status: Literal[
        "requires_human_review",
        "changes_requested",
        "approved",
    ] = "requires_human_review"

    notes: str = ""


class MedicalAsset(BaseModel):
    asset_type: Literal[
        "banner_memed",
        "article_pharmacist",
        "flyer"
    ]

    audience: str
    objective: str

    creative_concept: CreativeConcept
    content: AssetContent
    grounding: Grounding

    review: Review = Field(default_factory=Review)