"""
Defines a `Mattermost` class to interact with the Mattermost API for sending messages, uploading files,
and handling API requests with error handling.

The `Mattermost` class provides methods to:
1. Send GET and POST requests with appropriate authorization headers.
2. Send messages to a specified Mattermost channel.
3. Upload files to Mattermost and attach them to messages.

Custom exceptions, `ReqError` and `NotFoundError`, are raised for request errors and not-found scenarios.
"""
import json
from typing import Union, Optional
import logging

import httpx
from .exceptions import *

main_logger = logging.getLogger(__name__)


class Mattermost:
    """
    Class for interacting with the Mattermost API.

    Attributes:
        url (str): The base URL for the Mattermost API.
        token (str): The authorization token for the bot.
        channel_id (str): The ID of the Mattermost channel to send messages to.
    """
    def __init__(self, url: str, token: str, channel_id):
        self.url = url
        self.token = token
        self.channel_id = channel_id

    async def _send_get(self, url, params: dict = None):
        """
        Sends an asynchronous GET request to a specified Mattermost API endpoint.

        Args:
            url (str): The endpoint URL.
            params (dict, optional): Query parameters for the GET request.

        Returns:
            dict: Parsed JSON response.

        Raises:
            ReqError: If the request fails.
            NotFoundError: If the resource is not found.
        """
        headers = {"Authorization": f"Bearer {self.token}"}

        async with httpx.AsyncClient() as client:
            try:
                main_logger.info("Get from %s", url)
                result = await client.get(url, params=params, headers=headers, timeout=10)
            except httpx.HTTPError as e:
                raise ReqError(e) from e

        if result.status_code not in [200, 201]:
            if result.status_code == 404:
                raise NotFoundError("Not found somewhere")
            raise ReqError(f"Got error status code, {result.status_code}")

        parsed_response = json.loads(result.text)
        return parsed_response

    async def _send_post(self, url, data: Union[str, dict, None] = None,
                         json_content: bool = True, content: Optional[bytes] = None):
        """
        Sends an asynchronous POST request to a specified Mattermost API endpoint.

        Args:
            url (str): The endpoint URL.
            data (Union[str, dict, None], optional): The payload data.
            json_content (bool, optional): Whether to set the content type to JSON.
            content (bytes, optional): Raw byte content for file uploads.

        Returns:
            dict: Parsed JSON response.

        Raises:
            ReqError: If the request fails.
            NotFoundError: If the resource is not found.
        """
        headers = {"Authorization": f"Bearer {self.token}"}
        if data is not None and json_content:
            headers['Content-Type'] = 'application/json'

        async with httpx.AsyncClient() as client:
            try:
                main_logger.info("Post to %s", url)
                result = await client.post(url, headers=headers, data=data, content=content)
            except httpx.HTTPError as e:
                raise ReqError(e) from e

        if result.status_code not in [200, 201]:
            if result.status_code == 404:
                raise NotFoundError("Not found somewhere")
            raise ReqError(f"Got error status code, {result.status_code}")

        parsed_response = json.loads(result.text)
        return parsed_response

    async def send_message(self, message: str, file_ids: Optional[list[str]] = None):
        """
        Sends a message to the specified Mattermost channel.

        Args:
            message (str): The message content.
            file_ids (Optional[list[str]], optional): List of file IDs to attach to the message.
        """
        url = self.url + "/api/v4/posts"

        schema = {
            "channel_id": self.channel_id,
            "message": message,
            "file_ids": file_ids
        }

        await self._send_post(url, data=json.dumps(schema), json_content=True)

    async def upload_file(self, filename: str, content: bytes):
        """
        Uploads a file to the Mattermost channel and returns the file ID.

        Args:
            filename (str): The name of the file.
            content (bytes): The file content in bytes.

        Returns:
            str: The ID of the uploaded file.
        """
        url = self.url + f"/api/v4/files?channel_id={self.channel_id}&filename={filename}"
        # params = {"channel_id": self.channel_id, "filename": filename}
        r = await self._send_post(url, content=content, json_content=False)
        return r["file_infos"][0]["id"]

    async def send_message_with_files(self, message: str, additional_files: list[tuple[str, bytes]]):
        """
        Sends a message with attached files to the specified Mattermost channel.

        Args:
            message (str): The message content.
            additional_files (list[tuple[str, bytes]]): List of tuples with filename and file content.
        """
        ids = []
        for file in additional_files:
            name, content = file
            ids.append(await self.upload_file(name, content))

        await self.send_message(message, ids)
