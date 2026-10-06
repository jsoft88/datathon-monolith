from datetime import date, datetime, time
from decimal import Decimal

from pydantic import Field

from factored_api.models.base import ContractModel, contract_config
from factored_api.models.enums import (
    Accent,
    AgentStatus,
    AgentType,
    BranchStatus,
    BranchType,
    CampaignObjective,
    CampaignStatus,
    CampaignType,
    Country,
    Currency,
    CustomerSegment,
    CustomerStatus,
    DocumentType,
    ExperienceLevel,
    Gender,
    GeographicZone,
    NativeAccent,
    OpeningChannel,
    ProductStatus,
    ProductType,
    WorkShift,
)


class Customer(ContractModel):
    """Bank customer dimension table."""

    model_config = contract_config(
        "customers",
        kind="dimension",
        source="Core Banking",
        partition="monthly_snapshot",
        primary_key=["customer_id"],
        unique=["document_number"],
        foreign_keys={"registration_branch_id": "branches.branch_id"},
    )

    customer_id: str = Field(..., max_length=20, description="Unique customer ID")
    document_number: str = Field(..., max_length=20, description="Identity document number")
    document_type: DocumentType = Field(..., description="Document type (DNI, CURP, CC, CE, Passport)")
    first_name: str = Field(..., max_length=100, description="Customer first name (in Spanish)")
    last_name: str = Field(..., max_length=100, description="Customer last name (in Spanish)")
    date_of_birth: date = Field(..., description="Date of birth")
    gender: Gender | None = Field(default=None, description="Gender (M, F, O)")
    email: str | None = Field(default=None, max_length=100, description="Email address")
    mobile_phone: str | None = Field(default=None, max_length=20, description="Mobile phone number")
    landline_phone: str | None = Field(default=None, max_length=20, description="Landline phone number")
    address: str | None = Field(default=None, max_length=200, description="Full address (in Spanish)")
    city: str = Field(..., max_length=100, description="City of residence")
    state: str = Field(..., max_length=100, description="State/Province")
    country: Country = Field(..., description="Country (Mexico, Colombia, Argentina)")
    postal_code: str | None = Field(default=None, max_length=10, description="Postal code")
    detected_accent: Accent | None = Field(
        default=None,
        description="Spanish accent detected (mexican, colombian, argentine, neutral)",
    )
    segment: CustomerSegment = Field(..., description="Customer segment (Premium, Plus, Basic, Student)")
    credit_score: int | None = Field(default=None, ge=300, le=850, description="Credit score (300-850)")
    estimated_monthly_income: Decimal | None = Field(
        default=None,
        max_digits=12,
        decimal_places=2,
        description="Estimated monthly income in local currency",
    )
    occupation: str | None = Field(default=None, max_length=100, description="Customer occupation")
    marital_status: str | None = Field(default=None, max_length=20, description="Marital status")
    education_level: str | None = Field(default=None, max_length=50, description="Education level")
    registration_date: datetime = Field(..., description="Registration date as customer")
    # registration_branch_id: str = Field(..., max_length=20, description="Branch ID where registered")
    customer_status: CustomerStatus = Field(
        ...,
        description="Status (Active, Inactive, Suspended, Closed)",
    )
    last_updated: datetime = Field(..., description="Last record update")
    accepts_marketing: bool = Field(..., description="Accepts marketing communications")


class Product(ContractModel):
    """Active financial products of customers."""

    model_config = contract_config(
        "products",
        kind="dimension",
        source="Core Banking",
        partition="monthly_snapshot",
        primary_key=["product_id"],
        unique=["product_number"],
        foreign_keys={
            "customer_id": "customers.customer_id",
            "opening_branch_id": "branches.branch_id",
        },
    )

    product_id: str = Field(..., max_length=20, description="Unique product ID")
    customer_id: str = Field(..., max_length=20, description="Owner customer ID")
    product_type: ProductType = Field(..., description="Product type")
    product_number: str = Field(..., max_length=30, description="Account/card/policy number")
    currency: Currency = Field(..., description="Currency (MXN, COP, ARS, USD)")
    current_balance: Decimal = Field(..., max_digits=15, decimal_places=2, description="Current balance")
    credit_limit: Decimal | None = Field(
        default=None,
        max_digits=15,
        decimal_places=2,
        description="Credit limit (for credit products)",
    )
    interest_rate: Decimal | None = Field(
        default=None,
        max_digits=5,
        decimal_places=2,
        description="Annual interest rate (%)",
    )
    opening_date: date = Field(..., description="Product opening date")
    expiration_date: date | None = Field(default=None, description="Expiration date (for term products)")
    opening_branch_id: str = Field(..., max_length=20, description="Branch where opened")
    product_status: ProductStatus = Field(
        ...,
        description="Status (Active, Blocked, Closed, Suspended)",
    )
    opening_channel: OpeningChannel = Field(
        ...,
        description="Opening channel (Branch, Web, App, Call Center)",
    )
    has_linked_app: bool = Field(..., description="Product linked to mobile app")
    days_past_due: int | None = Field(default=None, ge=0, description="Days past due (for credits)")
    last_transaction_date: datetime | None = Field(default=None, description="Last transaction date")
    last_updated: datetime = Field(..., description="Last record update")


class Branch(ContractModel):
    """Physical bank branches."""

    model_config = contract_config(
        "branches",
        kind="dimension",
        source="Internal",
        partition="full_snapshot",
        primary_key=["branch_id"],
        unique=["branch_code"],
    )

    branch_id: str = Field(..., max_length=20, description="Unique branch ID")
    branch_code: str = Field(..., max_length=10, description="Internal branch code")
    branch_name: str = Field(..., max_length=100, description="Branch name")
    branch_type: BranchType = Field(..., description="Type (Main, Express, Premium, Corporate)")
    address: str = Field(..., max_length=200, description="Full address (in Spanish)")
    city: str = Field(..., max_length=100, description="City")
    state: str = Field(..., max_length=100, description="State/Province")
    country: Country = Field(..., description="Country")
    postal_code: str | None = Field(default=None, max_length=10, description="Postal code")
    geographic_zone: GeographicZone = Field(..., description="Zone (Urban, Suburban, Rural)")
    phone: str = Field(..., max_length=20, description="Contact phone")
    email: str | None = Field(default=None, max_length=100, description="Branch email")
    opening_time: time = Field(..., description="Opening time")
    closing_time: time = Field(..., description="Closing time")
    has_atms: bool = Field(..., description="Has ATMs")
    atm_count: int | None = Field(default=None, ge=0, description="Number of ATMs")
    has_teller_windows: bool = Field(..., description="Has teller windows")
    teller_window_count: int | None = Field(default=None, ge=0, description="Number of teller windows")
    latitude: Decimal | None = Field(
        default=None,
        max_digits=10,
        decimal_places=7,
        description="Geographic latitude",
    )
    longitude: Decimal | None = Field(
        default=None,
        max_digits=10,
        decimal_places=7,
        description="Geographic longitude",
    )
    branch_opening_date: date = Field(..., description="Branch opening date")
    branch_status: BranchStatus = Field(
        ...,
        description="Status (Active, Temporarily Closed, Closed)",
    )


class ServiceAgent(ContractModel):
    """Customer service agents."""

    model_config = contract_config(
        "service_agents",
        kind="dimension",
        source="Internal",
        partition="monthly_snapshot",
        primary_key=["agent_id"],
        unique=["employee_code"],
        foreign_keys={"assigned_branch_id": "branches.branch_id"},
    )

    agent_id: str = Field(..., max_length=20, description="Unique agent ID")
    employee_code: str = Field(..., max_length=15, description="Employee code")
    first_name: str = Field(..., max_length=100, description="Agent first name (in Spanish)")
    last_name: str = Field(..., max_length=100, description="Agent last name (in Spanish)")
    email: str = Field(..., max_length=100, description="Corporate email")
    phone: str | None = Field(default=None, max_length=20, description="Contact phone")
    native_accent: NativeAccent = Field(
        ...,
        description="Native Spanish accent (mexican, colombian, argentine)",
    )
    country_of_origin: Country = Field(..., description="Country of origin")
    assigned_branch_id: str | None = Field(default=None, max_length=20, description="Assigned branch")
    agent_type: AgentType = Field(..., description="Type (Phone, In-Person, Digital, Hybrid)")
    experience_level: ExperienceLevel = Field(
        ...,
        description="Level (Junior, Mid-Senior, Senior, Specialist)",
    )
    languages: str = Field(..., max_length=100, description="Languages spoken")
    specialty: str | None = Field(default=None, max_length=100, description="Specialty")
    hire_date: date = Field(..., description="Hire date")
    avg_csat: Decimal | None = Field(
        default=None,
        max_digits=3,
        decimal_places=2,
        ge=1,
        le=5,
        description="Average CSAT score (1-5)",
    )
    total_monthly_interactions: int | None = Field(
        default=None,
        ge=0,
        description="Total interactions in last month",
    )
    agent_status: AgentStatus = Field(
        ...,
        description="Status (Active, Vacation, Leave, Inactive)",
    )
    work_shift: WorkShift = Field(..., description="Shift (Morning, Afternoon, Night, Rotating)")


class MarketingCampaign(ContractModel):
    """Bank marketing campaigns."""

    model_config = contract_config(
        "marketing_campaigns",
        kind="dimension",
        source="Internal",
        partition="full_snapshot",
        primary_key=["campaign_id"],
    )

    campaign_id: str = Field(..., max_length=20, description="Unique campaign ID")
    campaign_name: str = Field(..., max_length=150, description="Campaign name")
    description: str | None = Field(default=None, description="Campaign description")
    campaign_type: CampaignType = Field(
        ...,
        description="Type (Email, SMS, Push, WhatsApp, Voice, Mix)",
    )
    campaign_objective: CampaignObjective = Field(
        ...,
        description="Objective (Acquisition, Retention, Cross-sell, Up-sell, Reactivation)",
    )
    promoted_product: str | None = Field(default=None, max_length=50, description="Promoted product")
    target_segment: str | None = Field(default=None, max_length=50, description="Target segment")
    target_country: Country | None = Field(default=None, description="Target country")
    start_date: date = Field(..., description="Start date")
    end_date: date = Field(..., description="End date")
    budget: Decimal | None = Field(
        default=None,
        max_digits=12,
        decimal_places=2,
        description="Assigned budget",
    )
    campaign_status: CampaignStatus = Field(
        ...,
        description="Status (Planned, Active, Paused, Completed)",
    )
    expected_conversion_rate: Decimal | None = Field(
        default=None,
        max_digits=5,
        decimal_places=2,
        description="Expected conversion rate (%)",
    )
