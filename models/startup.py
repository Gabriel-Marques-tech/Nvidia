from pydantic import BaseModel
from enum import Enum


class AIClassification(str, Enum):
    AI_NATIVE = "AI-native"
    AI_ENABLED = "AI-enabled"
    NON_AI = "non-AI"


class Evidence(BaseModel):
    content: str        # trecho de texto encontrado
    source_url: str     # URL de onde veio
    source_type: str    # "site", "blog", "news", "careers"


class Startup(BaseModel):
    name: str
    website: str | None = None
    sector: str | None = None
    description: str | None = None
    founders: list[str] = []
    funding_usd: float | None = None
    tech_stack: list[str] = []
    classification: AIClassification | None = None
    evidence: list[Evidence] = []
    raw_text: str | None = None     # texto bruto coletado pelo scraper
