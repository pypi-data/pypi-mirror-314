# swagger_client.TasksApi

All URIs are relative to *https://api.curia.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_many_base_task_controller_task**](TasksApi.md#create_many_base_task_controller_task) | **POST** /tasks/bulk | Create multiple Tasks
[**create_one_base_task_controller_task**](TasksApi.md#create_one_base_task_controller_task) | **POST** /tasks | Create a single Task
[**delete_one_base_task_controller_task**](TasksApi.md#delete_one_base_task_controller_task) | **DELETE** /tasks/{id} | Delete a single Task
[**get_many_base_task_controller_task**](TasksApi.md#get_many_base_task_controller_task) | **GET** /tasks | Retrieve multiple Tasks
[**get_one_base_task_controller_task**](TasksApi.md#get_one_base_task_controller_task) | **GET** /tasks/{id} | Retrieve a single Task
[**replace_one_base_task_controller_task**](TasksApi.md#replace_one_base_task_controller_task) | **PUT** /tasks/{id} | Replace a single Task
[**task_controller_create_task_from_databricks_job**](TasksApi.md#task_controller_create_task_from_databricks_job) | **POST** /tasks/create-from-databricks-job/ | Create task from Databricks job
[**task_controller_get_awsecr_repos**](TasksApi.md#task_controller_get_awsecr_repos) | **GET** /tasks/ecr-repos | List ECR repos
[**task_controller_list_databricks_jobs**](TasksApi.md#task_controller_list_databricks_jobs) | **GET** /tasks/databricks-jobs | List Databricks jobs
[**update_one_base_task_controller_task**](TasksApi.md#update_one_base_task_controller_task) | **PATCH** /tasks/{id} | Update a single Task

# **create_many_base_task_controller_task**
> list[TaskResponseDto] create_many_base_task_controller_task(body)

Create multiple Tasks

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
api_instance = swagger_client.TasksApi(swagger_client.ApiClient(configuration))
body = swagger_client.CreateManyTaskDto() # CreateManyTaskDto | 

try:
    # Create multiple Tasks
    api_response = api_instance.create_many_base_task_controller_task(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TasksApi->create_many_base_task_controller_task: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CreateManyTaskDto**](CreateManyTaskDto.md)|  | 

### Return type

[**list[TaskResponseDto]**](TaskResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_one_base_task_controller_task**
> TaskResponseDto create_one_base_task_controller_task(body)

Create a single Task

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
api_instance = swagger_client.TasksApi(swagger_client.ApiClient(configuration))
body = swagger_client.CreateTaskDto() # CreateTaskDto | 

try:
    # Create a single Task
    api_response = api_instance.create_one_base_task_controller_task(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TasksApi->create_one_base_task_controller_task: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CreateTaskDto**](CreateTaskDto.md)|  | 

### Return type

[**TaskResponseDto**](TaskResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_one_base_task_controller_task**
> delete_one_base_task_controller_task(id)

Delete a single Task

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
api_instance = swagger_client.TasksApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | 

try:
    # Delete a single Task
    api_instance.delete_one_base_task_controller_task(id)
except ApiException as e:
    print("Exception when calling TasksApi->delete_one_base_task_controller_task: %s\n" % e)
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

# **get_many_base_task_controller_task**
> GetManyTaskResponseDto get_many_base_task_controller_task(fields=fields, s=s, filter=filter, _or=_or, sort=sort, join=join, limit=limit, offset=offset, page=page, cache=cache)

Retrieve multiple Tasks

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
api_instance = swagger_client.TasksApi(swagger_client.ApiClient(configuration))
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
    # Retrieve multiple Tasks
    api_response = api_instance.get_many_base_task_controller_task(fields=fields, s=s, filter=filter, _or=_or, sort=sort, join=join, limit=limit, offset=offset, page=page, cache=cache)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TasksApi->get_many_base_task_controller_task: %s\n" % e)
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

[**GetManyTaskResponseDto**](GetManyTaskResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_one_base_task_controller_task**
> TaskResponseDto get_one_base_task_controller_task(id, fields=fields, join=join, cache=cache)

Retrieve a single Task

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
api_instance = swagger_client.TasksApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | 
fields = ['fields_example'] # list[str] | Selects resource fields. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#select\" target=\"_blank\">Docs</a> (optional)
join = ['join_example'] # list[str] | Adds relational resources. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#join\" target=\"_blank\">Docs</a> (optional)
cache = 56 # int | Reset cache (if was enabled). <a href=\"https://github.com/nestjsx/crud/wiki/Requests#cache\" target=\"_blank\">Docs</a> (optional)

try:
    # Retrieve a single Task
    api_response = api_instance.get_one_base_task_controller_task(id, fields=fields, join=join, cache=cache)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TasksApi->get_one_base_task_controller_task: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **fields** | [**list[str]**](str.md)| Selects resource fields. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#select\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **join** | [**list[str]**](str.md)| Adds relational resources. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#join\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **cache** | **int**| Reset cache (if was enabled). &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#cache\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 

### Return type

[**TaskResponseDto**](TaskResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_one_base_task_controller_task**
> TaskResponseDto replace_one_base_task_controller_task(body, id)

Replace a single Task

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
api_instance = swagger_client.TasksApi(swagger_client.ApiClient(configuration))
body = swagger_client.TaskResponseDto() # TaskResponseDto | 
id = 'id_example' # str | 

try:
    # Replace a single Task
    api_response = api_instance.replace_one_base_task_controller_task(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TasksApi->replace_one_base_task_controller_task: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TaskResponseDto**](TaskResponseDto.md)|  | 
 **id** | **str**|  | 

### Return type

[**TaskResponseDto**](TaskResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **task_controller_create_task_from_databricks_job**
> task_controller_create_task_from_databricks_job(body)

Create task from Databricks job

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
api_instance = swagger_client.TasksApi(swagger_client.ApiClient(configuration))
body = swagger_client.Body5() # Body5 | 

try:
    # Create task from Databricks job
    api_instance.task_controller_create_task_from_databricks_job(body)
except ApiException as e:
    print("Exception when calling TasksApi->task_controller_create_task_from_databricks_job: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Body5**](Body5.md)|  | 

### Return type

void (empty response body)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **task_controller_get_awsecr_repos**
> task_controller_get_awsecr_repos()

List ECR repos

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
api_instance = swagger_client.TasksApi(swagger_client.ApiClient(configuration))

try:
    # List ECR repos
    api_instance.task_controller_get_awsecr_repos()
except ApiException as e:
    print("Exception when calling TasksApi->task_controller_get_awsecr_repos: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **task_controller_list_databricks_jobs**
> task_controller_list_databricks_jobs()

List Databricks jobs

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
api_instance = swagger_client.TasksApi(swagger_client.ApiClient(configuration))

try:
    # List Databricks jobs
    api_instance.task_controller_list_databricks_jobs()
except ApiException as e:
    print("Exception when calling TasksApi->task_controller_list_databricks_jobs: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_one_base_task_controller_task**
> TaskResponseDto update_one_base_task_controller_task(body, id)

Update a single Task

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
api_instance = swagger_client.TasksApi(swagger_client.ApiClient(configuration))
body = swagger_client.UpdateTaskDto() # UpdateTaskDto | 
id = 'id_example' # str | 

try:
    # Update a single Task
    api_response = api_instance.update_one_base_task_controller_task(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TasksApi->update_one_base_task_controller_task: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**UpdateTaskDto**](UpdateTaskDto.md)|  | 
 **id** | **str**|  | 

### Return type

[**TaskResponseDto**](TaskResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

