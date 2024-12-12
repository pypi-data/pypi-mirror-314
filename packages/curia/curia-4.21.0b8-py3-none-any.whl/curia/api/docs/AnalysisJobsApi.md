# curia.api.curia.api.curia.api.swagger_client.AnalysisJobsApi

All URIs are relative to *https://api.curia.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**analysis_job_controller_start**](AnalysisJobsApi.md#analysis_job_controller_start) | **GET** /analysis-jobs/{id}/start | Start analysis job
[**analysis_job_controller_stop**](AnalysisJobsApi.md#analysis_job_controller_stop) | **GET** /analysis-jobs/{id}/stop | Stop analysis job
[**create_many_base_analysis_job_controller_analysis_job**](AnalysisJobsApi.md#create_many_base_analysis_job_controller_analysis_job) | **POST** /analysis-jobs/bulk | Create multiple AnalysisJobs
[**create_one_base_analysis_job_controller_analysis_job**](AnalysisJobsApi.md#create_one_base_analysis_job_controller_analysis_job) | **POST** /analysis-jobs | Create a single AnalysisJob
[**delete_one_base_analysis_job_controller_analysis_job**](AnalysisJobsApi.md#delete_one_base_analysis_job_controller_analysis_job) | **DELETE** /analysis-jobs/{id} | Delete a single AnalysisJob
[**get_many_base_analysis_job_controller_analysis_job**](AnalysisJobsApi.md#get_many_base_analysis_job_controller_analysis_job) | **GET** /analysis-jobs | Retrieve multiple AnalysisJobs
[**get_one_base_analysis_job_controller_analysis_job**](AnalysisJobsApi.md#get_one_base_analysis_job_controller_analysis_job) | **GET** /analysis-jobs/{id} | Retrieve a single AnalysisJob
[**replace_one_base_analysis_job_controller_analysis_job**](AnalysisJobsApi.md#replace_one_base_analysis_job_controller_analysis_job) | **PUT** /analysis-jobs/{id} | Replace a single AnalysisJob
[**update_one_base_analysis_job_controller_analysis_job**](AnalysisJobsApi.md#update_one_base_analysis_job_controller_analysis_job) | **PATCH** /analysis-jobs/{id} | Update a single AnalysisJob

# **analysis_job_controller_start**
> object analysis_job_controller_start(id)

Start analysis job

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
api_instance = curia.api.curia.api.curia.api.swagger_client.AnalysisJobsApi(curia.api.curia.api.curia.api.swagger_client.ApiClient(configuration))
id = 'id_example' # str | 

try:
    # Start analysis job
    api_response = api_instance.analysis_job_controller_start(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AnalysisJobsApi->analysis_job_controller_start: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

**object**

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **analysis_job_controller_stop**
> object analysis_job_controller_stop(id)

Stop analysis job

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
api_instance = curia.api.curia.api.curia.api.swagger_client.AnalysisJobsApi(curia.api.curia.api.curia.api.swagger_client.ApiClient(configuration))
id = 'id_example' # str | 

try:
    # Stop analysis job
    api_response = api_instance.analysis_job_controller_stop(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AnalysisJobsApi->analysis_job_controller_stop: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

**object**

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_many_base_analysis_job_controller_analysis_job**
> list[AnalysisJobResponseDto] create_many_base_analysis_job_controller_analysis_job(body)

Create multiple AnalysisJobs

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
api_instance = curia.api.curia.api.curia.api.swagger_client.AnalysisJobsApi(curia.api.curia.api.curia.api.swagger_client.ApiClient(configuration))
body = curia.api.curia.api.curia.api.swagger_client.CreateManyAnalysisJobDto() # CreateManyAnalysisJobDto | 

try:
    # Create multiple AnalysisJobs
    api_response = api_instance.create_many_base_analysis_job_controller_analysis_job(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AnalysisJobsApi->create_many_base_analysis_job_controller_analysis_job: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CreateManyAnalysisJobDto**](CreateManyAnalysisJobDto.md)|  | 

### Return type

[**list[AnalysisJobResponseDto]**](AnalysisJobResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_one_base_analysis_job_controller_analysis_job**
> AnalysisJobResponseDto create_one_base_analysis_job_controller_analysis_job(body)

Create a single AnalysisJob

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
api_instance = curia.api.curia.api.curia.api.swagger_client.AnalysisJobsApi(curia.api.curia.api.curia.api.swagger_client.ApiClient(configuration))
body = curia.api.curia.api.curia.api.swagger_client.CreateAnalysisJobDto() # CreateAnalysisJobDto | 

try:
    # Create a single AnalysisJob
    api_response = api_instance.create_one_base_analysis_job_controller_analysis_job(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AnalysisJobsApi->create_one_base_analysis_job_controller_analysis_job: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CreateAnalysisJobDto**](CreateAnalysisJobDto.md)|  | 

### Return type

[**AnalysisJobResponseDto**](AnalysisJobResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_one_base_analysis_job_controller_analysis_job**
> delete_one_base_analysis_job_controller_analysis_job(id)

Delete a single AnalysisJob

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
api_instance = curia.api.curia.api.curia.api.swagger_client.AnalysisJobsApi(curia.api.curia.api.curia.api.swagger_client.ApiClient(configuration))
id = 'id_example' # str | 

try:
    # Delete a single AnalysisJob
    api_instance.delete_one_base_analysis_job_controller_analysis_job(id)
except ApiException as e:
    print("Exception when calling AnalysisJobsApi->delete_one_base_analysis_job_controller_analysis_job: %s\n" % e)
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

# **get_many_base_analysis_job_controller_analysis_job**
> GetManyAnalysisJobResponseDto get_many_base_analysis_job_controller_analysis_job(fields=fields, s=s, filter=filter, _or=_or, sort=sort, join=join, limit=limit, offset=offset, page=page, cache=cache)

Retrieve multiple AnalysisJobs

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
api_instance = curia.api.curia.api.curia.api.swagger_client.AnalysisJobsApi(curia.api.curia.api.curia.api.swagger_client.ApiClient(configuration))
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
    # Retrieve multiple AnalysisJobs
    api_response = api_instance.get_many_base_analysis_job_controller_analysis_job(fields=fields, s=s, filter=filter, _or=_or, sort=sort, join=join, limit=limit, offset=offset, page=page, cache=cache)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AnalysisJobsApi->get_many_base_analysis_job_controller_analysis_job: %s\n" % e)
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

[**GetManyAnalysisJobResponseDto**](GetManyAnalysisJobResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_one_base_analysis_job_controller_analysis_job**
> AnalysisJobResponseDto get_one_base_analysis_job_controller_analysis_job(id, fields=fields, join=join, cache=cache)

Retrieve a single AnalysisJob

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
api_instance = curia.api.curia.api.curia.api.swagger_client.AnalysisJobsApi(curia.api.curia.api.curia.api.swagger_client.ApiClient(configuration))
id = 'id_example' # str | 
fields = ['fields_example'] # list[str] | Selects resource fields. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#select\" target=\"_blank\">Docs</a> (optional)
join = ['join_example'] # list[str] | Adds relational resources. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#join\" target=\"_blank\">Docs</a> (optional)
cache = 56 # int | Reset cache (if was enabled). <a href=\"https://github.com/nestjsx/crud/wiki/Requests#cache\" target=\"_blank\">Docs</a> (optional)

try:
    # Retrieve a single AnalysisJob
    api_response = api_instance.get_one_base_analysis_job_controller_analysis_job(id, fields=fields, join=join, cache=cache)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AnalysisJobsApi->get_one_base_analysis_job_controller_analysis_job: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **fields** | [**list[str]**](str.md)| Selects resource fields. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#select\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **join** | [**list[str]**](str.md)| Adds relational resources. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#join\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **cache** | **int**| Reset cache (if was enabled). &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#cache\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 

### Return type

[**AnalysisJobResponseDto**](AnalysisJobResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_one_base_analysis_job_controller_analysis_job**
> AnalysisJobResponseDto replace_one_base_analysis_job_controller_analysis_job(body, id)

Replace a single AnalysisJob

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
api_instance = curia.api.curia.api.curia.api.swagger_client.AnalysisJobsApi(curia.api.curia.api.curia.api.swagger_client.ApiClient(configuration))
body = curia.api.curia.api.curia.api.swagger_client.AnalysisJobResponseDto() # AnalysisJobResponseDto | 
id = 'id_example' # str | 

try:
    # Replace a single AnalysisJob
    api_response = api_instance.replace_one_base_analysis_job_controller_analysis_job(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AnalysisJobsApi->replace_one_base_analysis_job_controller_analysis_job: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AnalysisJobResponseDto**](AnalysisJobResponseDto.md)|  | 
 **id** | **str**|  | 

### Return type

[**AnalysisJobResponseDto**](AnalysisJobResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_one_base_analysis_job_controller_analysis_job**
> AnalysisJobResponseDto update_one_base_analysis_job_controller_analysis_job(body, id)

Update a single AnalysisJob

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
api_instance = curia.api.curia.api.curia.api.swagger_client.AnalysisJobsApi(curia.api.curia.api.curia.api.swagger_client.ApiClient(configuration))
body = curia.api.curia.api.curia.api.swagger_client.UpdateAnalysisJobDto() # UpdateAnalysisJobDto | 
id = 'id_example' # str | 

try:
    # Update a single AnalysisJob
    api_response = api_instance.update_one_base_analysis_job_controller_analysis_job(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AnalysisJobsApi->update_one_base_analysis_job_controller_analysis_job: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**UpdateAnalysisJobDto**](UpdateAnalysisJobDto.md)|  | 
 **id** | **str**|  | 

### Return type

[**AnalysisJobResponseDto**](AnalysisJobResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

