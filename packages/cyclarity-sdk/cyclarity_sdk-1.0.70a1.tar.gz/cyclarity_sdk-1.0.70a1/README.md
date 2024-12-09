Project description
CyClarity SDK

Introduction

CyClarity SDK is a Python package that provides an interface for interacting with the CyClarity platform. It includes classes and methods for creating, managing, and interacting with various resources on the platform.

Installation

You can install the CyClarity SDK using poetry in your poetry project:

```bash
  poetry add cyclarity-sdk
```

To create a poetry project use this docs: https://python-poetry.org/docs/

You can download your sdk-usage-example using cyclarity git hub example : https://github.com/cyclarity/cyclarity-sdk-usage-examples
Usage

Here are examples of how to use the classes in the CyClarity SDK. Runnable The Runnable class is a base class for creating objects that can be run with setup and teardown phases. It has setup, run, and teardown methods that need to be implemented. 

This is the structure of a runnable:
```python
from cyclarity_sdk.runnable import Runnable, BaseResultsModel
from cyclarity_sdk.sdk_models.findings import PTFinding
import cyclarity_sdk.sdk_models.findings.types import FindingStatus , FindingType , AssessmentCategory
import cyclarity_sdk.sdk_models.findings.types as PTFindingTypes
class MyResult(BaseResultsModel):
    res_str: str

class MyRunnable(Runnable[MyResult]):
    desc: str
    cli_args: str
    #self.platform_api inherited attribute,initiates PlatformApi class
    def setup(self):  
        self.logger.info("Setting up")  
    #the run function is the first function to be initiated when a runnable is executed.
    def run(self):  
        self.logger.info("Running")  
        self.platform_api.send_test_report_description("This is a test description")
        self.platform_api.send_finding(PTFinding(
            topic='hello world',
            status=PTFindingTypes.FindingStatus.FINISHED,
            type=PTFindingTypes.FindingType.FINDING,
            assessment_category=PTFindingTypes.AssessmentCategory.FUNCTIONAL_TEST,
            assessment_technique=PTFindingTypes.AssessmentTechnique.OTHER_EXPLORATION,
            purpose='Snippet example',
            description='This is an example snippet on how to user platform_api'))
        for percentage in range(101):
            self.platform_api.report_test_progress(percentage=percentage)
            time.sleep(0.01)  
        return MyResult(res_str="success!")  

    def teardown(self, exception_type, exception_value, traceback):  
        self.logger.info("Tearing down")  
```

## PlatformApi
The PlatformApi class provides methods for interacting with the CyClarity platform. It is used within a Runnable instance through the self.platform_api attribute.
```python

from cyclarity_sdk.platform_api.Iplatform_connector import IPlatformConnectorApi as IPlatformConnectorApi
from cyclarity_sdk.sdk_models.findings import PTFinding as PTFinding

class PlatformApi:
    def __init__(self, platform_connector: IPlatformConnectorApi | None = None) -> None: ...
    def send_test_report_description(self, description: str): ...
    def send_finding(self, pt_finding: PTFinding): ...
    def report_test_progress(self, percentage: int): ...

```
### send_test_report_description:
description: str (expects a description)
### send_finding:
Gets PTfinding object and sends it to be visible on the website (See [PTFinding](#ptfinding))
### report_test_progress
percentage: int (expects a percentage , example above)

## PTFinding
```python
from pydantic import BaseModel, Field, computed_field, field_validator
from enum import Enum
from cyclarity_sdk.sdk_models.findings.types import FindingStatus, FindingType, AssessmentCategory, AssessmentTechnique
from cyclarity_sdk.sdk_models import ExecutionMetadata, MessageType

class PTFinding(BaseModel):
    topic: str
    status: FindingStatus
    type: FindingType
    assessment_category: AssessmentCategory
    assessment_technique: AssessmentTechnique
    purpose: str
    description: str

class FindingStatus(str, Enum):
    FINISHED = 'Finished'
    PARTIALLY_PERFORMED = 'Partially Performed'
    NOT_PERFORMED = 'Not Performed'

class FindingType(str, Enum):
    FINDING = 'Finding'
    NON_FINDING = 'Non Finding'
    INSIGHT = 'Insight'
    ADDITIONAL_INFORMATION = 'Additional Information'

class AssessmentCategory(str, Enum):
    FUNCTIONAL_TEST = 'functional test'
    PENTEST = 'pentest'
    VULNERABILITY_ANALYSIS = 'vulnerability analysis'
    INCIDENT = 'incident'
    CODE_REVIEW = 'code review'
    UNKNOWN = 'unknown'

class AssessmentTechnique(str, Enum):
    SPEC_BASED_TEST_CASE = 'specification-based test case'
    HARDWARE_ANALYSIS = 'hardware analysis'
    BINARY_ANALYSIS = 'binary analysis'
    INTERFACE_ANALYSIS = 'interface analysis'
    NETWORK_ANALYSIS = 'network analysis'
    CODE_REVIEW = 'code review'
    SPECIFICATION_REVIEW = 'specification review'
    CVE_SEARCH = 'CVE search'
    OTHER_EXPLORATION = 'other exploration'
    UNKNOWN = 'unknown'
```