from pydantic import BaseModel, model_validator, ConfigDict
from datetime import datetime
from enum import Enum
import proto.dtx.services.prompts.v1.prompts_pb2 as prompts_pb2
from google.protobuf.json_format import ParseDict, ParseError, MessageToDict


# Existing Enums and Base Models

# Define enums for each field
class EventCategory(Enum):
    """
    Enum for different event categories.

    Currently supports:
    - ASSESSMENT: Represents an assessment-related event.
    """
    ASSESSMENT = "assessment"


class EventType(Enum):
    """
    Enum for different event types.

    Currently supports:
    - FINDING: Represents an event of type finding.
    """
    FINDING = "finding"


class BaseEvent(BaseModel):
    """
    Base class for events.

    Attributes:
    - category (EventCategory): The category of the event.
    - event_type (EventType): The type of event.
    """
    category: EventCategory  # Use EventCategory enum for defining event category
    event_type: EventType    # Use EventType enum for defining event type


# Assessment Related Models

class AssessmentRun(BaseModel):
    """
    Model representing an assessment run.

    Attributes:
    - run_id (str): Unique identifier for the assessment run.
    - title (str): Title or description of the assessment run.
    """
    run_id: str
    title: str


# Define an enum for the target type
class TargetType(Enum):
    """
    Enum for different types of assessment targets.

    Supports:
    - WEBAPP: Represents a web application target.
    - MODEL: Represents a model target.
    - CODE: Represents a codebase target.
    """
    WEBAPP = "webapp"
    MODEL = "model"
    CODE = "code"


class AssessmentTarget(BaseModel):
    """
    Model representing an assessment target.

    Attributes:
    - target_type (TargetType): The type of target (e.g., webapp, model, code).
    - uri (str): The URI or location of the target.
    - name (str): Name of the target, such as a domain name for web applications.
    """
    target_type: TargetType  # Use TargetType enum for defining target type
    uri: str
    name: str  # Name of the target, domain name for web apps, etc.


class AssessmentTool(BaseModel):
    """
    Model representing an assessment tool.

    Attributes:
    - title (str): Name of the assessment tool (e.g., Hacktor, Notebook).
    """
    title: str  # Title or name of the assessment tool


# Represents a finding associated with a case
class BaseFinding(BaseEvent):
    """
    Base class for findings related to an event.

    Inherits from:
    - BaseEvent: Includes common event attributes.

    Attributes:
    - run (AssessmentRun): The assessment run associated with the finding.
    - target (AssessmentTarget): The target under assessment.
    - tool (AssessmentTool): The tool used for assessment.
    - timestamp (datetime): Timestamp of the finding.
    """
    run: AssessmentRun  # The assessment run associated with the finding
    target: AssessmentTarget  # The target under test
    tool: AssessmentTool  # The assessment tool used
    timestamp: datetime  # Timestamp of the finding

    @model_validator(mode='before')
    def check_non_empty_fields(cls, values):
        """
        Validates that certain fields are non-empty.

        Checks if 'timestamp' is provided.

        Args:
            values (dict): Dictionary of field values.

        Raises:
            ValueError: If any of the required fields are empty.

        Returns:
            dict: Validated dictionary of field values.
        """
        timestamp = values.get('timestamp')  # Check if timestamp is provided

        if not timestamp:
            raise ValueError('timestamp cannot be empty')

        return values

    model_config = ConfigDict(
        populate_by_name=True,  # Allows population of model using field names
        json_encoders={
            datetime: lambda v: v.isoformat()  # Serialize datetime to ISO 8601 string
        }
    )


# Represents a case with details and associated findings
class AssessmentFinding(BaseFinding):
    """
    Detailed class for assessment findings.

    Inherits from:
    - BaseFinding: Includes common finding attributes.

    Attributes:
    - finding (dict): A dictionary representing the finding details.
    """
    finding: dict  # Dictionary containing details of the finding

    def to_dict(self):
        """
        Converts the AssessmentFinding instance to a dictionary representation.

        Uses alias for serialization to ensure proper field naming.

        Returns:
            dict: Dictionary representation of the instance.
        """
        return self.model_dump(by_alias=True)  # Use alias for serialization

    @model_validator(mode='before')
    def check_non_empty_fields(cls, values):
        """
        Validates that certain fields are non-empty and checks for data integrity.

        Ensures 'finding' field is provided and validates its structure.

        Args:
            values (dict): Dictionary of field values.

        Raises:
            ValueError: If any required fields are empty or if finding cannot be parsed into the expected protobuf message.

        Returns:
            dict: Validated dictionary of field values.
        """
        finding = values.get('finding')

        if not finding:
            raise ValueError('finding cannot be empty')

        # Validate if the finding can be converted to PromptEvaluationResponse
        try:
            protobuf_message = prompts_pb2.PromptEvaluationResponse()
            ParseDict(finding, protobuf_message)
        except ParseError as e:
            raise ValueError(f'finding dictionary cannot be converted to PromptEvaluationResponse: {e}')

        return values

    model_config = ConfigDict(
        populate_by_name=True,  # Allows population of model using field names
        json_encoders={
            datetime: lambda v: v.isoformat(),  # Serialize datetime to ISO 8601 string
        }
    )


