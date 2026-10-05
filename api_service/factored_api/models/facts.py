from datetime import date, datetime
from decimal import Decimal

from pydantic import Field

from factored_api.models.base import ContractModel, contract_config
from factored_api.models.enums import (
    Accent,
    AudioQuality,
    CampaignSendChannel,
    CaseType,
    ComplaintStatus,
    Currency,
    DigitalChannel,
    DigitalEventCategory,
    DigitalEventType,
    InteractionChannel,
    InteractionType,
    NpsCategory,
    Platform,
    Priority,
    ReasonCategory,
    ReceptionChannel,
    SendStatus,
    Sentiment,
    SurveySendChannel,
    SurveyType,
    TransactionCategory,
    TransactionChannel,
    TransactionStatus,
    TransactionType,
)


class Transaction(ContractModel):
    """Daily financial transactions."""

    model_config = contract_config(
        "transactions",
        kind="fact",
        source="Core Banking",
        partition="daily",
        primary_key=["transaction_id"],
        foreign_keys={
            "product_id": "products.product_id",
            "customer_id": "customers.customer_id",
            "branch_id": "branches.branch_id",
        },
    )

    transaction_id: str = Field(..., max_length=30, description="Unique transaction ID")
    transaction_date: datetime = Field(..., description="Transaction date and time")
    process_date: date = Field(..., description="Process date (partition key)")
    product_id: str = Field(..., max_length=20, description="Product ID")
    customer_id: str = Field(..., max_length=20, description="Customer ID")
    transaction_type: TransactionType = Field(..., description="Type (Deposit, Withdrawal, Transfer, Payment, Purchase, Adjustment)")
    transaction_category: TransactionCategory | None = Field(
        default=None,
        description="Category (Food, Transport, Services, Entertainment, Health, Other)",
    )
    amount: Decimal = Field(..., max_digits=15, decimal_places=2, description="Transaction amount")
    currency: Currency = Field(..., description="Currency")
    amount_usd: Decimal | None = Field(
        default=None,
        max_digits=15,
        decimal_places=2,
        description="Amount converted to USD",
    )
    channel: TransactionChannel = Field(..., description="Channel (ATM, Branch, Web, App, POS, Transfer)")
    branch_id: str | None = Field(default=None, max_length=20, description="Branch ID (if applicable)")
    merchant_name: str | None = Field(default=None, max_length=150, description="Merchant name (for purchases)")
    merchant_category: str | None = Field(default=None, max_length=50, description="MCC merchant category")
    transaction_country: str = Field(..., max_length=50, description="Country where transaction occurred")
    transaction_city: str | None = Field(default=None, max_length=100, description="City where transaction occurred")
    transaction_status: TransactionStatus = Field(
        ...,
        description="Status (Approved, Declined, Pending, Reversed)",
    )
    response_code: str | None = Field(default=None, max_length=10, description="System response code")
    is_fraud: bool = Field(..., description="Marked as fraud")
    fraud_score: Decimal | None = Field(
        default=None,
        max_digits=5,
        decimal_places=2,
        ge=0,
        le=100,
        description="Fraud risk score (0-100)",
    )
    latitude: Decimal | None = Field(
        default=None,
        max_digits=10,
        decimal_places=7,
        description="Transaction latitude",
    )
    longitude: Decimal | None = Field(
        default=None,
        max_digits=10,
        decimal_places=7,
        description="Transaction longitude",
    )


class CallCenterInteraction(ContractModel):
    """Call center interactions with customers."""

    model_config = contract_config(
        "call_center_interactions",
        kind="fact",
        source="Contact Center",
        partition="daily",
        primary_key=["interaction_id"],
        foreign_keys={
            "customer_id": "customers.customer_id",
            "agent_id": "service_agents.agent_id",
        },
    )

    interaction_id: str = Field(..., max_length=30, description="Unique interaction ID")
    interaction_date: datetime = Field(..., description="Interaction date and time")
    process_date: date = Field(..., description="Process date (partition key)")
    customer_id: str = Field(..., max_length=20, description="Customer ID")
    agent_id: str | None = Field(default=None, max_length=20, description="Agent ID who attended")
    interaction_type: InteractionType = Field(
        ...,
        description="Type (Inbound Call, Outbound Call, Chat, Email, Video)",
    )
    channel: InteractionChannel = Field(..., description="Channel (Phone, Web Chat, WhatsApp, Email, App)")
    contact_reason: str = Field(..., max_length=100, description="Main contact reason")
    reason_category: ReasonCategory = Field(
        ...,
        description="Category (Transactional, Product, Technical, Commercial, Complaint)",
    )
    duration_seconds: int | None = Field(default=None, ge=0, description="Duration in seconds")
    wait_time_seconds: int | None = Field(default=None, ge=0, description="Wait time before service")
    was_resolved: bool | None = Field(default=None, description="Resolved on first call (FCR)")
    requires_followup: bool = Field(..., description="Requires follow-up")
    detected_sentiment: Sentiment | None = Field(
        default=None,
        description="Sentiment (Positive, Neutral, Negative, Very Negative)",
    )
    sentiment_score: Decimal | None = Field(
        default=None,
        max_digits=3,
        decimal_places=2,
        ge=-1,
        le=1,
        description="Sentiment score (-1 to 1)",
    )
    customer_detected_accent: Accent | None = Field(default=None, description="Customer's detected accent")
    agent_used_accent: Accent | None = Field(default=None, description="Accent used by agent in response")
    was_escalated: bool = Field(..., description="Was escalated to supervisor")
    mentioned_products: str | None = Field(
        default=None,
        max_length=200,
        description="Product IDs mentioned (comma-separated)",
    )
    has_transcript: bool = Field(..., description="Has transcript available")
    has_recording: bool = Field(..., description="Has audio recording")


class CallTranscript(ContractModel):
    """Call center call transcripts."""

    model_config = contract_config(
        "call_transcripts",
        kind="fact",
        source="Contact Center",
        partition="daily",
        primary_key=["transcript_id"],
        foreign_keys={
            "interaction_id": "call_center_interactions.interaction_id",
            "customer_id": "customers.customer_id",
            "agent_id": "service_agents.agent_id",
        },
    )

    transcript_id: str = Field(..., max_length=30, description="Unique transcript ID")
    interaction_id: str = Field(..., max_length=30, description="Related interaction ID")
    process_date: date = Field(..., description="Process date (partition key)")
    customer_id: str = Field(..., max_length=20, description="Customer ID")
    agent_id: str = Field(..., max_length=20, description="Agent ID")
    full_text: str = Field(..., description="Full call transcript (in Spanish)")
    customer_text: str | None = Field(default=None, description="Only what customer said (in Spanish)")
    agent_text: str | None = Field(default=None, description="Only what agent said (in Spanish)")
    detected_language: str = Field(..., max_length=10, description="Main language detected")
    detected_accent: Accent | None = Field(default=None, description="Detected accent")
    accent_confidence: Decimal | None = Field(
        default=None,
        max_digits=3,
        decimal_places=2,
        ge=0,
        le=1,
        description="Accent detection confidence (0-1)",
    )
    detected_keywords: str | None = Field(default=None, max_length=500, description="Identified keywords")
    mentioned_entities: str | None = Field(default=None, description="Extracted entities (JSON)")
    detected_intents: str | None = Field(default=None, max_length=300, description="Identified intents")
    main_topics: str | None = Field(default=None, max_length=300, description="Main conversation topics")
    transcription_model: str = Field(..., max_length=50, description="Model used (Whisper, Google STT, etc.)")
    audio_quality: AudioQuality | None = Field(default=None, description="Audio quality (High, Medium, Low)")
    duration_seconds: int = Field(..., ge=0, description="Call duration")


class SatisfactionSurvey(ContractModel):
    """Post-interaction satisfaction surveys (CSAT, NPS)."""

    model_config = contract_config(
        "satisfaction_surveys",
        kind="fact",
        source="Contact Center",
        partition="daily",
        primary_key=["survey_id"],
        foreign_keys={
            "interaction_id": "call_center_interactions.interaction_id",
            "customer_id": "customers.customer_id",
            "agent_id": "service_agents.agent_id",
        },
    )

    survey_id: str = Field(..., max_length=30, description="Unique survey ID")
    survey_date: datetime = Field(..., description="Response date and time")
    process_date: date = Field(..., description="Process date (partition key)")
    interaction_id: str | None = Field(default=None, max_length=30, description="Evaluated interaction ID")
    customer_id: str = Field(..., max_length=20, description="Customer ID")
    agent_id: str | None = Field(default=None, max_length=20, description="Evaluated agent ID")
    survey_type: SurveyType = Field(..., description="Type (CSAT, NPS, CES)")
    send_channel: SurveySendChannel = Field(..., description="Send channel (Email, SMS, IVR, App, Web)")
    main_score: int = Field(..., ge=0, le=10, description="Main score (1-5 for CSAT, 0-10 for NPS)")
    nps_category: NpsCategory | None = Field(
        default=None,
        description="NPS category (Promoter, Passive, Detractor)",
    )
    question_1_text: str | None = Field(default=None, description="Question 1 text")
    question_1_response: int | None = Field(default=None, ge=1, le=5, description="Question 1 response (1-5)")
    question_2_text: str | None = Field(default=None, description="Question 2 text")
    question_2_response: int | None = Field(default=None, ge=1, le=5, description="Question 2 response (1-5)")
    question_3_text: str | None = Field(default=None, description="Question 3 text")
    question_3_response: int | None = Field(default=None, ge=1, le=5, description="Question 3 response (1-5)")
    open_comments: str | None = Field(default=None, description="Customer comments (in Spanish)")
    comment_sentiment: str | None = Field(default=None, max_length=20, description="Comment sentiment")
    response_time_hours: Decimal | None = Field(
        default=None,
        max_digits=8,
        decimal_places=2,
        ge=0,
        description="Hours between interaction and response",
    )
    campaign_response_rate: Decimal | None = Field(
        default=None,
        max_digits=5,
        decimal_places=2,
        description="Campaign response rate (%)",
    )


class DigitalEvent(ContractModel):
    """Digital channel interaction events (mobile app, web)."""

    model_config = contract_config(
        "digital_events",
        kind="fact",
        source="Digital Banking",
        partition="daily",
        primary_key=["event_id"],
        foreign_keys={
            "customer_id": "customers.customer_id",
            "product_id": "products.product_id",
        },
    )

    event_id: str = Field(..., max_length=30, description="Unique event ID")
    event_date: datetime = Field(..., description="Event date and time")
    process_date: date = Field(..., description="Process date (partition key)")
    customer_id: str | None = Field(default=None, max_length=20, description="Customer ID")
    session_id: str = Field(..., max_length=50, description="User session ID")
    event_type: DigitalEventType = Field(
        ...,
        description="Type (PageView, Click, FormSubmit, Login, Logout, Error, Purchase)",
    )
    event_category: DigitalEventCategory = Field(
        ...,
        description="Category (Navigation, Transaction, Authentication, Product)",
    )
    channel: DigitalChannel = Field(
        ...,
        description="Channel (Android App, iOS App, Desktop Web, Mobile Web)",
    )
    platform: Platform | None = Field(
        default=None,
        description="Platform (Android, iOS, Windows, MacOS, Linux)",
    )
    browser: str | None = Field(default=None, max_length=50, description="Browser used")
    app_version: str | None = Field(default=None, max_length=20, description="App version")
    page_url: str | None = Field(default=None, max_length=300, description="Page URL")
    page_title: str | None = Field(default=None, max_length=200, description="Page title")
    action: str | None = Field(default=None, max_length=100, description="Action performed")
    element_id: str | None = Field(default=None, max_length=100, description="Interacted element ID")
    product_id: str | None = Field(default=None, max_length=20, description="Related product ID")
    event_value: Decimal | None = Field(
        default=None,
        max_digits=15,
        decimal_places=2,
        description="Event monetary value (if applicable)",
    )
    duration_seconds: int | None = Field(default=None, ge=0, description="Event duration")
    ip_address: str | None = Field(default=None, max_length=45, description="User IP address")
    ip_country: str | None = Field(default=None, max_length=50, description="Country detected by IP")
    ip_city: str | None = Field(default=None, max_length=100, description="City detected by IP")
    is_mobile: bool = Field(..., description="Event from mobile device")
    referrer: str | None = Field(default=None, max_length=300, description="Referrer URL")
    utm_source: str | None = Field(default=None, max_length=100, description="UTM source")
    utm_medium: str | None = Field(default=None, max_length=100, description="UTM medium")
    utm_campaign: str | None = Field(default=None, max_length=100, description="UTM campaign")


class Complaint(ContractModel):
    """Complaints and claims system (PQR)."""

    model_config = contract_config(
        "complaints",
        kind="fact",
        source="PQR",
        partition="daily",
        primary_key=["complaint_id"],
        foreign_keys={
            "customer_id": "customers.customer_id",
            "affected_product_id": "products.product_id",
            "related_branch_id": "branches.branch_id",
            "origin_interaction_id": "call_center_interactions.interaction_id",
            "assigned_agent_id": "service_agents.agent_id",
        },
    )

    complaint_id: str = Field(..., max_length=30, description="Unique complaint/claim ID")
    creation_date: datetime = Field(..., description="Complaint creation date")
    process_date: date = Field(..., description="Process date (partition key)")
    customer_id: str = Field(..., max_length=20, description="Customer ID")
    case_type: CaseType = Field(..., description="Type (Complaint, Claim, Request, Suggestion)")
    category: str = Field(..., max_length=100, description="Case category")
    subcategory: str | None = Field(default=None, max_length=100, description="Subcategory")
    reception_channel: ReceptionChannel = Field(
        ...,
        description="Channel (Call Center, Email, Web, App, Branch, Regulator)",
    )
    affected_product_id: str | None = Field(default=None, max_length=20, description="Affected product ID")
    related_branch_id: str | None = Field(default=None, max_length=20, description="Related branch ID")
    origin_interaction_id: str | None = Field(default=None, max_length=30, description="Originating interaction ID")
    description: str = Field(..., description="Case description (in Spanish)")
    claimed_amount: Decimal | None = Field(
        default=None,
        max_digits=15,
        decimal_places=2,
        description="Claimed amount (if applicable)",
    )
    currency: Currency | None = Field(default=None, description="Claimed amount currency")
    priority: Priority = Field(..., description="Priority (Low, Medium, High, Critical)")
    status: ComplaintStatus = Field(
        ...,
        description="Status (Open, In Process, Escalated, Resolved, Closed, Rejected)",
    )
    assigned_agent_id: str | None = Field(default=None, max_length=20, description="Assigned agent ID")
    assignment_date: datetime | None = Field(default=None, description="Assignment date")
    first_response_date: datetime | None = Field(default=None, description="First response date")
    resolution_date: datetime | None = Field(default=None, description="Resolution date")
    closing_date: datetime | None = Field(default=None, description="Closing date")
    sla_breached: bool = Field(..., description="SLA breached")
    resolution_days: int | None = Field(default=None, ge=0, description="Days to resolution")
    resolution: str | None = Field(default=None, description="Resolution description (in Spanish)")
    compensation_granted: Decimal | None = Field(
        default=None,
        max_digits=15,
        decimal_places=2,
        description="Compensation amount granted",
    )
    resolution_satisfaction: int | None = Field(
        default=None,
        ge=1,
        le=5,
        description="Resolution satisfaction score (1-5)",
    )
    is_repeat_complainer: bool = Field(..., description="Customer with previous complaints in last 90 days")


class CampaignSend(ContractModel):
    """Individual marketing campaign sends."""

    model_config = contract_config(
        "campaign_sends",
        kind="fact",
        source="Internal",
        partition="daily",
        primary_key=["send_id"],
        foreign_keys={
            "campaign_id": "marketing_campaigns.campaign_id",
            "customer_id": "customers.customer_id",
        },
    )

    send_id: str = Field(..., max_length=30, description="Unique send ID")
    send_date: datetime = Field(..., description="Send date and time")
    process_date: date = Field(..., description="Process date (partition key)")
    campaign_id: str = Field(..., max_length=20, description="Campaign ID")
    customer_id: str = Field(..., max_length=20, description="Recipient customer ID")
    send_channel: CampaignSendChannel = Field(..., description="Channel (Email, SMS, Push, WhatsApp, Voice)")
    template_used: str | None = Field(default=None, max_length=100, description="Template used")
    subject: str | None = Field(default=None, max_length=200, description="Message subject")
    send_status: SendStatus = Field(..., description="Status (Sent, Failed, Bounced, Blocked)")
    was_delivered: bool = Field(..., description="Was delivered successfully")
    was_opened: bool | None = Field(default=None, description="Was opened/read")
    open_date: datetime | None = Field(default=None, description="Open date")
    was_clicked: bool | None = Field(default=None, description="Clicked on any link")
    click_date: datetime | None = Field(default=None, description="First click date")
    click_count: int | None = Field(default=None, ge=0, description="Total click count")
    had_conversion: bool = Field(..., description="Converted (completed desired action)")
    conversion_date: datetime | None = Field(default=None, description="Conversion date")
    conversion_value: Decimal | None = Field(
        default=None,
        max_digits=15,
        decimal_places=2,
        description="Conversion monetary value",
    )
    open_device: str | None = Field(default=None, max_length=30, description="Device used to open")
    open_country: str | None = Field(default=None, max_length=50, description="Country where opened")
    failure_reason: str | None = Field(default=None, max_length=200, description="Failure reason (if applicable)")
    send_cost: Decimal | None = Field(
        default=None,
        max_digits=10,
        decimal_places=4,
        description="Individual send cost",
    )
