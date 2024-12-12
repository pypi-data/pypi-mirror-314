# swagger_client.DatasetColumnsApi

All URIs are relative to *https://api.curia.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_many_base_dataset_column_controller_dataset_column**](DatasetColumnsApi.md#create_many_base_dataset_column_controller_dataset_column) | **POST** /dataset-columns/bulk | Create multiple DatasetColumns
[**create_one_base_dataset_column_controller_dataset_column**](DatasetColumnsApi.md#create_one_base_dataset_column_controller_dataset_column) | **POST** /dataset-columns | Create a single DatasetColumn
[**delete_one_base_dataset_column_controller_dataset_column**](DatasetColumnsApi.md#delete_one_base_dataset_column_controller_dataset_column) | **DELETE** /dataset-columns/{id} | Delete a single DatasetColumn
[**get_many_base_dataset_column_controller_dataset_column**](DatasetColumnsApi.md#get_many_base_dataset_column_controller_dataset_column) | **GET** /dataset-columns | Retrieve multiple DatasetColumns
[**get_one_base_dataset_column_controller_dataset_column**](DatasetColumnsApi.md#get_one_base_dataset_column_controller_dataset_column) | **GET** /dataset-columns/{id} | Retrieve a single DatasetColumn
[**replace_one_base_dataset_column_controller_dataset_column**](DatasetColumnsApi.md#replace_one_base_dataset_column_controller_dataset_column) | **PUT** /dataset-columns/{id} | Replace a single DatasetColumn
[**update_one_base_dataset_column_controller_dataset_column**](DatasetColumnsApi.md#update_one_base_dataset_column_controller_dataset_column) | **PATCH** /dataset-columns/{id} | Update a single DatasetColumn

# **create_many_base_dataset_column_controller_dataset_column**
> list[DatasetColumnResponseDto] create_many_base_dataset_column_controller_dataset_column(body)

Create multiple DatasetColumns

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
api_instance = swagger_client.DatasetColumnsApi(swagger_client.ApiClient(configuration))
body = swagger_client.CreateManyDatasetColumnDto() # CreateManyDatasetColumnDto | 

try:
    # Create multiple DatasetColumns
    api_response = api_instance.create_many_base_dataset_column_controller_dataset_column(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatasetColumnsApi->create_many_base_dataset_column_controller_dataset_column: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CreateManyDatasetColumnDto**](CreateManyDatasetColumnDto.md)|  | 

### Return type

[**list[DatasetColumnResponseDto]**](DatasetColumnResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_one_base_dataset_column_controller_dataset_column**
> DatasetColumnResponseDto create_one_base_dataset_column_controller_dataset_column(body)

Create a single DatasetColumn

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
api_instance = swagger_client.DatasetColumnsApi(swagger_client.ApiClient(configuration))
body = swagger_client.CreateDatasetColumnDto() # CreateDatasetColumnDto | 

try:
    # Create a single DatasetColumn
    api_response = api_instance.create_one_base_dataset_column_controller_dataset_column(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatasetColumnsApi->create_one_base_dataset_column_controller_dataset_column: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CreateDatasetColumnDto**](CreateDatasetColumnDto.md)|  | 

### Return type

[**DatasetColumnResponseDto**](DatasetColumnResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_one_base_dataset_column_controller_dataset_column**
> delete_one_base_dataset_column_controller_dataset_column(id)

Delete a single DatasetColumn

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
api_instance = swagger_client.DatasetColumnsApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | 

try:
    # Delete a single DatasetColumn
    api_instance.delete_one_base_dataset_column_controller_dataset_column(id)
except ApiException as e:
    print("Exception when calling DatasetColumnsApi->delete_one_base_dataset_column_controller_dataset_column: %s\n" % e)
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

# **get_many_base_dataset_column_controller_dataset_column**
> GetManyDatasetColumnResponseDto get_many_base_dataset_column_controller_dataset_column(fields=fields, s=s, filter=filter, _or=_or, sort=sort, join=join, limit=limit, offset=offset, page=page, cache=cache)

Retrieve multiple DatasetColumns

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
api_instance = swagger_client.DatasetColumnsApi(swagger_client.ApiClient(configuration))
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
    # Retrieve multiple DatasetColumns
    api_response = api_instance.get_many_base_dataset_column_controller_dataset_column(fields=fields, s=s, filter=filter, _or=_or, sort=sort, join=join, limit=limit, offset=offset, page=page, cache=cache)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatasetColumnsApi->get_many_base_dataset_column_controller_dataset_column: %s\n" % e)
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

[**GetManyDatasetColumnResponseDto**](GetManyDatasetColumnResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_one_base_dataset_column_controller_dataset_column**
> DatasetColumnResponseDto get_one_base_dataset_column_controller_dataset_column(id, fields=fields, join=join, cache=cache)

Retrieve a single DatasetColumn

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
api_instance = swagger_client.DatasetColumnsApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | 
fields = ['fields_example'] # list[str] | Selects resource fields. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#select\" target=\"_blank\">Docs</a> (optional)
join = ['join_example'] # list[str] | Adds relational resources. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#join\" target=\"_blank\">Docs</a> (optional)
cache = 56 # int | Reset cache (if was enabled). <a href=\"https://github.com/nestjsx/crud/wiki/Requests#cache\" target=\"_blank\">Docs</a> (optional)

try:
    # Retrieve a single DatasetColumn
    api_response = api_instance.get_one_base_dataset_column_controller_dataset_column(id, fields=fields, join=join, cache=cache)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatasetColumnsApi->get_one_base_dataset_column_controller_dataset_column: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **fields** | [**list[str]**](str.md)| Selects resource fields. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#select\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **join** | [**list[str]**](str.md)| Adds relational resources. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#join\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **cache** | **int**| Reset cache (if was enabled). &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#cache\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 

### Return type

[**DatasetColumnResponseDto**](DatasetColumnResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_one_base_dataset_column_controller_dataset_column**
> DatasetColumnResponseDto replace_one_base_dataset_column_controller_dataset_column(body, id)

Replace a single DatasetColumn

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
api_instance = swagger_client.DatasetColumnsApi(swagger_client.ApiClient(configuration))
body = swagger_client.DatasetColumnResponseDto() # DatasetColumnResponseDto | 
id = 'id_example' # str | 

try:
    # Replace a single DatasetColumn
    api_response = api_instance.replace_one_base_dataset_column_controller_dataset_column(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatasetColumnsApi->replace_one_base_dataset_column_controller_dataset_column: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**DatasetColumnResponseDto**](DatasetColumnResponseDto.md)|  | 
 **id** | **str**|  | 

### Return type

[**DatasetColumnResponseDto**](DatasetColumnResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_one_base_dataset_column_controller_dataset_column**
> DatasetColumnResponseDto update_one_base_dataset_column_controller_dataset_column(body, id)

Update a single DatasetColumn

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
api_instance = swagger_client.DatasetColumnsApi(swagger_client.ApiClient(configuration))
body = swagger_client.UpdateDatasetColumnDto() # UpdateDatasetColumnDto | 
id = 'id_example' # str | 

try:
    # Update a single DatasetColumn
    api_response = api_instance.update_one_base_dataset_column_controller_dataset_column(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatasetColumnsApi->update_one_base_dataset_column_controller_dataset_column: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**UpdateDatasetColumnDto**](UpdateDatasetColumnDto.md)|  | 
 **id** | **str**|  | 

### Return type

[**DatasetColumnResponseDto**](DatasetColumnResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

