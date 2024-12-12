from urllib.parse import urlparse
from datetime import datetime

class AssessmentURLParser:
    """
    A class to parse assessment-related details from a given URL.
    """

    def __init__(self, url):
        """
        Initializes the parser with a URL.

        Args:
            url (str): The URL containing the assessment details.
        """
        self.url = url
        self.parsed_url = urlparse(url)
        self.hostname = self.parsed_url.hostname
        self.path_segments = self.parsed_url.path.strip('/').split('/')

    def get_assessment_title(self):
        """
        Extracts and returns the assessment title from the URL, formatted with the current date and time.

        Returns:
            str: The assessment title.
        """
        # Get the current date and time in the desired short format
        current_datetime = datetime.now().strftime("%d %b %y : %I%p")
        
        if self.hostname and "huggingface.co" in self.hostname and "spaces" in self.path_segments:
            # Format the title specifically for Hugging Face URLs
            assessment_title = self._generate_huggingface_assessment_name()
        else:
            # Default behavior for other URLs with a hostname
            assessment_title = self._generate_name_from_path(self.hostname, self.path_segments)

        # Combine the date/time with the assessment title
        return f"{current_datetime} - {assessment_title}"

    def get_target_name(self):
        """
        Extracts and returns the target name from the URL.

        Returns:
            str: The target name.
        """
        # Handle URLs without a hostname
        return self._generate_name_from_path(self.hostname, self.path_segments)

    def _generate_huggingface_assessment_name(self):
        """
        Generates an assessment name based on Hugging Face space information.

        Returns:
            str: The assessment name formatted as "{target}".
        """
        try:
            user_id = self.path_segments[1]  # Extract the user ID from the URL path
            space_name = self.path_segments[2]  # Extract the space name from the URL path
            target = f"{user_id}/{space_name}"

            # Format the assessment name
            return f"{target}"
        except IndexError:
            return "GenAi Safety Assessment - Hugging Face Space"

    def _generate_name_from_path(self, hostname, path_segments):
        """
        Generates a name from the path, optionally including the hostname.

        Args:
            hostname (str): The hostname of the URL, or None if not present.
            path_segments (list): The segments of the URL path.

        Returns:
            str: A name generated from the path.
        """
        path_str = "/".join(path_segments)
        if hostname:
            suffix = path_str[:50]
            if path_str[:50]:
                suffix = f"-{path_str[:50]}"
            return f"{hostname}{suffix}"
        return path_str[:50]  # Return only the first 50 characters of the path
