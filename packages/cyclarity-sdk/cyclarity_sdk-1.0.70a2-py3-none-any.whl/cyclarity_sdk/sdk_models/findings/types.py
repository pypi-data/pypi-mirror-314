from enum import Enum
from pydantic import BaseModel, Field
''' Test step definitions'''


class RiskModel(BaseModel):
    category: str = Field(description="Risk category")
    level: str = Field(description="Risk level")
    description: str = Field(description="description of the level")
    risk_value: int = Field(description="The score of this risk level")


class FindingModelType(str, Enum):
    PT_FINDING = "pt_finding"


class Expertise(Enum):
    LAYMAN = RiskModel(category="Expertise", level="Layman", description="Attack did not require any skills (eg. It happens always)", risk_value=0)  # noqa
    PROFICIENT = RiskModel(category="Expertise", level="Proficient", description="Can read/write code/scripts. Can operate an OS (mount, create links etc.)",  risk_value=3)  # noqa
    EXPERT = RiskModel(category="Expertise", level="Expert", description="Can do reverse engineering. Can look at sniffing and raw memory and understand it. Can circumvent protections - NX bit, ASLR, etc.", risk_value=6)  # noqa
    SPECIALIST = RiskModel(category="Expertise", level="Specialist", description="Can do advanced niche things - side channel attacks, etc.", risk_value=8)  # noqa


class Access(Enum):
    REMOTE_ACCESS = RiskModel(category="Access", level="Remote Access", description="Remote access without the need for direct access to a vehicle", risk_value=0)  # noqa
    EASY = RiskModel(category="Access", level="Easy", description="Simple direct access to the component - does not require opening the box of the ECU", risk_value=1)  # noqa
    MODERATE = RiskModel(category="Access", level="Moderate", description="Requires access to vehicle parts (access to flash memory inside an ECU) - connection to ecu box / requires openning the box but not advanced soldiering - QFP components. This includes extracting flash (not BGA) memories etc.", risk_value=4)  # noqa
    HARD = RiskModel(category="Access", level="Hard", description="Requires advanced soldiering - BGA components / Anti tamper circumventions / requires control over some component using previous attack. This includes SPI attacks, attack from internal CAN (not obd), attack requiring control over internal elements not controllable by design (such as internal files, configuration, calling parameters of binary), etc.", risk_value=10)  # noqa


class ElapsedTime(Enum):
    HOURS = RiskModel(category="ElapsedTime", level="Hours", description="Very simple attack, very easily found and executed (hours).", risk_value=0)  # noqa
    DAYS = RiskModel(category="ElapsedTime", level="Days", description="Finding this vulnerability + exploiting it takes some time (days).", risk_value=1)  # noqa
    WEEKS = RiskModel(category="ElapsedTime", level="Weeks", description="It takes at least weeks to find/exploit this. Very likely exploitable.", risk_value=3)  # noqa
    MONTHS = RiskModel(category="ElapsedTime", level="Months", description="Causes unexpected behavior, unclear if code even gets there. Likely unexploitable, or exploitable with months of work.", risk_value=7)  # noqa
    DECADES = RiskModel(category="ElapsedTime", level="Decades", description="Not exploitable (currently), but should be fixed (therefore is still a finding)", risk_value=35)  # noqa


class Equipment(Enum):
    STANDARD = RiskModel(category="Equipment", level="Standard", description="Common IT-equipment (e.g., notebook, freely available OBD diagnosis-tools", risk_value=0)  # noqa
    SPECIALIZED = RiskModel(category="Equipment", level="Specialized", description="Professional garage-equipment (CAN-cards, diagnosis-equipment)", risk_value=4)  # noqa
    BESPOKE = RiskModel(category="Equipment", level="Bespoke", description="At least one special tool (e.g., tool only available to OEMs oder tool >50.000 € (e.g., electron microscope))", risk_value=7)  # noqa
    MULTIPLE_BESPOKE = RiskModel(category="Equipment", level="Multiple bespoke", description="Multiple bespoke tools", risk_value=9)  # noqa


class KnowledgeOfTarget(Enum):
    PUBLIC = RiskModel(category="Knowledge of SUD", level="public", description="Can find this problem without firmware (blackbox)", risk_value=0)  # noqa
    INTERNAL = RiskModel(category="Knowledge of SUD", level="Internal", description="Need to get firmware for finding/exploiting this", risk_value=3)  # noqa
    CLASSIFIED = RiskModel(category="Knowledge of SUD", level="Classified", description="Need some classified documentation to find this vulnerability.", risk_value=7)  # noqa
    CONFIDENTIAL = RiskModel(category="Knowledge of SUD", level="Confidential", description="Need protected HSM code to find this vulnerability.", risk_value=11)  # noqa


class FindingStatus(str, Enum):
    FINISHED = "Finished"
    PARTIALLY_PERFORMED = "Partially Performed"
    NOT_PERFORMED = "Not Performed"


class FindingType(str, Enum):
    FINDING = "Finding"
    NON_FINDING = "Non Finding"
    INSIGHT = "Insight"
    ADDITIONAL_INFORMATION = "Additional Information"


class AffectedTechnologies(str, Enum):
    SIGNAL_COMMUNICATION = "Signal Communication"
    SERVICE_COMMUNICATION = "service communication"
    MOBILE_COMMUNICATION = "mobile communication"
    WIRELESS_CHARGING = "wireless charging"
    WIRED_CHARGING = "wired charging"
    USB = "USB"
    WLAN_WiFi = "WLAN/WiFi"
    BLUETOOTH = "Bluetooth"
    NFC = "NFC"
    RADIO_TRANSPORTING = "radio/transporting"
    GPS = "GPS"
    EXTERNAL_DATA_STORAGE = "external data storage"
    PROGRAM_CODE_STORAGE = "program code storage"
    PROGRAM_CODE_EXECUTION = "program code execution"
    ECU_CONFIGURATION = "ECU configuration"
    DATA_STORAGE = "data storage"
    DATA_RECEPTION = "data reception"
    DATA_TRANSMISSION = "data transmission"
    DATA_PROCESSING = "data processing"
    INTERNAL_COMMUNICATION = "internal communication"
    EXTERNAL_COMMUNICATION = "external communication"
    DEBUG_INTERFACE = "Debug-Interface"


class AffectedSecurityGoal(str, Enum):
    DATA_INTEGRITY = "Data Integrity"
    DATA_AUTHENTICITY = "data authenticity"
    DATA_CONFIDENTIALITY = "data confidentiality"
    DATA_AVAILABILITY = "data availability"
    ECU_AUTHENTICITY = "ECU authenticity"
    ECU_INTEGRITY = "ECU integrity"
    ECU_AVAILABILITY = "ECU availability"


class AssessmentTechnique(str, Enum):
    SPEC_BASED_TEST_CASE = "specification-based test case"
    HARDWARE_ANALYSIS = "hardware analysis"
    BINARY_ANALYSIS = "binary analysis"
    INTERFACE_ANALYSIS = "interface analysis"
    NETWORK_ANALYSIS = "network analysis"
    CODE_REVIEW = "code review"
    SPECIFICATION_REVIEW = "specification review"
    CVE_SEARCH = "CVE search"
    OTHER_EXPLORATION = "other exploration"
    UNKNOWN = "unknown"


class AssessmentCategory(str, Enum):
    FUNCTIONAL_TEST = "functional test"
    PENTEST = "pentest"
    VULNERABILITY_ANALYSIS = "vulnerability analysis"
    INCIDENT = "incident"
    CODE_REVIEW = "code review"
    UNKNOWN = "unknown"
