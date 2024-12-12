# swagger_client.ModelJobsApi

All URIs are relative to *https://api.curia.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_many_base_model_job_controller_model_job**](ModelJobsApi.md#create_many_base_model_job_controller_model_job) | **POST** /model-jobs/bulk | Create multiple ModelJobs
[**create_one_base_model_job_controller_model_job**](ModelJobsApi.md#create_one_base_model_job_controller_model_job) | **POST** /model-jobs | Create a single ModelJob
[**delete_one_base_model_job_controller_model_job**](ModelJobsApi.md#delete_one_base_model_job_controller_model_job) | **DELETE** /model-jobs/{id} | Delete a single ModelJob
[**get_many_base_model_job_controller_model_job**](ModelJobsApi.md#get_many_base_model_job_controller_model_job) | **GET** /model-jobs | Retrieve multiple ModelJobs
[**get_one_base_model_job_controller_model_job**](ModelJobsApi.md#get_one_base_model_job_controller_model_job) | **GET** /model-jobs/{id} | Retrieve a single ModelJob
[**model_job_controller_generate_odhq**](ModelJobsApi.md#model_job_controller_generate_odhq) | **GET** /model-jobs/{id}/generate-odhq | Execute Outcome Distribution Histogram Query
[**model_job_controller_get_predictions_data**](ModelJobsApi.md#model_job_controller_get_predictions_data) | **GET** /model-jobs/{id}/predictions | Retrieve model job predictions
[**model_job_controller_start**](ModelJobsApi.md#model_job_controller_start) | **GET** /model-jobs/{id}/start | Start model job
[**model_job_controller_stop**](ModelJobsApi.md#model_job_controller_stop) | **GET** /model-jobs/{id}/stop | Stop Model job
[**replace_one_base_model_job_controller_model_job**](ModelJobsApi.md#replace_one_base_model_job_controller_model_job) | **PUT** /model-jobs/{id} | Replace a single ModelJob
[**update_one_base_model_job_controller_model_job**](ModelJobsApi.md#update_one_base_model_job_controller_model_job) | **PATCH** /model-jobs/{id} | Update a single ModelJob

# **create_many_base_model_job_controller_model_job**
> list[ModelJobResponseDto] create_many_base_model_job_controller_model_job(body)

Create multiple ModelJobs

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
api_instance = swagger_client.ModelJobsApi(swagger_client.ApiClient(configuration))
body = swagger_client.CreateManyModelJobDto() # CreateManyModelJobDto | 

try:
    # Create multiple ModelJobs
    api_response = api_instance.create_many_base_model_job_controller_model_job(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelJobsApi->create_many_base_model_job_controller_model_job: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CreateManyModelJobDto**](CreateManyModelJobDto.md)|  | 

### Return type

[**list[ModelJobResponseDto]**](ModelJobResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_one_base_model_job_controller_model_job**
> ModelJobResponseDto create_one_base_model_job_controller_model_job(body)

Create a single ModelJob

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
api_instance = swagger_client.ModelJobsApi(swagger_client.ApiClient(configuration))
body = swagger_client.CreateModelJobDto() # CreateModelJobDto | 

try:
    # Create a single ModelJob
    api_response = api_instance.create_one_base_model_job_controller_model_job(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelJobsApi->create_one_base_model_job_controller_model_job: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CreateModelJobDto**](CreateModelJobDto.md)|  | 

### Return type

[**ModelJobResponseDto**](ModelJobResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_one_base_model_job_controller_model_job**
> delete_one_base_model_job_controller_model_job(id)

Delete a single ModelJob

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
api_instance = swagger_client.ModelJobsApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | 

try:
    # Delete a single ModelJob
    api_instance.delete_one_base_model_job_controller_model_job(id)
except ApiException as e:
    print("Exception when calling ModelJobsApi->delete_one_base_model_job_controller_model_job: %s\n" % e)
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

# **get_many_base_model_job_controller_model_job**
> GetManyModelJobResponseDto get_many_base_model_job_controller_model_job(fields=fields, s=s, filter=filter, _or=_or, sort=sort, join=join, limit=limit, offset=offset, page=page, cache=cache)

Retrieve multiple ModelJobs

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
api_instance = swagger_client.ModelJobsApi(swagger_client.ApiClient(configuration))
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
    # Retrieve multiple ModelJobs
    api_response = api_instance.get_many_base_model_job_controller_model_job(fields=fields, s=s, filter=filter, _or=_or, sort=sort, join=join, limit=limit, offset=offset, page=page, cache=cache)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelJobsApi->get_many_base_model_job_controller_model_job: %s\n" % e)
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

[**GetManyModelJobResponseDto**](GetManyModelJobResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_one_base_model_job_controller_model_job**
> ModelJobResponseDto get_one_base_model_job_controller_model_job(id, fields=fields, join=join, cache=cache)

Retrieve a single ModelJob

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
api_instance = swagger_client.ModelJobsApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | 
fields = ['fields_example'] # list[str] | Selects resource fields. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#select\" target=\"_blank\">Docs</a> (optional)
join = ['join_example'] # list[str] | Adds relational resources. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#join\" target=\"_blank\">Docs</a> (optional)
cache = 56 # int | Reset cache (if was enabled). <a href=\"https://github.com/nestjsx/crud/wiki/Requests#cache\" target=\"_blank\">Docs</a> (optional)

try:
    # Retrieve a single ModelJob
    api_response = api_instance.get_one_base_model_job_controller_model_job(id, fields=fields, join=join, cache=cache)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelJobsApi->get_one_base_model_job_controller_model_job: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **fields** | [**list[str]**](str.md)| Selects resource fields. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#select\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **join** | [**list[str]**](str.md)| Adds relational resources. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#join\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **cache** | **int**| Reset cache (if was enabled). &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#cache\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 

### Return type

[**ModelJobResponseDto**](ModelJobResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **model_job_controller_generate_odhq**
> DataQuery model_job_controller_generate_odhq(id)

Execute Outcome Distribution Histogram Query

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
api_instance = swagger_client.ModelJobsApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | 

try:
    # Execute Outcome Distribution Histogram Query
    api_response = api_instance.model_job_controller_generate_odhq(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelJobsApi->model_job_controller_generate_odhq: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

[**DataQuery**](DataQuery.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **model_job_controller_get_predictions_data**
> str model_job_controller_get_predictions_data(id, type)

Retrieve model job predictions

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
api_instance = swagger_client.ModelJobsApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | 
type = 'type_example' # str | Model Job Type. Can be train or predict

try:
    # Retrieve model job predictions
    api_response = api_instance.model_job_controller_get_predictions_data(id, type)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelJobsApi->model_job_controller_get_predictions_data: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **type** | **str**| Model Job Type. Can be train or predict | 

### Return type

**str**

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **model_job_controller_start**
> ModelJob model_job_controller_start(id)

Start model job

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
api_instance = swagger_client.ModelJobsApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | 

try:
    # Start model job
    api_response = api_instance.model_job_controller_start(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelJobsApi->model_job_controller_start: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

[**ModelJob**](ModelJob.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **model_job_controller_stop**
> ModelJob model_job_controller_stop(id)

Stop Model job

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
api_instance = swagger_client.ModelJobsApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | 

try:
    # Stop Model job
    api_response = api_instance.model_job_controller_stop(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelJobsApi->model_job_controller_stop: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

[**ModelJob**](ModelJob.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_one_base_model_job_controller_model_job**
> ModelJobResponseDto replace_one_base_model_job_controller_model_job(body, id)

Replace a single ModelJob

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
api_instance = swagger_client.ModelJobsApi(swagger_client.ApiClient(configuration))
body = swagger_client.ModelJobResponseDto() # ModelJobResponseDto | 
id = 'id_example' # str | 

try:
    # Replace a single ModelJob
    api_response = api_instance.replace_one_base_model_job_controller_model_job(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelJobsApi->replace_one_base_model_job_controller_model_job: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ModelJobResponseDto**](ModelJobResponseDto.md)|  | 
 **id** | **str**|  | 

### Return type

[**ModelJobResponseDto**](ModelJobResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_one_base_model_job_controller_model_job**
> ModelJobResponseDto update_one_base_model_job_controller_model_job(body, id)

Update a single ModelJob

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
api_instance = swagger_client.ModelJobsApi(swagger_client.ApiClient(configuration))
body = swagger_client.UpdateModelJobDto() # UpdateModelJobDto | 
id = 'id_example' # str | 

try:
    # Update a single ModelJob
    api_response = api_instance.update_one_base_model_job_controller_model_job(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelJobsApi->update_one_base_model_job_controller_model_job: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**UpdateModelJobDto**](UpdateModelJobDto.md)|  | 
 **id** | **str**|  | 

### Return type

[**ModelJobResponseDto**](ModelJobResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

