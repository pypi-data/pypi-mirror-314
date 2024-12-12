import uuid
import requests
import base64
from urllib.parse import urlparse
from datetime import datetime
from urllib.parse import urljoin  # Import urljoin for URL construction
from datetime import datetime, timezone
from .finding import (
    AssessmentFinding, AssessmentRun, AssessmentTarget, 
    AssessmentTool, TargetType,
    EventCategory, EventType
)
from .utils import AssessmentURLParser
import proto.dtx.services.prompts.v1.prompts_pb2 as prompts_pb2
from google.protobuf.json_format import ParseDict, ParseError


class AssessmentFindingClient:
    """
    A client for posting AssessmentFinding models to a remote endpoint.
    """
    
    FINDING_ENDPOINT_PATH = "dtx.services.assessment.v1.EventProcessing/finding"

    def __init__(self, base_url, api_key):
        """
        Initializes the client with the base URL and API key.

        Args:
            base_url (str): The base URL of the API endpoint.
            api_key (str): The API key for authentication.
        """
        self.url = urljoin(base_url, self.FINDING_ENDPOINT_PATH)
        self.api_key = api_key

    def post(self, finding: AssessmentFinding):
        """
        Sends a POST request to the endpoint with the assessment model.

        Args:
            finding (AssessmentFinding): The assessment model to post.

        Returns:
            requests.Response: The response from the POST request.

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
            requests.exceptions.RequestException: For any other request-related errors.
        """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }

        try:
            response = requests.post(self.url, 
                                     data=finding.model_dump_json(), 
                                     headers=headers)
            # Raise an HTTPError for bad responses (4xx and 5xx)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as http_err:
            raise requests.exceptions.HTTPError(
                f"HTTP error occurred while posting assessment model with run_id {finding.run.run_id}: {http_err}"
            ) from http_err
        except requests.exceptions.RequestException as req_err:
            raise requests.exceptions.RequestException(
                f"Request error occurred while posting assessment model with run_id {finding.run.run_id}: {req_err}"
            ) from req_err

class AssessmentFindingBuilder:
    """
    A builder for creating AssessmentFinding models.
    
    # Initialize the builder
    builder = AssessmentFindingBuilder()

    # Set up the various components of the assessment finding
    assessment_finding = (builder
        .set_tool_name("Automated Testing Tool")
        .set_assessment_title("Web Application Security Assessment")
        .set_target(TargetType.WEBAPP, "http://example.com", "Example Web App")
        .set_record({"threat_level": "high", "description": "SQL Injection vulnerability found"})
        .set_timestamp(datetime.now())  # Optional: You can set a specific timestamp
        .build())
    
    """

    def __init__(self):
        """
        Initializes the builder with default values.
        """
        self.run_id = self._generate_random_run_id()
        self.tool_name = None
        self.assessment_title = None
        self.target_type = None
        self.target_url = None
        self.target_name = None
        self.record:dict = None
        self.timestamp = self._get_current_timestamp()
    
    @staticmethod
    def create_instance_with_default_names(target_url: str, 
                                        tool_name: str,
                                        target_type: TargetType = TargetType.WEBAPP,
                                        model_id:str=None):
        """
        Creates an instance of AssessmentFindingBuilder from a target URL.

        Args:
            cls: The class type to create an instance.
            target_url (str): The URL of the target to be assessed.
            tool_name (str): The name of the tool used for the assessment.
            model_id (str): Model id if target_url is a hosted url. Example meta/llama-2b-it
            target_type (TargetType, optional): The type of the target (default is TargetType.WEBAPP).

        Returns:
            AssessmentFindingBuilder: An instance of the builder initialized with the provided URL.
        
        This method performs the following steps:
        1. Parses the target URL to extract relevant details such as the assessment title and target name.
        2. Initializes a new builder instance with these extracted details.
        3. Sets the tool name and target details using the provided arguments and extracted information.
        """
        # Step 1: Parse the target URL to extract details
        parser = AssessmentURLParser(target_url)
        
        # Step 2: Initialize a new builder instance
        builder = (AssessmentFindingBuilder()
            .set_tool_name(tool_name)  # Step 3: Set the tool name
            .set_assessment_title(parser.get_assessment_title())  # Set the assessment title
            .set_target(target_type, target_url, model_id or parser.get_target_name())  # Set the target details
        )
        
        # Return the initialized builder instance
        return builder

    def set_tool_name(self, tool_name):
        """
        Sets the tool name for the assessment.

        Args:
            tool_name (str): The name of the assessment tool.
        """
        self.tool_name = tool_name
        return self

    def set_assessment_title(self, assessment_title):
        """
        Sets the title for the assessment run.

        Args:
            assessment_title (str): The title of the assessment run.
        """
        self.assessment_title = assessment_title
        return self

    def set_target(self, target_type:TargetType, target_url, target_name):
        """
        Sets the target details for the assessment.

        Args:
            target_type (TargetType): The type of the target (webapp, model, code).
            target_url (str): The URL or URI of the target.
            target_name (str): The name of the target.
        """
        self.target_type = target_type
        self.target_url = target_url
        self.target_name = target_name
        return self

    def set_record(self, record:dict):
        """
        Sets the record data for the assessment finding.

        Args:
            record (dict): The data record for creating an assessment finding.
        """
        self.record = record
        return self

    def set_timestamp(self, timestamp=None):
        """
        Sets the timestamp for the assessment finding.

        Args:
            timestamp (datetime, optional): The timestamp for the finding. Defaults to the current UTC time.
        """
        self.timestamp = timestamp or self._get_current_timestamp()
        return self

    def build_assessment_run(self):
        """
        Builds and returns the AssessmentRun object.
        """
        return AssessmentRun(
            run_id=self.run_id,
            title=self.assessment_title
        )

    def build_assessment_target(self):
        """
        Builds and returns the AssessmentTarget object.
        """
        return AssessmentTarget(
            target_type=self.target_type,
            uri=self.target_url,
            name=self.target_name
        )

    def build_assessment_tool(self):
        """
        Builds and returns the AssessmentTool object.
        """
        return AssessmentTool(
            title=self.tool_name
        )

    def build(self):
        """
        Builds the final AssessmentFinding model using the provided data.

        Returns:
            AssessmentFinding: The constructed assessment finding model.
        """
        assessment_run = self.build_assessment_run()
        assessment_target = self.build_assessment_target()
        assessment_tool = self.build_assessment_tool()

        # Validate if the finding can be converted to PromptEvaluationResponse
        try:
            protobuf_message = prompts_pb2.PromptEvaluationResponse()
            ParseDict(self.record, protobuf_message)
        except ParseError as e:
            raise ValueError(f'Validation Failed. Record can not be converted to PromptEvaluationResponse: {e}')

        # Convert encoded prompt (base64) into text
        self._decode_prompt_text(self.record)

        # Create the AssessmentFinding instance with the generated data
        model = AssessmentFinding(
            category=EventCategory.ASSESSMENT,
            event_type=EventType.FINDING,
            run=assessment_run,
            target=assessment_target,
            tool=assessment_tool,
            timestamp=self.timestamp,
            finding=self.record
        )
        return model

    def _decode_prompt_text(self, record:dict):
        prompt_dict = record.get("prompt")
        prompt_str = prompt_dict.get("data").get("content")
        prompt_encoding = prompt_dict.get("source_labels", {}).get("_prompt_encoding", None)
        if prompt_encoding == 'base64':
            decoded_prompt_str = base64.b64decode(prompt_str).decode('utf-8')
        else:
            decoded_prompt_str = prompt_str
        prompt_dict["data"]["content"] = decoded_prompt_str


    @staticmethod
    def _generate_random_run_id():
        """
        Generates a random run_id using UUID4.
        """
        return str(uuid.uuid4())

    @staticmethod
    def _get_current_timestamp():
        """
        Generates the current timestamp in UTC.
        """
        return datetime.now(timezone.utc)
