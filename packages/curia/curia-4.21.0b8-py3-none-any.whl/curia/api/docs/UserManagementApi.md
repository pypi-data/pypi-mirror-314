# swagger_client.UserManagementApi

All URIs are relative to *https://api.curia.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**user_management_controller_assign_user_roles**](UserManagementApi.md#user_management_controller_assign_user_roles) | **PUT** /user-management/{id}/assign-roles | Assign user roles
[**user_management_controller_cancel_user_invite**](UserManagementApi.md#user_management_controller_cancel_user_invite) | **POST** /user-management/invite/cancel | Cancel user invitation
[**user_management_controller_get_my_user**](UserManagementApi.md#user_management_controller_get_my_user) | **GET** /user-management/my-user | Retrieve your user
[**user_management_controller_get_my_user_api_key**](UserManagementApi.md#user_management_controller_get_my_user_api_key) | **GET** /user-management/my-api-key | Retrieve your api-key
[**user_management_controller_get_my_user_organizations**](UserManagementApi.md#user_management_controller_get_my_user_organizations) | **GET** /user-management/my-organizations | Retrieve user organizations
[**user_management_controller_get_roles**](UserManagementApi.md#user_management_controller_get_roles) | **GET** /user-management/roles | Retrieves user roles
[**user_management_controller_get_user**](UserManagementApi.md#user_management_controller_get_user) | **GET** /user-management/{id} | Retrieve one user
[**user_management_controller_get_users**](UserManagementApi.md#user_management_controller_get_users) | **GET** /user-management | Retrieve many users
[**user_management_controller_invite_user**](UserManagementApi.md#user_management_controller_invite_user) | **POST** /user-management/invite | Invite a User
[**user_management_controller_refresh_api_key**](UserManagementApi.md#user_management_controller_refresh_api_key) | **GET** /user-management/{id}/refresh-api-key | Refresh api key for userid
[**user_management_controller_refresh_my_api_key**](UserManagementApi.md#user_management_controller_refresh_my_api_key) | **GET** /user-management/refresh-my-api-key | Refresh user api key
[**user_management_controller_remove_user**](UserManagementApi.md#user_management_controller_remove_user) | **DELETE** /user-management/{id} | Delete one User
[**user_management_controller_remove_user_roles**](UserManagementApi.md#user_management_controller_remove_user_roles) | **PUT** /user-management/{id}/remove-roles | Remove user roles
[**user_management_controller_request_password_reset**](UserManagementApi.md#user_management_controller_request_password_reset) | **GET** /user-management/{id}/request-password-reset | Request user password reset
[**user_management_controller_resend_user_invite**](UserManagementApi.md#user_management_controller_resend_user_invite) | **POST** /user-management/invite/resend | Resend user invitation
[**user_management_controller_update_my_user**](UserManagementApi.md#user_management_controller_update_my_user) | **PATCH** /user-management/my-user | Update my User
[**user_management_controller_update_user**](UserManagementApi.md#user_management_controller_update_user) | **PATCH** /user-management/{id} | Update one User
[**user_management_controller_update_user_metadata**](UserManagementApi.md#user_management_controller_update_user_metadata) | **PUT** /user-management/{id}/metadata | Update one user metadata

# **user_management_controller_assign_user_roles**
> user_management_controller_assign_user_roles(id)

Assign user roles

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
api_instance = swagger_client.UserManagementApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | 

try:
    # Assign user roles
    api_instance.user_management_controller_assign_user_roles(id)
except ApiException as e:
    print("Exception when calling UserManagementApi->user_management_controller_assign_user_roles: %s\n" % e)
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

# **user_management_controller_cancel_user_invite**
> user_management_controller_cancel_user_invite()

Cancel user invitation

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
api_instance = swagger_client.UserManagementApi(swagger_client.ApiClient(configuration))

try:
    # Cancel user invitation
    api_instance.user_management_controller_cancel_user_invite()
except ApiException as e:
    print("Exception when calling UserManagementApi->user_management_controller_cancel_user_invite: %s\n" % e)
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

# **user_management_controller_get_my_user**
> object user_management_controller_get_my_user()

Retrieve your user

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
api_instance = swagger_client.UserManagementApi(swagger_client.ApiClient(configuration))

try:
    # Retrieve your user
    api_response = api_instance.user_management_controller_get_my_user()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UserManagementApi->user_management_controller_get_my_user: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**object**

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **user_management_controller_get_my_user_api_key**
> str user_management_controller_get_my_user_api_key()

Retrieve your api-key

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
api_instance = swagger_client.UserManagementApi(swagger_client.ApiClient(configuration))

try:
    # Retrieve your api-key
    api_response = api_instance.user_management_controller_get_my_user_api_key()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UserManagementApi->user_management_controller_get_my_user_api_key: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**str**

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **user_management_controller_get_my_user_organizations**
> user_management_controller_get_my_user_organizations()

Retrieve user organizations

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
api_instance = swagger_client.UserManagementApi(swagger_client.ApiClient(configuration))

try:
    # Retrieve user organizations
    api_instance.user_management_controller_get_my_user_organizations()
except ApiException as e:
    print("Exception when calling UserManagementApi->user_management_controller_get_my_user_organizations: %s\n" % e)
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

# **user_management_controller_get_roles**
> list[object] user_management_controller_get_roles()

Retrieves user roles

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
api_instance = swagger_client.UserManagementApi(swagger_client.ApiClient(configuration))

try:
    # Retrieves user roles
    api_response = api_instance.user_management_controller_get_roles()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UserManagementApi->user_management_controller_get_roles: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**list[object]**

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **user_management_controller_get_user**
> user_management_controller_get_user(id)

Retrieve one user

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
api_instance = swagger_client.UserManagementApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | 

try:
    # Retrieve one user
    api_instance.user_management_controller_get_user(id)
except ApiException as e:
    print("Exception when calling UserManagementApi->user_management_controller_get_user: %s\n" % e)
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

# **user_management_controller_get_users**
> user_management_controller_get_users()

Retrieve many users

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
api_instance = swagger_client.UserManagementApi(swagger_client.ApiClient(configuration))

try:
    # Retrieve many users
    api_instance.user_management_controller_get_users()
except ApiException as e:
    print("Exception when calling UserManagementApi->user_management_controller_get_users: %s\n" % e)
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

# **user_management_controller_invite_user**
> user_management_controller_invite_user()

Invite a User

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
api_instance = swagger_client.UserManagementApi(swagger_client.ApiClient(configuration))

try:
    # Invite a User
    api_instance.user_management_controller_invite_user()
except ApiException as e:
    print("Exception when calling UserManagementApi->user_management_controller_invite_user: %s\n" % e)
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

# **user_management_controller_refresh_api_key**
> str user_management_controller_refresh_api_key(id)

Refresh api key for userid

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
api_instance = swagger_client.UserManagementApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | 

try:
    # Refresh api key for userid
    api_response = api_instance.user_management_controller_refresh_api_key(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UserManagementApi->user_management_controller_refresh_api_key: %s\n" % e)
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

# **user_management_controller_refresh_my_api_key**
> str user_management_controller_refresh_my_api_key()

Refresh user api key

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
api_instance = swagger_client.UserManagementApi(swagger_client.ApiClient(configuration))

try:
    # Refresh user api key
    api_response = api_instance.user_management_controller_refresh_my_api_key()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UserManagementApi->user_management_controller_refresh_my_api_key: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**str**

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **user_management_controller_remove_user**
> user_management_controller_remove_user(id)

Delete one User

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
api_instance = swagger_client.UserManagementApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | 

try:
    # Delete one User
    api_instance.user_management_controller_remove_user(id)
except ApiException as e:
    print("Exception when calling UserManagementApi->user_management_controller_remove_user: %s\n" % e)
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

# **user_management_controller_remove_user_roles**
> user_management_controller_remove_user_roles(id)

Remove user roles

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
api_instance = swagger_client.UserManagementApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | 

try:
    # Remove user roles
    api_instance.user_management_controller_remove_user_roles(id)
except ApiException as e:
    print("Exception when calling UserManagementApi->user_management_controller_remove_user_roles: %s\n" % e)
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

# **user_management_controller_request_password_reset**
> object user_management_controller_request_password_reset(id)

Request user password reset

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
api_instance = swagger_client.UserManagementApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | 

try:
    # Request user password reset
    api_response = api_instance.user_management_controller_request_password_reset(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UserManagementApi->user_management_controller_request_password_reset: %s\n" % e)
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

# **user_management_controller_resend_user_invite**
> user_management_controller_resend_user_invite()

Resend user invitation

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
api_instance = swagger_client.UserManagementApi(swagger_client.ApiClient(configuration))

try:
    # Resend user invitation
    api_instance.user_management_controller_resend_user_invite()
except ApiException as e:
    print("Exception when calling UserManagementApi->user_management_controller_resend_user_invite: %s\n" % e)
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

# **user_management_controller_update_my_user**
> user_management_controller_update_my_user(body)

Update my User

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
api_instance = swagger_client.UserManagementApi(swagger_client.ApiClient(configuration))
body = swagger_client.UpdateUserDto() # UpdateUserDto | 

try:
    # Update my User
    api_instance.user_management_controller_update_my_user(body)
except ApiException as e:
    print("Exception when calling UserManagementApi->user_management_controller_update_my_user: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**UpdateUserDto**](UpdateUserDto.md)|  | 

### Return type

void (empty response body)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **user_management_controller_update_user**
> user_management_controller_update_user(body, id)

Update one User

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
api_instance = swagger_client.UserManagementApi(swagger_client.ApiClient(configuration))
body = swagger_client.UpdateUserDto() # UpdateUserDto | 
id = 'id_example' # str | 

try:
    # Update one User
    api_instance.user_management_controller_update_user(body, id)
except ApiException as e:
    print("Exception when calling UserManagementApi->user_management_controller_update_user: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**UpdateUserDto**](UpdateUserDto.md)|  | 
 **id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **user_management_controller_update_user_metadata**
> user_management_controller_update_user_metadata(id)

Update one user metadata

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
api_instance = swagger_client.UserManagementApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | 

try:
    # Update one user metadata
    api_instance.user_management_controller_update_user_metadata(id)
except ApiException as e:
    print("Exception when calling UserManagementApi->user_management_controller_update_user_metadata: %s\n" % e)
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

