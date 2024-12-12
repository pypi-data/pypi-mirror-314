# PyOnix

A Python client library for the Ionix API.

## Installation

```bash
pip install pyonix
```

## Usage

```python
from pyonix import IonixClient

# Initialize the client
client = IonixClient(
    base_url="https://api.portal.ionix.io/api/v1",
    api_token="your-api-token",
    account_name="" # Optional for MSSPs
)

# Synchronous usage
results = client.get("endpoint/path")

# Asynchronous usage
import asyncio

async def main():
    results = await client.get_async("endpoint/path")
    
    # Paginated results
    all_items = await client.paginate_async("endpoint/path")
    
    # Close the client when done
    await client.close()

asyncio.run(main())
```

## Features

- Synchronous and asynchronous API requests
- Automatic pagination handling
- Retry mechanism for failed requests
- Proper error handling with custom exceptions
- Concurrent batch processing for paginated results

## Error Handling

The library provides custom exceptions for different types of errors:

- `IonixApiError`: Base exception for all API errors
- `IonixClientError`: For 4xx client errors
- `IonixServerError`: For 5xx server errors

Example error handling:

```python
from pyonix import IonixClient, IonixClientError, IonixServerError

client = IonixClient(...)

try:
    result = client.get("endpoint/path")
except IonixClientError as e:
    print(f"Client error occurred: {e}")
except IonixServerError as e:
    print(f"Server error occurred: {e}")
```

## Configuration Options

When initializing the client, you can configure several options:

- `timeout`: Request timeout in seconds (default: 30)
- `max_retries`: Maximum number of retry attempts (default: 3)
- `batch_size`: Number of concurrent requests for pagination (default: 5)

```python
client = IonixClient(
    base_url="https://api.portal.ionix.io/api/v1",
    api_token="your-api-token",
    account_name="your-account-name", # optional for MSSPs
    timeout=60,
    max_retries=5,
    batch_size=10
)
```

## Development

To install the package in development mode:

```bash
git clone https://gitlab.com/josiahzimm/PyOnix.git
cd pyonix
pip install -e .
```

## Releasing New Versions

To release a new version:

1. Update the version in `setup.py` and `pyonix/__init__.py`
2. Create and push a new tag:
```bash
git tag v0.1.0
git push origin v0.1.0
```

The GitLab CI/CD pipeline will automatically build and publish the new version to PyPI.

### Setting up PyPI Deployment

To enable automatic PyPI deployment:

1. Create an account on [PyPI](https://pypi.org)
2. Generate an API token in your PyPI account settings
3. Add the token to your GitLab repository:
   - Go to Settings > CI/CD > Variables
   - Add a new variable named `PYPI_API_TOKEN`
   - Paste your PyPI token as the value
   - Make sure to mask the variable and mark it as protected

## License

MIT License
