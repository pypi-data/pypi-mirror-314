# curia.api.curia.api.curia.api.swagger_client.ModelBatchesApi

All URIs are relative to *https://api.curia.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_many_base_model_batch_controller_model_batch**](ModelBatchesApi.md#create_many_base_model_batch_controller_model_batch) | **POST** /model-batches/bulk | Create multiple ModelBatches
[**create_one_base_model_batch_controller_model_batch**](ModelBatchesApi.md#create_one_base_model_batch_controller_model_batch) | **POST** /model-batches | Create a single ModelBatch
[**delete_one_base_model_batch_controller_model_batch**](ModelBatchesApi.md#delete_one_base_model_batch_controller_model_batch) | **DELETE** /model-batches/{id} | Delete a single ModelBatch
[**get_many_base_model_batch_controller_model_batch**](ModelBatchesApi.md#get_many_base_model_batch_controller_model_batch) | **GET** /model-batches | Retrieve multiple ModelBatches
[**get_one_base_model_batch_controller_model_batch**](ModelBatchesApi.md#get_one_base_model_batch_controller_model_batch) | **GET** /model-batches/{id} | Retrieve a single ModelBatch
[**replace_one_base_model_batch_controller_model_batch**](ModelBatchesApi.md#replace_one_base_model_batch_controller_model_batch) | **PUT** /model-batches/{id} | Replace a single ModelBatch
[**update_one_base_model_batch_controller_model_batch**](ModelBatchesApi.md#update_one_base_model_batch_controller_model_batch) | **PATCH** /model-batches/{id} | Update a single ModelBatch

# **create_many_base_model_batch_controller_model_batch**
> list[ModelBatchResponseDto] create_many_base_model_batch_controller_model_batch(body)

Create multiple ModelBatches

### Example
```python
from __future__ import print_function
import time
import curia.api.curia.api.curia.api.curia.api.swagger_client
from curia.api.curia.api.curia.api.curia.api.swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = curia.api.curia.api.curia.api.swagger_client.Configuration()
configuration.api_key['Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = curia.api.curia.api.curia.api.swagger_client.ModelBatchesApi(curia.api.curia.api.curia.api.swagger_client.ApiClient(configuration))
body = curia.api.curia.api.curia.api.swagger_client.CreateManyModelBatchDto() # CreateManyModelBatchDto | 

try:
    # Create multiple ModelBatches
    api_response = api_instance.create_many_base_model_batch_controller_model_batch(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelBatchesApi->create_many_base_model_batch_controller_model_batch: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CreateManyModelBatchDto**](CreateManyModelBatchDto.md)|  | 

### Return type

[**list[ModelBatchResponseDto]**](ModelBatchResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_one_base_model_batch_controller_model_batch**
> ModelBatchResponseDto create_one_base_model_batch_controller_model_batch(body)

Create a single ModelBatch

### Example
```python
from __future__ import print_function
import time
import curia.api.curia.api.curia.api.curia.api.swagger_client
from curia.api.curia.api.curia.api.curia.api.swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = curia.api.curia.api.curia.api.swagger_client.Configuration()
configuration.api_key['Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = curia.api.curia.api.curia.api.swagger_client.ModelBatchesApi(curia.api.curia.api.curia.api.swagger_client.ApiClient(configuration))
body = curia.api.curia.api.curia.api.swagger_client.CreateModelBatchDto() # CreateModelBatchDto | 

try:
    # Create a single ModelBatch
    api_response = api_instance.create_one_base_model_batch_controller_model_batch(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelBatchesApi->create_one_base_model_batch_controller_model_batch: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CreateModelBatchDto**](CreateModelBatchDto.md)|  | 

### Return type

[**ModelBatchResponseDto**](ModelBatchResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_one_base_model_batch_controller_model_batch**
> delete_one_base_model_batch_controller_model_batch(id)

Delete a single ModelBatch

### Example
```python
from __future__ import print_function
import time
import curia.api.curia.api.curia.api.curia.api.swagger_client
from curia.api.curia.api.curia.api.curia.api.swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = curia.api.curia.api.curia.api.swagger_client.Configuration()
configuration.api_key['Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = curia.api.curia.api.curia.api.swagger_client.ModelBatchesApi(curia.api.curia.api.curia.api.swagger_client.ApiClient(configuration))
id = 'id_example' # str | 

try:
    # Delete a single ModelBatch
    api_instance.delete_one_base_model_batch_controller_model_batch(id)
except ApiException as e:
    print("Exception when calling ModelBatchesApi->delete_one_base_model_batch_controller_model_batch: %s\n" % e)
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

# **get_many_base_model_batch_controller_model_batch**
> GetManyModelBatchResponseDto get_many_base_model_batch_controller_model_batch(fields=fields, s=s, filter=filter, _or=_or, sort=sort, join=join, limit=limit, offset=offset, page=page, cache=cache)

Retrieve multiple ModelBatches

### Example
```python
from __future__ import print_function
import time
import curia.api.curia.api.curia.api.curia.api.swagger_client
from curia.api.curia.api.curia.api.curia.api.swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = curia.api.curia.api.curia.api.swagger_client.Configuration()
configuration.api_key['Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = curia.api.curia.api.curia.api.swagger_client.ModelBatchesApi(curia.api.curia.api.curia.api.swagger_client.ApiClient(configuration))
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
    # Retrieve multiple ModelBatches
    api_response = api_instance.get_many_base_model_batch_controller_model_batch(fields=fields, s=s, filter=filter, _or=_or, sort=sort, join=join, limit=limit, offset=offset, page=page, cache=cache)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelBatchesApi->get_many_base_model_batch_controller_model_batch: %s\n" % e)
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

[**GetManyModelBatchResponseDto**](GetManyModelBatchResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_one_base_model_batch_controller_model_batch**
> ModelBatchResponseDto get_one_base_model_batch_controller_model_batch(id, fields=fields, join=join, cache=cache)

Retrieve a single ModelBatch

### Example
```python
from __future__ import print_function
import time
import curia.api.curia.api.curia.api.curia.api.swagger_client
from curia.api.curia.api.curia.api.curia.api.swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = curia.api.curia.api.curia.api.swagger_client.Configuration()
configuration.api_key['Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = curia.api.curia.api.curia.api.swagger_client.ModelBatchesApi(curia.api.curia.api.curia.api.swagger_client.ApiClient(configuration))
id = 'id_example' # str | 
fields = ['fields_example'] # list[str] | Selects resource fields. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#select\" target=\"_blank\">Docs</a> (optional)
join = ['join_example'] # list[str] | Adds relational resources. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#join\" target=\"_blank\">Docs</a> (optional)
cache = 56 # int | Reset cache (if was enabled). <a href=\"https://github.com/nestjsx/crud/wiki/Requests#cache\" target=\"_blank\">Docs</a> (optional)

try:
    # Retrieve a single ModelBatch
    api_response = api_instance.get_one_base_model_batch_controller_model_batch(id, fields=fields, join=join, cache=cache)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelBatchesApi->get_one_base_model_batch_controller_model_batch: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **fields** | [**list[str]**](str.md)| Selects resource fields. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#select\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **join** | [**list[str]**](str.md)| Adds relational resources. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#join\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **cache** | **int**| Reset cache (if was enabled). &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#cache\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 

### Return type

[**ModelBatchResponseDto**](ModelBatchResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_one_base_model_batch_controller_model_batch**
> ModelBatchResponseDto replace_one_base_model_batch_controller_model_batch(body, id)

Replace a single ModelBatch

### Example
```python
from __future__ import print_function
import time
import curia.api.curia.api.curia.api.curia.api.swagger_client
from curia.api.curia.api.curia.api.curia.api.swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = curia.api.curia.api.curia.api.swagger_client.Configuration()
configuration.api_key['Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = curia.api.curia.api.curia.api.swagger_client.ModelBatchesApi(curia.api.curia.api.curia.api.swagger_client.ApiClient(configuration))
body = curia.api.curia.api.curia.api.swagger_client.ModelBatchResponseDto() # ModelBatchResponseDto | 
id = 'id_example' # str | 

try:
    # Replace a single ModelBatch
    api_response = api_instance.replace_one_base_model_batch_controller_model_batch(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelBatchesApi->replace_one_base_model_batch_controller_model_batch: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ModelBatchResponseDto**](ModelBatchResponseDto.md)|  | 
 **id** | **str**|  | 

### Return type

[**ModelBatchResponseDto**](ModelBatchResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_one_base_model_batch_controller_model_batch**
> ModelBatchResponseDto update_one_base_model_batch_controller_model_batch(body, id)

Update a single ModelBatch

### Example
```python
from __future__ import print_function
import time
import curia.api.curia.api.curia.api.curia.api.swagger_client
from curia.api.curia.api.curia.api.curia.api.swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = curia.api.curia.api.curia.api.swagger_client.Configuration()
configuration.api_key['Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = curia.api.curia.api.curia.api.swagger_client.ModelBatchesApi(curia.api.curia.api.curia.api.swagger_client.ApiClient(configuration))
body = curia.api.curia.api.curia.api.swagger_client.UpdateModelBatchDto() # UpdateModelBatchDto | 
id = 'id_example' # str | 

try:
    # Update a single ModelBatch
    api_response = api_instance.update_one_base_model_batch_controller_model_batch(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelBatchesApi->update_one_base_model_batch_controller_model_batch: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**UpdateModelBatchDto**](UpdateModelBatchDto.md)|  | 
 **id** | **str**|  | 

### Return type

[**ModelBatchResponseDto**](ModelBatchResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

