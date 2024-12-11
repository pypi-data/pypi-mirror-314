<div align="center">  
  <img src="./credal-dark-logo.svg" width="400" />
  <h1>Credal Python SDK</h1>

  <p>
    <strong>The Credal Python Library provides convenient access to the Credal API from applications written in Python.</strong>
  </p>

  <br>
  <div>
    <a href="https://buildwithfern.com/"><img src="https://img.shields.io/badge/%F0%9F%8C%BF-SDK%20generated%20by%20Fern-brightgreen">     
  </div>
  <br>
</div>

# Documentation

Docs for the API endpoints available through the SDK can be found [here](https://docs.credal.ai/getting-started/overview).

## Reference

A full reference of the SDK is available [here](./reference.md).

# Installation

```sh
pip install --upgrade credal
```

# Usage

```python
from credal.client import CredalApi

client = CredalApi(
    api_key="YOUR_API_KEY",
)

client.copilots.send_message(
    message="Is Credal SOC 2 compliant?",
    user_email="ravin@credal.ai",
)
```

## Self Hosted

```python
client = CredalApi(
    api_key="YOUR_API_KEY",
    base_url="https://<custom-domain>/api",
)
```

## Async Client

```python
from credal.client import AsyncCredalApi

client = AsyncCredalApi(
    api_key="YOUR_API_KEY",
)
```

## Exception Handling

All errors thrown by the SDK will be subclasses of [`ApiError`](./src/credal/core/api_error.py).

```python
import credal

...

try:
    client.copilots.send_message(...)
except credal.core.ApiError as e: # Handle all errors
    print(e.status_code)
    print(e.body)
```

## Advanced

### Timeouts

By default, requests time out after 60 seconds. You can configure this with a
timeout option at the client or request level.

```python
from credal.client import CredalApi

client = CredalApi(
    ...,
    # All timeouts are 20 seconds
    timeout=20.0,
)

# Override timeout for a specific method
client.copilots.send_message(..., {
    timeout_in_seconds=20.0
})
```

### Retries

The SDK is instrumented with automatic retries with exponential backoff. A request will be
retried as long as the request is deemed retriable and the number of retry attempts has not grown larger
than the configured retry limit (default: 2).

A request is deemed retriable when any of the following HTTP status codes is returned:

- [408](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/408) (Timeout)
- [429](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429) (Too Many Requests)
- [5XX](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/500) (Internal Server Errors)

Use the `max_retries` request option to configure this behavior.

```python
client.copilots.send_message(..., {
    max_retries=1
})
```

### Custom HTTP client

You can override the httpx client to customize it for your use-case. Some common use-cases
include support for proxies and transports.

```python
import httpx

from credal.client import CredalApi

client = CredalApi(...,
    http_client=httpx.Client(
        proxies="http://my.test.proxy.example.com",
        transport=httpx.HTTPTransport(local_address="0.0.0.0"),
    ),
)
```

# Beta Status

This SDK is in beta, and there may be breaking changes between versions without a major 
version update. Therefore, we recommend pinning the package version to a specific version. 
This way, you can install the same version each time without breaking changes.
