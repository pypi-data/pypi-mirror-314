# esi_client.WarsApi

All URIs are relative to *https://esi.evetech.net/latest*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_wars**](WarsApi.md#get_wars) | **GET** /wars/ | List wars
[**get_wars_war_id**](WarsApi.md#get_wars_war_id) | **GET** /wars/{war_id}/ | Get war information
[**get_wars_war_id_killmails**](WarsApi.md#get_wars_war_id_killmails) | **GET** /wars/{war_id}/killmails/ | List kills for a war


# **get_wars**
> [int] get_wars()

List wars

Return a list of wars  --- Alternate route: `/dev/wars/`  Alternate route: `/legacy/wars/`  Alternate route: `/v1/wars/`  --- This route is cached for up to 3600 seconds

### Example


```python
import time
import esi_client
from esi_client.api import wars_api
from esi_client.model.internal_server_error import InternalServerError
from esi_client.model.error_limited import ErrorLimited
from esi_client.model.gateway_timeout import GatewayTimeout
from esi_client.model.bad_request import BadRequest
from esi_client.model.service_unavailable import ServiceUnavailable
from pprint import pprint
# Defining the host is optional and defaults to https://esi.evetech.net/latest
# See configuration.py for a list of all supported configuration parameters.
configuration = esi_client.Configuration(
    host = "https://esi.evetech.net/latest"
)


# Enter a context with an instance of the API client
with esi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = wars_api.WarsApi(api_client)
    datasource = "tranquility" # str | The server name you would like data from (optional) if omitted the server will use the default value of "tranquility"
    if_none_match = "If-None-Match_example" # str | ETag from a previous request. A 304 will be returned if this matches the current ETag (optional)
    max_war_id = 1 # int | Only return wars with ID smaller than this (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # List wars
        api_response = api_instance.get_wars(datasource=datasource, if_none_match=if_none_match, max_war_id=max_war_id)
        pprint(api_response)
    except esi_client.ApiException as e:
        print("Exception when calling WarsApi->get_wars: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **datasource** | **str**| The server name you would like data from | [optional] if omitted the server will use the default value of "tranquility"
 **if_none_match** | **str**| ETag from a previous request. A 304 will be returned if this matches the current ETag | [optional]
 **max_war_id** | **int**| Only return wars with ID smaller than this | [optional]

### Return type

**[int]**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A list of war IDs, in descending order by war_id |  * Cache-Control - The caching mechanism used <br>  * ETag - RFC7232 compliant entity tag <br>  * Expires - RFC7231 formatted datetime string <br>  * Last-Modified - RFC7231 formatted datetime string <br>  |
**304** | Not modified |  * Cache-Control - The caching mechanism used <br>  * ETag - RFC7232 compliant entity tag <br>  * Expires - RFC7231 formatted datetime string <br>  * Last-Modified - RFC7231 formatted datetime string <br>  |
**400** | Bad request |  -  |
**420** | Error limited |  -  |
**500** | Internal server error |  -  |
**503** | Service unavailable |  -  |
**504** | Gateway timeout |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_wars_war_id**
> GetWarsWarIdOk get_wars_war_id(war_id)

Get war information

Return details about a war  --- Alternate route: `/dev/wars/{war_id}/`  Alternate route: `/legacy/wars/{war_id}/`  Alternate route: `/v1/wars/{war_id}/`  --- This route is cached for up to 3600 seconds

### Example


```python
import time
import esi_client
from esi_client.api import wars_api
from esi_client.model.get_wars_war_id_ok import GetWarsWarIdOk
from esi_client.model.internal_server_error import InternalServerError
from esi_client.model.error_limited import ErrorLimited
from esi_client.model.gateway_timeout import GatewayTimeout
from esi_client.model.get_wars_war_id_unprocessable_entity import GetWarsWarIdUnprocessableEntity
from esi_client.model.bad_request import BadRequest
from esi_client.model.service_unavailable import ServiceUnavailable
from pprint import pprint
# Defining the host is optional and defaults to https://esi.evetech.net/latest
# See configuration.py for a list of all supported configuration parameters.
configuration = esi_client.Configuration(
    host = "https://esi.evetech.net/latest"
)


# Enter a context with an instance of the API client
with esi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = wars_api.WarsApi(api_client)
    war_id = 1 # int | ID for a war
    datasource = "tranquility" # str | The server name you would like data from (optional) if omitted the server will use the default value of "tranquility"
    if_none_match = "If-None-Match_example" # str | ETag from a previous request. A 304 will be returned if this matches the current ETag (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get war information
        api_response = api_instance.get_wars_war_id(war_id)
        pprint(api_response)
    except esi_client.ApiException as e:
        print("Exception when calling WarsApi->get_wars_war_id: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get war information
        api_response = api_instance.get_wars_war_id(war_id, datasource=datasource, if_none_match=if_none_match)
        pprint(api_response)
    except esi_client.ApiException as e:
        print("Exception when calling WarsApi->get_wars_war_id: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **war_id** | **int**| ID for a war |
 **datasource** | **str**| The server name you would like data from | [optional] if omitted the server will use the default value of "tranquility"
 **if_none_match** | **str**| ETag from a previous request. A 304 will be returned if this matches the current ETag | [optional]

### Return type

[**GetWarsWarIdOk**](GetWarsWarIdOk.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Details about a war |  * Cache-Control - The caching mechanism used <br>  * ETag - RFC7232 compliant entity tag <br>  * Expires - RFC7231 formatted datetime string <br>  * Last-Modified - RFC7231 formatted datetime string <br>  |
**304** | Not modified |  * Cache-Control - The caching mechanism used <br>  * ETag - RFC7232 compliant entity tag <br>  * Expires - RFC7231 formatted datetime string <br>  * Last-Modified - RFC7231 formatted datetime string <br>  |
**400** | Bad request |  -  |
**420** | Error limited |  -  |
**422** | War not found |  -  |
**500** | Internal server error |  -  |
**503** | Service unavailable |  -  |
**504** | Gateway timeout |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_wars_war_id_killmails**
> [GetWarsWarIdKillmails200Ok] get_wars_war_id_killmails(war_id)

List kills for a war

Return a list of kills related to a war  --- Alternate route: `/dev/wars/{war_id}/killmails/`  Alternate route: `/legacy/wars/{war_id}/killmails/`  Alternate route: `/v1/wars/{war_id}/killmails/`  --- This route is cached for up to 3600 seconds

### Example


```python
import time
import esi_client
from esi_client.api import wars_api
from esi_client.model.internal_server_error import InternalServerError
from esi_client.model.error_limited import ErrorLimited
from esi_client.model.gateway_timeout import GatewayTimeout
from esi_client.model.get_wars_war_id_killmails_unprocessable_entity import GetWarsWarIdKillmailsUnprocessableEntity
from esi_client.model.bad_request import BadRequest
from esi_client.model.get_wars_war_id_killmails200_ok import GetWarsWarIdKillmails200Ok
from esi_client.model.service_unavailable import ServiceUnavailable
from pprint import pprint
# Defining the host is optional and defaults to https://esi.evetech.net/latest
# See configuration.py for a list of all supported configuration parameters.
configuration = esi_client.Configuration(
    host = "https://esi.evetech.net/latest"
)


# Enter a context with an instance of the API client
with esi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = wars_api.WarsApi(api_client)
    war_id = 1 # int | A valid war ID
    datasource = "tranquility" # str | The server name you would like data from (optional) if omitted the server will use the default value of "tranquility"
    if_none_match = "If-None-Match_example" # str | ETag from a previous request. A 304 will be returned if this matches the current ETag (optional)
    page = 1 # int | Which page of results to return (optional) if omitted the server will use the default value of 1

    # example passing only required values which don't have defaults set
    try:
        # List kills for a war
        api_response = api_instance.get_wars_war_id_killmails(war_id)
        pprint(api_response)
    except esi_client.ApiException as e:
        print("Exception when calling WarsApi->get_wars_war_id_killmails: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # List kills for a war
        api_response = api_instance.get_wars_war_id_killmails(war_id, datasource=datasource, if_none_match=if_none_match, page=page)
        pprint(api_response)
    except esi_client.ApiException as e:
        print("Exception when calling WarsApi->get_wars_war_id_killmails: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **war_id** | **int**| A valid war ID |
 **datasource** | **str**| The server name you would like data from | [optional] if omitted the server will use the default value of "tranquility"
 **if_none_match** | **str**| ETag from a previous request. A 304 will be returned if this matches the current ETag | [optional]
 **page** | **int**| Which page of results to return | [optional] if omitted the server will use the default value of 1

### Return type

[**[GetWarsWarIdKillmails200Ok]**](GetWarsWarIdKillmails200Ok.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A list of killmail IDs and hashes |  * Cache-Control - The caching mechanism used <br>  * ETag - RFC7232 compliant entity tag <br>  * Expires - RFC7231 formatted datetime string <br>  * Last-Modified - RFC7231 formatted datetime string <br>  * X-Pages - Maximum page number <br>  |
**304** | Not modified |  * Cache-Control - The caching mechanism used <br>  * ETag - RFC7232 compliant entity tag <br>  * Expires - RFC7231 formatted datetime string <br>  * Last-Modified - RFC7231 formatted datetime string <br>  |
**400** | Bad request |  -  |
**420** | Error limited |  -  |
**422** | War not found |  -  |
**500** | Internal server error |  -  |
**503** | Service unavailable |  -  |
**504** | Gateway timeout |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

