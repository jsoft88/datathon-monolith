from enum import Enum


class Country(str, Enum):
    MEXICO = "Mexico"
    COLOMBIA = "Colombia"
    ARGENTINA = "Argentina"


class Currency(str, Enum):
    MXN = "MXN"
    COP = "COP"
    ARS = "ARS"
    USD = "USD"


class Gender(str, Enum):
    M = "M"
    F = "F"
    O = "O"


class DocumentType(str, Enum):
    DNI = "DNI"
    CURP = "CURP"
    CC = "CC"
    CE = "CE"
    PASSPORT = "Passport"


class Accent(str, Enum):
    MEXICAN = "mexican"
    COLOMBIAN = "colombian"
    ARGENTINE = "argentine"
    NEUTRAL = "neutral"


class NativeAccent(str, Enum):
    MEXICAN = "mexican"
    COLOMBIAN = "colombian"
    ARGENTINE = "argentine"


class CustomerSegment(str, Enum):
    PREMIUM = "Premium"
    PLUS = "Plus"
    BASIC = "Basic"
    STUDENT = "Student"


class CustomerStatus(str, Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    SUSPENDED = "Suspended"
    CLOSED = "Closed"


class ProductType(str, Enum):
    CHECKING_ACCOUNT = "Checking Account"
    SAVINGS_ACCOUNT = "Savings Account"
    CREDIT_CARD = "Credit Card"
    DEBIT_CARD = "Debit Card"
    PERSONAL_LOAN = "Personal Loan"
    MORTGAGE = "Mortgage"
    INVESTMENT = "Investment"
    INSURANCE = "Insurance"


class ProductStatus(str, Enum):
    ACTIVE = "Active"
    BLOCKED = "Blocked"
    CLOSED = "Closed"
    SUSPENDED = "Suspended"


class OpeningChannel(str, Enum):
    BRANCH = "Branch"
    WEB = "Web"
    APP = "App"
    CALL_CENTER = "Call Center"


class BranchType(str, Enum):
    MAIN = "Main"
    EXPRESS = "Express"
    PREMIUM = "Premium"
    CORPORATE = "Corporate"


class GeographicZone(str, Enum):
    URBAN = "Urban"
    SUBURBAN = "Suburban"
    RURAL = "Rural"


class BranchStatus(str, Enum):
    ACTIVE = "Active"
    TEMPORARILY_CLOSED = "Temporarily Closed"
    CLOSED = "Closed"


class AgentType(str, Enum):
    PHONE = "Phone"
    IN_PERSON = "In-Person"
    DIGITAL = "Digital"
    HYBRID = "Hybrid"


class ExperienceLevel(str, Enum):
    JUNIOR = "Junior"
    MID_SENIOR = "Mid-Senior"
    SENIOR = "Senior"
    SPECIALIST = "Specialist"


class AgentStatus(str, Enum):
    ACTIVE = "Active"
    VACATION = "Vacation"
    LEAVE = "Leave"
    INACTIVE = "Inactive"


class WorkShift(str, Enum):
    MORNING = "Morning"
    AFTERNOON = "Afternoon"
    NIGHT = "Night"
    ROTATING = "Rotating"


class CampaignType(str, Enum):
    EMAIL = "Email"
    SMS = "SMS"
    PUSH = "Push"
    WHATSAPP = "WhatsApp"
    VOICE = "Voice"
    MIX = "Mix"


class CampaignObjective(str, Enum):
    ACQUISITION = "Acquisition"
    RETENTION = "Retention"
    CROSS_SELL = "Cross-sell"
    UP_SELL = "Up-sell"
    REACTIVATION = "Reactivation"


class CampaignStatus(str, Enum):
    PLANNED = "Planned"
    ACTIVE = "Active"
    PAUSED = "Paused"
    COMPLETED = "Completed"


class TransactionType(str, Enum):
    DEPOSIT = "Deposit"
    WITHDRAWAL = "Withdrawal"
    TRANSFER = "Transfer"
    PAYMENT = "Payment"
    PURCHASE = "Purchase"
    ADJUSTMENT = "Adjustment"


class TransactionCategory(str, Enum):
    FOOD = "Food"
    TRANSPORT = "Transport"
    SERVICES = "Services"
    ENTERTAINMENT = "Entertainment"
    HEALTH = "Health"
    OTHER = "Other"


class TransactionChannel(str, Enum):
    ATM = "ATM"
    BRANCH = "Branch"
    WEB = "Web"
    APP = "App"
    POS = "POS"
    TRANSFER = "Transfer"


class TransactionStatus(str, Enum):
    APPROVED = "Approved"
    DECLINED = "Declined"
    PENDING = "Pending"
    REVERSED = "Reversed"


class InteractionType(str, Enum):
    INBOUND_CALL = "Inbound Call"
    OUTBOUND_CALL = "Outbound Call"
    CHAT = "Chat"
    EMAIL = "Email"
    VIDEO = "Video"


class InteractionChannel(str, Enum):
    PHONE = "Phone"
    WEB_CHAT = "Web Chat"
    WHATSAPP = "WhatsApp"
    EMAIL = "Email"
    APP = "App"


class ReasonCategory(str, Enum):
    TRANSACTIONAL = "Transactional"
    PRODUCT = "Product"
    TECHNICAL = "Technical"
    COMMERCIAL = "Commercial"
    COMPLAINT = "Complaint"


class Sentiment(str, Enum):
    POSITIVE = "Positive"
    NEUTRAL = "Neutral"
    NEGATIVE = "Negative"
    VERY_NEGATIVE = "Very Negative"


class AudioQuality(str, Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class SurveyType(str, Enum):
    CSAT = "CSAT"
    NPS = "NPS"
    CES = "CES"


class SurveySendChannel(str, Enum):
    EMAIL = "Email"
    SMS = "SMS"
    IVR = "IVR"
    APP = "App"
    WEB = "Web"


class NpsCategory(str, Enum):
    PROMOTER = "Promoter"
    PASSIVE = "Passive"
    DETRACTOR = "Detractor"


class DigitalEventType(str, Enum):
    PAGE_VIEW = "PageView"
    CLICK = "Click"
    FORM_SUBMIT = "FormSubmit"
    LOGIN = "Login"
    LOGOUT = "Logout"
    ERROR = "Error"
    PURCHASE = "Purchase"


class DigitalEventCategory(str, Enum):
    NAVIGATION = "Navigation"
    TRANSACTION = "Transaction"
    AUTHENTICATION = "Authentication"
    PRODUCT = "Product"


class DigitalChannel(str, Enum):
    ANDROID_APP = "Android App"
    IOS_APP = "iOS App"
    DESKTOP_WEB = "Desktop Web"
    MOBILE_WEB = "Mobile Web"


class Platform(str, Enum):
    ANDROID = "Android"
    IOS = "iOS"
    WINDOWS = "Windows"
    MACOS = "MacOS"
    LINUX = "Linux"


class CaseType(str, Enum):
    COMPLAINT = "Complaint"
    CLAIM = "Claim"
    REQUEST = "Request"
    SUGGESTION = "Suggestion"


class ReceptionChannel(str, Enum):
    CALL_CENTER = "Call Center"
    EMAIL = "Email"
    WEB = "Web"
    APP = "App"
    BRANCH = "Branch"
    REGULATOR = "Regulator"


class Priority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class ComplaintStatus(str, Enum):
    OPEN = "Open"
    IN_PROCESS = "In Process"
    ESCALATED = "Escalated"
    RESOLVED = "Resolved"
    CLOSED = "Closed"
    REJECTED = "Rejected"


class CampaignSendChannel(str, Enum):
    EMAIL = "Email"
    SMS = "SMS"
    PUSH = "Push"
    WHATSAPP = "WhatsApp"
    VOICE = "Voice"


class SendStatus(str, Enum):
    SENT = "Sent"
    FAILED = "Failed"
    BOUNCED = "Bounced"
    BLOCKED = "Blocked"
