# esi_client.FittingsApi

All URIs are relative to *https://esi.evetech.net/latest*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_characters_character_id_fittings_fitting_id**](FittingsApi.md#delete_characters_character_id_fittings_fitting_id) | **DELETE** /characters/{character_id}/fittings/{fitting_id}/ | Delete fitting
[**get_characters_character_id_fittings**](FittingsApi.md#get_characters_character_id_fittings) | **GET** /characters/{character_id}/fittings/ | Get fittings
[**post_characters_character_id_fittings**](FittingsApi.md#post_characters_character_id_fittings) | **POST** /characters/{character_id}/fittings/ | Create fitting


# **delete_characters_character_id_fittings_fitting_id**
> delete_characters_character_id_fittings_fitting_id(character_id, fitting_id)

Delete fitting

Delete a fitting from a character  --- Alternate route: `/dev/characters/{character_id}/fittings/{fitting_id}/`  Alternate route: `/legacy/characters/{character_id}/fittings/{fitting_id}/`  Alternate route: `/v1/characters/{character_id}/fittings/{fitting_id}/` 

### Example

* OAuth Authentication (evesso):

```python
import time
import esi_client
from esi_client.api import fittings_api
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
    api_instance = fittings_api.FittingsApi(api_client)
    character_id = 1 # int | An EVE character ID
    fitting_id = 1 # int | ID for a fitting of this character
    datasource = "tranquility" # str | The server name you would like data from (optional) if omitted the server will use the default value of "tranquility"
    token = "token_example" # str | Access token to use if unable to set a header (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete fitting
        api_instance.delete_characters_character_id_fittings_fitting_id(character_id, fitting_id)
    except esi_client.ApiException as e:
        print("Exception when calling FittingsApi->delete_characters_character_id_fittings_fitting_id: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete fitting
        api_instance.delete_characters_character_id_fittings_fitting_id(character_id, fitting_id, datasource=datasource, token=token)
    except esi_client.ApiException as e:
        print("Exception when calling FittingsApi->delete_characters_character_id_fittings_fitting_id: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **character_id** | **int**| An EVE character ID |
 **fitting_id** | **int**| ID for a fitting of this character |
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
**204** | Fitting deleted |  -  |
**400** | Bad request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**420** | Error limited |  -  |
**500** | Internal server error |  -  |
**503** | Service unavailable |  -  |
**504** | Gateway timeout |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_characters_character_id_fittings**
> [GetCharactersCharacterIdFittings200Ok] get_characters_character_id_fittings(character_id)

Get fittings

Return fittings of a character  --- Alternate route: `/dev/characters/{character_id}/fittings/`  Alternate route: `/v2/characters/{character_id}/fittings/`  --- This route is cached for up to 300 seconds

### Example

* OAuth Authentication (evesso):

```python
import time
import esi_client
from esi_client.api import fittings_api
from esi_client.model.internal_server_error import InternalServerError
from esi_client.model.error_limited import ErrorLimited
from esi_client.model.get_characters_character_id_fittings200_ok import GetCharactersCharacterIdFittings200Ok
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
    api_instance = fittings_api.FittingsApi(api_client)
    character_id = 1 # int | An EVE character ID
    datasource = "tranquility" # str | The server name you would like data from (optional) if omitted the server will use the default value of "tranquility"
    if_none_match = "If-None-Match_example" # str | ETag from a previous request. A 304 will be returned if this matches the current ETag (optional)
    token = "token_example" # str | Access token to use if unable to set a header (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get fittings
        api_response = api_instance.get_characters_character_id_fittings(character_id)
        pprint(api_response)
    except esi_client.ApiException as e:
        print("Exception when calling FittingsApi->get_characters_character_id_fittings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get fittings
        api_response = api_instance.get_characters_character_id_fittings(character_id, datasource=datasource, if_none_match=if_none_match, token=token)
        pprint(api_response)
    except esi_client.ApiException as e:
        print("Exception when calling FittingsApi->get_characters_character_id_fittings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **character_id** | **int**| An EVE character ID |
 **datasource** | **str**| The server name you would like data from | [optional] if omitted the server will use the default value of "tranquility"
 **if_none_match** | **str**| ETag from a previous request. A 304 will be returned if this matches the current ETag | [optional]
 **token** | **str**| Access token to use if unable to set a header | [optional]

### Return type

[**[GetCharactersCharacterIdFittings200Ok]**](GetCharactersCharacterIdFittings200Ok.md)

### Authorization

[evesso](../README.md#evesso)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A list of fittings |  * Cache-Control - The caching mechanism used <br>  * ETag - RFC7232 compliant entity tag <br>  * Expires - RFC7231 formatted datetime string <br>  * Last-Modified - RFC7231 formatted datetime string <br>  |
**304** | Not modified |  * Cache-Control - The caching mechanism used <br>  * ETag - RFC7232 compliant entity tag <br>  * Expires - RFC7231 formatted datetime string <br>  * Last-Modified - RFC7231 formatted datetime string <br>  |
**400** | Bad request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**420** | Error limited |  -  |
**500** | Internal server error |  -  |
**503** | Service unavailable |  -  |
**504** | Gateway timeout |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_characters_character_id_fittings**
> PostCharactersCharacterIdFittingsCreated post_characters_character_id_fittings(character_id, fitting)

Create fitting

Save a new fitting for a character  --- Alternate route: `/dev/characters/{character_id}/fittings/`  Alternate route: `/v2/characters/{character_id}/fittings/` 

### Example

* OAuth Authentication (evesso):

```python
import time
import esi_client
from esi_client.api import fittings_api
from esi_client.model.post_characters_character_id_fittings_created import PostCharactersCharacterIdFittingsCreated
from esi_client.model.internal_server_error import InternalServerError
from esi_client.model.error_limited import ErrorLimited
from esi_client.model.unauthorized import Unauthorized
from esi_client.model.post_characters_character_id_fittings_fitting import PostCharactersCharacterIdFittingsFitting
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
    api_instance = fittings_api.FittingsApi(api_client)
    character_id = 1 # int | An EVE character ID
    fitting = PostCharactersCharacterIdFittingsFitting(
        description="description_example",
        items=[
            PostCharactersCharacterIdFittingsItem(
                flag="Cargo",
                quantity=1,
                type_id=1,
            ),
        ],
        name="name_example",
        ship_type_id=1,
    ) # PostCharactersCharacterIdFittingsFitting | Details about the new fitting
    datasource = "tranquility" # str | The server name you would like data from (optional) if omitted the server will use the default value of "tranquility"
    token = "token_example" # str | Access token to use if unable to set a header (optional)

    # example passing only required values which don't have defaults set
    try:
        # Create fitting
        api_response = api_instance.post_characters_character_id_fittings(character_id, fitting)
        pprint(api_response)
    except esi_client.ApiException as e:
        print("Exception when calling FittingsApi->post_characters_character_id_fittings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Create fitting
        api_response = api_instance.post_characters_character_id_fittings(character_id, fitting, datasource=datasource, token=token)
        pprint(api_response)
    except esi_client.ApiException as e:
        print("Exception when calling FittingsApi->post_characters_character_id_fittings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **character_id** | **int**| An EVE character ID |
 **fitting** | [**PostCharactersCharacterIdFittingsFitting**](PostCharactersCharacterIdFittingsFitting.md)| Details about the new fitting |
 **datasource** | **str**| The server name you would like data from | [optional] if omitted the server will use the default value of "tranquility"
 **token** | **str**| Access token to use if unable to set a header | [optional]

### Return type

[**PostCharactersCharacterIdFittingsCreated**](PostCharactersCharacterIdFittingsCreated.md)

### Authorization

[evesso](../README.md#evesso)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | A list of fittings |  -  |
**400** | Bad request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**420** | Error limited |  -  |
**500** | Internal server error |  -  |
**503** | Service unavailable |  -  |
**504** | Gateway timeout |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

