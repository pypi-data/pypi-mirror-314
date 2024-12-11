import base64
import os
from pprint import pprint

import requests
from gql import Client, gql
from gql.transport.exceptions import TransportQueryError
from gql.transport.requests import RequestsHTTPTransport


def upload_to_platform(params: dict):
    """
    Upload an image to the platform using GraphQL API. The function handles both the file upload process and assigns the uploaded image to a project.

    Parameters:
    - params (dict): Dictionary containing the following keys:
        - team_name (str): Team identifier for authentication.
        - access_key (str): API access key for authentication.
        - project_id (str): The project ID to which the uploaded data will be assigned.
        - binary_data (bytes): The binary data of the image to be uploaded.
        - file_type (str): The file type of the image (e.g., 'jpg', 'png').
        - file_size (int): The size of the image file in bytes.
        - data_key (str): The unique identifier for the image.
        - dataset_name (str): The dataset name to which the image is being uploaded.

    Raises:
    - Exception: If an unexpected error occurs during the upload or project assignment process.
    """

    url = "https://api.superb-ai.com/v3/graphql"

    auth_value = f"{params['team_name']}:{params['access_key']}"
    encoded_auth = base64.b64encode(auth_value.encode("utf-8")).decode("utf-8")

    headers = {
        "X-Api-Key": params["access_key"],
        "X-Tenant-Id": params["team_name"],
        "Authorization": f"Basic {encoded_auth}",
    }

    transport = RequestsHTTPTransport(
        url=url,
        use_json=True,
        headers=headers,
    )

    graphql_client = Client(
        transport=transport,
        fetch_schema_from_transport=True,
    )

    try:
        # Step 1: Create datum
        response_upload = create_datum(graphql_client, params)
        if "error_code" in response_upload:
            return response_upload

        presigned_url = response_upload["createDatum"]["uploadUrl"]["url"][
            "image_url"
        ]
        data_id = response_upload["createDatum"]["id"]

        # Step 2: Upload image
        upload_status = upload_image(presigned_url, params)
        if "error_code" in upload_status:
            return upload_status

        if upload_status["success"]:
            # Step 3: Create label
            label_result = create_label(
                graphql_client, params["project_id"], data_id
            )
            if "error_code" in label_result:
                return label_result

            return {
                "success": 200,
                "message": "Image uploaded and label created successfully",
            }
        else:
            return {
                "error_code": upload_status["response"].status_code,
                "message": "Image upload failed",
            }

    except Exception as e:
        return {"error_code": None, "message": str(e)}


def create_datum(client, params):
    query_upload = gql(
        """
        mutation($type: String!, $fileInfo: JSONObject!) {
            createDatum(type: $type, fileInfo: $fileInfo) {
                id
                uploadUrl
                dataKey
            }
        }
    """
    )
    params_upload = {
        "type": "img-presigned-url",
        "fileInfo": {
            "key": params["data_key"],
            "group": params["dataset_name"],
            "file_name": params["data_key"],
            "file_size": params["file_size"],
        },
    }
    try:
        return client.execute(query_upload, variable_values=params_upload)
    except TransportQueryError as e:
        error_dict = e.errors[0]
        return {
            "error_code": error_dict.get("extensions", {}).get("code"),
            "message": "Conflict error: The datum you're trying to create already exists.",
        }


def upload_image(presigned_url, params):
    headers_upload = {
        "Content-Type": f"image/{params['file_type']}",
        "Content-Length": str(params["file_size"]),
    }
    try:
        response = requests.put(
            presigned_url,
            data=params["binary_data"],
            headers=headers_upload,
        )
        return {"success": response.status_code == 200, "response": response}
    except Exception as e:
        return {"error_code": None, "message": str(e)}


def create_label(client, project_id, data_id):
    query_label = gql(
        """
        mutation ($projectId: String!, $dataId: String!) {
            createLabel(projectId: $projectId, dataId: $dataId)
        }
    """
    )
    params = {
        "projectId": str(project_id),
        "dataId": str(data_id),
    }
    try:
        return client.execute(query_label, variable_values=params)
    except TransportQueryError as e:
        error_dict = e.errors[0]
        return {
            "error_code": error_dict.get("extensions", {}).get("code"),
            "message": "Conflict error: The label you're trying to create already exists.",
        }
