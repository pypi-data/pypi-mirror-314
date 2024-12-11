# duckyai

Developer-friendly & type-safe Python SDK specifically catered to leverage *duckyai* API.

<div align="left">
    <a href="https://www.speakeasy.com/?utm_source=duckyai&utm_campaign=python"><img src="https://custom-icon-badges.demolab.com/badge/-Built%20By%20Speakeasy-212015?style=for-the-badge&logoColor=FBE331&logo=speakeasy&labelColor=545454" /></a>
    <a href="https://opensource.org/licenses/MIT">
        <img src="https://img.shields.io/badge/License-MIT-blue.svg" style="width: 100px; height: 28px;" />
    </a>
</div>


<br /><br />
> [!IMPORTANT]
> This SDK is not yet ready for production use. To complete setup please follow the steps outlined in your [workspace](https://app.speakeasy.com/org/ducky/feather-backend). Delete this section before > publishing to a package manager.

<!-- Start Summary [summary] -->
## Summary

RAG as a Service API: API for managing RAG configurations, integrations, prompt templates, and backtesting.
<!-- End Summary [summary] -->

<!-- Start Table of Contents [toc] -->
## Table of Contents
<!-- $toc-max-depth=2 -->
* [duckyai](#duckyai)
  * [SDK Installation](#sdk-installation)
  * [IDE Support](#ide-support)
  * [SDK Example Usage](#sdk-example-usage)
  * [Authentication](#authentication)
  * [Available Resources and Operations](#available-resources-and-operations)
  * [File uploads](#file-uploads)
  * [Retries](#retries)
  * [Error Handling](#error-handling)
  * [Server Selection](#server-selection)
  * [Custom HTTP Client](#custom-http-client)
  * [Debugging](#debugging)
* [Development](#development)
  * [Maturity](#maturity)
  * [Contributions](#contributions)

<!-- End Table of Contents [toc] -->

<!-- Start SDK Installation [installation] -->
## SDK Installation

The SDK can be installed with either *pip* or *poetry* package managers.

### PIP

*PIP* is the default package installer for Python, enabling easy installation and management of packages from PyPI via the command line.

```bash
pip install git+<UNSET>.git
```

### Poetry

*Poetry* is a modern tool that simplifies dependency management and package publishing by using a single `pyproject.toml` file to handle project metadata and dependencies.

```bash
poetry add git+<UNSET>.git
```
<!-- End SDK Installation [installation] -->

<!-- Start IDE Support [idesupport] -->
## IDE Support

### PyCharm

Generally, the SDK will work well with most IDEs out of the box. However, when using PyCharm, you can enjoy much better integration with Pydantic by installing an additional plugin.

- [PyCharm Pydantic Plugin](https://docs.pydantic.dev/latest/integrations/pycharm/)
<!-- End IDE Support [idesupport] -->

<!-- Start SDK Example Usage [usage] -->
## SDK Example Usage

### Example

```python
# Synchronous Example
import duckyai
from duckyai import DuckyAi
import io
import os

with DuckyAi() as ducky_ai:
    ducky_ai.internal.delete_index_internal(security=duckyai.DeleteIndexInternalSecurity(
        internal_api_key=os.getenv("DUCKYAI_INTERNAL_API_KEY", ""),
    ), request=io.BytesIO("0xC4FfFEA0fF".encode()))

    # Use the SDK ...
```

</br>

The same SDK client can also be used to make asychronous requests by importing asyncio.
```python
# Asynchronous Example
import asyncio
import duckyai
from duckyai import DuckyAi
import io
import os

async def main():
    async with DuckyAi() as ducky_ai:
        await ducky_ai.internal.delete_index_internal_async(security=duckyai.DeleteIndexInternalSecurity(
            internal_api_key=os.getenv("DUCKYAI_INTERNAL_API_KEY", ""),
        ), request=io.BytesIO("0xA70D56f9a1".encode()))

        # Use the SDK ...

asyncio.run(main())
```
<!-- End SDK Example Usage [usage] -->

<!-- Start Authentication [security] -->
## Authentication

### Per-Client Security Schemes

This SDK supports the following security scheme globally:

| Name      | Type   | Scheme  | Environment Variable |
| --------- | ------ | ------- | -------------------- |
| `api_key` | apiKey | API key | `DUCKYAI_API_KEY`    |

To authenticate with the API the `api_key` parameter must be set when initializing the SDK client instance. For example:
```python
from duckyai import DuckyAi
import os

with DuckyAi(
    api_key=os.getenv("DUCKYAI_API_KEY", ""),
) as ducky_ai:
    res = ducky_ai.ducky.list_indexes()

    if res is not None:
        # handle response
        pass

```

### Per-Operation Security Schemes

Some operations in this SDK require the security scheme to be specified at the request level. For example:
```python
import duckyai
from duckyai import DuckyAi
import io
import os

with DuckyAi() as ducky_ai:
    ducky_ai.internal.delete_index_internal(security=duckyai.DeleteIndexInternalSecurity(
        internal_api_key=os.getenv("DUCKYAI_INTERNAL_API_KEY", ""),
    ), request=io.BytesIO("0xC4FfFEA0fF".encode()))

    # Use the SDK ...

```
<!-- End Authentication [security] -->

<!-- Start Available Resources and Operations [operations] -->
## Available Resources and Operations

<details open>
<summary>Available methods</summary>

### [ducky](docs/sdks/ducky/README.md)

* [list_indexes](docs/sdks/ducky/README.md#list_indexes) - List indexes within a project
* [create_index](docs/sdks/ducky/README.md#create_index) - Create an index
* [delete_index](docs/sdks/ducky/README.md#delete_index) - Delete an index
* [index_document_text](docs/sdks/ducky/README.md#index_document_text) - Index a document from text content
* [delete_document](docs/sdks/ducky/README.md#delete_document) - Delete a document
* [get_document](docs/sdks/ducky/README.md#get_document) - Get a document by ID with pagination
* [retrieve_documents](docs/sdks/ducky/README.md#retrieve_documents) - Retrieve documents with dynamic configuration and variant name


### [internal](docs/sdks/internal/README.md)

* [delete_index_internal](docs/sdks/internal/README.md#delete_index_internal) - Delete an index (internal)
* [index_document_text_internal](docs/sdks/internal/README.md#index_document_text_internal) - Index a document from text content (internal)
* [delete_document_internal](docs/sdks/internal/README.md#delete_document_internal) - Delete a document (internal)

### [webapp](docs/sdks/webapp/README.md)

* [sign_in](docs/sdks/webapp/README.md#sign_in) - User Sign In
* [get_organizations](docs/sdks/webapp/README.md#get_organizations) - Get Organizations
* [list_api_keys](docs/sdks/webapp/README.md#list_api_keys) - Get API Keys
* [create_api_key](docs/sdks/webapp/README.md#create_api_key) - Create API Key
* [delete_api_key](docs/sdks/webapp/README.md#delete_api_key) - Delete API Key
* [list_projects](docs/sdks/webapp/README.md#list_projects) - List projects
* [create_project](docs/sdks/webapp/README.md#create_project) - Create a project
* [delete_project](docs/sdks/webapp/README.md#delete_project) - Delete a project
* [get_project](docs/sdks/webapp/README.md#get_project) - Get a project by ID
* [update_project](docs/sdks/webapp/README.md#update_project) - Update a project
* [list_webapp_indexes](docs/sdks/webapp/README.md#list_webapp_indexes) - List indexes within a project
* [create_webapp_index](docs/sdks/webapp/README.md#create_webapp_index) - Create an index
* [delete_webapp_index](docs/sdks/webapp/README.md#delete_webapp_index) - Delete an index
* [get_webapp_document](docs/sdks/webapp/README.md#get_webapp_document) - Get a document by ID with pagination
* [retrieve_webapp_documents](docs/sdks/webapp/README.md#retrieve_webapp_documents) - Retrieve documents with dynamic configuration and variant name
* [list_webapp_documents](docs/sdks/webapp/README.md#list_webapp_documents) - List documents in an index with pagination
* [generate_webapp_response](docs/sdks/webapp/README.md#generate_webapp_response) - Generate a response with dynamic configuration

</details>
<!-- End Available Resources and Operations [operations] -->

<!-- Start File uploads [file-upload] -->
## File uploads

Certain SDK methods accept file objects as part of a request body or multi-part request. It is possible and typically recommended to upload files as a stream rather than reading the entire contents into memory. This avoids excessive memory consumption and potentially crashing with out-of-memory errors when working with very large files. The following example demonstrates how to attach a file stream to a request.

> [!TIP]
>
> For endpoints that handle file uploads bytes arrays can also be used. However, using streams is recommended for large files.
>

```python
import duckyai
from duckyai import DuckyAi
import io
import os

with DuckyAi() as ducky_ai:
    ducky_ai.internal.delete_index_internal(security=duckyai.DeleteIndexInternalSecurity(
        internal_api_key=os.getenv("DUCKYAI_INTERNAL_API_KEY", ""),
    ), request=io.BytesIO("0xC4FfFEA0fF".encode()))

    # Use the SDK ...

```
<!-- End File uploads [file-upload] -->

<!-- Start Retries [retries] -->
## Retries

Some of the endpoints in this SDK support retries. If you use the SDK without any configuration, it will fall back to the default retry strategy provided by the API. However, the default retry strategy can be overridden on a per-operation basis, or across the entire SDK.

To change the default retry strategy for a single API call, simply provide a `RetryConfig` object to the call:
```python
import duckyai
from duckyai import DuckyAi
from duckyai.utils import BackoffStrategy, RetryConfig
import io
import os

with DuckyAi() as ducky_ai:
    ducky_ai.internal.delete_index_internal(security=duckyai.DeleteIndexInternalSecurity(
        internal_api_key=os.getenv("DUCKYAI_INTERNAL_API_KEY", ""),
    ), request=io.BytesIO("0xC4FfFEA0fF".encode()),
        RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False))

    # Use the SDK ...

```

If you'd like to override the default retry strategy for all operations that support retries, you can use the `retry_config` optional parameter when initializing the SDK:
```python
import duckyai
from duckyai import DuckyAi
from duckyai.utils import BackoffStrategy, RetryConfig
import io
import os

with DuckyAi(
    retry_config=RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False),
) as ducky_ai:
    ducky_ai.internal.delete_index_internal(security=duckyai.DeleteIndexInternalSecurity(
        internal_api_key=os.getenv("DUCKYAI_INTERNAL_API_KEY", ""),
    ), request=io.BytesIO("0xC4FfFEA0fF".encode()))

    # Use the SDK ...

```
<!-- End Retries [retries] -->

<!-- Start Error Handling [errors] -->
## Error Handling

Handling errors in this SDK should largely match your expectations. All operations return a response object or raise an exception.

By default, an API error will raise a models.APIError exception, which has the following properties:

| Property        | Type             | Description           |
|-----------------|------------------|-----------------------|
| `.status_code`  | *int*            | The HTTP status code  |
| `.message`      | *str*            | The error message     |
| `.raw_response` | *httpx.Response* | The raw HTTP response |
| `.body`         | *str*            | The response content  |

When custom error responses are specified for an operation, the SDK may also raise their associated exceptions. You can refer to respective *Errors* tables in SDK docs for more details on possible exception types for each operation. For example, the `sign_in_async` method may raise the following exceptions:

| Error Type                | Status Code   | Content Type     |
| ------------------------- | ------------- | ---------------- |
| models.ErrorResponseError | 400, 401, 500 | application/json |
| models.APIError           | 4XX, 5XX      | \*/\*            |

### Example

```python
import duckyai
from duckyai import DuckyAi, models
import os

with DuckyAi() as ducky_ai:
    res = None
    try:
        res = ducky_ai.webapp.sign_in(security=duckyai.SignInSecurity(
            bearer_auth=os.getenv("DUCKYAI_BEARER_AUTH", ""),
        ))

        if res is not None:
            # handle response
            pass

    except models.ErrorResponseError as e:
        # handle e.data: models.ErrorResponseErrorData
        raise(e)
    except models.APIError as e:
        # handle exception
        raise(e)
```
<!-- End Error Handling [errors] -->

<!-- Start Server Selection [server] -->
## Server Selection

### Override Server URL Per-Client

The default server can also be overridden globally by passing a URL to the `server_url: str` optional parameter when initializing the SDK client instance. For example:
```python
import duckyai
from duckyai import DuckyAi
import io
import os

with DuckyAi(
    server_url="https://${BACKEND_ADDRESS}/",
) as ducky_ai:
    ducky_ai.internal.delete_index_internal(security=duckyai.DeleteIndexInternalSecurity(
        internal_api_key=os.getenv("DUCKYAI_INTERNAL_API_KEY", ""),
    ), request=io.BytesIO("0xC4FfFEA0fF".encode()))

    # Use the SDK ...

```
<!-- End Server Selection [server] -->

<!-- Start Custom HTTP Client [http-client] -->
## Custom HTTP Client

The Python SDK makes API calls using the [httpx](https://www.python-httpx.org/) HTTP library.  In order to provide a convenient way to configure timeouts, cookies, proxies, custom headers, and other low-level configuration, you can initialize the SDK client with your own HTTP client instance.
Depending on whether you are using the sync or async version of the SDK, you can pass an instance of `HttpClient` or `AsyncHttpClient` respectively, which are Protocol's ensuring that the client has the necessary methods to make API calls.
This allows you to wrap the client with your own custom logic, such as adding custom headers, logging, or error handling, or you can just pass an instance of `httpx.Client` or `httpx.AsyncClient` directly.

For example, you could specify a header for every request that this sdk makes as follows:
```python
from duckyai import DuckyAi
import httpx

http_client = httpx.Client(headers={"x-custom-header": "someValue"})
s = DuckyAi(client=http_client)
```

or you could wrap the client with your own custom logic:
```python
from duckyai import DuckyAi
from duckyai.httpclient import AsyncHttpClient
import httpx

class CustomClient(AsyncHttpClient):
    client: AsyncHttpClient

    def __init__(self, client: AsyncHttpClient):
        self.client = client

    async def send(
        self,
        request: httpx.Request,
        *,
        stream: bool = False,
        auth: Union[
            httpx._types.AuthTypes, httpx._client.UseClientDefault, None
        ] = httpx.USE_CLIENT_DEFAULT,
        follow_redirects: Union[
            bool, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
    ) -> httpx.Response:
        request.headers["Client-Level-Header"] = "added by client"

        return await self.client.send(
            request, stream=stream, auth=auth, follow_redirects=follow_redirects
        )

    def build_request(
        self,
        method: str,
        url: httpx._types.URLTypes,
        *,
        content: Optional[httpx._types.RequestContent] = None,
        data: Optional[httpx._types.RequestData] = None,
        files: Optional[httpx._types.RequestFiles] = None,
        json: Optional[Any] = None,
        params: Optional[httpx._types.QueryParamTypes] = None,
        headers: Optional[httpx._types.HeaderTypes] = None,
        cookies: Optional[httpx._types.CookieTypes] = None,
        timeout: Union[
            httpx._types.TimeoutTypes, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
        extensions: Optional[httpx._types.RequestExtensions] = None,
    ) -> httpx.Request:
        return self.client.build_request(
            method,
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            extensions=extensions,
        )

s = DuckyAi(async_client=CustomClient(httpx.AsyncClient()))
```
<!-- End Custom HTTP Client [http-client] -->

<!-- Start Debugging [debug] -->
## Debugging

You can setup your SDK to emit debug logs for SDK requests and responses.

You can pass your own logger class directly into your SDK.
```python
from duckyai import DuckyAi
import logging

logging.basicConfig(level=logging.DEBUG)
s = DuckyAi(debug_logger=logging.getLogger("duckyai"))
```

You can also enable a default debug logger by setting an environment variable `DUCKYAI_DEBUG` to true.
<!-- End Debugging [debug] -->

<!-- Placeholder for Future Speakeasy SDK Sections -->

# Development

## Maturity

This SDK is in beta, and there may be breaking changes between versions without a major version update. Therefore, we recommend pinning usage
to a specific package version. This way, you can install the same version each time without breaking changes unless you are intentionally
looking for the latest version.

## Contributions

While we value open-source contributions to this SDK, this library is generated programmatically. Any manual changes added to internal files will be overwritten on the next generation. 
We look forward to hearing your feedback. Feel free to open a PR or an issue with a proof of concept and we'll do our best to include it in a future release. 

### SDK Created by [Speakeasy](https://www.speakeasy.com/?utm_source=duckyai&utm_campaign=python)
