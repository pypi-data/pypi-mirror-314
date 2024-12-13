# PyOnix

A Python client library for the Ionix API that provides both synchronous and asynchronous access to Ionix's security and assessment features.

## Installation

```bash
pip install pyonix
```

## Basic Usage

```python
from pyonix import IonixClient

# Initialize the client
client = IonixClient(
    base_url="https://api.portal.ionix.io/api/v1",
    api_token="your-api-token",
    account_name="" # Optional for MSSPs
)
```

## Working with Action Items

The Action Items API allows you to retrieve and manage security action items. Here are some common usage examples:

### Get Open Action Items

```python
# Get paginated action items
response = client.action_items.get(
    asset="example-asset",  # Optional: Filter by asset name
    limit=10,              # Optional: Results per page
    offset=0               # Optional: Pagination offset
)

# Access the results
print(f"Total items: {response.count}")
for item in response.results:
    print(f"Title: {item['title']}")
    print(f"Urgency: {item['urgency']}")
    print(f"Asset: {item['asset']}")
    print("---")

# Get all action items (automatically handles pagination)
all_items = client.action_items.get_all(
    asset="example-asset"  # Optional: Filter by asset name
)

for item in all_items:
    print(f"Title: {item['title']}")
```

### Asynchronous Action Items

```python
import asyncio

async def main():
    # Get paginated action items asynchronously
    response = await client.action_items.get_async(
        asset="example-asset",
        limit=10
    )
    
    # Get all action items asynchronously
    all_items = await client.action_items.get_all_async(
        asset="example-asset"
    )
    
    # Don't forget to close the client
    await client.close()

asyncio.run(main())
```

### Acknowledge Action Items

```python
# Acknowledge items synchronously
response = client.action_items.acknowledge(
    ids=["item-id-1", "item-id-2"],
    is_acknowledged=True,
    reason="Issue resolved"  # Optional
)

# Acknowledge items asynchronously
async def acknowledge():
    response = await client.action_items.acknowledge_async(
        ids=["item-id-1", "item-id-2"],
        is_acknowledged=True,
        reason="Issue resolved"
    )
```

## Working with Assessments

The Assessments API provides access to both organizational asset assessments and digital supply chain assessments.

### Organizational Asset Assessments

```python
# Get paginated assessments
response = client.assessments.get(
    asset="example-asset",
    limit=10
)

# Get all assessments
all_assessments = client.assessments.get_all(
    asset="example-asset"
)

# Async example
async def get_assessments():
    response = await client.assessments.get_async(
        asset="example-asset"
    )
    all_assessments = await client.assessments.get_all_async(
        asset="example-asset"
    )
```

### Digital Supply Chain Assessments

```python
# Get paginated supply chain assessments
response = client.assessments.get_digital_supply_chain(
    asset="example-asset",
    limit=10
)

# Get all supply chain assessments
all_assessments = client.assessments.get_all_digital_supply_chain(
    asset="example-asset"
)

# Async example
async def get_supply_chain():
    response = await client.assessments.get_digital_supply_chain_async(
        asset="example-asset"
    )
    all_assessments = await client.assessments.get_all_digital_supply_chain_async(
        asset="example-asset"
    )
```

## Working with Connections

The Connections API allows you to retrieve information about asset connections and their risk rankings.

### Get Connections

```python
# Get paginated connections
response = client.connections.get(
    asset="example-asset",  # Optional: Filter by asset name
    limit=10,              # Optional: Results per page
    offset=0               # Optional: Pagination offset
)

# Get all connections (automatically handles pagination)
all_connections = client.connections.get_all(
    asset="example-asset"
)

# Each connection contains:
for connection in all_connections:
    print(f"Source: {connection['source']}")
    print(f"Target: {connection['target']}")
    print(f"Type: {connection['type']}")
    print(f"Risk Score: {connection['risk']['risk_score']}")
```

### Asynchronous Connections

```python
async def get_connections():
    # Get paginated connections asynchronously
    response = await client.connections.get_async(
        asset="example-asset",
        limit=10
    )
    
    # Get all connections asynchronously
    all_connections = await client.connections.get_all_async(
        asset="example-asset"
    )
```

## Working with Dashboards

The Dashboards API provides access to summary information about your assets and security posture.

```python
# Get dashboard summary
dashboard = client.dashboards.get(
    asset="example-asset",  # Optional: Filter by asset name
    limit=10,              # Optional: Results per page
    offset=0               # Optional: Pagination offset
)

# Access dashboard data
print(f"Dashboard Summary: {dashboard}")
```

## Working with Tags

The Tags API allows you to manage tags for organizational assets.

```python
# Add tags to assets
response = client.tags.post(
    ids=["asset-id-1", "asset-id-2"],  # List of asset IDs to tag
    tags=["production", "critical"]     # List of tags to apply
)

# The response includes updated asset information including:
# - id
# - risk_score
# - asset name
# - type
# - importance
# - hosting provider
# - technologies
# - first seen date
# - service information
# - tags
# - groups
```

## Error Handling

The library provides custom exceptions for different types of errors:

```python
from pyonix import IonixClient, IonixClientError, IonixServerError

client = IonixClient(...)

try:
    result = client.action_items.get(asset="example-asset")
except IonixClientError as e:
    print(f"Client error occurred: {e}")  # Handles 4xx errors
except IonixServerError as e:
    print(f"Server error occurred: {e}")  # Handles 5xx errors
```

## Configuration Options

When initializing the client, you can configure several options:

```python
client = IonixClient(
    base_url="https://api.portal.ionix.io/api/v1",
    api_token="your-api-token",
    account_name="your-account-name",  # Optional for MSSPs
    timeout=60,                        # Request timeout in seconds (default: 30)
    max_retries=5,                     # Maximum retry attempts (default: 3)
    batch_size=10                      # Concurrent requests for pagination (default: 5)
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
