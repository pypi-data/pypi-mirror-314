# esi_client.OpportunitiesApi

All URIs are relative to *https://esi.evetech.net/latest*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_characters_character_id_opportunities**](OpportunitiesApi.md#get_characters_character_id_opportunities) | **GET** /characters/{character_id}/opportunities/ | Get a character&#39;s completed tasks
[**get_opportunities_groups**](OpportunitiesApi.md#get_opportunities_groups) | **GET** /opportunities/groups/ | Get opportunities groups
[**get_opportunities_groups_group_id**](OpportunitiesApi.md#get_opportunities_groups_group_id) | **GET** /opportunities/groups/{group_id}/ | Get opportunities group
[**get_opportunities_tasks**](OpportunitiesApi.md#get_opportunities_tasks) | **GET** /opportunities/tasks/ | Get opportunities tasks
[**get_opportunities_tasks_task_id**](OpportunitiesApi.md#get_opportunities_tasks_task_id) | **GET** /opportunities/tasks/{task_id}/ | Get opportunities task


# **get_characters_character_id_opportunities**
> [GetCharactersCharacterIdOpportunities200Ok] get_characters_character_id_opportunities(character_id)

Get a character's completed tasks

Return a list of tasks finished by a character  --- Alternate route: `/dev/characters/{character_id}/opportunities/`  Alternate route: `/legacy/characters/{character_id}/opportunities/`  Alternate route: `/v1/characters/{character_id}/opportunities/`  --- This route is cached for up to 3600 seconds

### Example

* OAuth Authentication (evesso):

```python
import time
import esi_client
from esi_client.api import opportunities_api
from esi_client.model.internal_server_error import InternalServerError
from esi_client.model.error_limited import ErrorLimited
from esi_client.model.unauthorized import Unauthorized
from esi_client.model.gateway_timeout import GatewayTimeout
from esi_client.model.forbidden import Forbidden
from esi_client.model.get_characters_character_id_opportunities200_ok import GetCharactersCharacterIdOpportunities200Ok
from esi_client.model.bad_request import BadRequest
from esi_client.model.service_unavailable import ServiceUnavailable
from pprint import pprint
# Defining the host is optional and defaults to https://esi.evetech.net/latest
# See configuration.py for a list of all supported configuration parameters.
configuration = esi_client.Configuration(
    host = "https://esi.evetech.net/latest"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure OAuth2 access token for authorization: evesso
configuration = esi_client.Configuration(
    host = "https://esi.evetech.net/latest"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with esi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = opportunities_api.OpportunitiesApi(api_client)
    character_id = 1 # int | An EVE character ID
    datasource = "tranquility" # str | The server name you would like data from (optional) if omitted the server will use the default value of "tranquility"
    if_none_match = "If-None-Match_example" # str | ETag from a previous request. A 304 will be returned if this matches the current ETag (optional)
    token = "token_example" # str | Access token to use if unable to set a header (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get a character's completed tasks
        api_response = api_instance.get_characters_character_id_opportunities(character_id)
        pprint(api_response)
    except esi_client.ApiException as e:
        print("Exception when calling OpportunitiesApi->get_characters_character_id_opportunities: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a character's completed tasks
        api_response = api_instance.get_characters_character_id_opportunities(character_id, datasource=datasource, if_none_match=if_none_match, token=token)
        pprint(api_response)
    except esi_client.ApiException as e:
        print("Exception when calling OpportunitiesApi->get_characters_character_id_opportunities: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **character_id** | **int**| An EVE character ID |
 **datasource** | **str**| The server name you would like data from | [optional] if omitted the server will use the default value of "tranquility"
 **if_none_match** | **str**| ETag from a previous request. A 304 will be returned if this matches the current ETag | [optional]
 **token** | **str**| Access token to use if unable to set a header | [optional]

### Return type

[**[GetCharactersCharacterIdOpportunities200Ok]**](GetCharactersCharacterIdOpportunities200Ok.md)

### Authorization

[evesso](../README.md#evesso)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A list of opportunities task ids |  * Cache-Control - The caching mechanism used <br>  * ETag - RFC7232 compliant entity tag <br>  * Expires - RFC7231 formatted datetime string <br>  * Last-Modified - RFC7231 formatted datetime string <br>  |
**304** | Not modified |  * Cache-Control - The caching mechanism used <br>  * ETag - RFC7232 compliant entity tag <br>  * Expires - RFC7231 formatted datetime string <br>  * Last-Modified - RFC7231 formatted datetime string <br>  |
**400** | Bad request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**420** | Error limited |  -  |
**500** | Internal server error |  -  |
**503** | Service unavailable |  -  |
**504** | Gateway timeout |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_opportunities_groups**
> [int] get_opportunities_groups()

Get opportunities groups

Return a list of opportunities groups  --- Alternate route: `/dev/opportunities/groups/`  Alternate route: `/legacy/opportunities/groups/`  Alternate route: `/v1/opportunities/groups/`  --- This route expires daily at 11:05

### Example


```python
import time
import esi_client
from esi_client.api import opportunities_api
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
    api_instance = opportunities_api.OpportunitiesApi(api_client)
    datasource = "tranquility" # str | The server name you would like data from (optional) if omitted the server will use the default value of "tranquility"
    if_none_match = "If-None-Match_example" # str | ETag from a previous request. A 304 will be returned if this matches the current ETag (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get opportunities groups
        api_response = api_instance.get_opportunities_groups(datasource=datasource, if_none_match=if_none_match)
        pprint(api_response)
    except esi_client.ApiException as e:
        print("Exception when calling OpportunitiesApi->get_opportunities_groups: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **datasource** | **str**| The server name you would like data from | [optional] if omitted the server will use the default value of "tranquility"
 **if_none_match** | **str**| ETag from a previous request. A 304 will be returned if this matches the current ETag | [optional]

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
**200** | A list of opportunities group ids |  * Cache-Control - The caching mechanism used <br>  * ETag - RFC7232 compliant entity tag <br>  * Expires - RFC7231 formatted datetime string <br>  * Last-Modified - RFC7231 formatted datetime string <br>  |
**304** | Not modified |  * Cache-Control - The caching mechanism used <br>  * ETag - RFC7232 compliant entity tag <br>  * Expires - RFC7231 formatted datetime string <br>  * Last-Modified - RFC7231 formatted datetime string <br>  |
**400** | Bad request |  -  |
**420** | Error limited |  -  |
**500** | Internal server error |  -  |
**503** | Service unavailable |  -  |
**504** | Gateway timeout |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_opportunities_groups_group_id**
> GetOpportunitiesGroupsGroupIdOk get_opportunities_groups_group_id(group_id)

Get opportunities group

Return information of an opportunities group  --- Alternate route: `/dev/opportunities/groups/{group_id}/`  Alternate route: `/legacy/opportunities/groups/{group_id}/`  Alternate route: `/v1/opportunities/groups/{group_id}/`  --- This route expires daily at 11:05

### Example


```python
import time
import esi_client
from esi_client.api import opportunities_api
from esi_client.model.internal_server_error import InternalServerError
from esi_client.model.error_limited import ErrorLimited
from esi_client.model.gateway_timeout import GatewayTimeout
from esi_client.model.get_opportunities_groups_group_id_ok import GetOpportunitiesGroupsGroupIdOk
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
    api_instance = opportunities_api.OpportunitiesApi(api_client)
    group_id = 1 # int | ID of an opportunities group
    accept_language = "en" # str | Language to use in the response (optional) if omitted the server will use the default value of "en"
    datasource = "tranquility" # str | The server name you would like data from (optional) if omitted the server will use the default value of "tranquility"
    if_none_match = "If-None-Match_example" # str | ETag from a previous request. A 304 will be returned if this matches the current ETag (optional)
    language = "en" # str | Language to use in the response, takes precedence over Accept-Language (optional) if omitted the server will use the default value of "en"

    # example passing only required values which don't have defaults set
    try:
        # Get opportunities group
        api_response = api_instance.get_opportunities_groups_group_id(group_id)
        pprint(api_response)
    except esi_client.ApiException as e:
        print("Exception when calling OpportunitiesApi->get_opportunities_groups_group_id: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get opportunities group
        api_response = api_instance.get_opportunities_groups_group_id(group_id, accept_language=accept_language, datasource=datasource, if_none_match=if_none_match, language=language)
        pprint(api_response)
    except esi_client.ApiException as e:
        print("Exception when calling OpportunitiesApi->get_opportunities_groups_group_id: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_id** | **int**| ID of an opportunities group |
 **accept_language** | **str**| Language to use in the response | [optional] if omitted the server will use the default value of "en"
 **datasource** | **str**| The server name you would like data from | [optional] if omitted the server will use the default value of "tranquility"
 **if_none_match** | **str**| ETag from a previous request. A 304 will be returned if this matches the current ETag | [optional]
 **language** | **str**| Language to use in the response, takes precedence over Accept-Language | [optional] if omitted the server will use the default value of "en"

### Return type

[**GetOpportunitiesGroupsGroupIdOk**](GetOpportunitiesGroupsGroupIdOk.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Details of an opportunities group |  * Cache-Control - The caching mechanism used <br>  * ETag - RFC7232 compliant entity tag <br>  * Expires - RFC7231 formatted datetime string <br>  * Last-Modified - RFC7231 formatted datetime string <br>  * Content-Language - The language used in the response <br>  |
**304** | Not modified |  * Cache-Control - The caching mechanism used <br>  * ETag - RFC7232 compliant entity tag <br>  * Expires - RFC7231 formatted datetime string <br>  * Last-Modified - RFC7231 formatted datetime string <br>  |
**400** | Bad request |  -  |
**420** | Error limited |  -  |
**500** | Internal server error |  -  |
**503** | Service unavailable |  -  |
**504** | Gateway timeout |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_opportunities_tasks**
> [int] get_opportunities_tasks()

Get opportunities tasks

Return a list of opportunities tasks  --- Alternate route: `/dev/opportunities/tasks/`  Alternate route: `/legacy/opportunities/tasks/`  Alternate route: `/v1/opportunities/tasks/`  --- This route expires daily at 11:05

### Example


```python
import time
import esi_client
from esi_client.api import opportunities_api
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
    api_instance = opportunities_api.OpportunitiesApi(api_client)
    datasource = "tranquility" # str | The server name you would like data from (optional) if omitted the server will use the default value of "tranquility"
    if_none_match = "If-None-Match_example" # str | ETag from a previous request. A 304 will be returned if this matches the current ETag (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get opportunities tasks
        api_response = api_instance.get_opportunities_tasks(datasource=datasource, if_none_match=if_none_match)
        pprint(api_response)
    except esi_client.ApiException as e:
        print("Exception when calling OpportunitiesApi->get_opportunities_tasks: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **datasource** | **str**| The server name you would like data from | [optional] if omitted the server will use the default value of "tranquility"
 **if_none_match** | **str**| ETag from a previous request. A 304 will be returned if this matches the current ETag | [optional]

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
**200** | A list of opportunities task ids |  * Cache-Control - The caching mechanism used <br>  * ETag - RFC7232 compliant entity tag <br>  * Expires - RFC7231 formatted datetime string <br>  * Last-Modified - RFC7231 formatted datetime string <br>  |
**304** | Not modified |  * Cache-Control - The caching mechanism used <br>  * ETag - RFC7232 compliant entity tag <br>  * Expires - RFC7231 formatted datetime string <br>  * Last-Modified - RFC7231 formatted datetime string <br>  |
**400** | Bad request |  -  |
**420** | Error limited |  -  |
**500** | Internal server error |  -  |
**503** | Service unavailable |  -  |
**504** | Gateway timeout |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_opportunities_tasks_task_id**
> GetOpportunitiesTasksTaskIdOk get_opportunities_tasks_task_id(task_id)

Get opportunities task

Return information of an opportunities task  --- Alternate route: `/dev/opportunities/tasks/{task_id}/`  Alternate route: `/legacy/opportunities/tasks/{task_id}/`  Alternate route: `/v1/opportunities/tasks/{task_id}/`  --- This route expires daily at 11:05

### Example


```python
import time
import esi_client
from esi_client.api import opportunities_api
from esi_client.model.get_opportunities_tasks_task_id_ok import GetOpportunitiesTasksTaskIdOk
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
    api_instance = opportunities_api.OpportunitiesApi(api_client)
    task_id = 1 # int | ID of an opportunities task
    datasource = "tranquility" # str | The server name you would like data from (optional) if omitted the server will use the default value of "tranquility"
    if_none_match = "If-None-Match_example" # str | ETag from a previous request. A 304 will be returned if this matches the current ETag (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get opportunities task
        api_response = api_instance.get_opportunities_tasks_task_id(task_id)
        pprint(api_response)
    except esi_client.ApiException as e:
        print("Exception when calling OpportunitiesApi->get_opportunities_tasks_task_id: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get opportunities task
        api_response = api_instance.get_opportunities_tasks_task_id(task_id, datasource=datasource, if_none_match=if_none_match)
        pprint(api_response)
    except esi_client.ApiException as e:
        print("Exception when calling OpportunitiesApi->get_opportunities_tasks_task_id: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **task_id** | **int**| ID of an opportunities task |
 **datasource** | **str**| The server name you would like data from | [optional] if omitted the server will use the default value of "tranquility"
 **if_none_match** | **str**| ETag from a previous request. A 304 will be returned if this matches the current ETag | [optional]

### Return type

[**GetOpportunitiesTasksTaskIdOk**](GetOpportunitiesTasksTaskIdOk.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Details of an opportunities task |  * Cache-Control - The caching mechanism used <br>  * ETag - RFC7232 compliant entity tag <br>  * Expires - RFC7231 formatted datetime string <br>  * Last-Modified - RFC7231 formatted datetime string <br>  |
**304** | Not modified |  * Cache-Control - The caching mechanism used <br>  * ETag - RFC7232 compliant entity tag <br>  * Expires - RFC7231 formatted datetime string <br>  * Last-Modified - RFC7231 formatted datetime string <br>  |
**400** | Bad request |  -  |
**420** | Error limited |  -  |
**500** | Internal server error |  -  |
**503** | Service unavailable |  -  |
**504** | Gateway timeout |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

