# swagger_client.DatasetsApi

All URIs are relative to *https://api.curia.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_many_base_dataset_controller_dataset**](DatasetsApi.md#create_many_base_dataset_controller_dataset) | **POST** /datasets/bulk | Create multiple Datasets
[**create_one_base_dataset_controller_dataset**](DatasetsApi.md#create_one_base_dataset_controller_dataset) | **POST** /datasets | Create a single Dataset
[**dataset_controller_calculate_stats**](DatasetsApi.md#dataset_controller_calculate_stats) | **GET** /datasets/{id}/calculate-stats | Calculate dataset stats
[**dataset_controller_download_dataset**](DatasetsApi.md#dataset_controller_download_dataset) | **GET** /datasets/{id}/download | Download dataset
[**dataset_controller_get_datasets_by_tag**](DatasetsApi.md#dataset_controller_get_datasets_by_tag) | **GET** /datasets/tag/{tag} | Retrieve datasets by tag
[**dataset_controller_internal_download_dataset**](DatasetsApi.md#dataset_controller_internal_download_dataset) | **GET** /datasets/internal/{id}/download | Download dataset
[**dataset_controller_sync_to_snowflake**](DatasetsApi.md#dataset_controller_sync_to_snowflake) | **POST** /datasets/{id}/snowflake-upload | Copy the dataset into snowflake
[**dataset_controller_upload**](DatasetsApi.md#dataset_controller_upload) | **POST** /datasets/upload | Upload dataset
[**dataset_controller_upload_abort**](DatasetsApi.md#dataset_controller_upload_abort) | **POST** /datasets/upload-large-cancel | cancel multipart upload for large dataset
[**dataset_controller_upload_finish**](DatasetsApi.md#dataset_controller_upload_finish) | **POST** /datasets/upload-large-complete | complete upload for large dataset using multipart upload
[**dataset_controller_upload_multipart_start**](DatasetsApi.md#dataset_controller_upload_multipart_start) | **POST** /datasets/upload-large-start | Initiate upload for large dataset using multipart upload
[**delete_one_base_dataset_controller_dataset**](DatasetsApi.md#delete_one_base_dataset_controller_dataset) | **DELETE** /datasets/{id} | Delete a single Dataset
[**get_many_base_dataset_controller_dataset**](DatasetsApi.md#get_many_base_dataset_controller_dataset) | **GET** /datasets | Retrieve multiple Datasets
[**get_one_base_dataset_controller_dataset**](DatasetsApi.md#get_one_base_dataset_controller_dataset) | **GET** /datasets/{id} | Retrieve a single Dataset
[**replace_one_base_dataset_controller_dataset**](DatasetsApi.md#replace_one_base_dataset_controller_dataset) | **PUT** /datasets/{id} | Replace a single Dataset
[**update_one_base_dataset_controller_dataset**](DatasetsApi.md#update_one_base_dataset_controller_dataset) | **PATCH** /datasets/{id} | Update a single Dataset

# **create_many_base_dataset_controller_dataset**
> list[DatasetResponseDto] create_many_base_dataset_controller_dataset(body)

Create multiple Datasets

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
api_instance = swagger_client.DatasetsApi(swagger_client.ApiClient(configuration))
body = swagger_client.CreateManyDatasetDto() # CreateManyDatasetDto | 

try:
    # Create multiple Datasets
    api_response = api_instance.create_many_base_dataset_controller_dataset(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatasetsApi->create_many_base_dataset_controller_dataset: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CreateManyDatasetDto**](CreateManyDatasetDto.md)|  | 

### Return type

[**list[DatasetResponseDto]**](DatasetResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_one_base_dataset_controller_dataset**
> DatasetResponseDto create_one_base_dataset_controller_dataset(body)

Create a single Dataset

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
api_instance = swagger_client.DatasetsApi(swagger_client.ApiClient(configuration))
body = swagger_client.CreateDatasetDto() # CreateDatasetDto | 

try:
    # Create a single Dataset
    api_response = api_instance.create_one_base_dataset_controller_dataset(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatasetsApi->create_one_base_dataset_controller_dataset: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CreateDatasetDto**](CreateDatasetDto.md)|  | 

### Return type

[**DatasetResponseDto**](DatasetResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **dataset_controller_calculate_stats**
> str dataset_controller_calculate_stats(id)

Calculate dataset stats

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
api_instance = swagger_client.DatasetsApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | 

try:
    # Calculate dataset stats
    api_response = api_instance.dataset_controller_calculate_stats(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatasetsApi->dataset_controller_calculate_stats: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

**str**

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **dataset_controller_download_dataset**
> str dataset_controller_download_dataset(id, filetype=filetype)

Download dataset

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
api_instance = swagger_client.DatasetsApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | 
filetype = 'filetype_example' # str | Filetype for download can be csv or parquet. Default is parquet (optional)

try:
    # Download dataset
    api_response = api_instance.dataset_controller_download_dataset(id, filetype=filetype)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatasetsApi->dataset_controller_download_dataset: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **filetype** | **str**| Filetype for download can be csv or parquet. Default is parquet | [optional] 

### Return type

**str**

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **dataset_controller_get_datasets_by_tag**
> list[Dataset] dataset_controller_get_datasets_by_tag(tag, take=take, page=page)

Retrieve datasets by tag

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
api_instance = swagger_client.DatasetsApi(swagger_client.ApiClient(configuration))
tag = 'tag_example' # str | 
take = 1.2 # float | How many per page (optional)
page = 1.2 # float | page of query results (optional)

try:
    # Retrieve datasets by tag
    api_response = api_instance.dataset_controller_get_datasets_by_tag(tag, take=take, page=page)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatasetsApi->dataset_controller_get_datasets_by_tag: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tag** | **str**|  | 
 **take** | **float**| How many per page | [optional] 
 **page** | **float**| page of query results | [optional] 

### Return type

[**list[Dataset]**](Dataset.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **dataset_controller_internal_download_dataset**
> str dataset_controller_internal_download_dataset(id, filetype=filetype)

Download dataset

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
api_instance = swagger_client.DatasetsApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | 
filetype = 'filetype_example' # str | Filetype for download can be csv or parquet. Default is parquet (optional)

try:
    # Download dataset
    api_response = api_instance.dataset_controller_internal_download_dataset(id, filetype=filetype)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatasetsApi->dataset_controller_internal_download_dataset: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **filetype** | **str**| Filetype for download can be csv or parquet. Default is parquet | [optional] 

### Return type

**str**

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **dataset_controller_sync_to_snowflake**
> str dataset_controller_sync_to_snowflake(body, id)

Copy the dataset into snowflake

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
api_instance = swagger_client.DatasetsApi(swagger_client.ApiClient(configuration))
body = swagger_client.Body4() # Body4 | 
id = 'id_example' # str | 

try:
    # Copy the dataset into snowflake
    api_response = api_instance.dataset_controller_sync_to_snowflake(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatasetsApi->dataset_controller_sync_to_snowflake: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Body4**](Body4.md)|  | 
 **id** | **str**|  | 

### Return type

**str**

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **dataset_controller_upload**
> Dataset dataset_controller_upload(file)

Upload dataset

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
api_instance = swagger_client.DatasetsApi(swagger_client.ApiClient(configuration))
file = 'file_example' # str | 

try:
    # Upload dataset
    api_response = api_instance.dataset_controller_upload(file)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatasetsApi->dataset_controller_upload: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file** | **str**|  | 

### Return type

[**Dataset**](Dataset.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **dataset_controller_upload_abort**
> dataset_controller_upload_abort(body)

cancel multipart upload for large dataset

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
api_instance = swagger_client.DatasetsApi(swagger_client.ApiClient(configuration))
body = swagger_client.Body3() # Body3 | 

try:
    # cancel multipart upload for large dataset
    api_instance.dataset_controller_upload_abort(body)
except ApiException as e:
    print("Exception when calling DatasetsApi->dataset_controller_upload_abort: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Body3**](Body3.md)|  | 

### Return type

void (empty response body)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **dataset_controller_upload_finish**
> Dataset dataset_controller_upload_finish(body)

complete upload for large dataset using multipart upload

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
api_instance = swagger_client.DatasetsApi(swagger_client.ApiClient(configuration))
body = swagger_client.Body2() # Body2 | 

try:
    # complete upload for large dataset using multipart upload
    api_response = api_instance.dataset_controller_upload_finish(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatasetsApi->dataset_controller_upload_finish: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Body2**](Body2.md)|  | 

### Return type

[**Dataset**](Dataset.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **dataset_controller_upload_multipart_start**
> dataset_controller_upload_multipart_start(body)

Initiate upload for large dataset using multipart upload

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
api_instance = swagger_client.DatasetsApi(swagger_client.ApiClient(configuration))
body = swagger_client.Body1() # Body1 | 

try:
    # Initiate upload for large dataset using multipart upload
    api_instance.dataset_controller_upload_multipart_start(body)
except ApiException as e:
    print("Exception when calling DatasetsApi->dataset_controller_upload_multipart_start: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Body1**](Body1.md)|  | 

### Return type

void (empty response body)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_one_base_dataset_controller_dataset**
> delete_one_base_dataset_controller_dataset(id)

Delete a single Dataset

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
api_instance = swagger_client.DatasetsApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | 

try:
    # Delete a single Dataset
    api_instance.delete_one_base_dataset_controller_dataset(id)
except ApiException as e:
    print("Exception when calling DatasetsApi->delete_one_base_dataset_controller_dataset: %s\n" % e)
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

# **get_many_base_dataset_controller_dataset**
> GetManyDatasetResponseDto get_many_base_dataset_controller_dataset(fields=fields, s=s, filter=filter, _or=_or, sort=sort, join=join, limit=limit, offset=offset, page=page, cache=cache)

Retrieve multiple Datasets

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
api_instance = swagger_client.DatasetsApi(swagger_client.ApiClient(configuration))
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
    # Retrieve multiple Datasets
    api_response = api_instance.get_many_base_dataset_controller_dataset(fields=fields, s=s, filter=filter, _or=_or, sort=sort, join=join, limit=limit, offset=offset, page=page, cache=cache)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatasetsApi->get_many_base_dataset_controller_dataset: %s\n" % e)
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

[**GetManyDatasetResponseDto**](GetManyDatasetResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_one_base_dataset_controller_dataset**
> DatasetResponseDto get_one_base_dataset_controller_dataset(id, fields=fields, join=join, cache=cache)

Retrieve a single Dataset

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
api_instance = swagger_client.DatasetsApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | 
fields = ['fields_example'] # list[str] | Selects resource fields. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#select\" target=\"_blank\">Docs</a> (optional)
join = ['join_example'] # list[str] | Adds relational resources. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#join\" target=\"_blank\">Docs</a> (optional)
cache = 56 # int | Reset cache (if was enabled). <a href=\"https://github.com/nestjsx/crud/wiki/Requests#cache\" target=\"_blank\">Docs</a> (optional)

try:
    # Retrieve a single Dataset
    api_response = api_instance.get_one_base_dataset_controller_dataset(id, fields=fields, join=join, cache=cache)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatasetsApi->get_one_base_dataset_controller_dataset: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **fields** | [**list[str]**](str.md)| Selects resource fields. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#select\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **join** | [**list[str]**](str.md)| Adds relational resources. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#join\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **cache** | **int**| Reset cache (if was enabled). &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#cache\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 

### Return type

[**DatasetResponseDto**](DatasetResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_one_base_dataset_controller_dataset**
> DatasetResponseDto replace_one_base_dataset_controller_dataset(body, id)

Replace a single Dataset

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
api_instance = swagger_client.DatasetsApi(swagger_client.ApiClient(configuration))
body = swagger_client.DatasetResponseDto() # DatasetResponseDto | 
id = 'id_example' # str | 

try:
    # Replace a single Dataset
    api_response = api_instance.replace_one_base_dataset_controller_dataset(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatasetsApi->replace_one_base_dataset_controller_dataset: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**DatasetResponseDto**](DatasetResponseDto.md)|  | 
 **id** | **str**|  | 

### Return type

[**DatasetResponseDto**](DatasetResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_one_base_dataset_controller_dataset**
> DatasetResponseDto update_one_base_dataset_controller_dataset(body, id)

Update a single Dataset

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
api_instance = swagger_client.DatasetsApi(swagger_client.ApiClient(configuration))
body = swagger_client.UpdateDatasetDto() # UpdateDatasetDto | 
id = 'id_example' # str | 

try:
    # Update a single Dataset
    api_response = api_instance.update_one_base_dataset_controller_dataset(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatasetsApi->update_one_base_dataset_controller_dataset: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**UpdateDatasetDto**](UpdateDatasetDto.md)|  | 
 **id** | **str**|  | 

### Return type

[**DatasetResponseDto**](DatasetResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

