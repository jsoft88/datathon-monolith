from factored_api.models.base import ContractModel
from factored_api.models.chat import ChatRequest, ChatResponse
from factored_api.models.dimensions import Branch, Customer, MarketingCampaign, Product, ServiceAgent
from factored_api.models.facts import (
    CallCenterInteraction,
    CallTranscript,
    CampaignSend,
    Complaint,
    DigitalEvent,
    SatisfactionSurvey,
    Transaction,
)
from factored_api.models.reference import DailyExchangeRate

TABLE_CONTRACTS: dict[str, type[ContractModel]] = {
    "customers": Customer,
    "products": Product,
    "branches": Branch,
    "service_agents": ServiceAgent,
    "marketing_campaigns": MarketingCampaign,
    "transactions": Transaction,
    "call_center_interactions": CallCenterInteraction,
    "call_transcripts": CallTranscript,
    "satisfaction_surveys": SatisfactionSurvey,
    "digital_events": DigitalEvent,
    "complaints": Complaint,
    "campaign_sends": CampaignSend,
    "daily_exchange_rates": DailyExchangeRate,
}

__all__ = [
    "Branch",
    "CallCenterInteraction",
    "CallTranscript",
    "CampaignSend",
    "ChatRequest",
    "ChatResponse",
    "Complaint",
    "ContractModel",
    "Customer",
    "DailyExchangeRate",
    "DigitalEvent",
    "MarketingCampaign",
    "Product",
    "SatisfactionSurvey",
    "ServiceAgent",
    "TABLE_CONTRACTS",
    "Transaction",
]
