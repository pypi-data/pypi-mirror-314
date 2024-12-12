# agilicus_api.RegionsApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_point_of_presence**](RegionsApi.md#add_point_of_presence) | **POST** /v1/point_of_presences | Add a point of presence.
[**delete_point_of_presence**](RegionsApi.md#delete_point_of_presence) | **DELETE** /v1/point_of_presences/{point_of_presence_id} | Delete a point of presence
[**get_point_of_presence**](RegionsApi.md#get_point_of_presence) | **GET** /v1/point_of_presences/{point_of_presence_id} | Get a point of presence
[**list_point_of_presences**](RegionsApi.md#list_point_of_presences) | **GET** /v1/point_of_presences | List all regions
[**replace_point_of_presence**](RegionsApi.md#replace_point_of_presence) | **PUT** /v1/point_of_presences/{point_of_presence_id} | update a point of presence


# **add_point_of_presence**
> PointOfPresence add_point_of_presence(point_of_presence)

Add a point of presence.

Adds a new point of presence. 

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import regions_api
from agilicus_api.model.error_message import ErrorMessage
from agilicus_api.model.point_of_presence import PointOfPresence
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = regions_api.RegionsApi(api_client)
    point_of_presence = PointOfPresence(
        metadata=MetadataWithId(),
        spec=PointOfPresenceSpec(
            name=FeatureTagName("north-america"),
            tags=[
                FeatureTagName("north-america"),
            ],
            routing=PointOfPresenceRouting(
                domains=[
                    Domain("domains_example"),
                ],
            ),
        ),
    ) # PointOfPresence | 

    # example passing only required values which don't have defaults set
    try:
        # Add a point of presence.
        api_response = api_instance.add_point_of_presence(point_of_presence)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling RegionsApi->add_point_of_presence: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **point_of_presence** | [**PointOfPresence**](PointOfPresence.md)|  |

### Return type

[**PointOfPresence**](PointOfPresence.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New region created |  -  |
**400** | The request is invalid |  -  |
**409** | region already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_point_of_presence**
> delete_point_of_presence(point_of_presence_id)

Delete a point of presence

Delete a point of presence

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import regions_api
from agilicus_api.model.error_message import ErrorMessage
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = regions_api.RegionsApi(api_client)
    point_of_presence_id = "aL31kzArc8YSA2" # str | point of presence id in path

    # example passing only required values which don't have defaults set
    try:
        # Delete a point of presence
        api_instance.delete_point_of_presence(point_of_presence_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling RegionsApi->delete_point_of_presence: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **point_of_presence_id** | **str**| point of presence id in path |

### Return type

void (empty response body)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | PointOfPresence was deleted |  -  |
**404** | PointOfPresence does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_point_of_presence**
> PointOfPresence get_point_of_presence(point_of_presence_id)

Get a point of presence

Get a point of presence

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import regions_api
from agilicus_api.model.error_message import ErrorMessage
from agilicus_api.model.point_of_presence import PointOfPresence
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = regions_api.RegionsApi(api_client)
    point_of_presence_id = "aL31kzArc8YSA2" # str | point of presence id in path

    # example passing only required values which don't have defaults set
    try:
        # Get a point of presence
        api_response = api_instance.get_point_of_presence(point_of_presence_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling RegionsApi->get_point_of_presence: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **point_of_presence_id** | **str**| point of presence id in path |

### Return type

[**PointOfPresence**](PointOfPresence.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return a PointOfPresence |  -  |
**404** | PointOfPresence does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_point_of_presences**
> ListPointOfPresencesResponse list_point_of_presences()

List all regions

List all regions matching the provided query parameters. Perform keyset pagination by setting the page_at_name parameter to the name for the next page to fetch. Set it to `\"\"` to start from the beginning. 

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import regions_api
from agilicus_api.model.list_point_of_presences_response import ListPointOfPresencesResponse
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = regions_api.RegionsApi(api_client)
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500
    name = "name-1" # str | Filters based on whether or not the items in the collection have the given name.  (optional)
    page_at_name = "ca-1" # str | Pagination based query with the name as the key. To get the initial entries supply an empty string. On subsequent requests, supply the `page_at_name` field from the list response.  (optional)
    includes_all_tag = [
        "Canada",
    ] # [str] | A list of case-sensitive tags to include in the search. Each provided tag must match in order for the item to be returned.  (optional)
    includes_any_tag = [
        "Canada",
    ] # [str] | A list of case-sensitive tags to include in the search. If any provided tag matches then the item is returned.  (optional)
    excludes_all_tag = [
        "Canada",
    ] # [str] | A list of case-sensitive tags to exclude in the search. If all provided tags match, then the item is not returned.  (optional)
    excludes_any_tag = [
        "Canada",
    ] # [str] | A list of case-sensitive tags to exclude in the search. If any provided tag matches, then the item is not returned.  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # List all regions
        api_response = api_instance.list_point_of_presences(limit=limit, name=name, page_at_name=page_at_name, includes_all_tag=includes_all_tag, includes_any_tag=includes_any_tag, excludes_all_tag=excludes_all_tag, excludes_any_tag=excludes_any_tag)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling RegionsApi->list_point_of_presences: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] if omitted the server will use the default value of 500
 **name** | **str**| Filters based on whether or not the items in the collection have the given name.  | [optional]
 **page_at_name** | **str**| Pagination based query with the name as the key. To get the initial entries supply an empty string. On subsequent requests, supply the &#x60;page_at_name&#x60; field from the list response.  | [optional]
 **includes_all_tag** | **[str]**| A list of case-sensitive tags to include in the search. Each provided tag must match in order for the item to be returned.  | [optional]
 **includes_any_tag** | **[str]**| A list of case-sensitive tags to include in the search. If any provided tag matches then the item is returned.  | [optional]
 **excludes_all_tag** | **[str]**| A list of case-sensitive tags to exclude in the search. If all provided tags match, then the item is not returned.  | [optional]
 **excludes_any_tag** | **[str]**| A list of case-sensitive tags to exclude in the search. If any provided tag matches, then the item is not returned.  | [optional]

### Return type

[**ListPointOfPresencesResponse**](ListPointOfPresencesResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Query succeeded |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_point_of_presence**
> PointOfPresence replace_point_of_presence(point_of_presence_id)

update a point of presence

update a point of presence

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import regions_api
from agilicus_api.model.error_message import ErrorMessage
from agilicus_api.model.point_of_presence import PointOfPresence
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = regions_api.RegionsApi(api_client)
    point_of_presence_id = "aL31kzArc8YSA2" # str | point of presence id in path
    point_of_presence = PointOfPresence(
        metadata=MetadataWithId(),
        spec=PointOfPresenceSpec(
            name=FeatureTagName("north-america"),
            tags=[
                FeatureTagName("north-america"),
            ],
            routing=PointOfPresenceRouting(
                domains=[
                    Domain("domains_example"),
                ],
            ),
        ),
    ) # PointOfPresence |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # update a point of presence
        api_response = api_instance.replace_point_of_presence(point_of_presence_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling RegionsApi->replace_point_of_presence: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # update a point of presence
        api_response = api_instance.replace_point_of_presence(point_of_presence_id, point_of_presence=point_of_presence)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling RegionsApi->replace_point_of_presence: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **point_of_presence_id** | **str**| point of presence id in path |
 **point_of_presence** | [**PointOfPresence**](PointOfPresence.md)|  | [optional]

### Return type

[**PointOfPresence**](PointOfPresence.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return updated PointOfPresence |  -  |
**400** | The request is invalid |  -  |
**404** | PointOfPresence does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

