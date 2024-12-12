from dataclasses import dataclass
from datetime import datetime
import json
import os
from typing import Dict, List, Literal, Optional

import requests


@dataclass
class ContextualSettings:
    API_BASE_URL: str = "https://api.app.contextual.ai/v1"
    APPLICATION_ID: str = ""


class ContextualAPIClient:
    """
    ContextualAPIClient is a class that provides a set of methods for interacting with the Contextual API.

    """

    def __init__(
        self,
        api_base_url: str = ContextualSettings.API_BASE_URL,
        application_id: str = ContextualSettings.APPLICATION_ID,
        **kwargs,
    ):
        """Initializes the ContextualAPIClient

        Args:
            application_id (str, optional): Application ID.
                Defaults to ContextualSettings.APPLICATION_ID.
            api_base_url (str, optional): Base URL for the API.
            chat_base_url (str, optional): Base URL for the chat API.
        """
        self.settings = ContextualSettings(
            APPLICATION_ID=application_id,
            API_BASE_URL=api_base_url,
        )
        self.application_id = self.settings.APPLICATION_ID
        self.api_base_url = self.settings.API_BASE_URL
        self.kwargs = kwargs

        env_var_name = "CONTEXTUAL_API_KEY"
        if env_var_name not in os.environ:
            raise EnvironmentError(
                f"The environment variable '{env_var_name}' is not set."
            )
        self.contextual_api_key = os.environ.get(env_var_name)

    # Datastore/Document APIs
    def list_datastores(
        self, limit: Optional[int] = 1000, cursor: Optional[str] = None
    ) -> dict:
        """
        List all Datastores with pagination support.

        Args:
            limit (int, optional): Maximum number of datastores to return (1-1000, defaults to 1000)
            cursor (str, optional): Cursor from previous call to get next set of results

        Returns:
            dict: JSON response containing list of datastores and pagination details

        Raises:
            ValueError: If limit is outside valid range
            requests.exceptions.RequestException: If the request fails
        """
        endpoint = "/datastores"

        # Validate limit
        if limit is not None and not 1 <= limit <= 1000:
            raise ValueError("Limit must be between 1 and 1000")

        # Build query parameters
        params = {}
        if limit is not None:
            params["limit"] = limit
        if cursor is not None:
            params["cursor"] = cursor

        response = self._fetch_with_access_token(
            path=endpoint, method="GET", params=params
        )
        return response.json()

    def create_datastore(self, name: str) -> dict:
        """
        Create a new Datastore.

        A Datastore is a collection of documents that can be linked to one or more Applications
        to provide data for grounding responses. Documents can be ingested into and deleted
        from a Datastore.

        Args:
            name (str): Name of the datastore to create

        Returns:
            dict: JSON response containing the created datastore details

        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        endpoint = "/datastores"

        json = {"name": name}

        response = self._fetch_with_access_token(
            path=endpoint, method="POST", json=json
        )
        return response.json()

    def get_datastore_metadata(self, datastore_id: str) -> dict:
        """
        Get the details of a given Datastore, including its name, create time,
        and the list of Applications which are currently configured to use the Datastore.

        Args:
            datastore_id (str): Datastore ID of the datastore to get details of

        Returns:
            dict: JSON response containing datastore metadata including:
                - name: Name of the datastore
                - create_time: Time when the datastore was created
                - applications: List of applications configured to use this datastore

        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        # Construct the endpoint
        endpoint = f"/datastores/{datastore_id}/metadata"

        # Make GET request using the helper method
        response = self._fetch_with_access_token(path=endpoint, method="GET")
        return response.json()

    def delete_datastore(self, datastore_id: str) -> dict:
        """
        Delete a given Datastore, including all the documents ingested into it.
        This operation is irreversible.

        Args:
            datastore_id (str): Datastore ID of the datastore to delete

        Returns:
            dict: JSON response confirming the deletion

        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        # Construct the endpoint
        endpoint = f"/datastores/{datastore_id}"

        # Make DELETE request using the helper method
        response = self._fetch_with_access_token(path=endpoint, method="DELETE")
        return response.json()

    def list_documents(
        self,
        datastore_id: str,
        *,
        limit: Optional[int] = 1000,
        cursor: Optional[str] = None,
        ingestion_job_status: Optional[List[str]] = None,
        uploaded_after: Optional[datetime] = None,
        uploaded_before: Optional[datetime] = None,
    ) -> dict:
        """
        Get list of documents in a given Datastore, including document id, name,
        and ingestion job status. Supports cursor-based pagination and filtering.

        Args:
            datastore_id (str): Datastore ID of the datastore to retrieve documents for
            limit (int, optional): Maximum number of documents to return. Must be between 1 and 1000.
                Defaults to 1000.
            cursor (str, optional): Cursor from the previous call to list documents,
                used to retrieve the next set of results
            ingestion_job_status (List[str], optional): Filter documents by one or more
                ingestion job statuses
            uploaded_after (datetime, optional): Filter documents uploaded at or after
                specified timestamp
            uploaded_before (datetime, optional): Filter documents uploaded at or before
                specified timestamp

        Returns:
            dict: JSON response containing:
                - documents: List of document objects with id, name, and status
                - cursor: Pagination cursor for the next set of results (if any)

        Raises:
            ValueError: If limit is outside allowed range
            requests.exceptions.RequestException: If the request fails
        """
        # Validate limit
        if limit is not None:
            if not isinstance(limit, int) or limit < 1 or limit > 1000:
                raise ValueError("limit must be an integer between 1 and 1000")

        # Construct the endpoint
        endpoint = f"/datastores/{datastore_id}/documents"

        # Build query parameters
        params = {}
        if limit is not None:
            params["limit"] = limit
        if cursor is not None:
            params["cursor"] = cursor
        if ingestion_job_status is not None:
            params["ingestion_job_status"] = ingestion_job_status
        if uploaded_after is not None:
            params["uploaded_after"] = uploaded_after.isoformat()
        if uploaded_before is not None:
            params["uploaded_before"] = uploaded_before.isoformat()

        # Make GET request using the helper method
        response = self._fetch_with_access_token(
            path=endpoint, method="GET", params=params
        )
        return response.json()

    def ingest_document(self, datastore_id: str, file_path: str) -> dict:
        """
        Ingest a document into a given Datastore. This is an asynchronous operation.

        The function uploads a PDF or HTML file to the specified datastore and returns
        a document ID that can be used to track the ingestion status or delete the
        document later.

        Args:
            datastore_id (str): Datastore ID of the datastore in which to ingest the document
            file_path (str): Path to the PDF or HTML file to be ingested

        Returns:
            dict: JSON response containing the document ID and other metadata

        Raises:
            ValueError: If the file is not PDF or HTML
            FileNotFoundError: If the specified file does not exist
            requests.exceptions.RequestException: If the request fails
        """
        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # Validate file extension
        if file_path.lower().endswith(".pdf"):
            file_type = "application/pdf"
        elif file_path.lower().endswith(".html"):
            file_type = "text/html"
        else:
            raise ValueError("File must be PDF or HTML format")

        # Construct the endpoint
        endpoint = f"/datastores/{datastore_id}/documents"

        # Prepare the file for upload
        files = {
            "file": (os.path.basename(file_path), open(file_path, "rb"), file_type)
        }

        # Make POST request using the helper method
        response = self._fetch_with_access_token(
            path=endpoint, method="POST", files=files
        )
        return response.json()

    def get_document_metadata(self, datastore_id: str, document_id: str) -> dict:
        """
        Get details of a given document, including its name and ingestion job status.

        Args:
            datastore_id (str): Datastore ID of the datastore from which to retrieve the document
            document_id (str): Document ID of the document to retrieve details for

        Returns:
            dict: JSON response containing document metadata including:
                - name: Name of the document
                - status: Status of the ingestion job

        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        # Construct the endpoint
        endpoint = f"/datastores/{datastore_id}/documents/{document_id}/metadata"

        # Make GET request using the helper method
        response = self._fetch_with_access_token(path=endpoint, method="GET")
        return response.json()

    def delete_document(self, datastore_id: str, document_id: str) -> dict:
        """
        Delete a given document from its Datastore. This operation is irreversible.

        Args:
            datastore_id (str): Datastore ID of the datastore from which to delete the document
            document_id (str): Document ID of the document to delete

        Returns:
            dict: JSON response confirming the deletion

        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        # Construct the endpoint
        endpoint = f"/datastores/{datastore_id}/documents/{document_id}"

        # Make DELETE request using the helper method
        response = self._fetch_with_access_token(path=endpoint, method="DELETE")
        return response.json()

    # Application APIs
    def list_applications(
        self, limit: Optional[int] = 1000, cursor: Optional[str] = None
    ) -> dict:
        """
        Retrieve a list of all Applications with pagination.

        Args:
            limit (int, optional): Maximum number of applications to return (1-1000, defaults to 1000)
            cursor (str, optional): Cursor from previous call to get next set of results

        Returns:
            dict: JSON response containing list of applications and pagination details

        Raises:
            ValueError: If limit is outside valid range
        """
        endpoint = "/applications"

        # Validate limit
        if limit is not None and not 1 <= limit <= 1000:
            raise ValueError("Limit must be between 1 and 1000")

        # Build query parameters
        params = {}
        if limit is not None:
            params["limit"] = limit
        if cursor is not None:
            params["cursor"] = cursor

        response = self._fetch_with_access_token(
            path=endpoint, method="GET", params=params
        )
        return response.json()

    def create_application(
        self,
        name: str,
        description: Optional[str] = None,
        datastore_ids: Optional[List[str]] = None,
        system_prompt: Optional[str] = None,
    ) -> dict:
        """
        Create a new Application with specified configuration.

        Args:
            name (str): Name of the application (required, length between 3 and 200)
            description (str, optional): Description of the application (length between 3 and 500)
            datastore_ids (list[str], optional): List of datastore IDs associated with the application.
                Provide at most one datastore. Leave empty to automatically create a new datastore.
            system_prompt (str, optional): Instructions for the RAG system to reference when generating
                responses (length ≤ 3400)

        Returns:
            dict: JSON response from the API containing the created application details

        Raises:
            ValueError: If name length is invalid
        """
        endpoint = "/applications"

        # Validate name length
        if not 3 <= len(name) <= 200:
            raise ValueError("Name must be between 3 and 200 characters")

        # Validate description length if provided
        if description and not 3 <= len(description) <= 500:
            raise ValueError("Description must be between 3 and 500 characters")

        # Validate system prompt length if provided
        if system_prompt and len(system_prompt) > 3400:
            raise ValueError("System prompt must not exceed 3400 characters")

        # Validate datastore_ids if provided
        if datastore_ids and len(datastore_ids) > 1:
            raise ValueError(
                "Provide at most one datastore ID. Support for multiple datastores is coming soon."
            )

        json = {"name": name}

        # Add optional parameters if provided
        if description:
            json["description"] = description
        if datastore_ids:
            json["datastore_ids"] = datastore_ids
        if system_prompt:
            json["system_prompt"] = system_prompt

        response = self._fetch_with_access_token(
            path=endpoint, method="POST", json=json
        )
        return response.json()

    def edit_application(
        self,
        application_id: str,
        datastore_ids: Optional[List[str]] = None,
        system_prompt: Optional[str] = None,
        llm_model_id: Optional[str] = None,
    ) -> dict:
        """
        Modify an existing Application with the provided configuration.
        Only included fields will be modified.

        Args:
            application_id (str): The ID of the application to edit (required)
            datastore_ids (list[str], optional): List of datastore IDs to associate with the application.
                Must provide exactly one datastore ID.
            system_prompt (str, optional): Instructions for the RAG system to reference when generating
                responses (length ≤ 3400)
            llm_model_id (str, optional): Model ID of a tuned model to use for generation.
                Must be tuned on this application. Set to 'default' to use the default model.

        Returns:
            dict: JSON response from the API containing the updated application details

        Raises:
            ValueError: If system_prompt length is invalid
        """
        endpoint = f"/applications/{application_id}"

        # Initialize empty body
        json = {}

        # Validate and add datastore_ids if provided
        if datastore_ids:
            if len(datastore_ids) != 1:
                raise ValueError(
                    "Must provide exactly one datastore ID. Support for multiple datastores is coming soon."
                )
            json["datastore_ids"] = datastore_ids

        # Validate and add system_prompt if provided
        if system_prompt:
            if len(system_prompt) > 3400:
                raise ValueError("System prompt must not exceed 3400 characters")
            json["system_prompt"] = system_prompt

        # Add llm_model_id if provided
        if llm_model_id:
            json["llm_model_id"] = llm_model_id

        response = self._fetch_with_access_token(path=endpoint, method="PUT", json=json)
        return response.json()

    def delete_application(self, application_id: str) -> dict:
        """
        Delete an Application. This is an irreversible operation.
        Note: Associated Datastores will not be deleted automatically.

        Args:
            application_id (str): The ID of the application to delete

        Returns:
            dict: JSON response from the API confirming deletion

        Raises:
            requests.exceptions.RequestException: If the delete request fails
        """
        endpoint = f"/applications/{application_id}"

        response = self._fetch_with_access_token(path=endpoint, method="DELETE")
        return response.json()

    def get_application_metadata(self, application_id: str) -> dict:
        """
        Get metadata and configuration of a given Application.

        Args:
            application_id (str): The ID of the application to retrieve details for

        Returns:
            dict: JSON response containing the application's metadata and configuration

        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        endpoint = f"/applications/{application_id}/metadata"

        response = self._fetch_with_access_token(path=endpoint, method="GET")
        return response.json()

    # Chat/Feedback APIs
    def query(
        self,
        application_id: str,
        messages: List[dict],
        *,
        stream: bool = False,
        conversation_id: Optional[str] = None,
        model_id: Optional[str] = None,
    ) -> dict:
        """
        Start a conversation with an Application and receive its generated response.

        Args:
            application_id (str): The ID of the application to query
            messages (List[dict]): List of message objects in the conversation
            stream (bool, optional): Whether to receive a streamed response (defaults to False)
            conversation_id (str, optional): Conversation ID - alternative to providing message history.
                If provided, history in messages will be ignored.
            model_id (str, optional): ID of specific fine-tuned or aligned model to use.
                Defaults to base model if not specified.

        Returns:
            dict: JSON response containing the application's response, retrieved data and attributions

        Raises:
            ValueError: If required parameters are missing
            requests.exceptions.RequestException: If the request fails
        """
        endpoint = f"/applications/{application_id}/query"

        # Validate required parameters
        if not messages and not conversation_id:
            raise ValueError("Either messages or conversation_id must be provided")

        if stream:
            raise ValueError("Streamed responses are not supported yet")

        # Build request body
        json = {"messages": messages, "stream": stream}

        # Add optional parameters
        if conversation_id is not None:
            json["conversation_id"] = conversation_id
        if model_id is not None:
            json["model_id"] = model_id

        response = self._fetch_with_access_token(
            path=endpoint, method="POST", json=json
        )
        return response.json()

    def provide_feedback(
        self,
        application_id: str,
        message_id: str,
        feedback: Literal["thumbs_up", "thumbs_down", "flagged", "removed"],
        *,
        explanation: Optional[str] = None,
        content_id: Optional[str] = None,
    ) -> dict:
        """
        Provide feedback for a generation or retrieval.

        Args:
            application_id (str): The ID of the application to provide feedback for
            message_id (str): ID of the message to provide feedback on
            feedback (str): Feedback type. Must be one of: "thumbs_up", "thumbs_down", "flagged", "removed"
                Use "removed" to undo previously provided feedback.
            explanation (str, optional): Optional explanation for the feedback
            content_id (str, optional): Content ID for retrieval feedback.
                Leave as None for generation feedback.

        Returns:
            dict: JSON response confirming the feedback submission

        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        endpoint = f"/applications/{application_id}/feedback"

        # Build request body
        json = {"message_id": message_id, "feedback": feedback}

        # Add optional parameters
        if explanation is not None:
            json["explanation"] = explanation
        if content_id is not None:
            json["content_id"] = content_id

        response = self._fetch_with_access_token(
            path=endpoint, method="POST", json=json
        )
        return response.json()

    # Evaluation APIs
    def create_evaluation(
        self,
        application_id: str,
        metrics: List[Literal["equivalence", "factuality", "unit_test"]],
        *,
        evalset_file: Optional[str] = None,
        dataset_name: Optional[str] = None,
        model_name: Optional[str] = None,
    ) -> dict:
        """
        Launch an evaluation round for an Application using specified metrics and evaluation data.

        The evaluation can use either an uploaded CSV file or a previously created dataset.
        Supported metrics are 'equivalence', 'factuality', and 'unit_test'.

        Args:
            application_id (str): Application ID of the application to evaluate
            metrics (List[str]): List of metrics to use for evaluation
            evalset_file (str, optional): Path to CSV file containing evaluation data.
                Must include 'prompt' and 'reference' columns, plus additional columns
                based on selected metrics
            dataset_name (str, optional): Name of the dataset created through the dataset API
            model_name (str, optional): Model name of the tuned or aligned model to use.
                Defaults to the default model if not specified.

        Returns:
            dict: JSON response containing evaluation details

        Raises:
            ValueError: If neither or both evalset_file and dataset_name are provided
            FileNotFoundError: If evalset_file is provided but doesn't exist
            requests.exceptions.RequestException: If the request fails
        """
        # Validate input parameters
        if (evalset_file is None and dataset_name is None) or (
            evalset_file is not None and dataset_name is not None
        ):
            raise ValueError(
                "Either evalset_file or dataset_name must be provided, but not both"
            )

        # Construct the endpoint
        endpoint = f"/applications/{application_id}/evaluate"

        # Prepare the request
        data = {"metrics": metrics}

        if model_name:
            data["model_name"] = model_name

        if evalset_file:
            # Check if file exists
            if not os.path.exists(evalset_file):
                raise FileNotFoundError(f"File not found: {evalset_file}")

            # Prepare multipart form data with file
            files = {
                "evalset_file": (
                    os.path.basename(evalset_file),
                    open(evalset_file, "rb"),
                    "text/csv",
                )
            }

            # Make POST request with file upload
            response = self._fetch_with_access_token(
                path=endpoint,
                method="POST",
                data=data,
                files=files,
            )

        elif dataset_name:
            # Prepare JSON payload for dataset_name case
            data["dataset_name"] = dataset_name

            # Make POST request with JSON payload
            response = self._fetch_with_access_token(
                path=endpoint, method="POST", data=data
            )

        return response.json()

    def list_evaluations(
        self,
        application_id: str,
        limit: Optional[int] = 1000,
        cursor: Optional[str] = None,
    ) -> dict:
        """
        List all Evaluations for a specific Application with pagination support.

        Args:
            application_id (str): Application ID for which to retrieve evaluations
            limit (int, optional): Maximum number of evaluations to return (1-1000, defaults to 1000)
            cursor (str, optional): Cursor from previous call to get next set of results

        Returns:
            dict: JSON response containing list of evaluations and pagination details

        Raises:
            ValueError: If limit is outside valid range
            requests.exceptions.RequestException: If the request fails
        """
        # Validate limit
        if limit is not None and not 1 <= limit <= 1000:
            raise ValueError("Limit must be between 1 and 1000")

        endpoint = f"/applications/{application_id}/evaluate/jobs"

        # Build query parameters
        params = {}
        if limit is not None:
            params["limit"] = limit
        if cursor is not None:
            params["cursor"] = cursor

        response = self._fetch_with_access_token(
            path=endpoint, method="GET", params=params
        )
        return response.json()

    def get_evaluation_metadata(self, application_id: str, job_id: str) -> dict:
        """
        Get status and results for a specific Evaluation round.

        Args:
            application_id (str): Application ID for which to retrieve the evaluation
            job_id (str): Evaluation round ID to retrieve status and results for

        Returns:
            dict: JSON response containing evaluation metadata and results

        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        endpoint = f"/applications/{application_id}/evaluate/jobs/{job_id}/metadata"

        response = self._fetch_with_access_token(path=endpoint, method="GET")
        return response.json()

    def cancel_evaluation(self, application_id: str, job_id: str) -> dict:
        """
        Cancel a specific Evaluation round.

        Args:
            application_id (str): Application ID for which to cancel the evaluation
            job_id (str): Evaluation round ID to cancel

        Returns:
            dict: JSON response confirming the cancellation

        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        endpoint = f"/applications/{application_id}/evaluate/jobs/{job_id}"

        response = self._fetch_with_access_token(path=endpoint, method="DELETE")
        return response.json()

    # Dataset APIs
    def list_datasets(
        self,
        application_id: str,
        dataset_name: Optional[str] = None,
        limit: Optional[int] = 1000,
        cursor: Optional[str] = None,
    ) -> dict:
        """
        List all Datasets and their versions for a specific Application.

        Args:
            application_id (str): Application ID for which to list associated datasets
            dataset_name (str, optional): Dataset name to filter results by
            limit (int, optional): Maximum number of datasets to return (1-1000, defaults to 1000)
            cursor (str, optional): Cursor from previous call to get next set of results

        Returns:
            dict: JSON response containing list of datasets, their versions, metadata and schema

        Raises:
            ValueError: If limit is outside valid range
            requests.exceptions.RequestException: If the request fails
        """
        # Validate limit
        if limit is not None and not 1 <= limit <= 1000:
            raise ValueError("Limit must be between 1 and 1000")

        endpoint = f"/applications/{application_id}/datasets"

        # Build query parameters
        params = {}
        if dataset_name is not None:
            params["dataset_name"] = dataset_name
        if limit is not None:
            params["limit"] = limit
        if cursor is not None:
            params["cursor"] = cursor

        response = self._fetch_with_access_token(
            path=endpoint, method="GET", params=params
        )
        return response.json()

    def create_dataset(
        self, application_id: str, dataset_name: str, dataset_type: str, file_path: str
    ) -> dict:
        """
        Create a new Dataset in the specified Application using a JSONL file.

        The dataset file must conform to the schema defined for the dataset_type.
        For 'evaluation_set' type, each line in the JSONL file must be a JSON object with:
            - response (optional, string): Optional response to evaluate
            - reference (required, string): Required reference or ground truth response
            - guideline (optional, string): Optional evaluation guidelines
            - knowledge (optional, string): Optional context for evaluation

        Args:
            application_id (str): Application ID to associate with the dataset
            dataset_name (str): Name of the dataset
            dataset_type (str): Type of dataset which determines its schema and validation rules
            file_path (str): Path to the JSONL file containing the dataset

        Returns:
            dict: JSON response containing the created dataset details

        Raises:
            ValueError: If dataset_type is not supported or file is not JSONL format
            FileNotFoundError: If the specified file does not exist
            requests.exceptions.RequestException: If the request fails
        """
        # Validate file extension
        if not file_path.lower().endswith(".jsonl"):
            raise ValueError("File must be in JSONL format with .jsonl extension")

        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # Construct the endpoint
        endpoint = f"/applications/{application_id}/datasets"

        # Prepare the file for upload
        files = {
            "file": (
                os.path.basename(file_path),
                open(file_path, "rb"),
                "application/jsonl",
            )
        }

        # Prepare the form data
        data = {"dataset_name": dataset_name, "dataset_type": dataset_type}

        # Make POST request using the helper method
        response = self._fetch_with_access_token(
            path=endpoint, method="POST", files=files, data=data
        )
        return response.json()

    def get_dataset(
        self,
        application_id: str,
        dataset_name: str,
        *,
        version: Optional[str] = None,
        batch_size: Optional[int] = 64,
        output_file: Optional[str] = None,
    ) -> List[dict]:
        """
        Stream the raw content of a Dataset version. If no version is specified,
        the latest version is used.

        The Dataset content is downloaded in batches. The function can either return
        an iterator of the content chunks or save directly to a file.

        Args:
            application_id (str): Application ID associated with the dataset
            dataset_name (str): Name of the dataset to retrieve
            version (str, optional): Version number of the dataset to retrieve.
                Defaults to the latest version if not specified
            batch_size (int, optional): Batch size for processing. Must be between
                1 and 1000. Defaults to 64
            output_file (str, optional): Path where to save the downloaded content.
                If not provided, returns an iterator of content chunks

        Returns:
            Iterator[bytes] | None: If output_file is None, returns an iterator of content
                chunks. If output_file is provided, saves to file and returns None

        Raises:
            ValueError: If batch_size is outside allowed range
            requests.exceptions.RequestException: If the request fails
            IOError: If unable to write to output_file
        """
        # Validate batch_size
        if batch_size is not None:
            if not isinstance(batch_size, int) or batch_size < 1 or batch_size > 1000:
                raise ValueError("batch_size must be an integer between 1 and 1000")

        # Construct the endpoint
        endpoint = f"/applications/{application_id}/datasets/{dataset_name}"

        # Build query parameters
        params = {}
        if version is not None:
            params["version"] = version
        if batch_size is not None:
            params["batch_size"] = batch_size

        # Make GET request using the helper method with stream=True
        response = self._fetch_with_access_token(
            path=endpoint,
            method="GET",
            params=params,
        )
        return [json.loads(line) for line in response.text.strip().split("\n")]

    def append_dataset(
        self, application_id: str, dataset_name: str, dataset_type: str, file_path: str
    ) -> dict:
        """
        Append content to an existing Dataset, creating a new version.

        The appended content must conform to the schema of the existing dataset.
        For 'evaluation_set' type, each line in the JSONL file must be a JSON object with:
            - response (optional, string): Optional response to evaluate
            - reference (required, string): Required reference or ground truth response
            - guideline (optional, string): Optional evaluation guidelines
            - knowledge (optional, string): Optional context for evaluation

        Args:
            application_id (str): Application ID to associate with the dataset
            dataset_name (str): Name of the dataset
            dataset_type (str): Type of dataset which determines its schema and validation rules
            file_path (str): Path to the JSONL file containing the dataset

        Returns:
            dict: JSON response containing the created dataset details

        Raises:
            ValueError: If dataset_type is not supported or file is not JSONL format
            FileNotFoundError: If the specified file does not exist
            requests.exceptions.RequestException: If the request fails
        """
        # Validate file extension
        if not file_path.lower().endswith(".jsonl"):
            raise ValueError("File must be in JSONL format with .jsonl extension")

        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # Construct the endpoint
        endpoint = f"/applications/{application_id}/datasets"

        # Prepare the file for upload
        files = {
            "file": (
                os.path.basename(file_path),
                open(file_path, "rb"),
                "application/jsonl",
            )
        }

        # Prepare the form data
        data = {"dataset_name": dataset_name, "dataset_type": dataset_type}

        # Make POST request using the helper method
        response = self._fetch_with_access_token(
            path=endpoint, method="PUT", files=files, data=data
        )
        return response.json()

    def delete_dataset(self, application_id: str, dataset_name: str) -> dict:
        """
        Delete a Dataset and all its versions permanently.

        Args:
            application_id (str): Application ID associated with the dataset
            dataset_name (str): Name of the dataset to delete

        Returns:
            dict: JSON response confirming the deletion

        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        endpoint = f"/applications/{application_id}/datasets/{dataset_name}"

        response = self._fetch_with_access_token(path=endpoint, method="DELETE")
        return response.json()

    def get_dataset_metadata(
        self, application_id: str, dataset_name: str, version: Optional[str] = None
    ) -> dict:
        """
        Retrieve metadata and schema details for a specific Dataset version.
        If no version is specified, retrieves details for the latest version.

        Args:
            application_id (str): Application ID associated with dataset
            dataset_name (str): Name of the dataset to retrieve details for
            version (str, optional): Version number of the dataset. Defaults to latest if not specified

        Returns:
            dict: JSON response containing dataset metadata and schema

        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        endpoint = f"/applications/{application_id}/datasets/{dataset_name}/metadata"

        # Build query parameters
        params = {}
        if version is not None:
            params["version"] = version

        response = self._fetch_with_access_token(
            path=endpoint, method="GET", params=params
        )
        return response.json()

    # Tuning APIs
    def create_tune_job(
        self,
        application_id: str,
        training_file: str,
        *,
        test_file: Optional[str] = None,
        model_id: Optional[str] = None,
    ) -> dict:
        """
        Create a tuning job for the specified Application to specialize it for a specific
        domain or use case.

        The training and test files should be in JSON array format, where each element
        represents a training example with the following required fields:
            - guideline (str): Description of the expected response
            - prompt (str): Question or statement for the model to respond to
            - response (str): Model's response to the prompt
            - knowledge (List[str]): Array of knowledge pieces for response generation

        Args:
            application_id (str): Application ID of the application to tune
            training_file (str): Path to the training data file in JSON format
            test_file (str, optional): Path to the test data file in JSON format.
                If not provided, a portion of training data will be used as test set
            model_id (str, optional): ID of an existing model to tune.
                Defaults to the application's default model if not specified

        Returns:
            dict: JSON response containing the tune job ID and other metadata

        Raises:
            ValueError: If files are not in JSON format
            FileNotFoundError: If specified files do not exist
            requests.exceptions.RequestException: If the request fails
        """
        # Validate training file
        if not (
            training_file.lower().endswith(".json")
            or training_file.lower().endswith(".jsonl")
        ):
            raise ValueError(
                "Training file must be in JSON format with .json extension"
            )
        if not os.path.exists(training_file):
            raise FileNotFoundError(f"Training file not found: {training_file}")

        # Validate test file if provided
        if test_file:
            if not (
                test_file.lower().endswith(".json")
                or test_file.lower().endswith(".jsonl")
            ):
                raise ValueError(
                    "Test file must be in JSON format with .json extension"
                )
            if not os.path.exists(test_file):
                raise FileNotFoundError(f"Test file not found: {test_file}")

        # Construct the endpoint
        endpoint = f"/applications/{application_id}/tune"

        # Prepare the files for upload
        files = {
            "training_file": (
                os.path.basename(training_file),
                open(training_file, "rb"),
                "application/json",
            )
        }

        if test_file:
            files["test_file"] = (
                os.path.basename(test_file),
                open(test_file, "rb"),
                "application/json",
            )

        # Prepare the form data
        data = {}
        if model_id:
            data["model_id"] = model_id

        # Make POST request using the helper method
        response = self._fetch_with_access_token(
            path=endpoint, method="POST", files=files, data=data
        )
        return response.json()

    def list_tune_jobs(
        self,
        application_id: str,
        limit: Optional[int] = 1000,
        cursor: Optional[str] = None,
    ) -> dict:
        """
        List all tune jobs for a specific Application with pagination support.
        Includes status, evaluation results, and model IDs for each job.

        Args:
            application_id (str): Application ID of the application to list tuning jobs for
            limit (int, optional): Maximum number of tune jobs to return (1-1000, defaults to 1000)
            cursor (str, optional): Cursor from previous call to get next set of results

        Returns:
            dict: JSON response containing list of tune jobs and their details

        Raises:
            ValueError: If limit is outside valid range
            requests.exceptions.RequestException: If the request fails
        """
        # Validate limit
        if limit is not None and not 1 <= limit <= 1000:
            raise ValueError("Limit must be between 1 and 1000")

        endpoint = f"/applications/{application_id}/tune/jobs"

        # Build query parameters
        params = {}
        if limit is not None:
            params["limit"] = limit
        if cursor is not None:
            params["cursor"] = cursor

        response = self._fetch_with_access_token(
            path=endpoint, method="GET", params=params
        )
        return response.json()

    def get_tune_job(self, application_id: str, job_id: str) -> dict:
        """
        Retrieve the status and details of a specific tune job.

        Args:
            application_id (str): Application ID of the application associated with the tuning job
            job_id (str): ID of the tuning job to retrieve the status for

        Returns:
            dict: JSON response containing tune job status and evaluation results

        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        endpoint = f"/applications/{application_id}/tune/jobs/{job_id}/metadata"

        response = self._fetch_with_access_token(path=endpoint, method="GET")
        return response.json()

    def cancel_tune_job(self, application_id: str, job_id: str) -> dict:
        """
        Cancel a specific tuning job.
        If the job is in progress, it will be terminated.
        If the job has completed, the tuned model will not be deleted.

        Args:
            application_id (str): Application ID of the application associated with the tuning job
            job_id (str): ID of the tuning job to cancel

        Returns:
            dict: JSON response confirming the cancellation

        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        endpoint = f"/applications/{application_id}/tune/jobs/{job_id}"

        response = self._fetch_with_access_token(path=endpoint, method="DELETE")
        return response.json()

    def list_tuned_models(
        self,
        application_id: str,
        limit: Optional[int] = 1000,
        cursor: Optional[str] = None,
    ) -> dict:
        """
        List all tuned models associated with a specific Application.

        Args:
            application_id (str): Application ID of the application from which to retrieve tuned models
            limit (int, optional): Maximum number of models to return (1-1000, defaults to 1000)
            cursor (str, optional): Cursor from previous call to get next set of results

        Returns:
            dict: JSON response containing list of tuned models

        Raises:
            ValueError: If limit is outside valid range
            requests.exceptions.RequestException: If the request fails
        """
        # Validate limit
        if limit is not None and not 1 <= limit <= 1000:
            raise ValueError("Limit must be between 1 and 1000")

        endpoint = f"/applications/{application_id}/tune/models"

        # Build query parameters
        params = {}
        if limit is not None:
            params["limit"] = limit
        if cursor is not None:
            params["cursor"] = cursor

        response = self._fetch_with_access_token(
            path=endpoint, method="GET", params=params
        )
        return response.json()

    def _fetch_with_access_token(
        self,
        path: str,
        method: str,
        *,
        content_type: Optional[str] = None,
        data: Optional[dict] = None,
        params: Optional[dict] = None,
        json: Optional[dict] = None,
        files: Optional[dict] = None,
    ) -> requests.Response:
        """
        Makes an authenticated request to the Contextual AI API.

        Args:
            path (str): API endpoint path
            method (str): HTTP method ('GET', 'POST', 'PUT', or 'DELETE')
            content_type (str, optional): Content type for POST/PUT requests
            params (dict, optional): Query parameters for GET requests
            data (dict, optional): Request body for POST/PUT requests
            json (dict, optional): JSON data for POST/PUT requests
            files (dict, optional): Files to upload

        Returns:
            requests.Response: Response from the API

        Raises:
            NotImplementedError: If the HTTP method is not supported
        """
        headers = {
            "authorization": f"Bearer {self.contextual_api_key}",
            "accept": "application/json",
        }
        if content_type:
            headers["content-type"] = content_type

        url = f"{self.settings.API_BASE_URL}{path}"

        return requests.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            data=data,
            json=json,
            files=files,
        )
