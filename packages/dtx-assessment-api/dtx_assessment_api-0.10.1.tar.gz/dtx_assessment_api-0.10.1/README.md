`dtx-assessment-client-py` is a Python library that provides an API client for interacting with the Detoxio Assessment API. This client simplifies the process of sending assessment findings and managing assessment data within the Detoxio platform.

## Installation

To install `dtx-assessment-client-py`, you can use pip:

```bash
pip install dtx-assessment-client-py
```

Alternatively, you can clone the repository and install it manually:

```bash
git clone https://github.com/yourusername/dtx-assessment-client-py.git
cd dtx-assessment-client-py
pip install .
```

## Usage

Below are examples of how to use the `dtx-assessment-client-py` library to interact with the Detoxio Assessment API.

### Creating a Client

First, you need to create an instance of the `AssessmentFindingClient`. You will need the base URL of your API endpoint and an API key for authentication.

```python
from dtx_assessment_api.finding_client import AssessmentFindingClient

# Replace with your API base URL and API key
base_url = "https://api.example.com/"
api_key = "your_api_key_here"

# Initialize the client
client = AssessmentFindingClient(base_url, api_key)
```

### Posting an Assessment Finding

To post an assessment finding, you need to create an `AssessmentFinding` object and then use the `post` method of the client.

```python
from dtx_assessment_api.finding import AssessmentFinding, AssessmentRun, AssessmentTarget

# Example data for creating an AssessmentFinding
run = AssessmentRun(run_id="run-1234")
target = AssessmentTarget(target_id="target-5678", target_type="example_target_type")
finding = AssessmentFinding(run=run, target=target, finding_id="finding-91011")

# Post the assessment finding
response = client.post(finding)

print("Response Status Code:", response.status_code)
print("Response Body:", response.text)
```

## Configuration

You can configure the client by passing different parameters during initialization. Ensure that you have the correct base URL and a valid API key. The client handles authentication via Bearer tokens.

```python
client = AssessmentFindingClient(base_url="https://api.example.com/", api_key="your_api_key_here")
```

## Contributing

Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.

### Steps to Contribute

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with descriptive messages.
4. Push your changes to your fork.
5. Submit a pull request to the main repository.

Please ensure your code follows the project's coding standards and includes appropriate tests.


