# Mattermost Integration Library

This library provides a straightforward and asynchronous way to interact with the Mattermost API. It allows sending messages, uploading files, and seamlessly handling API requests, complete with robust error handling. By using this library, you can integrate your Python-based services with your Mattermost workspace efficiently and reliably.

## Key Features

- **Asynchronous Communication:** Leverages `httpx.AsyncClient` for performing non-blocking I/O operations.
- **Message Sending:** Post messages directly into a specified Mattermost channel.
- **File Uploads:** Upload files (images, documents, and more) to Mattermost and include them in posted messages.
- **Robust Error Handling:** Raises custom exceptions (`ReqError` and `NotFoundError`) to make troubleshooting and handling HTTP errors simpler.

## Requirements

- Python 3.9+ (recommended)
- A Mattermost server endpoint that you have access to.
- A valid Mattermost user/bot token.
- A specific channel ID from your Mattermost server where messages and files will be posted.

## Installation

You can install this library with standard Python tools. For example:

```bash
pip install -r requirements.txt
```

Make sure `httpx` and other dependencies are listed in your `requirements.txt` and installed.

## Usage Example

Before using the `Mattermost` class, ensure that:
- You have a Mattermost URL (e.g., `https://mattermost.example.com`).
- You have a valid Mattermost bot token (e.g., generated from the Mattermost system console or developer tools).
- You know the channel ID where you want to post messages and upload files.

**Important:** Do not use placeholders. Provide real, working values for `url`, `token`, and `channel_id` when creating an instance of `Mattermost`. For instance, if your Mattermost instance runs at `https://mattermost.example.com`, your token is `xoxb-abc1234exampletoken`, and your target channel ID is `1234567890abcde`, then use those exact values directly.

### Sending a Simple Message

```python
import asyncio
from mattermost_integration import Mattermost  # adjust the import path as needed

async def main():
    # Replace values below with your real Mattermost details
    url = "https://mattermost.example.com"
    token = "xoxb-abc1234exampletoken"
    channel_id = "1234567890abcde"

    mm = Mattermost(url, token, channel_id)

    # Send a simple text message
    await mm.send_message("Hello from the Mattermost integration library!")

asyncio.run(main())
```

### Uploading a File and Sending It with a Message

If you want to send an image, document, or any other file type, you can upload it first and then attach it to a message:

```python
import asyncio
from mattermost_integration import Mattermost  # adjust the import path as needed

async def main():
    url = "https://mattermost.example.com"
    token = "xoxb-abc1234exampletoken"
    channel_id = "1234567890abcde"
    
    mm = Mattermost(url, token, channel_id)

    # Assume we have some file content in memory. For example, read a local file:
    with open("path/to/yourfile.png", "rb") as f:
        file_content = f.read()

    # Upload the file
    file_id = await mm.upload_file("yourfile.png", file_content)

    # Send a message with the uploaded file attached
    await mm.send_message("Here's the file you requested:", file_ids=[file_id])

asyncio.run(main())
```

### Sending Multiple Files at Once

```python
import asyncio
from mattermost_integration import Mattermost  # adjust the import path as needed

async def main():
    url = "https://mattermost.example.com"
    token = "xoxb-abc1234exampletoken"
    channel_id = "1234567890abcde"

    mm = Mattermost(url, token, channel_id)

    additional_files = []
    for file_path in ["path/to/file1.pdf", "path/to/file2.jpg"]:
        with open(file_path, "rb") as f:
            file_content = f.read()
        additional_files.append((file_path.split("/")[-1], file_content))

    await mm.send_message_with_files("Here are the documents you wanted.", additional_files)

asyncio.run(main())
```

## Error Handling

This library defines custom exceptions to help you handle errors gracefully:

- **`ReqError`**: Raised if a request fails due to non-200/201 status codes, excluding 404.
- **`NotFoundError`**: Raised specifically if a requested resource (e.g., a channel or file) is not found (404).

You can wrap your API calls in try-except blocks to manage these conditions:

```python
try:
    await mm.send_message("Testing error handling.")
except ReqError as e:
    print(f"Request failed: {e}")
except NotFoundError:
    print("The requested resource was not found!")
```

## Logging

The library uses Python’s built-in `logging` for informational messages. Configure the logging as desired in your application to display or store logs, for example:

```python
import logging

logging.basicConfig(level=logging.INFO)
```

With the logging level set to `INFO`, you’ll see details about requests made to the Mattermost API.

## Contributing

- Fork this repository.
- Create a new branch for your feature or bug fix.
- Submit a pull request describing your changes.

We welcome improvements and fixes to make this library more powerful and user-friendly!

## License

This project is licensed under the MIT License. Refer to `LICENSE` file for more details.

---

By following these instructions, you’ll have full control over sending messages and files to your Mattermost channels asynchronously. The focus on no placeholders ensures that all provided values must be actual, working credentials and URLs, resulting in a clean and direct integration experience.