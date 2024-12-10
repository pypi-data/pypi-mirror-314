from pydantic import BaseModel, Field, computed_field, field_validator
from enum import Enum
from .types import FindingStatus, FindingType, AssessmentCategory, AssessmentTechnique, Expertise, Access, ElapsedTime, \
    Equipment, KnowledgeOfTarget, FindingModelType, RiskModel  # noqa
from cyclarity_sdk.sdk_models import ExecutionMetadata, MessageType
from cwe2.database import Database as CWEDatabase
from typing import Optional

''' Finding API'''


class PTFinding(BaseModel):
    topic: str = Field(description="Subject")
    status: FindingStatus = Field(description="status of the finding")
    type: FindingType = Field(description="The type of the finding")
    assessment_category: AssessmentCategory = Field(AssessmentCategory.PENTEST, description="assessment category")  # noqa
    assessment_technique: AssessmentTechnique = Field(AssessmentTechnique.NETWORK_ANALYSIS, description="assessment technique")  # noqa
    purpose: str = Field(description="purpose of the test")
    description: str = Field(description="description")
    preconditions: Optional[str] = Field(None, description="precondition for the test")  # noqa
    steps: Optional[str] = Field(None, description="steps performed for executing the test")  # noqa
    threat: Optional[str] = Field(None, description="threat description")
    recommendations: Optional[str] = Field(None, description="recommendations")
    expertise: Optional[Expertise] = Field(None, description="expertise needed by the attack in order to manipulate it")  # noqa
    access: Optional[Access] = Field(None, description="access needed in order to perform this attack")  # noqa
    time: Optional[ElapsedTime] = Field(None, description="the estimated time it takes to execute the exploit")  # noqa
    equipment: Optional[Equipment] = Field(None, description="required equipment level needed in order to execute the exploit")  # noqa
    knowledge_of_target: Optional[KnowledgeOfTarget] = Field(None, description="")  # noqa
    cwe_number: Optional[int] = Field(None, description="cwe num")

    # Custom validator that checks if different fields are matching 'RiskModel'
    @field_validator('expertise', 'access', 'time', 'equipment',
                     'knowledge_of_target', mode="before")
    def convert_enum_attributes_to_model(cls, v, info):
        """
        Convert enums values to pydantic model
        """
        field_to_enum_mapping = {
            'expertise': Expertise,
            'access': Access,
            'time': ElapsedTime,
            'equipment': Equipment,
            'knowledge_of_target': KnowledgeOfTarget
        }
        enum_class = field_to_enum_mapping.get(info.field_name)
        if not enum_class:
            raise ValueError(f"No enum class found for field "
                             f"{info.field_name}")
        if isinstance(v, dict):
            # Cover the case where the information is already a dict.
            return RiskModel(**v)
        if isinstance(v, str):
            try:
                return getattr(enum_class, v)
            except AttributeError:
                raise ValueError(f"{v} is not a valid value for enum class"
                                 f" {enum_class} and field {info.field_name}")
        return v

    @computed_field
    @property
    def cwe_description(self) -> str:
        try:
            cwe_db = CWEDatabase()
            weakness = cwe_db.get(self.cwe_number)
            return weakness.description
        except Exception:
            return ""  # not available

    @computed_field
    @property
    def sum(self) -> int:
        risk_sum = 0
        for field_name, field_value in self:
            if isinstance(field_value, Enum) and isinstance(
                    field_value.value, RiskModel):
                risk_sum += field_value.value.risk_value
        return risk_sum

    @computed_field
    @property
    def attack_difficulty(self) -> str:
        if self.type != FindingType.FINDING:
            return ""
        elif self.sum < 14:
            return "Very Low"
        elif self.sum < 20:
            return "Low"
        elif self.sum < 25:
            return "Moderate"
        elif self.sum < 35:
            return "High"
        return "Very High"

    def as_text(self):
        nl = "\n"
        text = ""

        text += f"\n\n--- {self.type.value} ---\n"
        text += f"  TOPIC: {self.topic}\n"
        text += f"  Status: {self.status.value}\n"
        text += f"  Assessment Category: {self.assessment_category.value} | Assessment_Technique: {self.assessment_technique.value}\n"
        text += f"  Purpose: {self.purpose}\n"

        if self.preconditions:
            text += f"\n  Preconditions:\n{self.preconditions.replace(nl, f'{nl}    ')}\n"
        text += f"\n  Description:\n{self.description.replace(nl, f'{nl}    ')}\n"
        if self.steps:
            text += f"\n  Steps:\n{self.steps.replace(nl, f'{nl}    ')}\n"
        if self.threat:
            text += f"\n  Threat:\n{self.threat.replace(nl, f'{nl}    ')}\n"
        if self.recommendations:
            text += f"\n  Recomendations:\n{self.recommendations.replace(nl, f'{nl}    ')}\n"

        if self.type == FindingType.FINDING:
            text += f"\n  Attack Difficulty: {self.attack_difficulty}\n"
            text += f"    Expertise: {self.expertise.value.level}\n"
            text += f"    Access: {self.access.value.level}\n"
            text += f"    Time: {self.time.value.level}\n"
            text += f"    Equipment: {self.equipment.value.level}\n"
            text += f"    Knowledge of Target: {self.knowledge_of_target.value.level}\n"
            text += f"    CWE: {self.cwe_number}\n"

        return text


class Finding(BaseModel):
    metadata: ExecutionMetadata
    model_type: FindingModelType
    data: PTFinding
    type: MessageType = MessageType.FINDING

    @computed_field
    @property
    def subtype(self) -> FindingType:
        return self.data.type
