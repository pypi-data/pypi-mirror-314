from typing import List, Union
from pydantic import BaseModel, Field
from cyclarity_sdk.sdk_models import ExecutionMetadata, MessageType
from cyclarity_sdk.sdk_models.artifacts.types import ArtifactType

'''Test Artifacts - artifacts that might be sent from test execution '''


class ScanGraphItemProp(BaseModel):
    name: str
    value: str


class ScanGraphItem(BaseModel):
    type: int = 0
    props: List[ScanGraphItemProp]
    name: str
    component_id: str


class ScanGraphMapping(BaseModel):
    arrow_id: str
    start: str
    end: str


class ScanGraph(BaseModel):
    type: ArtifactType
    items: List[ScanGraphItem] = Field(default_factory=list)
    mapping: List[ScanGraphMapping] = Field(default_factory=list)


class TestReportDescription(BaseModel):
    type: ArtifactType
    description: str


class TestArtifact(BaseModel):
    execution_metadata: ExecutionMetadata
    type: MessageType = MessageType.TEST_ARTIFACT
    data: Union[TestReportDescription, ScanGraph]
