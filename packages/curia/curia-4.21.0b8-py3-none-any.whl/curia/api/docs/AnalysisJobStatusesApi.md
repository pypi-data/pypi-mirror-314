# curia.api.curia.api.curia.api.swagger_client.AnalysisJobStatusesApi

All URIs are relative to *https://api.curia.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_many_base_analysis_job_status_controller_analysis_job_status**](AnalysisJobStatusesApi.md#create_many_base_analysis_job_status_controller_analysis_job_status) | **POST** /analysis-job-statuses/bulk | Create multiple AnalysisJobStatuses
[**create_one_base_analysis_job_status_controller_analysis_job_status**](AnalysisJobStatusesApi.md#create_one_base_analysis_job_status_controller_analysis_job_status) | **POST** /analysis-job-statuses | Create a single AnalysisJobStatus
[**delete_one_base_analysis_job_status_controller_analysis_job_status**](AnalysisJobStatusesApi.md#delete_one_base_analysis_job_status_controller_analysis_job_status) | **DELETE** /analysis-job-statuses/{id} | Delete a single AnalysisJobStatus
[**get_many_base_analysis_job_status_controller_analysis_job_status**](AnalysisJobStatusesApi.md#get_many_base_analysis_job_status_controller_analysis_job_status) | **GET** /analysis-job-statuses | Retrieve multiple AnalysisJobStatuses
[**get_one_base_analysis_job_status_controller_analysis_job_status**](AnalysisJobStatusesApi.md#get_one_base_analysis_job_status_controller_analysis_job_status) | **GET** /analysis-job-statuses/{id} | Retrieve a single AnalysisJobStatus
[**replace_one_base_analysis_job_status_controller_analysis_job_status**](AnalysisJobStatusesApi.md#replace_one_base_analysis_job_status_controller_analysis_job_status) | **PUT** /analysis-job-statuses/{id} | Replace a single AnalysisJobStatus
[**update_one_base_analysis_job_status_controller_analysis_job_status**](AnalysisJobStatusesApi.md#update_one_base_analysis_job_status_controller_analysis_job_status) | **PATCH** /analysis-job-statuses/{id} | Update a single AnalysisJobStatus

# **create_many_base_analysis_job_status_controller_analysis_job_status**
> list[AnalysisJobStatusResponseDto] create_many_base_analysis_job_status_controller_analysis_job_status(body)

Create multiple AnalysisJobStatuses

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
api_instance = curia.api.curia.api.curia.api.swagger_client.AnalysisJobStatusesApi(curia.api.curia.api.curia.api.swagger_client.ApiClient(configuration))
body = curia.api.curia.api.curia.api.swagger_client.CreateManyAnalysisJobStatusDto() # CreateManyAnalysisJobStatusDto | 

try:
    # Create multiple AnalysisJobStatuses
    api_response = api_instance.create_many_base_analysis_job_status_controller_analysis_job_status(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AnalysisJobStatusesApi->create_many_base_analysis_job_status_controller_analysis_job_status: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CreateManyAnalysisJobStatusDto**](CreateManyAnalysisJobStatusDto.md)|  | 

### Return type

[**list[AnalysisJobStatusResponseDto]**](AnalysisJobStatusResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_one_base_analysis_job_status_controller_analysis_job_status**
> AnalysisJobStatusResponseDto create_one_base_analysis_job_status_controller_analysis_job_status(body)

Create a single AnalysisJobStatus

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
api_instance = curia.api.curia.api.curia.api.swagger_client.AnalysisJobStatusesApi(curia.api.curia.api.curia.api.swagger_client.ApiClient(configuration))
body = curia.api.curia.api.curia.api.swagger_client.CreateAnalysisJobStatusDto() # CreateAnalysisJobStatusDto | 

try:
    # Create a single AnalysisJobStatus
    api_response = api_instance.create_one_base_analysis_job_status_controller_analysis_job_status(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AnalysisJobStatusesApi->create_one_base_analysis_job_status_controller_analysis_job_status: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CreateAnalysisJobStatusDto**](CreateAnalysisJobStatusDto.md)|  | 

### Return type

[**AnalysisJobStatusResponseDto**](AnalysisJobStatusResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_one_base_analysis_job_status_controller_analysis_job_status**
> delete_one_base_analysis_job_status_controller_analysis_job_status(id)

Delete a single AnalysisJobStatus

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
api_instance = curia.api.curia.api.curia.api.swagger_client.AnalysisJobStatusesApi(curia.api.curia.api.curia.api.swagger_client.ApiClient(configuration))
id = 'id_example' # str | 

try:
    # Delete a single AnalysisJobStatus
    api_instance.delete_one_base_analysis_job_status_controller_analysis_job_status(id)
except ApiException as e:
    print("Exception when calling AnalysisJobStatusesApi->delete_one_base_analysis_job_status_controller_analysis_job_status: %s\n" % e)
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

# **get_many_base_analysis_job_status_controller_analysis_job_status**
> GetManyAnalysisJobStatusResponseDto get_many_base_analysis_job_status_controller_analysis_job_status(fields=fields, s=s, filter=filter, _or=_or, sort=sort, join=join, limit=limit, offset=offset, page=page, cache=cache)

Retrieve multiple AnalysisJobStatuses

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
api_instance = curia.api.curia.api.curia.api.swagger_client.AnalysisJobStatusesApi(curia.api.curia.api.curia.api.swagger_client.ApiClient(configuration))
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
    # Retrieve multiple AnalysisJobStatuses
    api_response = api_instance.get_many_base_analysis_job_status_controller_analysis_job_status(fields=fields, s=s, filter=filter, _or=_or, sort=sort, join=join, limit=limit, offset=offset, page=page, cache=cache)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AnalysisJobStatusesApi->get_many_base_analysis_job_status_controller_analysis_job_status: %s\n" % e)
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

[**GetManyAnalysisJobStatusResponseDto**](GetManyAnalysisJobStatusResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_one_base_analysis_job_status_controller_analysis_job_status**
> AnalysisJobStatusResponseDto get_one_base_analysis_job_status_controller_analysis_job_status(id, fields=fields, join=join, cache=cache)

Retrieve a single AnalysisJobStatus

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
api_instance = curia.api.curia.api.curia.api.swagger_client.AnalysisJobStatusesApi(curia.api.curia.api.curia.api.swagger_client.ApiClient(configuration))
id = 'id_example' # str | 
fields = ['fields_example'] # list[str] | Selects resource fields. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#select\" target=\"_blank\">Docs</a> (optional)
join = ['join_example'] # list[str] | Adds relational resources. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#join\" target=\"_blank\">Docs</a> (optional)
cache = 56 # int | Reset cache (if was enabled). <a href=\"https://github.com/nestjsx/crud/wiki/Requests#cache\" target=\"_blank\">Docs</a> (optional)

try:
    # Retrieve a single AnalysisJobStatus
    api_response = api_instance.get_one_base_analysis_job_status_controller_analysis_job_status(id, fields=fields, join=join, cache=cache)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AnalysisJobStatusesApi->get_one_base_analysis_job_status_controller_analysis_job_status: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **fields** | [**list[str]**](str.md)| Selects resource fields. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#select\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **join** | [**list[str]**](str.md)| Adds relational resources. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#join\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **cache** | **int**| Reset cache (if was enabled). &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#cache\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 

### Return type

[**AnalysisJobStatusResponseDto**](AnalysisJobStatusResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_one_base_analysis_job_status_controller_analysis_job_status**
> AnalysisJobStatusResponseDto replace_one_base_analysis_job_status_controller_analysis_job_status(body, id)

Replace a single AnalysisJobStatus

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
api_instance = curia.api.curia.api.curia.api.swagger_client.AnalysisJobStatusesApi(curia.api.curia.api.curia.api.swagger_client.ApiClient(configuration))
body = curia.api.curia.api.curia.api.swagger_client.AnalysisJobStatusResponseDto() # AnalysisJobStatusResponseDto | 
id = 'id_example' # str | 

try:
    # Replace a single AnalysisJobStatus
    api_response = api_instance.replace_one_base_analysis_job_status_controller_analysis_job_status(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AnalysisJobStatusesApi->replace_one_base_analysis_job_status_controller_analysis_job_status: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AnalysisJobStatusResponseDto**](AnalysisJobStatusResponseDto.md)|  | 
 **id** | **str**|  | 

### Return type

[**AnalysisJobStatusResponseDto**](AnalysisJobStatusResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_one_base_analysis_job_status_controller_analysis_job_status**
> AnalysisJobStatusResponseDto update_one_base_analysis_job_status_controller_analysis_job_status(body, id)

Update a single AnalysisJobStatus

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
api_instance = curia.api.curia.api.curia.api.swagger_client.AnalysisJobStatusesApi(curia.api.curia.api.curia.api.swagger_client.ApiClient(configuration))
body = curia.api.curia.api.curia.api.swagger_client.UpdateAnalysisJobStatusDto() # UpdateAnalysisJobStatusDto | 
id = 'id_example' # str | 

try:
    # Update a single AnalysisJobStatus
    api_response = api_instance.update_one_base_analysis_job_status_controller_analysis_job_status(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AnalysisJobStatusesApi->update_one_base_analysis_job_status_controller_analysis_job_status: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**UpdateAnalysisJobStatusDto**](UpdateAnalysisJobStatusDto.md)|  | 
 **id** | **str**|  | 

### Return type

[**AnalysisJobStatusResponseDto**](AnalysisJobStatusResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

