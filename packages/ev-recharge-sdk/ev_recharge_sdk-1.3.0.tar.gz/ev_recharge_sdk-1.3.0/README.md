
# Getting Started with Shell EV

## Introduction

This API Product provides the list of all Shell Recharge locations. The list includes all Shell Recharge network and all locations available through our roaming partners.

Supported Functions

* Get the list of all the locations and its details.
* Get the details of a particular location.
* Get the list of locations nearby using the latitude and longitude.
* Get the list of locations for a given set of bounds with different zoom levels.

The Charging endpoints provides control to start, stop and get status of the charging session.

Supported Functions

* Start a charging session\n
* Stop a charging session \n
* Retrieve the status of a charging session \n
* Retrieve the list of all active sessions for a card

Go to the Shell Developer Portal: [https://developer.shell.com](https://developer.shell.com)

## Install the Package

The package is compatible with Python versions `3 >=3.7, <= 3.11`.
Install the package from PyPi using the following pip command:

```bash
pip install ev-recharge-sdk==1.3.0
```

You can also view the package at:
https://pypi.python.org/pypi/ev-recharge-sdk/1.3.0

## Test the SDK

You can test the generated SDK and the server with test cases. `unittest` is used as the testing framework and `pytest` is used as the test runner. You can run the tests as follows:

Navigate to the root directory of the SDK and run the following commands

```
pip install -r test-requirements.txt
pytest
```

## Initialize the API Client

**_Note:_** Documentation for the client can be found [here.](https://www.github.com/sdks-io/ev-recharge-python-sdk/tree/1.3.0/doc/client.md)

The following parameters are configurable for the API Client:

| Parameter | Type | Description |
|  --- | --- | --- |
| `environment` | `Environment` | The API environment. <br> **Default: `Environment.PRODUCTION`** |
| `http_client_instance` | `HttpClient` | The Http Client passed from the sdk user for making requests |
| `override_http_client_configuration` | `bool` | The value which determines to override properties of the passed Http Client from the sdk user |
| `http_call_back` | `HttpCallBack` | The callback value that is invoked before and after an HTTP call is made to an endpoint |
| `timeout` | `float` | The value to use for connection timeout. <br> **Default: 60** |
| `max_retries` | `int` | The number of times to retry an endpoint call if it fails. <br> **Default: 0** |
| `backoff_factor` | `float` | A backoff factor to apply between attempts after the second try. <br> **Default: 2** |
| `retry_statuses` | `Array of int` | The http statuses on which retry is to be done. <br> **Default: [408, 413, 429, 500, 502, 503, 504, 521, 522, 524]** |
| `retry_methods` | `Array of string` | The http methods on which retry is to be done. <br> **Default: ['GET', 'PUT']** |
| `client_credentials_auth_credentials` | [`ClientCredentialsAuthCredentials`](https://www.github.com/sdks-io/ev-recharge-python-sdk/tree/1.3.0/doc/auth/oauth-2-client-credentials-grant.md) | The credential object for OAuth 2 Client Credentials Grant |

The API client can be initialized as follows:

```python
client = ShellevClient(
    client_credentials_auth_credentials=ClientCredentialsAuthCredentials(
        o_auth_client_id='OAuthClientId',
        o_auth_client_secret='OAuthClientSecret'
    ),
    environment=Environment.PRODUCTION
)
```

## Environments

The SDK can be configured to use a different environment for making API calls. Available environments are:

### Fields

| Name | Description |
|  --- | --- |
| production | **Default** Production Server |
| environment2 | Test Server |

## Authorization

This API uses the following authentication schemes.

* [`BearerAuth (OAuth 2 Client Credentials Grant)`](https://www.github.com/sdks-io/ev-recharge-python-sdk/tree/1.3.0/doc/auth/oauth-2-client-credentials-grant.md)

## List of APIs

* [Locations](https://www.github.com/sdks-io/ev-recharge-python-sdk/tree/1.3.0/doc/controllers/locations.md)
* [Charging](https://www.github.com/sdks-io/ev-recharge-python-sdk/tree/1.3.0/doc/controllers/charging.md)

## Classes Documentation

* [Utility Classes](https://www.github.com/sdks-io/ev-recharge-python-sdk/tree/1.3.0/doc/utility-classes.md)
* [HttpResponse](https://www.github.com/sdks-io/ev-recharge-python-sdk/tree/1.3.0/doc/http-response.md)
* [HttpRequest](https://www.github.com/sdks-io/ev-recharge-python-sdk/tree/1.3.0/doc/http-request.md)

