# esi_client.UserInterfaceApi

All URIs are relative to *https://esi.evetech.net/latest*

Method | HTTP request | Description
------------- | ------------- | -------------
[**post_ui_autopilot_waypoint**](UserInterfaceApi.md#post_ui_autopilot_waypoint) | **POST** /ui/autopilot/waypoint/ | Set Autopilot Waypoint
[**post_ui_openwindow_contract**](UserInterfaceApi.md#post_ui_openwindow_contract) | **POST** /ui/openwindow/contract/ | Open Contract Window
[**post_ui_openwindow_information**](UserInterfaceApi.md#post_ui_openwindow_information) | **POST** /ui/openwindow/information/ | Open Information Window
[**post_ui_openwindow_marketdetails**](UserInterfaceApi.md#post_ui_openwindow_marketdetails) | **POST** /ui/openwindow/marketdetails/ | Open Market Details
[**post_ui_openwindow_newmail**](UserInterfaceApi.md#post_ui_openwindow_newmail) | **POST** /ui/openwindow/newmail/ | Open New Mail Window


# **post_ui_autopilot_waypoint**
> post_ui_autopilot_waypoint(destination_id)

Set Autopilot Waypoint

Set a solar system as autopilot waypoint  --- Alternate route: `/dev/ui/autopilot/waypoint/`  Alternate route: `/legacy/ui/autopilot/waypoint/`  Alternate route: `/v2/ui/autopilot/waypoint/` 

### Example

* OAuth Authentication (evesso):

```python
import time
import esi_client
from esi_client.api import user_interface_api
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
    api_instance = user_interface_api.UserInterfaceApi(api_client)
    destination_id = 1 # int | The destination to travel to, can be solar system, station or structure's id
    datasource = "tranquility" # str | The server name you would like data from (optional) if omitted the server will use the default value of "tranquility"
    token = "token_example" # str | Access token to use if unable to set a header (optional)

    # example passing only required values which don't have defaults set
    try:
        # Set Autopilot Waypoint
        api_instance.post_ui_autopilot_waypoint(destination_id)
    except esi_client.ApiException as e:
        print("Exception when calling UserInterfaceApi->post_ui_autopilot_waypoint: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Set Autopilot Waypoint
        api_instance.post_ui_autopilot_waypoint(destination_id, datasource=datasource, token=token)
    except esi_client.ApiException as e:
        print("Exception when calling UserInterfaceApi->post_ui_autopilot_waypoint: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **destination_id** | **int**| The destination to travel to, can be solar system, station or structure&#39;s id |
 **add_to_beginning** | **bool**| Whether this solar system should be added to the beginning of all waypoints | defaults to False
 **clear_other_waypoints** | **bool**| Whether clean other waypoints beforing adding this one | defaults to False
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
**204** | Open window request received |  -  |
**400** | Bad request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**420** | Error limited |  -  |
**500** | Internal server error |  -  |
**503** | Service unavailable |  -  |
**504** | Gateway timeout |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_ui_openwindow_contract**
> post_ui_openwindow_contract(contract_id)

Open Contract Window

Open the contract window inside the client  --- Alternate route: `/dev/ui/openwindow/contract/`  Alternate route: `/legacy/ui/openwindow/contract/`  Alternate route: `/v1/ui/openwindow/contract/` 

### Example

* OAuth Authentication (evesso):

```python
import time
import esi_client
from esi_client.api import user_interface_api
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
    api_instance = user_interface_api.UserInterfaceApi(api_client)
    contract_id = 1 # int | The contract to open
    datasource = "tranquility" # str | The server name you would like data from (optional) if omitted the server will use the default value of "tranquility"
    token = "token_example" # str | Access token to use if unable to set a header (optional)

    # example passing only required values which don't have defaults set
    try:
        # Open Contract Window
        api_instance.post_ui_openwindow_contract(contract_id)
    except esi_client.ApiException as e:
        print("Exception when calling UserInterfaceApi->post_ui_openwindow_contract: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Open Contract Window
        api_instance.post_ui_openwindow_contract(contract_id, datasource=datasource, token=token)
    except esi_client.ApiException as e:
        print("Exception when calling UserInterfaceApi->post_ui_openwindow_contract: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **contract_id** | **int**| The contract to open |
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
**204** | Open window request received |  -  |
**400** | Bad request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**420** | Error limited |  -  |
**500** | Internal server error |  -  |
**503** | Service unavailable |  -  |
**504** | Gateway timeout |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_ui_openwindow_information**
> post_ui_openwindow_information(target_id)

Open Information Window

Open the information window for a character, corporation or alliance inside the client  --- Alternate route: `/dev/ui/openwindow/information/`  Alternate route: `/legacy/ui/openwindow/information/`  Alternate route: `/v1/ui/openwindow/information/` 

### Example

* OAuth Authentication (evesso):

```python
import time
import esi_client
from esi_client.api import user_interface_api
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
    api_instance = user_interface_api.UserInterfaceApi(api_client)
    target_id = 1 # int | The target to open
    datasource = "tranquility" # str | The server name you would like data from (optional) if omitted the server will use the default value of "tranquility"
    token = "token_example" # str | Access token to use if unable to set a header (optional)

    # example passing only required values which don't have defaults set
    try:
        # Open Information Window
        api_instance.post_ui_openwindow_information(target_id)
    except esi_client.ApiException as e:
        print("Exception when calling UserInterfaceApi->post_ui_openwindow_information: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Open Information Window
        api_instance.post_ui_openwindow_information(target_id, datasource=datasource, token=token)
    except esi_client.ApiException as e:
        print("Exception when calling UserInterfaceApi->post_ui_openwindow_information: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **target_id** | **int**| The target to open |
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
**204** | Open window request received |  -  |
**400** | Bad request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**420** | Error limited |  -  |
**500** | Internal server error |  -  |
**503** | Service unavailable |  -  |
**504** | Gateway timeout |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_ui_openwindow_marketdetails**
> post_ui_openwindow_marketdetails(type_id)

Open Market Details

Open the market details window for a specific typeID inside the client  --- Alternate route: `/dev/ui/openwindow/marketdetails/`  Alternate route: `/legacy/ui/openwindow/marketdetails/`  Alternate route: `/v1/ui/openwindow/marketdetails/` 

### Example

* OAuth Authentication (evesso):

```python
import time
import esi_client
from esi_client.api import user_interface_api
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
    api_instance = user_interface_api.UserInterfaceApi(api_client)
    type_id = 1 # int | The item type to open in market window
    datasource = "tranquility" # str | The server name you would like data from (optional) if omitted the server will use the default value of "tranquility"
    token = "token_example" # str | Access token to use if unable to set a header (optional)

    # example passing only required values which don't have defaults set
    try:
        # Open Market Details
        api_instance.post_ui_openwindow_marketdetails(type_id)
    except esi_client.ApiException as e:
        print("Exception when calling UserInterfaceApi->post_ui_openwindow_marketdetails: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Open Market Details
        api_instance.post_ui_openwindow_marketdetails(type_id, datasource=datasource, token=token)
    except esi_client.ApiException as e:
        print("Exception when calling UserInterfaceApi->post_ui_openwindow_marketdetails: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **type_id** | **int**| The item type to open in market window |
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
**204** | Open window request received |  -  |
**400** | Bad request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**420** | Error limited |  -  |
**500** | Internal server error |  -  |
**503** | Service unavailable |  -  |
**504** | Gateway timeout |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_ui_openwindow_newmail**
> post_ui_openwindow_newmail(new_mail)

Open New Mail Window

Open the New Mail window, according to settings from the request if applicable  --- Alternate route: `/dev/ui/openwindow/newmail/`  Alternate route: `/legacy/ui/openwindow/newmail/`  Alternate route: `/v1/ui/openwindow/newmail/` 

### Example

* OAuth Authentication (evesso):

```python
import time
import esi_client
from esi_client.api import user_interface_api
from esi_client.model.post_ui_openwindow_newmail_unprocessable_entity import PostUiOpenwindowNewmailUnprocessableEntity
from esi_client.model.internal_server_error import InternalServerError
from esi_client.model.error_limited import ErrorLimited
from esi_client.model.unauthorized import Unauthorized
from esi_client.model.post_ui_openwindow_newmail_new_mail import PostUiOpenwindowNewmailNewMail
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
    api_instance = user_interface_api.UserInterfaceApi(api_client)
    new_mail = PostUiOpenwindowNewmailNewMail(
        body="body_example",
        recipients=[
            1,
        ],
        subject="subject_example",
        to_corp_or_alliance_id=1,
        to_mailing_list_id=1,
    ) # PostUiOpenwindowNewmailNewMail | The details of mail to create
    datasource = "tranquility" # str | The server name you would like data from (optional) if omitted the server will use the default value of "tranquility"
    token = "token_example" # str | Access token to use if unable to set a header (optional)

    # example passing only required values which don't have defaults set
    try:
        # Open New Mail Window
        api_instance.post_ui_openwindow_newmail(new_mail)
    except esi_client.ApiException as e:
        print("Exception when calling UserInterfaceApi->post_ui_openwindow_newmail: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Open New Mail Window
        api_instance.post_ui_openwindow_newmail(new_mail, datasource=datasource, token=token)
    except esi_client.ApiException as e:
        print("Exception when calling UserInterfaceApi->post_ui_openwindow_newmail: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **new_mail** | [**PostUiOpenwindowNewmailNewMail**](PostUiOpenwindowNewmailNewMail.md)| The details of mail to create |
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
**204** | Open window request received |  -  |
**400** | Bad request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**420** | Error limited |  -  |
**422** | Invalid request |  -  |
**500** | Internal server error |  -  |
**503** | Service unavailable |  -  |
**504** | Gateway timeout |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

