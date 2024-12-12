# curia.api.curia.api.curia.api.swagger_client.ProcessJobStatusesApi

All URIs are relative to *https://api.curia.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_many_base_process_job_status_controller_process_job_status**](ProcessJobStatusesApi.md#create_many_base_process_job_status_controller_process_job_status) | **POST** /process-job-statuses/bulk | Create multiple ProcessJobStatuses
[**create_one_base_process_job_status_controller_process_job_status**](ProcessJobStatusesApi.md#create_one_base_process_job_status_controller_process_job_status) | **POST** /process-job-statuses | Create a single ProcessJobStatus
[**delete_one_base_process_job_status_controller_process_job_status**](ProcessJobStatusesApi.md#delete_one_base_process_job_status_controller_process_job_status) | **DELETE** /process-job-statuses/{id} | Delete a single ProcessJobStatus
[**get_many_base_process_job_status_controller_process_job_status**](ProcessJobStatusesApi.md#get_many_base_process_job_status_controller_process_job_status) | **GET** /process-job-statuses | Retrieve multiple ProcessJobStatuses
[**get_one_base_process_job_status_controller_process_job_status**](ProcessJobStatusesApi.md#get_one_base_process_job_status_controller_process_job_status) | **GET** /process-job-statuses/{id} | Retrieve a single ProcessJobStatus
[**replace_one_base_process_job_status_controller_process_job_status**](ProcessJobStatusesApi.md#replace_one_base_process_job_status_controller_process_job_status) | **PUT** /process-job-statuses/{id} | Replace a single ProcessJobStatus
[**update_one_base_process_job_status_controller_process_job_status**](ProcessJobStatusesApi.md#update_one_base_process_job_status_controller_process_job_status) | **PATCH** /process-job-statuses/{id} | Update a single ProcessJobStatus

# **create_many_base_process_job_status_controller_process_job_status**
> list[ProcessJobStatusResponseDto] create_many_base_process_job_status_controller_process_job_status(body)

Create multiple ProcessJobStatuses

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
api_instance = curia.api.curia.api.curia.api.swagger_client.ProcessJobStatusesApi(curia.api.curia.api.curia.api.swagger_client.ApiClient(configuration))
body = curia.api.curia.api.curia.api.swagger_client.CreateManyProcessJobStatusDto() # CreateManyProcessJobStatusDto | 

try:
    # Create multiple ProcessJobStatuses
    api_response = api_instance.create_many_base_process_job_status_controller_process_job_status(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProcessJobStatusesApi->create_many_base_process_job_status_controller_process_job_status: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CreateManyProcessJobStatusDto**](CreateManyProcessJobStatusDto.md)|  | 

### Return type

[**list[ProcessJobStatusResponseDto]**](ProcessJobStatusResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_one_base_process_job_status_controller_process_job_status**
> ProcessJobStatusResponseDto create_one_base_process_job_status_controller_process_job_status(body)

Create a single ProcessJobStatus

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
api_instance = curia.api.curia.api.curia.api.swagger_client.ProcessJobStatusesApi(curia.api.curia.api.curia.api.swagger_client.ApiClient(configuration))
body = curia.api.curia.api.curia.api.swagger_client.CreateProcessJobStatusDto() # CreateProcessJobStatusDto | 

try:
    # Create a single ProcessJobStatus
    api_response = api_instance.create_one_base_process_job_status_controller_process_job_status(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProcessJobStatusesApi->create_one_base_process_job_status_controller_process_job_status: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CreateProcessJobStatusDto**](CreateProcessJobStatusDto.md)|  | 

### Return type

[**ProcessJobStatusResponseDto**](ProcessJobStatusResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_one_base_process_job_status_controller_process_job_status**
> delete_one_base_process_job_status_controller_process_job_status(id)

Delete a single ProcessJobStatus

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
api_instance = curia.api.curia.api.curia.api.swagger_client.ProcessJobStatusesApi(curia.api.curia.api.curia.api.swagger_client.ApiClient(configuration))
id = 'id_example' # str | 

try:
    # Delete a single ProcessJobStatus
    api_instance.delete_one_base_process_job_status_controller_process_job_status(id)
except ApiException as e:
    print("Exception when calling ProcessJobStatusesApi->delete_one_base_process_job_status_controller_process_job_status: %s\n" % e)
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

# **get_many_base_process_job_status_controller_process_job_status**
> GetManyProcessJobStatusResponseDto get_many_base_process_job_status_controller_process_job_status(fields=fields, s=s, filter=filter, _or=_or, sort=sort, join=join, limit=limit, offset=offset, page=page, cache=cache)

Retrieve multiple ProcessJobStatuses

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
api_instance = curia.api.curia.api.curia.api.swagger_client.ProcessJobStatusesApi(curia.api.curia.api.curia.api.swagger_client.ApiClient(configuration))
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
    # Retrieve multiple ProcessJobStatuses
    api_response = api_instance.get_many_base_process_job_status_controller_process_job_status(fields=fields, s=s, filter=filter, _or=_or, sort=sort, join=join, limit=limit, offset=offset, page=page, cache=cache)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProcessJobStatusesApi->get_many_base_process_job_status_controller_process_job_status: %s\n" % e)
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

[**GetManyProcessJobStatusResponseDto**](GetManyProcessJobStatusResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_one_base_process_job_status_controller_process_job_status**
> ProcessJobStatusResponseDto get_one_base_process_job_status_controller_process_job_status(id, fields=fields, join=join, cache=cache)

Retrieve a single ProcessJobStatus

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
api_instance = curia.api.curia.api.curia.api.swagger_client.ProcessJobStatusesApi(curia.api.curia.api.curia.api.swagger_client.ApiClient(configuration))
id = 'id_example' # str | 
fields = ['fields_example'] # list[str] | Selects resource fields. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#select\" target=\"_blank\">Docs</a> (optional)
join = ['join_example'] # list[str] | Adds relational resources. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#join\" target=\"_blank\">Docs</a> (optional)
cache = 56 # int | Reset cache (if was enabled). <a href=\"https://github.com/nestjsx/crud/wiki/Requests#cache\" target=\"_blank\">Docs</a> (optional)

try:
    # Retrieve a single ProcessJobStatus
    api_response = api_instance.get_one_base_process_job_status_controller_process_job_status(id, fields=fields, join=join, cache=cache)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProcessJobStatusesApi->get_one_base_process_job_status_controller_process_job_status: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **fields** | [**list[str]**](str.md)| Selects resource fields. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#select\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **join** | [**list[str]**](str.md)| Adds relational resources. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#join\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **cache** | **int**| Reset cache (if was enabled). &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#cache\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 

### Return type

[**ProcessJobStatusResponseDto**](ProcessJobStatusResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_one_base_process_job_status_controller_process_job_status**
> ProcessJobStatusResponseDto replace_one_base_process_job_status_controller_process_job_status(body, id)

Replace a single ProcessJobStatus

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
api_instance = curia.api.curia.api.curia.api.swagger_client.ProcessJobStatusesApi(curia.api.curia.api.curia.api.swagger_client.ApiClient(configuration))
body = curia.api.curia.api.curia.api.swagger_client.ProcessJobStatusResponseDto() # ProcessJobStatusResponseDto | 
id = 'id_example' # str | 

try:
    # Replace a single ProcessJobStatus
    api_response = api_instance.replace_one_base_process_job_status_controller_process_job_status(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProcessJobStatusesApi->replace_one_base_process_job_status_controller_process_job_status: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ProcessJobStatusResponseDto**](ProcessJobStatusResponseDto.md)|  | 
 **id** | **str**|  | 

### Return type

[**ProcessJobStatusResponseDto**](ProcessJobStatusResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_one_base_process_job_status_controller_process_job_status**
> ProcessJobStatusResponseDto update_one_base_process_job_status_controller_process_job_status(body, id)

Update a single ProcessJobStatus

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
api_instance = curia.api.curia.api.curia.api.swagger_client.ProcessJobStatusesApi(curia.api.curia.api.curia.api.swagger_client.ApiClient(configuration))
body = curia.api.curia.api.curia.api.swagger_client.UpdateProcessJobStatusDto() # UpdateProcessJobStatusDto | 
id = 'id_example' # str | 

try:
    # Update a single ProcessJobStatus
    api_response = api_instance.update_one_base_process_job_status_controller_process_job_status(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProcessJobStatusesApi->update_one_base_process_job_status_controller_process_job_status: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**UpdateProcessJobStatusDto**](UpdateProcessJobStatusDto.md)|  | 
 **id** | **str**|  | 

### Return type

[**ProcessJobStatusResponseDto**](ProcessJobStatusResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

