from typing import Any

from celery import shared_task
from django.contrib.contenttypes.models import ContentType
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field
from wbcore.contrib.ai.exceptions import APIStatusErrors
from wbcore.contrib.ai.llm.utils import run_llm


class CompanyModel(BaseModel):
    name: str = Field(..., description="The name of the publicly listed company.")
    isin: str | None = Field(..., description="The ISIN of the publicly listed company. May be null if not available.")
    ticker: str | None = Field(
        ..., description="The ticker of the publicly listed company. May be null if not available."
    )
    refinitiv_identifier_code: str | None = Field(
        ..., description="The RIC of the publicly listed company. May be null if not available."
    )
    sentiment: int = Field(
        ...,
        ge=1,
        le=4,
        description="The sentiment of the news article towards the company. 1 is negative, 2 is neutral, 3 is positive, 4 is very positive.",
    )
    analysis: str = Field(
        ...,
        description="The analysis of the news article towards the company. This should include an explanation of the sentiment.",
    )


class CompaniesModel(BaseModel):
    companies: list[CompanyModel] = Field(
        default=[], description="The list of companies mentioned in the news article."
    )


@shared_task(
    autoretry_for=tuple(APIStatusErrors),
    retry_backoff=10,
    max_retries=5,  # retry i5 times maximum
    default_retry_delay=30,  # retry in 30s
    retry_jitter=False,
)
def run_company_extraction_llm(title: str, description: str, *args) -> list[dict[str, Any]]:
    from wbfdm.import_export.handlers.instrument import InstrumentLookup
    from wbfdm.models import Instrument

    res = run_llm(
        prompt=[
            SystemMessage(
                content="You will be parsed a news article, please provide the name of the publicly listed companies mentioned in the article, along with their ISIN, ticker, RIC, sentiment, and analysis."
            ),
            HumanMessage(content=f"Title: {title}, Description: {description}"),
        ],
        output_model=CompaniesModel,
    )
    relationships = []
    instrument_ct = ContentType.objects.get_for_model(Instrument)
    for company in res.get("companies", []):
        instrument = InstrumentLookup(Instrument).lookup(
            only_security=True,
            name=company.name,
            isin=company.isin,
            ticker=company.ticker,
            refinitiv_identifier_code=company.refinitiv_identifier_code,
        )
        if instrument is not None:
            relationships.append(
                {
                    "content_type_id": instrument_ct.id,
                    "object_id": instrument.get_root().id,
                    "sentiment": company.sentiment,
                    "analysis": company.analysis,
                }
            )

    return relationships
