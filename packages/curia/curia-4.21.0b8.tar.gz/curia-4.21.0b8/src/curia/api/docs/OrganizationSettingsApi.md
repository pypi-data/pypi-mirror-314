# swagger_client.OrganizationSettingsApi

All URIs are relative to *https://api.curia.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_many_base_organization_setting_controller_organization_setting**](OrganizationSettingsApi.md#create_many_base_organization_setting_controller_organization_setting) | **POST** /organization-settings/bulk | Create multiple OrganizationSettings
[**create_one_base_organization_setting_controller_organization_setting**](OrganizationSettingsApi.md#create_one_base_organization_setting_controller_organization_setting) | **POST** /organization-settings | Create a single OrganizationSetting
[**delete_one_base_organization_setting_controller_organization_setting**](OrganizationSettingsApi.md#delete_one_base_organization_setting_controller_organization_setting) | **DELETE** /organization-settings/{id} | Delete a single OrganizationSetting
[**get_many_base_organization_setting_controller_organization_setting**](OrganizationSettingsApi.md#get_many_base_organization_setting_controller_organization_setting) | **GET** /organization-settings | Retrieve multiple OrganizationSettings
[**get_one_base_organization_setting_controller_organization_setting**](OrganizationSettingsApi.md#get_one_base_organization_setting_controller_organization_setting) | **GET** /organization-settings/{id} | Retrieve a single OrganizationSetting
[**organization_setting_controller_get_unscoped_organization_settings**](OrganizationSettingsApi.md#organization_setting_controller_get_unscoped_organization_settings) | **GET** /organization-settings/unscoped | Retrieve all organization settings
[**organization_setting_controller_get_versions**](OrganizationSettingsApi.md#organization_setting_controller_get_versions) | **GET** /organization-settings/versions | Retrieve container versions
[**replace_one_base_organization_setting_controller_organization_setting**](OrganizationSettingsApi.md#replace_one_base_organization_setting_controller_organization_setting) | **PUT** /organization-settings/{id} | Replace a single OrganizationSetting
[**update_one_base_organization_setting_controller_organization_setting**](OrganizationSettingsApi.md#update_one_base_organization_setting_controller_organization_setting) | **PATCH** /organization-settings/{id} | Update a single OrganizationSetting

# **create_many_base_organization_setting_controller_organization_setting**
> list[OrganizationSettingResponseDto] create_many_base_organization_setting_controller_organization_setting(body)

Create multiple OrganizationSettings

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
api_instance = swagger_client.OrganizationSettingsApi(swagger_client.ApiClient(configuration))
body = swagger_client.CreateManyOrganizationSettingDto() # CreateManyOrganizationSettingDto | 

try:
    # Create multiple OrganizationSettings
    api_response = api_instance.create_many_base_organization_setting_controller_organization_setting(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrganizationSettingsApi->create_many_base_organization_setting_controller_organization_setting: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CreateManyOrganizationSettingDto**](CreateManyOrganizationSettingDto.md)|  | 

### Return type

[**list[OrganizationSettingResponseDto]**](OrganizationSettingResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_one_base_organization_setting_controller_organization_setting**
> OrganizationSettingResponseDto create_one_base_organization_setting_controller_organization_setting(body)

Create a single OrganizationSetting

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
api_instance = swagger_client.OrganizationSettingsApi(swagger_client.ApiClient(configuration))
body = swagger_client.CreateOrganizationSettingDto() # CreateOrganizationSettingDto | 

try:
    # Create a single OrganizationSetting
    api_response = api_instance.create_one_base_organization_setting_controller_organization_setting(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrganizationSettingsApi->create_one_base_organization_setting_controller_organization_setting: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CreateOrganizationSettingDto**](CreateOrganizationSettingDto.md)|  | 

### Return type

[**OrganizationSettingResponseDto**](OrganizationSettingResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_one_base_organization_setting_controller_organization_setting**
> delete_one_base_organization_setting_controller_organization_setting(id)

Delete a single OrganizationSetting

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
api_instance = swagger_client.OrganizationSettingsApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | 

try:
    # Delete a single OrganizationSetting
    api_instance.delete_one_base_organization_setting_controller_organization_setting(id)
except ApiException as e:
    print("Exception when calling OrganizationSettingsApi->delete_one_base_organization_setting_controller_organization_setting: %s\n" % e)
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

# **get_many_base_organization_setting_controller_organization_setting**
> GetManyOrganizationSettingResponseDto get_many_base_organization_setting_controller_organization_setting(fields=fields, s=s, filter=filter, _or=_or, sort=sort, join=join, limit=limit, offset=offset, page=page, cache=cache)

Retrieve multiple OrganizationSettings

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
api_instance = swagger_client.OrganizationSettingsApi(swagger_client.ApiClient(configuration))
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
    # Retrieve multiple OrganizationSettings
    api_response = api_instance.get_many_base_organization_setting_controller_organization_setting(fields=fields, s=s, filter=filter, _or=_or, sort=sort, join=join, limit=limit, offset=offset, page=page, cache=cache)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrganizationSettingsApi->get_many_base_organization_setting_controller_organization_setting: %s\n" % e)
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

[**GetManyOrganizationSettingResponseDto**](GetManyOrganizationSettingResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_one_base_organization_setting_controller_organization_setting**
> OrganizationSettingResponseDto get_one_base_organization_setting_controller_organization_setting(id, fields=fields, join=join, cache=cache)

Retrieve a single OrganizationSetting

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
api_instance = swagger_client.OrganizationSettingsApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | 
fields = ['fields_example'] # list[str] | Selects resource fields. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#select\" target=\"_blank\">Docs</a> (optional)
join = ['join_example'] # list[str] | Adds relational resources. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#join\" target=\"_blank\">Docs</a> (optional)
cache = 56 # int | Reset cache (if was enabled). <a href=\"https://github.com/nestjsx/crud/wiki/Requests#cache\" target=\"_blank\">Docs</a> (optional)

try:
    # Retrieve a single OrganizationSetting
    api_response = api_instance.get_one_base_organization_setting_controller_organization_setting(id, fields=fields, join=join, cache=cache)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrganizationSettingsApi->get_one_base_organization_setting_controller_organization_setting: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **fields** | [**list[str]**](str.md)| Selects resource fields. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#select\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **join** | [**list[str]**](str.md)| Adds relational resources. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#join\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **cache** | **int**| Reset cache (if was enabled). &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#cache\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 

### Return type

[**OrganizationSettingResponseDto**](OrganizationSettingResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **organization_setting_controller_get_unscoped_organization_settings**
> list[OrganizationSetting] organization_setting_controller_get_unscoped_organization_settings()

Retrieve all organization settings

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
api_instance = swagger_client.OrganizationSettingsApi(swagger_client.ApiClient(configuration))

try:
    # Retrieve all organization settings
    api_response = api_instance.organization_setting_controller_get_unscoped_organization_settings()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrganizationSettingsApi->organization_setting_controller_get_unscoped_organization_settings: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[OrganizationSetting]**](OrganizationSetting.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **organization_setting_controller_get_versions**
> Json organization_setting_controller_get_versions()

Retrieve container versions

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
api_instance = swagger_client.OrganizationSettingsApi(swagger_client.ApiClient(configuration))

try:
    # Retrieve container versions
    api_response = api_instance.organization_setting_controller_get_versions()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrganizationSettingsApi->organization_setting_controller_get_versions: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**Json**](Json.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_one_base_organization_setting_controller_organization_setting**
> OrganizationSettingResponseDto replace_one_base_organization_setting_controller_organization_setting(body, id)

Replace a single OrganizationSetting

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
api_instance = swagger_client.OrganizationSettingsApi(swagger_client.ApiClient(configuration))
body = swagger_client.OrganizationSettingResponseDto() # OrganizationSettingResponseDto | 
id = 'id_example' # str | 

try:
    # Replace a single OrganizationSetting
    api_response = api_instance.replace_one_base_organization_setting_controller_organization_setting(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrganizationSettingsApi->replace_one_base_organization_setting_controller_organization_setting: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**OrganizationSettingResponseDto**](OrganizationSettingResponseDto.md)|  | 
 **id** | **str**|  | 

### Return type

[**OrganizationSettingResponseDto**](OrganizationSettingResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_one_base_organization_setting_controller_organization_setting**
> OrganizationSettingResponseDto update_one_base_organization_setting_controller_organization_setting(body, id)

Update a single OrganizationSetting

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
api_instance = swagger_client.OrganizationSettingsApi(swagger_client.ApiClient(configuration))
body = swagger_client.UpdateOrganizationSettingDto() # UpdateOrganizationSettingDto | 
id = 'id_example' # str | 

try:
    # Update a single OrganizationSetting
    api_response = api_instance.update_one_base_organization_setting_controller_organization_setting(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrganizationSettingsApi->update_one_base_organization_setting_controller_organization_setting: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**UpdateOrganizationSettingDto**](UpdateOrganizationSettingDto.md)|  | 
 **id** | **str**|  | 

### Return type

[**OrganizationSettingResponseDto**](OrganizationSettingResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

