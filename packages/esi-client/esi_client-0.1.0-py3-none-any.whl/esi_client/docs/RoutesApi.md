# esi_client.RoutesApi

All URIs are relative to *https://esi.evetech.net/latest*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_route_origin_destination**](RoutesApi.md#get_route_origin_destination) | **GET** /route/{origin}/{destination}/ | Get route


# **get_route_origin_destination**
> [int] get_route_origin_destination(destination, origin)

Get route

Get the systems between origin and destination  --- Alternate route: `/dev/route/{origin}/{destination}/`  Alternate route: `/legacy/route/{origin}/{destination}/`  Alternate route: `/v1/route/{origin}/{destination}/`  --- This route is cached for up to 86400 seconds

### Example


```python
import time
import esi_client
from esi_client.api import routes_api
from esi_client.model.internal_server_error import InternalServerError
from esi_client.model.get_route_origin_destination_not_found import GetRouteOriginDestinationNotFound
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
    api_instance = routes_api.RoutesApi(api_client)
    destination = 1 # int | destination solar system ID
    origin = 1 # int | origin solar system ID
    avoid = [
        1,
    ] # [int] | avoid solar system ID(s) (optional)
    connections = [
        [
            1,
        ],
    ] # [[int]] | connected solar system pairs (optional)
    datasource = "tranquility" # str | The server name you would like data from (optional) if omitted the server will use the default value of "tranquility"
    flag = "shortest" # str | route security preference (optional) if omitted the server will use the default value of "shortest"
    if_none_match = "If-None-Match_example" # str | ETag from a previous request. A 304 will be returned if this matches the current ETag (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get route
        api_response = api_instance.get_route_origin_destination(destination, origin)
        pprint(api_response)
    except esi_client.ApiException as e:
        print("Exception when calling RoutesApi->get_route_origin_destination: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get route
        api_response = api_instance.get_route_origin_destination(destination, origin, avoid=avoid, connections=connections, datasource=datasource, flag=flag, if_none_match=if_none_match)
        pprint(api_response)
    except esi_client.ApiException as e:
        print("Exception when calling RoutesApi->get_route_origin_destination: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **destination** | **int**| destination solar system ID |
 **origin** | **int**| origin solar system ID |
 **avoid** | **[int]**| avoid solar system ID(s) | [optional]
 **connections** | [**[[int]]**]([int].md)| connected solar system pairs | [optional]
 **datasource** | **str**| The server name you would like data from | [optional] if omitted the server will use the default value of "tranquility"
 **flag** | **str**| route security preference | [optional] if omitted the server will use the default value of "shortest"
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
**200** | Solar systems in route from origin to destination |  * Cache-Control - The caching mechanism used <br>  * ETag - RFC7232 compliant entity tag <br>  * Expires - RFC7231 formatted datetime string <br>  * Last-Modified - RFC7231 formatted datetime string <br>  |
**304** | Not modified |  * Cache-Control - The caching mechanism used <br>  * ETag - RFC7232 compliant entity tag <br>  * Expires - RFC7231 formatted datetime string <br>  * Last-Modified - RFC7231 formatted datetime string <br>  |
**400** | Bad request |  -  |
**404** | No route found |  -  |
**420** | Error limited |  -  |
**500** | Internal server error |  -  |
**503** | Service unavailable |  -  |
**504** | Gateway timeout |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

