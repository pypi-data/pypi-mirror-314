# esi_client.SearchApi

All URIs are relative to *https://esi.evetech.net/latest*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_characters_character_id_search**](SearchApi.md#get_characters_character_id_search) | **GET** /characters/{character_id}/search/ | Search on a string


# **get_characters_character_id_search**
> GetCharactersCharacterIdSearchOk get_characters_character_id_search(categories, character_id, search)

Search on a string

Search for entities that match a given sub-string.  --- Alternate route: `/dev/characters/{character_id}/search/`  Alternate route: `/legacy/characters/{character_id}/search/`  Alternate route: `/v3/characters/{character_id}/search/`  --- This route is cached for up to 3600 seconds

### Example

* OAuth Authentication (evesso):

```python
import time
import esi_client
from esi_client.api import search_api
from esi_client.model.get_characters_character_id_search_ok import GetCharactersCharacterIdSearchOk
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
    api_instance = search_api.SearchApi(api_client)
    categories = [
        "agent",
    ] # [str] | Type of entities to search for
    character_id = 1 # int | An EVE character ID
    search = "search_example" # str | The string to search on
    accept_language = "en" # str | Language to use in the response (optional) if omitted the server will use the default value of "en"
    datasource = "tranquility" # str | The server name you would like data from (optional) if omitted the server will use the default value of "tranquility"
    if_none_match = "If-None-Match_example" # str | ETag from a previous request. A 304 will be returned if this matches the current ETag (optional)
    language = "en" # str | Language to use in the response, takes precedence over Accept-Language (optional) if omitted the server will use the default value of "en"
    strict = False # bool | Whether the search should be a strict match (optional) if omitted the server will use the default value of False
    token = "token_example" # str | Access token to use if unable to set a header (optional)

    # example passing only required values which don't have defaults set
    try:
        # Search on a string
        api_response = api_instance.get_characters_character_id_search(categories, character_id, search)
        pprint(api_response)
    except esi_client.ApiException as e:
        print("Exception when calling SearchApi->get_characters_character_id_search: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Search on a string
        api_response = api_instance.get_characters_character_id_search(categories, character_id, search, accept_language=accept_language, datasource=datasource, if_none_match=if_none_match, language=language, strict=strict, token=token)
        pprint(api_response)
    except esi_client.ApiException as e:
        print("Exception when calling SearchApi->get_characters_character_id_search: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **categories** | **[str]**| Type of entities to search for |
 **character_id** | **int**| An EVE character ID |
 **search** | **str**| The string to search on |
 **accept_language** | **str**| Language to use in the response | [optional] if omitted the server will use the default value of "en"
 **datasource** | **str**| The server name you would like data from | [optional] if omitted the server will use the default value of "tranquility"
 **if_none_match** | **str**| ETag from a previous request. A 304 will be returned if this matches the current ETag | [optional]
 **language** | **str**| Language to use in the response, takes precedence over Accept-Language | [optional] if omitted the server will use the default value of "en"
 **strict** | **bool**| Whether the search should be a strict match | [optional] if omitted the server will use the default value of False
 **token** | **str**| Access token to use if unable to set a header | [optional]

### Return type

[**GetCharactersCharacterIdSearchOk**](GetCharactersCharacterIdSearchOk.md)

### Authorization

[evesso](../README.md#evesso)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A list of search results |  * Cache-Control - The caching mechanism used <br>  * ETag - RFC7232 compliant entity tag <br>  * Expires - RFC7231 formatted datetime string <br>  * Last-Modified - RFC7231 formatted datetime string <br>  * Content-Language - The language used in the response <br>  |
**304** | Not modified |  * Cache-Control - The caching mechanism used <br>  * ETag - RFC7232 compliant entity tag <br>  * Expires - RFC7231 formatted datetime string <br>  * Last-Modified - RFC7231 formatted datetime string <br>  |
**400** | Bad request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**420** | Error limited |  -  |
**500** | Internal server error |  -  |
**503** | Service unavailable |  -  |
**504** | Gateway timeout |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

