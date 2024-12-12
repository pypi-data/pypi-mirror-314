"""ScrapingPros' client for Python. Check https://console.sprosdata.com/ for more info."""

from __future__ import annotations
import json
import logging
import sys
from enum import Enum
from time import sleep
from requests import request, Response




URL_CREATE_BATCH = "https://api.sprosdata.com/batches"
MAX_ATTEMPTS = 10
WAIT_TIME_SECONDS = 6
SUCCESS = 200


class ScrapMode(Enum):
    """Enumeration of scraping modes.

    This enum is used to specify the mode of scraping for each job.

    Attributes:
        HTTP_REQUEST (int): Use simple HTTP requests for scraping.
        SELENIUM (int): Use Selenium browser automation.
        PUPPETEER (int): Use Puppeteer for headless browser automation.
    """
    HTTP_REQUEST = 2
    SELENIUM = 5
    PUPPETEER = 7


class Logger:
    """Logger utility for tracking operations.

    This class sets up logging to both a log file and standard output.

    Attributes:
        logger (logging.Logger): The logger instance used for logging.
        verbose (bool): Whether to enable verbose logging.
    """

    def __init__(self, logger_name: str, verbose: bool = True):
        """Initializes the Logger.

        Args:
            logger_name (str): The name of the logger.
            verbose (bool): Whether to enable logging to stdout.
        """
        self.logger = None
        self.verbose = verbose

        if verbose:
            logging.basicConfig(filename=f"{logger_name}.log", level=logging.INFO)
            self.logger = logging.getLogger(logger_name)

            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def _log_info(self, message: str, *args):
        """Logs an informational message.

        Args:
            message (str): The message to log.
            *args: Additional arguments for message formatting.
        """
        if self.logger:
            self.logger.info(message, *args)


class APIWrapper(Logger):
    """Base class for interacting with the API.

    This class provides common functionality for API requests and logging.
    It is inherited by more specific classes such as `Project` and `Batch`.

    Attributes:
        api_key (str): API key for authentication.
    """

    def __init__(self, api_key: str, logger_name: str, verbose: bool = True):
        """Initializes the API wrapper.

        Args:
            api_key (str): The API key for authentication.
            logger_name (str): The name to use for logging.
            verbose (bool): Whether to enable verbose logging.
        """
        super().__init__(logger_name, verbose)
        self.api_key = api_key

    def _send_request_to_api(
        self, method: str, url: str, payload: dict = None
    ) -> Response:
        """Sends an API request.

        Args:
            method (str): HTTP method (e.g., 'GET', 'POST').
            url (str): The API endpoint URL.
            payload (dict, optional): Data to send in the request body.

        Returns:
            Response: The HTTP response object.
        """
        if payload is None:
            payload = {}

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        response = request(method, url, headers=headers, data=payload, timeout=30)

        return response


class Batch(APIWrapper):
    """Represents a batch of jobs related to a project.

    Provides methods to manage batches, such as adding jobs, 
    fetching job data, and analyzing scrap modes.

    Attributes:
        batch_id (int): The unique ID of the batch.
        jobs (list): A list of jobs associated with the batch.

    The batch MUST be created previously.
    """

    def __init__(self, api_key: str, batch_id: int, verbose: bool = True):
        """Initializes the Batch object.

        Args:
            api_key (str): API key for authentication.
            batch_id (int): The ID of the batch.
            verbose (bool): Whether to enable verbose logging.
        """
        super().__init__(api_key, f"Batch {batch_id}", verbose)
        self.batch_id = batch_id
        self.jobs = None
    
    def get_scrap_modes_info(self) -> dict:
        """Gets information about scrap modes used in the batch and their statistics.

        Returns:
            dict: A dictionary containing job counts and costs per scrap mode and status.
                 Returns None if no jobs are found or if an error occurs.

        Example response:
        {
            "result": {
                "S": {  # Status (S for Success)
                    "HTTP_REQUEST": {
                        "count": 10,
                        "cost": 5.0
                    },
                    "SELENIUM": {
                        "count": 5,
                        "cost": 7.5
                    }
                },
                "P": {  # Status (P for Pending)
                    "HTTP_REQUEST": 3,
                    "SELENIUM": 2
                }
            }
        }
        """
        self._log_info(f"Fetching scrap modes info for batch {self.batch_id}...")

        url = f"https://api.sprosdata.com/batches/{self.batch_id}/scrap-modes"

        try:
            response = self._send_request_to_api("GET", url)

            if response.status_code == SUCCESS:
                parsed_response = response.json()
                self._log_info("Successfully fetched scrap modes info ✅️")
                return parsed_response
            
            elif response.status_code == 404:
                self._log_info(f"No jobs found for batch {self.batch_id}")
                return None
            
            else:
                self._log_info("Failed to fetch scrap modes info: %s", 
                             response.json().get("message", "Unknown error"))
                return None

        except Exception as e:
            self._log_info("Error on GET /batches/%s/scrap-modes: %s", self.batch_id, str(e))
            return None
    def analyze_scrap_modes(self) -> dict:
        """Analyzes and summarizes scrap modes information in a more readable format.
        
        Returns:
            dict: A dictionary containing analyzed information about scrap modes,
                 or None if the data couldn't be fetched.
        """
        data = self.get_scrap_modes_info()
        if not data or 'result' not in data:
            return None

        result = data['result']
        analysis = {
            'successful_jobs': {},
            'pending_jobs': {},
            'total_cost': 0,
            'total_jobs': 0
        }

        if 'S' in result:
            for mode, details in result['S'].items():
                analysis['successful_jobs'][mode] = details
                analysis['total_cost'] += details['cost']
                analysis['total_jobs'] += details['count']

        if 'P' in result:
            for mode, count in result['P'].items():
                analysis['pending_jobs'][mode] = count
                analysis['total_jobs'] += count

        return analysis

    def append_jobs(self, job_urls: list[str], scrap_mode: ScrapMode) -> None:
        """Appends jobs to the batch, using the same scrape mode for all of them."""

        self._log_info("Appending jobs to batch %s...", self.batch_id)

        url = f"https://api.sprosdata.com/batches/{self.batch_id}/append-jobs"

        self.jobs = [
            {"url": url, "scrap_mode": scrap_mode.value, "arguments": {}}
            for url in job_urls
        ]

        payload = json.dumps({"jobs": self.jobs})

        self._send_request_to_api("POST", url, payload)
        self._log_info("Finished appending jobs ✅️")

    def run(self) -> None:
        """Sets the batch to run. It waits for the jobs to be added to the batch."""

        attempts = 0
        run_yet = False

        while attempts < MAX_ATTEMPTS and not run_yet:
            if attempts != 0:
                sleep(WAIT_TIME_SECONDS)

            url = f"https://api.sprosdata.com/batches/{self.batch_id}/run"

            response = self._send_request_to_api("POST", url)

            if response.status_code == SUCCESS:
                run_yet = True
                parsed_response = json.loads(response.text)
                self._log_info(f'{parsed_response["message"]} ✅️')

            attempts += 1

        if not run_yet:
            self._log_info("Batch not set to run after %s attempts ❌", attempts)

    def get_data(self) -> dict:
        """Returns the data from all of the jobs in the batch.

        It does not wait for all of the jobs to have finished.
        """

        attempts = 0
        got_data = False

        self._log_info("Fetching the data from batch %i...", self.batch_id)

        parsed_response = None
        while attempts < MAX_ATTEMPTS and not got_data:
            if attempts != 0:
                self._log_info(
                    "Waiting to fetch the data from the batch %i...", self.batch_id
                )
                sleep(WAIT_TIME_SECONDS * 10)

            url = f"https://api.sprosdata.com/get_data/batch/{self.batch_id}"

            response = self._send_request_to_api("GET", url)
            parsed_response = json.loads(response.text)

            if response.status_code == SUCCESS:
                got_data = True
                self._log_info("Got the data from batch %i ✅️", self.batch_id)
                return parsed_response

            attempts += 1

        if not got_data:
            self._log_info(
                "Could not get data from batch %i after %s attempts ❌",
                self.batch_id,
                attempts,
            )

            # self._log_info(parsed_response)

            return None


class Project(APIWrapper):
    """Group of related batches.

    The project must be created previously.
    """

    def __init__(self, api_key: str, project_id: int, verbose: bool = True):
        super().__init__(api_key, f"Project {project_id}", verbose)
        self.project_id = project_id

    def create_batch(self, batch_name: str) -> Batch:
        """Creates a batch and returns its ID."""

        self._log_info("Creating a batch...")

        payload = json.dumps(
            {"project": self.project_id, "name": batch_name, "priority": 1}
        )

        response = self._send_request_to_api("POST", URL_CREATE_BATCH, payload)

        parsed_response = json.loads(response.text)
        batch_id = parsed_response["batch"]["id"]

        self._log_info(f"Batch {batch_id} created succesfully ✅️")

        return Batch(self.api_key, batch_id, self.verbose)

    @classmethod
    def get_projects_summary(cls, api_key: str, verbose: bool = True) -> dict:
        """Gets a summary of all projects for the authenticated user.

        Returns:
            dict: A dictionary containing the projects summary data.
                  Returns None if no projects are found or if an error occurs.

        Example response:
            {
                "summary": [
                    {
                        "project_id": 123,
                        "name": "Project Name",
                        ...other project details...
                    },
                    ...
                ]
            }
        """
        logger = cls(api_key, "Projects Summary", verbose)
        logger._log_info("Fetching projects summary...")

        url = "https://api.sprosdata.com/projects/summary"

        try:
            response = logger._send_request_to_api("GET", url)
            
            if response.status_code == SUCCESS:
                parsed_response = response.json()
                logger._log_info("Successfully fetched projects summary ✅️")
                return parsed_response
            
            elif response.status_code == 404:
                logger._log_info("No projects found for user")
                return None
            
            else:
                logger._log_info("Failed to fetch projects summary: %s", 
                               response.json().get("message", "Unknown error"))
                return None

        except Exception as e:
            logger._log_info("Error on GET /projects/summary: %s", str(e))
            return None
    def get_batches(self) -> list:
        """Gets all non-deleted batches for this project.

        Returns:
            list: A list of dictionaries containing batch information.
                 Returns None if no batches are found or if an error occurs.

        Example response:
        [
            {
                "id": 123,
                "project_id": 456,
                "name": "Batch Name",
                "priority": 1,
                "status": "P"
            },
            ...
        ]
        """
        self._log_info(f"Fetching batches for project {self.project_id}...")

        url = f"https://api.sprosdata.com/batches"
        params = {"project": self.project_id}

        try:
            response = self._send_request_to_api("GET", url, json.dumps(params))
            
            if response.status_code == SUCCESS:
                parsed_response = response.json()
                batches = parsed_response.get("batches", [])
                
                if batches:
                    self._log_info(f"Successfully fetched {len(batches)} batches ✅️")
                else:
                    self._log_info("No batches found for this project")
                    
                return batches
            
            else:
                self._log_info("Failed to fetch batches: %s", 
                             response.json().get("message", "Unknown error"))
                return None

        except Exception as e:
            self._log_info("Error on GET /batches: %s", str(e))
            return None

class ProjectManager(APIWrapper):
    """Handles operations related to projects.

    This class provides methods to create and manage projects.

    Methods:
        create_project: Creates a new project.
        close_project: Closes an existing project.
    """

    def __init__(self, api_key: str, verbose: bool = True):
        super().__init__(api_key, "Project Manager", verbose)

    def create_project(self, name: str, priority: int, description: str = None) -> Project:
        """Creates a new project.

        Args:
            name (str): The name of the project.
            priority (int): The priority of the project.
            description (str, optional): Description of the project.

        Returns:
            Project: The created project object.
        """

        self._log_info("Creating a project...")

        payload = {
            "name": name,
            "priority": priority,
            "description": description,
        }

        try:
            url = "https://api.sprosdata.com/projects"
            response = self._send_request_to_api("POST", url, json.dumps(payload))
            parsed_response = response.json()

            if response.status_code == SUCCESS:
                project_id = parsed_response["project"]["id"]
                self._log_info("Project %s successfully created ✅️", project_id)
                return Project(self.api_key, project_id, self.verbose)

            else:
                self._log_info("Failed to create project: %s", parsed_response.get("message", "Unknown error"))
                return None

        except Exception as e:
            self._log_info("Error on POST /projects: %s", str(e))
            return None
    def close_project(self, project_id: int) -> dict:
        """Closes a project and returns a confirmation message.

        Parameters:
        - project_id: The ID of the project to close.
        """

        self._log_info("Closing project %s...", project_id)

        url = f"https://api.sprosdata.com/projects/{project_id}/close"

        payload = {
            "project": project_id
        }

        try:
            response = self._send_request_to_api("PUT", url, payload)

            if response.status_code == SUCCESS:
                parsed_response = response.json()
                self._log_info("Project %s successfully closed ✅️", project_id)
                return {"message": "Project successfully closed.", "project": parsed_response["project"]}

            elif response.status_code == 404:
                self._log_info("No project by ID %s found for user.", project_id)
                return {"message": "No project by ID found for user."}

            else:
                self._log_info("Failed to close project: %s", response.text)
                return {"message": "Failed to close project.", "details": response.text}

        except Exception as e:
            self._log_info("Error on PUT /projects/%s/close: %s", project_id, str(e))
            return {"message": "Internal server error."}

class Job(APIWrapper):
    """Represents a job and provides methods to interact with job-related data.

    Attributes:
        job_id (str): The unique identifier of the job.
    """

    def __init__(self, api_key: str, job_id: str, verbose: bool = True):
        """Initializes the Job object.

        Args:
            api_key (str): API key for authentication.
            job_id (str): The ID of the job.
            verbose (bool): Whether to enable verbose logging.
        """
        super().__init__(api_key, f"Job {job_id}", verbose)
        self.job_id = job_id

    def get_data(self) -> dict:
        """Fetches the data for the specified job.

        Returns:
            dict: The job data if found, otherwise returns None.
        """
        self._log_info(f"Fetching data for job {self.job_id}...")

        url = f"https://api.sprosdata.com/get_data/{self.job_id}"
        attempts = 0
        got_data = False
        parsed_response = None

        while attempts < MAX_ATTEMPTS and not got_data:
            if attempts != 0:
                self._log_info(f"Waiting to fetch data for job {self.job_id}...")
                sleep(WAIT_TIME_SECONDS * 2)

            response = self._send_request_to_api("GET", url)

            if response.status_code == SUCCESS:
                got_data = True
                parsed_response = str(response)
                self._log_info("Successfully fetched data for job %s ✅️", self.job_id)
                return parsed_response

            attempts += 1

        if not got_data:
            self._log_info("Could not get data for job %s after %s attempts ❌", self.job_id, attempts)
            return None  

