# esi_client.FleetsApi

All URIs are relative to *https://esi.evetech.net/latest*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_fleets_fleet_id_members_member_id**](FleetsApi.md#delete_fleets_fleet_id_members_member_id) | **DELETE** /fleets/{fleet_id}/members/{member_id}/ | Kick fleet member
[**delete_fleets_fleet_id_squads_squad_id**](FleetsApi.md#delete_fleets_fleet_id_squads_squad_id) | **DELETE** /fleets/{fleet_id}/squads/{squad_id}/ | Delete fleet squad
[**delete_fleets_fleet_id_wings_wing_id**](FleetsApi.md#delete_fleets_fleet_id_wings_wing_id) | **DELETE** /fleets/{fleet_id}/wings/{wing_id}/ | Delete fleet wing
[**get_characters_character_id_fleet**](FleetsApi.md#get_characters_character_id_fleet) | **GET** /characters/{character_id}/fleet/ | Get character fleet info
[**get_fleets_fleet_id**](FleetsApi.md#get_fleets_fleet_id) | **GET** /fleets/{fleet_id}/ | Get fleet information
[**get_fleets_fleet_id_members**](FleetsApi.md#get_fleets_fleet_id_members) | **GET** /fleets/{fleet_id}/members/ | Get fleet members
[**get_fleets_fleet_id_wings**](FleetsApi.md#get_fleets_fleet_id_wings) | **GET** /fleets/{fleet_id}/wings/ | Get fleet wings
[**post_fleets_fleet_id_members**](FleetsApi.md#post_fleets_fleet_id_members) | **POST** /fleets/{fleet_id}/members/ | Create fleet invitation
[**post_fleets_fleet_id_wings**](FleetsApi.md#post_fleets_fleet_id_wings) | **POST** /fleets/{fleet_id}/wings/ | Create fleet wing
[**post_fleets_fleet_id_wings_wing_id_squads**](FleetsApi.md#post_fleets_fleet_id_wings_wing_id_squads) | **POST** /fleets/{fleet_id}/wings/{wing_id}/squads/ | Create fleet squad
[**put_fleets_fleet_id**](FleetsApi.md#put_fleets_fleet_id) | **PUT** /fleets/{fleet_id}/ | Update fleet
[**put_fleets_fleet_id_members_member_id**](FleetsApi.md#put_fleets_fleet_id_members_member_id) | **PUT** /fleets/{fleet_id}/members/{member_id}/ | Move fleet member
[**put_fleets_fleet_id_squads_squad_id**](FleetsApi.md#put_fleets_fleet_id_squads_squad_id) | **PUT** /fleets/{fleet_id}/squads/{squad_id}/ | Rename fleet squad
[**put_fleets_fleet_id_wings_wing_id**](FleetsApi.md#put_fleets_fleet_id_wings_wing_id) | **PUT** /fleets/{fleet_id}/wings/{wing_id}/ | Rename fleet wing


# **delete_fleets_fleet_id_members_member_id**
> delete_fleets_fleet_id_members_member_id(fleet_id, member_id)

Kick fleet member

Kick a fleet member  --- Alternate route: `/dev/fleets/{fleet_id}/members/{member_id}/`  Alternate route: `/legacy/fleets/{fleet_id}/members/{member_id}/`  Alternate route: `/v1/fleets/{fleet_id}/members/{member_id}/` 

### Example

* OAuth Authentication (evesso):

```python
import time
import esi_client
from esi_client.api import fleets_api
from esi_client.model.delete_fleets_fleet_id_members_member_id_not_found import DeleteFleetsFleetIdMembersMemberIdNotFound
from esi_client.model.internal_server_error import InternalServerError
from esi_client.model.error_limited import ErrorLimited
from esi_client.model.unauthorized import Unauthorized
from esi_client.model.gateway_timeout import GatewayTimeout
from esi_client.model.forbidden import Forbidden
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
    api_instance = fleets_api.FleetsApi(api_client)
    fleet_id = 1 # int | ID for a fleet
    member_id = 1 # int | The character ID of a member in this fleet
    datasource = "tranquility" # str | The server name you would like data from (optional) if omitted the server will use the default value of "tranquility"
    token = "token_example" # str | Access token to use if unable to set a header (optional)

    # example passing only required values which don't have defaults set
    try:
        # Kick fleet member
        api_instance.delete_fleets_fleet_id_members_member_id(fleet_id, member_id)
    except esi_client.ApiException as e:
        print("Exception when calling FleetsApi->delete_fleets_fleet_id_members_member_id: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Kick fleet member
        api_instance.delete_fleets_fleet_id_members_member_id(fleet_id, member_id, datasource=datasource, token=token)
    except esi_client.ApiException as e:
        print("Exception when calling FleetsApi->delete_fleets_fleet_id_members_member_id: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **int**| ID for a fleet |
 **member_id** | **int**| The character ID of a member in this fleet |
 **datasource** | **str**| The server name you would like data from | [optional] if omitted the server will use the default value of "tranquility"
 **token** | **str**| Access token to use if unable to set a header | [optional]

### Return type

void (empty response body)

### Authorization

[evesso](../README.md#evesso)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Fleet member kicked |  -  |
**400** | Bad request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | The fleet does not exist or you don&#39;t have access to it |  -  |
**420** | Error limited |  -  |
**500** | Internal server error |  -  |
**503** | Service unavailable |  -  |
**504** | Gateway timeout |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_fleets_fleet_id_squads_squad_id**
> delete_fleets_fleet_id_squads_squad_id(fleet_id, squad_id)

Delete fleet squad

Delete a fleet squad, only empty squads can be deleted  --- Alternate route: `/dev/fleets/{fleet_id}/squads/{squad_id}/`  Alternate route: `/legacy/fleets/{fleet_id}/squads/{squad_id}/`  Alternate route: `/v1/fleets/{fleet_id}/squads/{squad_id}/` 

### Example

* OAuth Authentication (evesso):

```python
import time
import esi_client
from esi_client.api import fleets_api
from esi_client.model.delete_fleets_fleet_id_squads_squad_id_not_found import DeleteFleetsFleetIdSquadsSquadIdNotFound
from esi_client.model.internal_server_error import InternalServerError
from esi_client.model.error_limited import ErrorLimited
from esi_client.model.unauthorized import Unauthorized
from esi_client.model.gateway_timeout import GatewayTimeout
from esi_client.model.forbidden import Forbidden
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
    api_instance = fleets_api.FleetsApi(api_client)
    fleet_id = 1 # int | ID for a fleet
    squad_id = 1 # int | The squad to delete
    datasource = "tranquility" # str | The server name you would like data from (optional) if omitted the server will use the default value of "tranquility"
    token = "token_example" # str | Access token to use if unable to set a header (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete fleet squad
        api_instance.delete_fleets_fleet_id_squads_squad_id(fleet_id, squad_id)
    except esi_client.ApiException as e:
        print("Exception when calling FleetsApi->delete_fleets_fleet_id_squads_squad_id: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete fleet squad
        api_instance.delete_fleets_fleet_id_squads_squad_id(fleet_id, squad_id, datasource=datasource, token=token)
    except esi_client.ApiException as e:
        print("Exception when calling FleetsApi->delete_fleets_fleet_id_squads_squad_id: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **int**| ID for a fleet |
 **squad_id** | **int**| The squad to delete |
 **datasource** | **str**| The server name you would like data from | [optional] if omitted the server will use the default value of "tranquility"
 **token** | **str**| Access token to use if unable to set a header | [optional]

### Return type

void (empty response body)

### Authorization

[evesso](../README.md#evesso)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Squad deleted |  -  |
**400** | Bad request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | The fleet does not exist or you don&#39;t have access to it |  -  |
**420** | Error limited |  -  |
**500** | Internal server error |  -  |
**503** | Service unavailable |  -  |
**504** | Gateway timeout |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_fleets_fleet_id_wings_wing_id**
> delete_fleets_fleet_id_wings_wing_id(fleet_id, wing_id)

Delete fleet wing

Delete a fleet wing, only empty wings can be deleted. The wing may contain squads, but the squads must be empty  --- Alternate route: `/dev/fleets/{fleet_id}/wings/{wing_id}/`  Alternate route: `/legacy/fleets/{fleet_id}/wings/{wing_id}/`  Alternate route: `/v1/fleets/{fleet_id}/wings/{wing_id}/` 

### Example

* OAuth Authentication (evesso):

```python
import time
import esi_client
from esi_client.api import fleets_api
from esi_client.model.delete_fleets_fleet_id_wings_wing_id_not_found import DeleteFleetsFleetIdWingsWingIdNotFound
from esi_client.model.internal_server_error import InternalServerError
from esi_client.model.error_limited import ErrorLimited
from esi_client.model.unauthorized import Unauthorized
from esi_client.model.gateway_timeout import GatewayTimeout
from esi_client.model.forbidden import Forbidden
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
    api_instance = fleets_api.FleetsApi(api_client)
    fleet_id = 1 # int | ID for a fleet
    wing_id = 1 # int | The wing to delete
    datasource = "tranquility" # str | The server name you would like data from (optional) if omitted the server will use the default value of "tranquility"
    token = "token_example" # str | Access token to use if unable to set a header (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete fleet wing
        api_instance.delete_fleets_fleet_id_wings_wing_id(fleet_id, wing_id)
    except esi_client.ApiException as e:
        print("Exception when calling FleetsApi->delete_fleets_fleet_id_wings_wing_id: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete fleet wing
        api_instance.delete_fleets_fleet_id_wings_wing_id(fleet_id, wing_id, datasource=datasource, token=token)
    except esi_client.ApiException as e:
        print("Exception when calling FleetsApi->delete_fleets_fleet_id_wings_wing_id: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **int**| ID for a fleet |
 **wing_id** | **int**| The wing to delete |
 **datasource** | **str**| The server name you would like data from | [optional] if omitted the server will use the default value of "tranquility"
 **token** | **str**| Access token to use if unable to set a header | [optional]

### Return type

void (empty response body)

### Authorization

[evesso](../README.md#evesso)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Wing deleted |  -  |
**400** | Bad request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | The fleet does not exist or you don&#39;t have access to it |  -  |
**420** | Error limited |  -  |
**500** | Internal server error |  -  |
**503** | Service unavailable |  -  |
**504** | Gateway timeout |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_characters_character_id_fleet**
> GetCharactersCharacterIdFleetOk get_characters_character_id_fleet(character_id)

Get character fleet info

Return the fleet ID the character is in, if any.  --- Alternate route: `/legacy/characters/{character_id}/fleet/`  Alternate route: `/v1/characters/{character_id}/fleet/`  --- This route is cached for up to 60 seconds  --- Warning: This route has an upgrade available  --- [Diff of the upcoming changes](https://esi.evetech.net/diff/latest/dev/#GET-/characters/{character_id}/fleet/)

### Example

* OAuth Authentication (evesso):

```python
import time
import esi_client
from esi_client.api import fleets_api
from esi_client.model.internal_server_error import InternalServerError
from esi_client.model.get_characters_character_id_fleet_not_found import GetCharactersCharacterIdFleetNotFound
from esi_client.model.error_limited import ErrorLimited
from esi_client.model.unauthorized import Unauthorized
from esi_client.model.gateway_timeout import GatewayTimeout
from esi_client.model.forbidden import Forbidden
from esi_client.model.get_characters_character_id_fleet_ok import GetCharactersCharacterIdFleetOk
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
    api_instance = fleets_api.FleetsApi(api_client)
    character_id = 1 # int | An EVE character ID
    datasource = "tranquility" # str | The server name you would like data from (optional) if omitted the server will use the default value of "tranquility"
    if_none_match = "If-None-Match_example" # str | ETag from a previous request. A 304 will be returned if this matches the current ETag (optional)
    token = "token_example" # str | Access token to use if unable to set a header (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get character fleet info
        api_response = api_instance.get_characters_character_id_fleet(character_id)
        pprint(api_response)
    except esi_client.ApiException as e:
        print("Exception when calling FleetsApi->get_characters_character_id_fleet: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get character fleet info
        api_response = api_instance.get_characters_character_id_fleet(character_id, datasource=datasource, if_none_match=if_none_match, token=token)
        pprint(api_response)
    except esi_client.ApiException as e:
        print("Exception when calling FleetsApi->get_characters_character_id_fleet: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **character_id** | **int**| An EVE character ID |
 **datasource** | **str**| The server name you would like data from | [optional] if omitted the server will use the default value of "tranquility"
 **if_none_match** | **str**| ETag from a previous request. A 304 will be returned if this matches the current ETag | [optional]
 **token** | **str**| Access token to use if unable to set a header | [optional]

### Return type

[**GetCharactersCharacterIdFleetOk**](GetCharactersCharacterIdFleetOk.md)

### Authorization

[evesso](../README.md#evesso)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Details about the character&#39;s fleet |  * Cache-Control - The caching mechanism used <br>  * ETag - RFC7232 compliant entity tag <br>  * Expires - RFC7231 formatted datetime string <br>  * Last-Modified - RFC7231 formatted datetime string <br>  |
**304** | Not modified |  * Cache-Control - The caching mechanism used <br>  * ETag - RFC7232 compliant entity tag <br>  * Expires - RFC7231 formatted datetime string <br>  * Last-Modified - RFC7231 formatted datetime string <br>  |
**400** | Bad request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | The character is not in a fleet |  -  |
**420** | Error limited |  -  |
**500** | Internal server error |  -  |
**503** | Service unavailable |  -  |
**504** | Gateway timeout |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_fleets_fleet_id**
> GetFleetsFleetIdOk get_fleets_fleet_id(fleet_id)

Get fleet information

Return details about a fleet  --- Alternate route: `/dev/fleets/{fleet_id}/`  Alternate route: `/legacy/fleets/{fleet_id}/`  Alternate route: `/v1/fleets/{fleet_id}/`  --- This route is cached for up to 5 seconds

### Example

* OAuth Authentication (evesso):

```python
import time
import esi_client
from esi_client.api import fleets_api
from esi_client.model.get_fleets_fleet_id_ok import GetFleetsFleetIdOk
from esi_client.model.get_fleets_fleet_id_not_found import GetFleetsFleetIdNotFound
from esi_client.model.internal_server_error import InternalServerError
from esi_client.model.error_limited import ErrorLimited
from esi_client.model.unauthorized import Unauthorized
from esi_client.model.gateway_timeout import GatewayTimeout
from esi_client.model.forbidden import Forbidden
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
    api_instance = fleets_api.FleetsApi(api_client)
    fleet_id = 1 # int | ID for a fleet
    datasource = "tranquility" # str | The server name you would like data from (optional) if omitted the server will use the default value of "tranquility"
    if_none_match = "If-None-Match_example" # str | ETag from a previous request. A 304 will be returned if this matches the current ETag (optional)
    token = "token_example" # str | Access token to use if unable to set a header (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get fleet information
        api_response = api_instance.get_fleets_fleet_id(fleet_id)
        pprint(api_response)
    except esi_client.ApiException as e:
        print("Exception when calling FleetsApi->get_fleets_fleet_id: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get fleet information
        api_response = api_instance.get_fleets_fleet_id(fleet_id, datasource=datasource, if_none_match=if_none_match, token=token)
        pprint(api_response)
    except esi_client.ApiException as e:
        print("Exception when calling FleetsApi->get_fleets_fleet_id: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **int**| ID for a fleet |
 **datasource** | **str**| The server name you would like data from | [optional] if omitted the server will use the default value of "tranquility"
 **if_none_match** | **str**| ETag from a previous request. A 304 will be returned if this matches the current ETag | [optional]
 **token** | **str**| Access token to use if unable to set a header | [optional]

### Return type

[**GetFleetsFleetIdOk**](GetFleetsFleetIdOk.md)

### Authorization

[evesso](../README.md#evesso)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Details about a fleet |  * Cache-Control - The caching mechanism used <br>  * ETag - RFC7232 compliant entity tag <br>  * Expires - RFC7231 formatted datetime string <br>  * Last-Modified - RFC7231 formatted datetime string <br>  |
**304** | Not modified |  * Cache-Control - The caching mechanism used <br>  * ETag - RFC7232 compliant entity tag <br>  * Expires - RFC7231 formatted datetime string <br>  * Last-Modified - RFC7231 formatted datetime string <br>  |
**400** | Bad request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | The fleet does not exist or you don&#39;t have access to it |  -  |
**420** | Error limited |  -  |
**500** | Internal server error |  -  |
**503** | Service unavailable |  -  |
**504** | Gateway timeout |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_fleets_fleet_id_members**
> [GetFleetsFleetIdMembers200Ok] get_fleets_fleet_id_members(fleet_id)

Get fleet members

Return information about fleet members  --- Alternate route: `/dev/fleets/{fleet_id}/members/`  Alternate route: `/legacy/fleets/{fleet_id}/members/`  Alternate route: `/v1/fleets/{fleet_id}/members/`  --- This route is cached for up to 5 seconds

### Example

* OAuth Authentication (evesso):

```python
import time
import esi_client
from esi_client.api import fleets_api
from esi_client.model.internal_server_error import InternalServerError
from esi_client.model.error_limited import ErrorLimited
from esi_client.model.unauthorized import Unauthorized
from esi_client.model.gateway_timeout import GatewayTimeout
from esi_client.model.get_fleets_fleet_id_members200_ok import GetFleetsFleetIdMembers200Ok
from esi_client.model.forbidden import Forbidden
from esi_client.model.get_fleets_fleet_id_members_not_found import GetFleetsFleetIdMembersNotFound
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
    api_instance = fleets_api.FleetsApi(api_client)
    fleet_id = 1 # int | ID for a fleet
    accept_language = "en" # str | Language to use in the response (optional) if omitted the server will use the default value of "en"
    datasource = "tranquility" # str | The server name you would like data from (optional) if omitted the server will use the default value of "tranquility"
    if_none_match = "If-None-Match_example" # str | ETag from a previous request. A 304 will be returned if this matches the current ETag (optional)
    language = "en" # str | Language to use in the response, takes precedence over Accept-Language (optional) if omitted the server will use the default value of "en"
    token = "token_example" # str | Access token to use if unable to set a header (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get fleet members
        api_response = api_instance.get_fleets_fleet_id_members(fleet_id)
        pprint(api_response)
    except esi_client.ApiException as e:
        print("Exception when calling FleetsApi->get_fleets_fleet_id_members: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get fleet members
        api_response = api_instance.get_fleets_fleet_id_members(fleet_id, accept_language=accept_language, datasource=datasource, if_none_match=if_none_match, language=language, token=token)
        pprint(api_response)
    except esi_client.ApiException as e:
        print("Exception when calling FleetsApi->get_fleets_fleet_id_members: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **int**| ID for a fleet |
 **accept_language** | **str**| Language to use in the response | [optional] if omitted the server will use the default value of "en"
 **datasource** | **str**| The server name you would like data from | [optional] if omitted the server will use the default value of "tranquility"
 **if_none_match** | **str**| ETag from a previous request. A 304 will be returned if this matches the current ETag | [optional]
 **language** | **str**| Language to use in the response, takes precedence over Accept-Language | [optional] if omitted the server will use the default value of "en"
 **token** | **str**| Access token to use if unable to set a header | [optional]

### Return type

[**[GetFleetsFleetIdMembers200Ok]**](GetFleetsFleetIdMembers200Ok.md)

### Authorization

[evesso](../README.md#evesso)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A list of fleet members |  * Cache-Control - The caching mechanism used <br>  * ETag - RFC7232 compliant entity tag <br>  * Expires - RFC7231 formatted datetime string <br>  * Last-Modified - RFC7231 formatted datetime string <br>  * Content-Language - The language used in the response <br>  |
**304** | Not modified |  * Cache-Control - The caching mechanism used <br>  * ETag - RFC7232 compliant entity tag <br>  * Expires - RFC7231 formatted datetime string <br>  * Last-Modified - RFC7231 formatted datetime string <br>  |
**400** | Bad request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | The fleet does not exist or you don&#39;t have access to it |  -  |
**420** | Error limited |  -  |
**500** | Internal server error |  -  |
**503** | Service unavailable |  -  |
**504** | Gateway timeout |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_fleets_fleet_id_wings**
> [GetFleetsFleetIdWings200Ok] get_fleets_fleet_id_wings(fleet_id)

Get fleet wings

Return information about wings in a fleet  --- Alternate route: `/dev/fleets/{fleet_id}/wings/`  Alternate route: `/legacy/fleets/{fleet_id}/wings/`  Alternate route: `/v1/fleets/{fleet_id}/wings/`  --- This route is cached for up to 5 seconds

### Example

* OAuth Authentication (evesso):

```python
import time
import esi_client
from esi_client.api import fleets_api
from esi_client.model.internal_server_error import InternalServerError
from esi_client.model.error_limited import ErrorLimited
from esi_client.model.unauthorized import Unauthorized
from esi_client.model.gateway_timeout import GatewayTimeout
from esi_client.model.forbidden import Forbidden
from esi_client.model.bad_request import BadRequest
from esi_client.model.get_fleets_fleet_id_wings_not_found import GetFleetsFleetIdWingsNotFound
from esi_client.model.get_fleets_fleet_id_wings200_ok import GetFleetsFleetIdWings200Ok
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
    api_instance = fleets_api.FleetsApi(api_client)
    fleet_id = 1 # int | ID for a fleet
    accept_language = "en" # str | Language to use in the response (optional) if omitted the server will use the default value of "en"
    datasource = "tranquility" # str | The server name you would like data from (optional) if omitted the server will use the default value of "tranquility"
    if_none_match = "If-None-Match_example" # str | ETag from a previous request. A 304 will be returned if this matches the current ETag (optional)
    language = "en" # str | Language to use in the response, takes precedence over Accept-Language (optional) if omitted the server will use the default value of "en"
    token = "token_example" # str | Access token to use if unable to set a header (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get fleet wings
        api_response = api_instance.get_fleets_fleet_id_wings(fleet_id)
        pprint(api_response)
    except esi_client.ApiException as e:
        print("Exception when calling FleetsApi->get_fleets_fleet_id_wings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get fleet wings
        api_response = api_instance.get_fleets_fleet_id_wings(fleet_id, accept_language=accept_language, datasource=datasource, if_none_match=if_none_match, language=language, token=token)
        pprint(api_response)
    except esi_client.ApiException as e:
        print("Exception when calling FleetsApi->get_fleets_fleet_id_wings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **int**| ID for a fleet |
 **accept_language** | **str**| Language to use in the response | [optional] if omitted the server will use the default value of "en"
 **datasource** | **str**| The server name you would like data from | [optional] if omitted the server will use the default value of "tranquility"
 **if_none_match** | **str**| ETag from a previous request. A 304 will be returned if this matches the current ETag | [optional]
 **language** | **str**| Language to use in the response, takes precedence over Accept-Language | [optional] if omitted the server will use the default value of "en"
 **token** | **str**| Access token to use if unable to set a header | [optional]

### Return type

[**[GetFleetsFleetIdWings200Ok]**](GetFleetsFleetIdWings200Ok.md)

### Authorization

[evesso](../README.md#evesso)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A list of fleet wings |  * Cache-Control - The caching mechanism used <br>  * ETag - RFC7232 compliant entity tag <br>  * Expires - RFC7231 formatted datetime string <br>  * Last-Modified - RFC7231 formatted datetime string <br>  * Content-Language - The language used in the response <br>  |
**304** | Not modified |  * Cache-Control - The caching mechanism used <br>  * ETag - RFC7232 compliant entity tag <br>  * Expires - RFC7231 formatted datetime string <br>  * Last-Modified - RFC7231 formatted datetime string <br>  |
**400** | Bad request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | The fleet does not exist or you don&#39;t have access to it |  -  |
**420** | Error limited |  -  |
**500** | Internal server error |  -  |
**503** | Service unavailable |  -  |
**504** | Gateway timeout |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_fleets_fleet_id_members**
> post_fleets_fleet_id_members(fleet_id, invitation)

Create fleet invitation

Invite a character into the fleet. If a character has a CSPA charge set it is not possible to invite them to the fleet using ESI  --- Alternate route: `/dev/fleets/{fleet_id}/members/`  Alternate route: `/legacy/fleets/{fleet_id}/members/`  Alternate route: `/v1/fleets/{fleet_id}/members/` 

### Example

* OAuth Authentication (evesso):

```python
import time
import esi_client
from esi_client.api import fleets_api
from esi_client.model.post_fleets_fleet_id_members_invitation import PostFleetsFleetIdMembersInvitation
from esi_client.model.internal_server_error import InternalServerError
from esi_client.model.error_limited import ErrorLimited
from esi_client.model.unauthorized import Unauthorized
from esi_client.model.gateway_timeout import GatewayTimeout
from esi_client.model.forbidden import Forbidden
from esi_client.model.post_fleets_fleet_id_members_not_found import PostFleetsFleetIdMembersNotFound
from esi_client.model.post_fleets_fleet_id_members_unprocessable_entity import PostFleetsFleetIdMembersUnprocessableEntity
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
    api_instance = fleets_api.FleetsApi(api_client)
    fleet_id = 1 # int | ID for a fleet
    invitation = PostFleetsFleetIdMembersInvitation(
        character_id=1,
        role="fleet_commander",
        squad_id=0,
        wing_id=0,
    ) # PostFleetsFleetIdMembersInvitation | Details of the invitation
    datasource = "tranquility" # str | The server name you would like data from (optional) if omitted the server will use the default value of "tranquility"
    token = "token_example" # str | Access token to use if unable to set a header (optional)

    # example passing only required values which don't have defaults set
    try:
        # Create fleet invitation
        api_instance.post_fleets_fleet_id_members(fleet_id, invitation)
    except esi_client.ApiException as e:
        print("Exception when calling FleetsApi->post_fleets_fleet_id_members: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Create fleet invitation
        api_instance.post_fleets_fleet_id_members(fleet_id, invitation, datasource=datasource, token=token)
    except esi_client.ApiException as e:
        print("Exception when calling FleetsApi->post_fleets_fleet_id_members: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **int**| ID for a fleet |
 **invitation** | [**PostFleetsFleetIdMembersInvitation**](PostFleetsFleetIdMembersInvitation.md)| Details of the invitation |
 **datasource** | **str**| The server name you would like data from | [optional] if omitted the server will use the default value of "tranquility"
 **token** | **str**| Access token to use if unable to set a header | [optional]

### Return type

void (empty response body)

### Authorization

[evesso](../README.md#evesso)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Fleet invitation sent |  -  |
**400** | Bad request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | The fleet does not exist or you don&#39;t have access to it |  -  |
**420** | Error limited |  -  |
**422** | Errors in invitation |  -  |
**500** | Internal server error |  -  |
**503** | Service unavailable |  -  |
**504** | Gateway timeout |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_fleets_fleet_id_wings**
> PostFleetsFleetIdWingsCreated post_fleets_fleet_id_wings(fleet_id)

Create fleet wing

Create a new wing in a fleet  --- Alternate route: `/dev/fleets/{fleet_id}/wings/`  Alternate route: `/legacy/fleets/{fleet_id}/wings/`  Alternate route: `/v1/fleets/{fleet_id}/wings/` 

### Example

* OAuth Authentication (evesso):

```python
import time
import esi_client
from esi_client.api import fleets_api
from esi_client.model.internal_server_error import InternalServerError
from esi_client.model.error_limited import ErrorLimited
from esi_client.model.unauthorized import Unauthorized
from esi_client.model.gateway_timeout import GatewayTimeout
from esi_client.model.post_fleets_fleet_id_wings_created import PostFleetsFleetIdWingsCreated
from esi_client.model.forbidden import Forbidden
from esi_client.model.bad_request import BadRequest
from esi_client.model.post_fleets_fleet_id_wings_not_found import PostFleetsFleetIdWingsNotFound
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
    api_instance = fleets_api.FleetsApi(api_client)
    fleet_id = 1 # int | ID for a fleet
    datasource = "tranquility" # str | The server name you would like data from (optional) if omitted the server will use the default value of "tranquility"
    token = "token_example" # str | Access token to use if unable to set a header (optional)

    # example passing only required values which don't have defaults set
    try:
        # Create fleet wing
        api_response = api_instance.post_fleets_fleet_id_wings(fleet_id)
        pprint(api_response)
    except esi_client.ApiException as e:
        print("Exception when calling FleetsApi->post_fleets_fleet_id_wings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Create fleet wing
        api_response = api_instance.post_fleets_fleet_id_wings(fleet_id, datasource=datasource, token=token)
        pprint(api_response)
    except esi_client.ApiException as e:
        print("Exception when calling FleetsApi->post_fleets_fleet_id_wings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **int**| ID for a fleet |
 **datasource** | **str**| The server name you would like data from | [optional] if omitted the server will use the default value of "tranquility"
 **token** | **str**| Access token to use if unable to set a header | [optional]

### Return type

[**PostFleetsFleetIdWingsCreated**](PostFleetsFleetIdWingsCreated.md)

### Authorization

[evesso](../README.md#evesso)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Wing created |  -  |
**400** | Bad request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | The fleet does not exist or you don&#39;t have access to it |  -  |
**420** | Error limited |  -  |
**500** | Internal server error |  -  |
**503** | Service unavailable |  -  |
**504** | Gateway timeout |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_fleets_fleet_id_wings_wing_id_squads**
> PostFleetsFleetIdWingsWingIdSquadsCreated post_fleets_fleet_id_wings_wing_id_squads(fleet_id, wing_id)

Create fleet squad

Create a new squad in a fleet  --- Alternate route: `/dev/fleets/{fleet_id}/wings/{wing_id}/squads/`  Alternate route: `/legacy/fleets/{fleet_id}/wings/{wing_id}/squads/`  Alternate route: `/v1/fleets/{fleet_id}/wings/{wing_id}/squads/` 

### Example

* OAuth Authentication (evesso):

```python
import time
import esi_client
from esi_client.api import fleets_api
from esi_client.model.internal_server_error import InternalServerError
from esi_client.model.error_limited import ErrorLimited
from esi_client.model.unauthorized import Unauthorized
from esi_client.model.gateway_timeout import GatewayTimeout
from esi_client.model.forbidden import Forbidden
from esi_client.model.post_fleets_fleet_id_wings_wing_id_squads_created import PostFleetsFleetIdWingsWingIdSquadsCreated
from esi_client.model.bad_request import BadRequest
from esi_client.model.post_fleets_fleet_id_wings_wing_id_squads_not_found import PostFleetsFleetIdWingsWingIdSquadsNotFound
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
    api_instance = fleets_api.FleetsApi(api_client)
    fleet_id = 1 # int | ID for a fleet
    wing_id = 1 # int | The wing_id to create squad in
    datasource = "tranquility" # str | The server name you would like data from (optional) if omitted the server will use the default value of "tranquility"
    token = "token_example" # str | Access token to use if unable to set a header (optional)

    # example passing only required values which don't have defaults set
    try:
        # Create fleet squad
        api_response = api_instance.post_fleets_fleet_id_wings_wing_id_squads(fleet_id, wing_id)
        pprint(api_response)
    except esi_client.ApiException as e:
        print("Exception when calling FleetsApi->post_fleets_fleet_id_wings_wing_id_squads: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Create fleet squad
        api_response = api_instance.post_fleets_fleet_id_wings_wing_id_squads(fleet_id, wing_id, datasource=datasource, token=token)
        pprint(api_response)
    except esi_client.ApiException as e:
        print("Exception when calling FleetsApi->post_fleets_fleet_id_wings_wing_id_squads: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **int**| ID for a fleet |
 **wing_id** | **int**| The wing_id to create squad in |
 **datasource** | **str**| The server name you would like data from | [optional] if omitted the server will use the default value of "tranquility"
 **token** | **str**| Access token to use if unable to set a header | [optional]

### Return type

[**PostFleetsFleetIdWingsWingIdSquadsCreated**](PostFleetsFleetIdWingsWingIdSquadsCreated.md)

### Authorization

[evesso](../README.md#evesso)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Squad created |  -  |
**400** | Bad request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | The fleet does not exist or you don&#39;t have access to it |  -  |
**420** | Error limited |  -  |
**500** | Internal server error |  -  |
**503** | Service unavailable |  -  |
**504** | Gateway timeout |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_fleets_fleet_id**
> put_fleets_fleet_id(fleet_id, new_settings)

Update fleet

Update settings about a fleet  --- Alternate route: `/dev/fleets/{fleet_id}/`  Alternate route: `/legacy/fleets/{fleet_id}/`  Alternate route: `/v1/fleets/{fleet_id}/` 

### Example

* OAuth Authentication (evesso):

```python
import time
import esi_client
from esi_client.api import fleets_api
from esi_client.model.internal_server_error import InternalServerError
from esi_client.model.error_limited import ErrorLimited
from esi_client.model.unauthorized import Unauthorized
from esi_client.model.gateway_timeout import GatewayTimeout
from esi_client.model.forbidden import Forbidden
from esi_client.model.bad_request import BadRequest
from esi_client.model.put_fleets_fleet_id_not_found import PutFleetsFleetIdNotFound
from esi_client.model.put_fleets_fleet_id_new_settings import PutFleetsFleetIdNewSettings
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
    api_instance = fleets_api.FleetsApi(api_client)
    fleet_id = 1 # int | ID for a fleet
    new_settings = PutFleetsFleetIdNewSettings(
        is_free_move=True,
        motd="motd_example",
    ) # PutFleetsFleetIdNewSettings | What to update for this fleet
    datasource = "tranquility" # str | The server name you would like data from (optional) if omitted the server will use the default value of "tranquility"
    token = "token_example" # str | Access token to use if unable to set a header (optional)

    # example passing only required values which don't have defaults set
    try:
        # Update fleet
        api_instance.put_fleets_fleet_id(fleet_id, new_settings)
    except esi_client.ApiException as e:
        print("Exception when calling FleetsApi->put_fleets_fleet_id: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Update fleet
        api_instance.put_fleets_fleet_id(fleet_id, new_settings, datasource=datasource, token=token)
    except esi_client.ApiException as e:
        print("Exception when calling FleetsApi->put_fleets_fleet_id: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **int**| ID for a fleet |
 **new_settings** | [**PutFleetsFleetIdNewSettings**](PutFleetsFleetIdNewSettings.md)| What to update for this fleet |
 **datasource** | **str**| The server name you would like data from | [optional] if omitted the server will use the default value of "tranquility"
 **token** | **str**| Access token to use if unable to set a header | [optional]

### Return type

void (empty response body)

### Authorization

[evesso](../README.md#evesso)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Fleet updated |  -  |
**400** | Bad request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | The fleet does not exist or you don&#39;t have access to it |  -  |
**420** | Error limited |  -  |
**500** | Internal server error |  -  |
**503** | Service unavailable |  -  |
**504** | Gateway timeout |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_fleets_fleet_id_members_member_id**
> put_fleets_fleet_id_members_member_id(fleet_id, member_id, movement)

Move fleet member

Move a fleet member around  --- Alternate route: `/dev/fleets/{fleet_id}/members/{member_id}/`  Alternate route: `/legacy/fleets/{fleet_id}/members/{member_id}/`  Alternate route: `/v1/fleets/{fleet_id}/members/{member_id}/` 

### Example

* OAuth Authentication (evesso):

```python
import time
import esi_client
from esi_client.api import fleets_api
from esi_client.model.put_fleets_fleet_id_members_member_id_movement import PutFleetsFleetIdMembersMemberIdMovement
from esi_client.model.internal_server_error import InternalServerError
from esi_client.model.error_limited import ErrorLimited
from esi_client.model.unauthorized import Unauthorized
from esi_client.model.gateway_timeout import GatewayTimeout
from esi_client.model.forbidden import Forbidden
from esi_client.model.put_fleets_fleet_id_members_member_id_not_found import PutFleetsFleetIdMembersMemberIdNotFound
from esi_client.model.put_fleets_fleet_id_members_member_id_unprocessable_entity import PutFleetsFleetIdMembersMemberIdUnprocessableEntity
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
    api_instance = fleets_api.FleetsApi(api_client)
    fleet_id = 1 # int | ID for a fleet
    member_id = 1 # int | The character ID of a member in this fleet
    movement = PutFleetsFleetIdMembersMemberIdMovement(
        role="fleet_commander",
        squad_id=0,
        wing_id=0,
    ) # PutFleetsFleetIdMembersMemberIdMovement | Details of the invitation
    datasource = "tranquility" # str | The server name you would like data from (optional) if omitted the server will use the default value of "tranquility"
    token = "token_example" # str | Access token to use if unable to set a header (optional)

    # example passing only required values which don't have defaults set
    try:
        # Move fleet member
        api_instance.put_fleets_fleet_id_members_member_id(fleet_id, member_id, movement)
    except esi_client.ApiException as e:
        print("Exception when calling FleetsApi->put_fleets_fleet_id_members_member_id: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Move fleet member
        api_instance.put_fleets_fleet_id_members_member_id(fleet_id, member_id, movement, datasource=datasource, token=token)
    except esi_client.ApiException as e:
        print("Exception when calling FleetsApi->put_fleets_fleet_id_members_member_id: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **int**| ID for a fleet |
 **member_id** | **int**| The character ID of a member in this fleet |
 **movement** | [**PutFleetsFleetIdMembersMemberIdMovement**](PutFleetsFleetIdMembersMemberIdMovement.md)| Details of the invitation |
 **datasource** | **str**| The server name you would like data from | [optional] if omitted the server will use the default value of "tranquility"
 **token** | **str**| Access token to use if unable to set a header | [optional]

### Return type

void (empty response body)

### Authorization

[evesso](../README.md#evesso)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Fleet invitation sent |  -  |
**400** | Bad request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | The fleet does not exist or you don&#39;t have access to it |  -  |
**420** | Error limited |  -  |
**422** | Errors in invitation |  -  |
**500** | Internal server error |  -  |
**503** | Service unavailable |  -  |
**504** | Gateway timeout |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_fleets_fleet_id_squads_squad_id**
> put_fleets_fleet_id_squads_squad_id(fleet_id, squad_id, naming)

Rename fleet squad

Rename a fleet squad  --- Alternate route: `/dev/fleets/{fleet_id}/squads/{squad_id}/`  Alternate route: `/legacy/fleets/{fleet_id}/squads/{squad_id}/`  Alternate route: `/v1/fleets/{fleet_id}/squads/{squad_id}/` 

### Example

* OAuth Authentication (evesso):

```python
import time
import esi_client
from esi_client.api import fleets_api
from esi_client.model.internal_server_error import InternalServerError
from esi_client.model.put_fleets_fleet_id_squads_squad_id_not_found import PutFleetsFleetIdSquadsSquadIdNotFound
from esi_client.model.error_limited import ErrorLimited
from esi_client.model.unauthorized import Unauthorized
from esi_client.model.put_fleets_fleet_id_squads_squad_id_naming import PutFleetsFleetIdSquadsSquadIdNaming
from esi_client.model.gateway_timeout import GatewayTimeout
from esi_client.model.forbidden import Forbidden
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
    api_instance = fleets_api.FleetsApi(api_client)
    fleet_id = 1 # int | ID for a fleet
    squad_id = 1 # int | The squad to rename
    naming = PutFleetsFleetIdSquadsSquadIdNaming(
        name="name_example",
    ) # PutFleetsFleetIdSquadsSquadIdNaming | New name of the squad
    datasource = "tranquility" # str | The server name you would like data from (optional) if omitted the server will use the default value of "tranquility"
    token = "token_example" # str | Access token to use if unable to set a header (optional)

    # example passing only required values which don't have defaults set
    try:
        # Rename fleet squad
        api_instance.put_fleets_fleet_id_squads_squad_id(fleet_id, squad_id, naming)
    except esi_client.ApiException as e:
        print("Exception when calling FleetsApi->put_fleets_fleet_id_squads_squad_id: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Rename fleet squad
        api_instance.put_fleets_fleet_id_squads_squad_id(fleet_id, squad_id, naming, datasource=datasource, token=token)
    except esi_client.ApiException as e:
        print("Exception when calling FleetsApi->put_fleets_fleet_id_squads_squad_id: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **int**| ID for a fleet |
 **squad_id** | **int**| The squad to rename |
 **naming** | [**PutFleetsFleetIdSquadsSquadIdNaming**](PutFleetsFleetIdSquadsSquadIdNaming.md)| New name of the squad |
 **datasource** | **str**| The server name you would like data from | [optional] if omitted the server will use the default value of "tranquility"
 **token** | **str**| Access token to use if unable to set a header | [optional]

### Return type

void (empty response body)

### Authorization

[evesso](../README.md#evesso)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Squad renamed |  -  |
**400** | Bad request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | The fleet does not exist or you don&#39;t have access to it |  -  |
**420** | Error limited |  -  |
**500** | Internal server error |  -  |
**503** | Service unavailable |  -  |
**504** | Gateway timeout |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_fleets_fleet_id_wings_wing_id**
> put_fleets_fleet_id_wings_wing_id(fleet_id, wing_id, naming)

Rename fleet wing

Rename a fleet wing  --- Alternate route: `/dev/fleets/{fleet_id}/wings/{wing_id}/`  Alternate route: `/legacy/fleets/{fleet_id}/wings/{wing_id}/`  Alternate route: `/v1/fleets/{fleet_id}/wings/{wing_id}/` 

### Example

* OAuth Authentication (evesso):

```python
import time
import esi_client
from esi_client.api import fleets_api
from esi_client.model.put_fleets_fleet_id_wings_wing_id_not_found import PutFleetsFleetIdWingsWingIdNotFound
from esi_client.model.internal_server_error import InternalServerError
from esi_client.model.error_limited import ErrorLimited
from esi_client.model.unauthorized import Unauthorized
from esi_client.model.gateway_timeout import GatewayTimeout
from esi_client.model.put_fleets_fleet_id_wings_wing_id_naming import PutFleetsFleetIdWingsWingIdNaming
from esi_client.model.forbidden import Forbidden
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
    api_instance = fleets_api.FleetsApi(api_client)
    fleet_id = 1 # int | ID for a fleet
    wing_id = 1 # int | The wing to rename
    naming = PutFleetsFleetIdWingsWingIdNaming(
        name="name_example",
    ) # PutFleetsFleetIdWingsWingIdNaming | New name of the wing
    datasource = "tranquility" # str | The server name you would like data from (optional) if omitted the server will use the default value of "tranquility"
    token = "token_example" # str | Access token to use if unable to set a header (optional)

    # example passing only required values which don't have defaults set
    try:
        # Rename fleet wing
        api_instance.put_fleets_fleet_id_wings_wing_id(fleet_id, wing_id, naming)
    except esi_client.ApiException as e:
        print("Exception when calling FleetsApi->put_fleets_fleet_id_wings_wing_id: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Rename fleet wing
        api_instance.put_fleets_fleet_id_wings_wing_id(fleet_id, wing_id, naming, datasource=datasource, token=token)
    except esi_client.ApiException as e:
        print("Exception when calling FleetsApi->put_fleets_fleet_id_wings_wing_id: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **int**| ID for a fleet |
 **wing_id** | **int**| The wing to rename |
 **naming** | [**PutFleetsFleetIdWingsWingIdNaming**](PutFleetsFleetIdWingsWingIdNaming.md)| New name of the wing |
 **datasource** | **str**| The server name you would like data from | [optional] if omitted the server will use the default value of "tranquility"
 **token** | **str**| Access token to use if unable to set a header | [optional]

### Return type

void (empty response body)

### Authorization

[evesso](../README.md#evesso)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Wing renamed |  -  |
**400** | Bad request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | The fleet does not exist or you don&#39;t have access to it |  -  |
**420** | Error limited |  -  |
**500** | Internal server error |  -  |
**503** | Service unavailable |  -  |
**504** | Gateway timeout |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

