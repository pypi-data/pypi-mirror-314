# swagger_client.ModelJobOutputsApi

All URIs are relative to *https://api.curia.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_many_base_model_job_output_controller_model_job_output**](ModelJobOutputsApi.md#create_many_base_model_job_output_controller_model_job_output) | **POST** /model-job-outputs/bulk | Create multiple ModelJobOutputs
[**create_one_base_model_job_output_controller_model_job_output**](ModelJobOutputsApi.md#create_one_base_model_job_output_controller_model_job_output) | **POST** /model-job-outputs | Create a single ModelJobOutput
[**delete_one_base_model_job_output_controller_model_job_output**](ModelJobOutputsApi.md#delete_one_base_model_job_output_controller_model_job_output) | **DELETE** /model-job-outputs/{id} | Delete a single ModelJobOutput
[**get_many_base_model_job_output_controller_model_job_output**](ModelJobOutputsApi.md#get_many_base_model_job_output_controller_model_job_output) | **GET** /model-job-outputs | Retrieve multiple ModelJobOutputs
[**get_one_base_model_job_output_controller_model_job_output**](ModelJobOutputsApi.md#get_one_base_model_job_output_controller_model_job_output) | **GET** /model-job-outputs/{id} | Retrieve a single ModelJobOutput
[**replace_one_base_model_job_output_controller_model_job_output**](ModelJobOutputsApi.md#replace_one_base_model_job_output_controller_model_job_output) | **PUT** /model-job-outputs/{id} | Replace a single ModelJobOutput
[**update_one_base_model_job_output_controller_model_job_output**](ModelJobOutputsApi.md#update_one_base_model_job_output_controller_model_job_output) | **PATCH** /model-job-outputs/{id} | Update a single ModelJobOutput

# **create_many_base_model_job_output_controller_model_job_output**
> list[ModelJobOutputResponseDto] create_many_base_model_job_output_controller_model_job_output(body)

Create multiple ModelJobOutputs

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
api_instance = swagger_client.ModelJobOutputsApi(swagger_client.ApiClient(configuration))
body = swagger_client.CreateManyModelJobOutputDto() # CreateManyModelJobOutputDto | 

try:
    # Create multiple ModelJobOutputs
    api_response = api_instance.create_many_base_model_job_output_controller_model_job_output(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelJobOutputsApi->create_many_base_model_job_output_controller_model_job_output: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CreateManyModelJobOutputDto**](CreateManyModelJobOutputDto.md)|  | 

### Return type

[**list[ModelJobOutputResponseDto]**](ModelJobOutputResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_one_base_model_job_output_controller_model_job_output**
> ModelJobOutput create_one_base_model_job_output_controller_model_job_output(body)

Create a single ModelJobOutput

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
api_instance = swagger_client.ModelJobOutputsApi(swagger_client.ApiClient(configuration))
body = swagger_client.ModelJobOutput() # ModelJobOutput | 

try:
    # Create a single ModelJobOutput
    api_response = api_instance.create_one_base_model_job_output_controller_model_job_output(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelJobOutputsApi->create_one_base_model_job_output_controller_model_job_output: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ModelJobOutput**](ModelJobOutput.md)|  | 

### Return type

[**ModelJobOutput**](ModelJobOutput.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_one_base_model_job_output_controller_model_job_output**
> delete_one_base_model_job_output_controller_model_job_output(id)

Delete a single ModelJobOutput

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
api_instance = swagger_client.ModelJobOutputsApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | 

try:
    # Delete a single ModelJobOutput
    api_instance.delete_one_base_model_job_output_controller_model_job_output(id)
except ApiException as e:
    print("Exception when calling ModelJobOutputsApi->delete_one_base_model_job_output_controller_model_job_output: %s\n" % e)
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

# **get_many_base_model_job_output_controller_model_job_output**
> GetManyModelJobOutputResponseDto get_many_base_model_job_output_controller_model_job_output(fields=fields, s=s, filter=filter, _or=_or, sort=sort, join=join, limit=limit, offset=offset, page=page, cache=cache)

Retrieve multiple ModelJobOutputs

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
api_instance = swagger_client.ModelJobOutputsApi(swagger_client.ApiClient(configuration))
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
    # Retrieve multiple ModelJobOutputs
    api_response = api_instance.get_many_base_model_job_output_controller_model_job_output(fields=fields, s=s, filter=filter, _or=_or, sort=sort, join=join, limit=limit, offset=offset, page=page, cache=cache)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelJobOutputsApi->get_many_base_model_job_output_controller_model_job_output: %s\n" % e)
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

[**GetManyModelJobOutputResponseDto**](GetManyModelJobOutputResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_one_base_model_job_output_controller_model_job_output**
> ModelJobOutputResponseDto get_one_base_model_job_output_controller_model_job_output(id, fields=fields, join=join, cache=cache)

Retrieve a single ModelJobOutput

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
api_instance = swagger_client.ModelJobOutputsApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | 
fields = ['fields_example'] # list[str] | Selects resource fields. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#select\" target=\"_blank\">Docs</a> (optional)
join = ['join_example'] # list[str] | Adds relational resources. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#join\" target=\"_blank\">Docs</a> (optional)
cache = 56 # int | Reset cache (if was enabled). <a href=\"https://github.com/nestjsx/crud/wiki/Requests#cache\" target=\"_blank\">Docs</a> (optional)

try:
    # Retrieve a single ModelJobOutput
    api_response = api_instance.get_one_base_model_job_output_controller_model_job_output(id, fields=fields, join=join, cache=cache)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelJobOutputsApi->get_one_base_model_job_output_controller_model_job_output: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **fields** | [**list[str]**](str.md)| Selects resource fields. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#select\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **join** | [**list[str]**](str.md)| Adds relational resources. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#join\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **cache** | **int**| Reset cache (if was enabled). &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#cache\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 

### Return type

[**ModelJobOutputResponseDto**](ModelJobOutputResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_one_base_model_job_output_controller_model_job_output**
> ModelJobOutputResponseDto replace_one_base_model_job_output_controller_model_job_output(body, id)

Replace a single ModelJobOutput

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
api_instance = swagger_client.ModelJobOutputsApi(swagger_client.ApiClient(configuration))
body = swagger_client.ModelJobOutputResponseDto() # ModelJobOutputResponseDto | 
id = 'id_example' # str | 

try:
    # Replace a single ModelJobOutput
    api_response = api_instance.replace_one_base_model_job_output_controller_model_job_output(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelJobOutputsApi->replace_one_base_model_job_output_controller_model_job_output: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ModelJobOutputResponseDto**](ModelJobOutputResponseDto.md)|  | 
 **id** | **str**|  | 

### Return type

[**ModelJobOutputResponseDto**](ModelJobOutputResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_one_base_model_job_output_controller_model_job_output**
> ModelJobOutputResponseDto update_one_base_model_job_output_controller_model_job_output(body, id)

Update a single ModelJobOutput

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
api_instance = swagger_client.ModelJobOutputsApi(swagger_client.ApiClient(configuration))
body = swagger_client.UpdateModelJobOutputDto() # UpdateModelJobOutputDto | 
id = 'id_example' # str | 

try:
    # Update a single ModelJobOutput
    api_response = api_instance.update_one_base_model_job_output_controller_model_job_output(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelJobOutputsApi->update_one_base_model_job_output_controller_model_job_output: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**UpdateModelJobOutputDto**](UpdateModelJobOutputDto.md)|  | 
 **id** | **str**|  | 

### Return type

[**ModelJobOutputResponseDto**](ModelJobOutputResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

