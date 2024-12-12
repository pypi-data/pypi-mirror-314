# curia.api.curia.api.curia.api.swagger_client.ModelBatchJobsApi

All URIs are relative to *https://api.curia.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_many_base_model_batch_job_controller_model_batch_job**](ModelBatchJobsApi.md#create_many_base_model_batch_job_controller_model_batch_job) | **POST** /model-batch-jobs/bulk | Create multiple ModelBatchJobs
[**create_one_base_model_batch_job_controller_model_batch_job**](ModelBatchJobsApi.md#create_one_base_model_batch_job_controller_model_batch_job) | **POST** /model-batch-jobs | Create a single ModelBatchJob
[**delete_one_base_model_batch_job_controller_model_batch_job**](ModelBatchJobsApi.md#delete_one_base_model_batch_job_controller_model_batch_job) | **DELETE** /model-batch-jobs/{id} | Delete a single ModelBatchJob
[**get_many_base_model_batch_job_controller_model_batch_job**](ModelBatchJobsApi.md#get_many_base_model_batch_job_controller_model_batch_job) | **GET** /model-batch-jobs | Retrieve multiple ModelBatchJobs
[**get_one_base_model_batch_job_controller_model_batch_job**](ModelBatchJobsApi.md#get_one_base_model_batch_job_controller_model_batch_job) | **GET** /model-batch-jobs/{id} | Retrieve a single ModelBatchJob
[**model_batch_job_controller_start**](ModelBatchJobsApi.md#model_batch_job_controller_start) | **GET** /model-batch-jobs/{id}/start | Start model batch job
[**model_batch_job_controller_status**](ModelBatchJobsApi.md#model_batch_job_controller_status) | **GET** /model-batch-jobs/{id}/status | Retrieve model batch job status
[**model_batch_job_controller_stop**](ModelBatchJobsApi.md#model_batch_job_controller_stop) | **GET** /model-batch-jobs/{id}/stop | Stop model batch job
[**replace_one_base_model_batch_job_controller_model_batch_job**](ModelBatchJobsApi.md#replace_one_base_model_batch_job_controller_model_batch_job) | **PUT** /model-batch-jobs/{id} | Replace a single ModelBatchJob
[**update_one_base_model_batch_job_controller_model_batch_job**](ModelBatchJobsApi.md#update_one_base_model_batch_job_controller_model_batch_job) | **PATCH** /model-batch-jobs/{id} | Update a single ModelBatchJob

# **create_many_base_model_batch_job_controller_model_batch_job**
> list[ModelBatchJobResponseDto] create_many_base_model_batch_job_controller_model_batch_job(body)

Create multiple ModelBatchJobs

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
api_instance = curia.api.curia.api.curia.api.swagger_client.ModelBatchJobsApi(curia.api.curia.api.curia.api.swagger_client.ApiClient(configuration))
body = curia.api.curia.api.curia.api.swagger_client.CreateManyModelBatchJobDto() # CreateManyModelBatchJobDto | 

try:
    # Create multiple ModelBatchJobs
    api_response = api_instance.create_many_base_model_batch_job_controller_model_batch_job(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelBatchJobsApi->create_many_base_model_batch_job_controller_model_batch_job: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CreateManyModelBatchJobDto**](CreateManyModelBatchJobDto.md)|  | 

### Return type

[**list[ModelBatchJobResponseDto]**](ModelBatchJobResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_one_base_model_batch_job_controller_model_batch_job**
> ModelBatchJobResponseDto create_one_base_model_batch_job_controller_model_batch_job(body)

Create a single ModelBatchJob

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
api_instance = curia.api.curia.api.curia.api.swagger_client.ModelBatchJobsApi(curia.api.curia.api.curia.api.swagger_client.ApiClient(configuration))
body = curia.api.curia.api.curia.api.swagger_client.CreateModelBatchJobDto() # CreateModelBatchJobDto | 

try:
    # Create a single ModelBatchJob
    api_response = api_instance.create_one_base_model_batch_job_controller_model_batch_job(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelBatchJobsApi->create_one_base_model_batch_job_controller_model_batch_job: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CreateModelBatchJobDto**](CreateModelBatchJobDto.md)|  | 

### Return type

[**ModelBatchJobResponseDto**](ModelBatchJobResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_one_base_model_batch_job_controller_model_batch_job**
> delete_one_base_model_batch_job_controller_model_batch_job(id)

Delete a single ModelBatchJob

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
api_instance = curia.api.curia.api.curia.api.swagger_client.ModelBatchJobsApi(curia.api.curia.api.curia.api.swagger_client.ApiClient(configuration))
id = 'id_example' # str | 

try:
    # Delete a single ModelBatchJob
    api_instance.delete_one_base_model_batch_job_controller_model_batch_job(id)
except ApiException as e:
    print("Exception when calling ModelBatchJobsApi->delete_one_base_model_batch_job_controller_model_batch_job: %s\n" % e)
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

# **get_many_base_model_batch_job_controller_model_batch_job**
> GetManyModelBatchJobResponseDto get_many_base_model_batch_job_controller_model_batch_job(fields=fields, s=s, filter=filter, _or=_or, sort=sort, join=join, limit=limit, offset=offset, page=page, cache=cache)

Retrieve multiple ModelBatchJobs

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
api_instance = curia.api.curia.api.curia.api.swagger_client.ModelBatchJobsApi(curia.api.curia.api.curia.api.swagger_client.ApiClient(configuration))
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
    # Retrieve multiple ModelBatchJobs
    api_response = api_instance.get_many_base_model_batch_job_controller_model_batch_job(fields=fields, s=s, filter=filter, _or=_or, sort=sort, join=join, limit=limit, offset=offset, page=page, cache=cache)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelBatchJobsApi->get_many_base_model_batch_job_controller_model_batch_job: %s\n" % e)
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

[**GetManyModelBatchJobResponseDto**](GetManyModelBatchJobResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_one_base_model_batch_job_controller_model_batch_job**
> ModelBatchJobResponseDto get_one_base_model_batch_job_controller_model_batch_job(id, fields=fields, join=join, cache=cache)

Retrieve a single ModelBatchJob

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
api_instance = curia.api.curia.api.curia.api.swagger_client.ModelBatchJobsApi(curia.api.curia.api.curia.api.swagger_client.ApiClient(configuration))
id = 'id_example' # str | 
fields = ['fields_example'] # list[str] | Selects resource fields. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#select\" target=\"_blank\">Docs</a> (optional)
join = ['join_example'] # list[str] | Adds relational resources. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#join\" target=\"_blank\">Docs</a> (optional)
cache = 56 # int | Reset cache (if was enabled). <a href=\"https://github.com/nestjsx/crud/wiki/Requests#cache\" target=\"_blank\">Docs</a> (optional)

try:
    # Retrieve a single ModelBatchJob
    api_response = api_instance.get_one_base_model_batch_job_controller_model_batch_job(id, fields=fields, join=join, cache=cache)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelBatchJobsApi->get_one_base_model_batch_job_controller_model_batch_job: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **fields** | [**list[str]**](str.md)| Selects resource fields. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#select\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **join** | [**list[str]**](str.md)| Adds relational resources. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#join\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **cache** | **int**| Reset cache (if was enabled). &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#cache\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 

### Return type

[**ModelBatchJobResponseDto**](ModelBatchJobResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **model_batch_job_controller_start**
> ModelBatchJob model_batch_job_controller_start(id, type)

Start model batch job

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
api_instance = curia.api.curia.api.curia.api.swagger_client.ModelBatchJobsApi(curia.api.curia.api.curia.api.swagger_client.ApiClient(configuration))
id = 'id_example' # str | 
type = 'type_example' # str | Model Job Type. Can be train or predict

try:
    # Start model batch job
    api_response = api_instance.model_batch_job_controller_start(id, type)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelBatchJobsApi->model_batch_job_controller_start: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **type** | **str**| Model Job Type. Can be train or predict | 

### Return type

[**ModelBatchJob**](ModelBatchJob.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **model_batch_job_controller_status**
> ModelBatchJob model_batch_job_controller_status(id)

Retrieve model batch job status

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
api_instance = curia.api.curia.api.curia.api.swagger_client.ModelBatchJobsApi(curia.api.curia.api.curia.api.swagger_client.ApiClient(configuration))
id = 'id_example' # str | 

try:
    # Retrieve model batch job status
    api_response = api_instance.model_batch_job_controller_status(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelBatchJobsApi->model_batch_job_controller_status: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

[**ModelBatchJob**](ModelBatchJob.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **model_batch_job_controller_stop**
> ModelBatchJob model_batch_job_controller_stop(id)

Stop model batch job

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
api_instance = curia.api.curia.api.curia.api.swagger_client.ModelBatchJobsApi(curia.api.curia.api.curia.api.swagger_client.ApiClient(configuration))
id = 'id_example' # str | 

try:
    # Stop model batch job
    api_response = api_instance.model_batch_job_controller_stop(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelBatchJobsApi->model_batch_job_controller_stop: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

[**ModelBatchJob**](ModelBatchJob.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_one_base_model_batch_job_controller_model_batch_job**
> ModelBatchJobResponseDto replace_one_base_model_batch_job_controller_model_batch_job(body, id)

Replace a single ModelBatchJob

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
api_instance = curia.api.curia.api.curia.api.swagger_client.ModelBatchJobsApi(curia.api.curia.api.curia.api.swagger_client.ApiClient(configuration))
body = curia.api.curia.api.curia.api.swagger_client.ModelBatchJobResponseDto() # ModelBatchJobResponseDto | 
id = 'id_example' # str | 

try:
    # Replace a single ModelBatchJob
    api_response = api_instance.replace_one_base_model_batch_job_controller_model_batch_job(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelBatchJobsApi->replace_one_base_model_batch_job_controller_model_batch_job: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ModelBatchJobResponseDto**](ModelBatchJobResponseDto.md)|  | 
 **id** | **str**|  | 

### Return type

[**ModelBatchJobResponseDto**](ModelBatchJobResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_one_base_model_batch_job_controller_model_batch_job**
> ModelBatchJobResponseDto update_one_base_model_batch_job_controller_model_batch_job(body, id)

Update a single ModelBatchJob

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
api_instance = curia.api.curia.api.curia.api.swagger_client.ModelBatchJobsApi(curia.api.curia.api.curia.api.swagger_client.ApiClient(configuration))
body = curia.api.curia.api.curia.api.swagger_client.UpdateModelBatchJobDto() # UpdateModelBatchJobDto | 
id = 'id_example' # str | 

try:
    # Update a single ModelBatchJob
    api_response = api_instance.update_one_base_model_batch_job_controller_model_batch_job(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelBatchJobsApi->update_one_base_model_batch_job_controller_model_batch_job: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**UpdateModelBatchJobDto**](UpdateModelBatchJobDto.md)|  | 
 **id** | **str**|  | 

### Return type

[**ModelBatchJobResponseDto**](ModelBatchJobResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

