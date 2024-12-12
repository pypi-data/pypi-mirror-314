# swagger_client.FeatureStoresApi

All URIs are relative to *https://api.curia.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_many_base_feature_store_controller_feature_store**](FeatureStoresApi.md#create_many_base_feature_store_controller_feature_store) | **POST** /feature-stores/bulk | Create multiple FeatureStores
[**create_one_base_feature_store_controller_feature_store**](FeatureStoresApi.md#create_one_base_feature_store_controller_feature_store) | **POST** /feature-stores | Create a single FeatureStore
[**delete_one_base_feature_store_controller_feature_store**](FeatureStoresApi.md#delete_one_base_feature_store_controller_feature_store) | **DELETE** /feature-stores/{id} | Delete a single FeatureStore
[**get_many_base_feature_store_controller_feature_store**](FeatureStoresApi.md#get_many_base_feature_store_controller_feature_store) | **GET** /feature-stores | Retrieve multiple FeatureStores
[**get_one_base_feature_store_controller_feature_store**](FeatureStoresApi.md#get_one_base_feature_store_controller_feature_store) | **GET** /feature-stores/{id} | Retrieve a single FeatureStore
[**replace_one_base_feature_store_controller_feature_store**](FeatureStoresApi.md#replace_one_base_feature_store_controller_feature_store) | **PUT** /feature-stores/{id} | Replace a single FeatureStore
[**update_one_base_feature_store_controller_feature_store**](FeatureStoresApi.md#update_one_base_feature_store_controller_feature_store) | **PATCH** /feature-stores/{id} | Update a single FeatureStore

# **create_many_base_feature_store_controller_feature_store**
> list[FeatureStoreResponseDto] create_many_base_feature_store_controller_feature_store(body)

Create multiple FeatureStores

### Example
```python
from __future__ import print_function
import time
import curia.api.swagger_client
from curia.api.swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.FeatureStoresApi(swagger_client.ApiClient(configuration))
body = swagger_client.CreateManyFeatureStoreDto() # CreateManyFeatureStoreDto | 

try:
    # Create multiple FeatureStores
    api_response = api_instance.create_many_base_feature_store_controller_feature_store(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FeatureStoresApi->create_many_base_feature_store_controller_feature_store: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CreateManyFeatureStoreDto**](CreateManyFeatureStoreDto.md)|  | 

### Return type

[**list[FeatureStoreResponseDto]**](FeatureStoreResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_one_base_feature_store_controller_feature_store**
> FeatureStoreResponseDto create_one_base_feature_store_controller_feature_store(body)

Create a single FeatureStore

### Example
```python
from __future__ import print_function
import time
import curia.api.swagger_client
from curia.api.swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.FeatureStoresApi(swagger_client.ApiClient(configuration))
body = swagger_client.CreateFeatureStoreDto() # CreateFeatureStoreDto | 

try:
    # Create a single FeatureStore
    api_response = api_instance.create_one_base_feature_store_controller_feature_store(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FeatureStoresApi->create_one_base_feature_store_controller_feature_store: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CreateFeatureStoreDto**](CreateFeatureStoreDto.md)|  | 

### Return type

[**FeatureStoreResponseDto**](FeatureStoreResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_one_base_feature_store_controller_feature_store**
> delete_one_base_feature_store_controller_feature_store(id)

Delete a single FeatureStore

### Example
```python
from __future__ import print_function
import time
import curia.api.swagger_client
from curia.api.swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.FeatureStoresApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | 

try:
    # Delete a single FeatureStore
    api_instance.delete_one_base_feature_store_controller_feature_store(id)
except ApiException as e:
    print("Exception when calling FeatureStoresApi->delete_one_base_feature_store_controller_feature_store: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_many_base_feature_store_controller_feature_store**
> GetManyFeatureStoreResponseDto get_many_base_feature_store_controller_feature_store(fields=fields, s=s, filter=filter, _or=_or, sort=sort, join=join, limit=limit, offset=offset, page=page, cache=cache)

Retrieve multiple FeatureStores

### Example
```python
from __future__ import print_function
import time
import curia.api.swagger_client
from curia.api.swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.FeatureStoresApi(swagger_client.ApiClient(configuration))
fields = ['fields_example'] # list[str] | Selects resource fields. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#select\" target=\"_blank\">Docs</a> (optional)
s = 's_example' # str | Adds search condition. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#search\" target=\"_blank\">Docs</a> (optional)
filter = ['filter_example'] # list[str] | Adds filter condition. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#filter\" target=\"_blank\">Docs</a> (optional)
_or = ['_or_example'] # list[str] | Adds OR condition. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#or\" target=\"_blank\">Docs</a> (optional)
sort = ['sort_example'] # list[str] | Adds sort by field. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#sort\" target=\"_blank\">Docs</a> (optional)
join = ['join_example'] # list[str] | Adds relational resources. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#join\" target=\"_blank\">Docs</a> (optional)
limit = 56 # int | Limit amount of resources. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#limit\" target=\"_blank\">Docs</a> (optional)
offset = 56 # int | Offset amount of resources. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#offset\" target=\"_blank\">Docs</a> (optional)
page = 56 # int | Page portion of resources. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#page\" target=\"_blank\">Docs</a> (optional)
cache = 56 # int | Reset cache (if was enabled). <a href=\"https://github.com/nestjsx/crud/wiki/Requests#cache\" target=\"_blank\">Docs</a> (optional)

try:
    # Retrieve multiple FeatureStores
    api_response = api_instance.get_many_base_feature_store_controller_feature_store(fields=fields, s=s, filter=filter, _or=_or, sort=sort, join=join, limit=limit, offset=offset, page=page, cache=cache)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FeatureStoresApi->get_many_base_feature_store_controller_feature_store: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fields** | [**list[str]**](str.md)| Selects resource fields. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#select\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **s** | **str**| Adds search condition. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#search\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **filter** | [**list[str]**](str.md)| Adds filter condition. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#filter\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **_or** | [**list[str]**](str.md)| Adds OR condition. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#or\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **sort** | [**list[str]**](str.md)| Adds sort by field. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#sort\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **join** | [**list[str]**](str.md)| Adds relational resources. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#join\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **limit** | **int**| Limit amount of resources. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#limit\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **offset** | **int**| Offset amount of resources. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#offset\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **page** | **int**| Page portion of resources. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#page\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **cache** | **int**| Reset cache (if was enabled). &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#cache\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 

### Return type

[**GetManyFeatureStoreResponseDto**](GetManyFeatureStoreResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_one_base_feature_store_controller_feature_store**
> FeatureStoreResponseDto get_one_base_feature_store_controller_feature_store(id, fields=fields, join=join, cache=cache)

Retrieve a single FeatureStore

### Example
```python
from __future__ import print_function
import time
import curia.api.swagger_client
from curia.api.swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.FeatureStoresApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | 
fields = ['fields_example'] # list[str] | Selects resource fields. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#select\" target=\"_blank\">Docs</a> (optional)
join = ['join_example'] # list[str] | Adds relational resources. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#join\" target=\"_blank\">Docs</a> (optional)
cache = 56 # int | Reset cache (if was enabled). <a href=\"https://github.com/nestjsx/crud/wiki/Requests#cache\" target=\"_blank\">Docs</a> (optional)

try:
    # Retrieve a single FeatureStore
    api_response = api_instance.get_one_base_feature_store_controller_feature_store(id, fields=fields, join=join, cache=cache)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FeatureStoresApi->get_one_base_feature_store_controller_feature_store: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **fields** | [**list[str]**](str.md)| Selects resource fields. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#select\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **join** | [**list[str]**](str.md)| Adds relational resources. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#join\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **cache** | **int**| Reset cache (if was enabled). &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#cache\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 

### Return type

[**FeatureStoreResponseDto**](FeatureStoreResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_one_base_feature_store_controller_feature_store**
> FeatureStoreResponseDto replace_one_base_feature_store_controller_feature_store(body, id)

Replace a single FeatureStore

### Example
```python
from __future__ import print_function
import time
import curia.api.swagger_client
from curia.api.swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.FeatureStoresApi(swagger_client.ApiClient(configuration))
body = swagger_client.FeatureStoreResponseDto() # FeatureStoreResponseDto | 
id = 'id_example' # str | 

try:
    # Replace a single FeatureStore
    api_response = api_instance.replace_one_base_feature_store_controller_feature_store(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FeatureStoresApi->replace_one_base_feature_store_controller_feature_store: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**FeatureStoreResponseDto**](FeatureStoreResponseDto.md)|  | 
 **id** | **str**|  | 

### Return type

[**FeatureStoreResponseDto**](FeatureStoreResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_one_base_feature_store_controller_feature_store**
> FeatureStoreResponseDto update_one_base_feature_store_controller_feature_store(body, id)

Update a single FeatureStore

### Example
```python
from __future__ import print_function
import time
import curia.api.swagger_client
from curia.api.swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.FeatureStoresApi(swagger_client.ApiClient(configuration))
body = swagger_client.UpdateFeatureStoreDto() # UpdateFeatureStoreDto | 
id = 'id_example' # str | 

try:
    # Update a single FeatureStore
    api_response = api_instance.update_one_base_feature_store_controller_feature_store(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FeatureStoresApi->update_one_base_feature_store_controller_feature_store: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**UpdateFeatureStoreDto**](UpdateFeatureStoreDto.md)|  | 
 **id** | **str**|  | 

### Return type

[**FeatureStoreResponseDto**](FeatureStoreResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

